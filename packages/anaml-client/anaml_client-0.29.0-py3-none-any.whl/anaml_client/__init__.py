#
#  Copyright 2021 Simple Machines Pty Ltd - All Rights Reserved.
#
#  This file is part of Anaml.
#
#  Unauthorized copying and/or distribution of this file, via any medium
#  is strictly prohibited.
#

"""The core of the Python SDK is the `anaml_client.Anaml` class.

Its methods simplify the process of interacting with the REST API and
accessing data stored in supported external data stores.
"""

from __future__ import annotations

import base64
from datetime import datetime, date
import glob
import json
import logging
import os.path
import typing
from typing import List, Optional, Union
# from unicodedata import unidata_version
from uuid import UUID

import requests

# Import the optional libraries during type-checking. This allows us to use them
# in type annotations without insisting that every user install PySpark whether
# or not they will use it.
#
# NB: This relies on the __future__ import changing the way that type annotations
# are processed.
#
# This is supported in Python 3.7+

if typing.TYPE_CHECKING:
    import pandas
    import pyspark.sql
    import s3fs
    from google.cloud import bigquery

from .exceptions import AnamlError, Reason

from .models import AggregateExpression
from .models import Attribute
from .models import BigQueryDestination
from .models import BranchName
from .models import BranchRef
from .models import CategoricalSummaryStatistics
from .models import Check
from .models import CheckCreationRequest
from .models import CheckId
from .models import Cluster
from .models import ClusterCreatedUpdated
from .models import ClusterCreationRequest
from .models import ClusterId
from .models import ClusterName
from .models import Commit
from .models import CommitId
from .models import CSV
from .models import Destination
from .models import DestinationCreatedUpdated
from .models import DestinationCreationRequest
from .models import DestinationId
from .models import DestinationName
from .models import EmptySummaryStatistics
from .models import Entity
from .models import EntityCreatedUpdated
from .models import EntityCreationRequest
from .models import EntityId
from .models import EntityName
from .models import EntityPopulation
from .models import EntityPopulationCreatedUpdated
from .models import EntityPopulationCreationRequest
from .models import EntityPopulationId
from .models import EntityPopulationName
from .models import EventDescription
from .models import EventFeatureCreationRequest
from .models import EventStore
from .models import EventStoreId
from .models import EventWindow
from .models import Feature
from .models import FeatureCreatedUpdated
from .models import FeatureCreationRequest
from .models import FeatureId
from .models import FeatureName
from .models import FeatureRunSummary
from .models import FeatureSet
from .models import FeatureSetCreatedUpdated
from .models import FeatureSetCreationRequest
from .models import FeatureSetId
from .models import FeatureSetName
from .models import FeatureStore
from .models import FeatureStoreCreatedUpdated
from .models import FeatureStoreCreationRequest
from .models import FeatureStoreId
from .models import FeatureStoreName
from .models import FeatureStoreRun
from .models import FeatureStoreRunId
from .models import FeatureTemplate
from .models import TemplateCreatedUpdated as FeatureTemplateCreatedUpdated
from .models import FeatureTemplateCreationRequest
from .models import TemplateId as FeatureTemplateId
from .models import TemplateName as FeatureTemplateName
from .models import FileFormat
from .models import FilterExpression
from .models import FolderDestinationReference
from .models import FolderSourceReference
from .models import GCSDestination
from .models import GeneratedFeatures
from .models import HDFSDestination
from .models import Label
from .models import Lineage
from .models import LocalDestination
from .models import MergeRequest
from .models import MergeRequestComment
from .models import MergeRequestCommentCreationRequest
from .models import MergeRequestCreationRequest
from .models import MergeRequestId
from .models import MonitoringResult
from .models import MonitoringResultPartial
from .models import NullCell
from .models import NumericalSummaryStatistics
from .models import Orc
from .models import Parquet
from .models import PostAggregateExpression
from .models import PreviewSummary
from .models import Ref
from .models import RootTableCreationRequest
from .models import RunStatus
from .models import S3ADestination
from .models import S3Destination
from .models import SelectExpression
from .models import Source
from .models import SourceCreatedUpdated
from .models import SourceCreationRequest
from .models import SourceId
from .models import SourceName
from .models import SummaryStatistics
from .models import Table
from .models import TableCreatedUpdated
from .models import TableCreationRequest
from .models import TableDestinationReference
from .models import TableId
from .models import TableMonitoringRunId
from .models import TableName
from .models import TablePreview
from .models import TemplateId
from .models import TimestampInfo
from .models import User
from .models import UserCreationRequest
from .models import UserGroup
from .models import UserGroupCreationRequest
from .models import UserGroupId
from .models import UserGroupName
from .models import UserId
from .models import ViewMaterialisationJob
from .models import ViewMaterialisationJobCreatedUpdated
from .models import ViewMaterialisationJobCreationRequest
from .models import ViewMaterialisationJobId
from .models import ViewMaterialisationJobName
from .models import ViewMaterialisationRun
from .models import ViewMaterialisationRunId
from .models import ViewTableCreationRequest

from . import version


__version__ = version.__version__

_NO_FEATURES = """No feature instances were generated for the following """
_NO_FEATURES += """features:\n{the_features}.\n"""
_NO_FEATURES += """This could be because the underlying dataset was empty, """
_NO_FEATURES += """or because a predicate or window in the feature excluded"""
_NO_FEATURES += """ all records in the dataset."""


class Anaml:
    """Anaml is a service class providing access to all functionality."""

    _bigquery_client_instance: Optional[bigquery.Client] = None
    _s3fs_client_instance: Optional[s3fs.S3FileSystem] = None

    def __init__(
        self,
        url: str,
        apikey: str,
        secret: str,
        ref: Optional[Ref] = None,
        log: Optional[logging.Logger] = None
    ):
        """Create a new `Anaml` instance.

        Access to the API requires a Personal Access Token which can be obtain on the users profile page
        on the web interface.

        Arguments:
            url: Base URL for the Anaml server API. e.g. https://anaml.company.com/api
            apikey: API key for Personal Access Token.
            secret: API secret for Personal Access Token.
            ref: The BranchRef or CommitRef reference to act on.
            log: Optional logger to use. If omitted, a logger will be created.
        """
        self._url = url
        self._token = base64.b64encode(bytes(apikey + ':' + secret, 'utf-8')).decode('utf-8')
        self._headers = {'Authorization': 'Basic ' + self._token}
        self._log = log or logging.getLogger('anaml_client.Anaml')
        if ref is not None:
            self._ref = {ref.adt_type: ref.ref}
        else:
            self._ref = {}

    def __enter__(self):
        """Enter the runtime context client in a context manager."""
        return self

    def __exit__(self, exc_type: typing.Type[Exception], exc_value: Exception, traceback):
        """Exit the runtime context related to this object.

        All internal clients and services are stopped.
        """
        self.close()
        # We don't handle any exceptions: the context manager machinery should not swallow them.
        return None

    @property
    def _bigquery_client(self) -> bigquery.Client:
        """Initialise and cache a BigQuery client object."""
        if self._bigquery_client_instance is None:
            from google.cloud import bigquery
            # TODO: Do we need to support manual configuration of the BigQuery client?
            self._bigquery_client_instance = bigquery.Client()
        return self._bigquery_client_instance

    @property
    def _s3fs_client(self) -> s3fs.S3FileSystem:
        """Initialise and cache an s3fs filesystem object."""
        if self._s3fs_client_instance is None:
            import s3fs
            # TODO: Do we need to support manual configuration of the S3 client?
            self._s3fs_client_instance = s3fs.S3FileSystem(anon=False)
        return self._s3fs_client_instance

    def close(self) -> None:
        """Close and discard internal clients and services."""
        if self._bigquery_client_instance is not None:
            self._bigquery_client_instance.close()
            self._bigquery_client_instance = None
        if self._s3fs_client_instance is not None:
            self._s3fs_client_instance = None

    def with_ref(self, new_ref: Ref) -> Anaml:
        """Return a new instance of "Anaml" that will act on the given `new_ref`.

        Args:
            new_ref: A reference to a branch or commit.

        Returns:
            A new Anaml instance configured to use the new reference.
        """
        # This is a bit hacky
        new_anaml = Anaml(self._url, "", "", new_ref)
        new_anaml._token = self._token
        new_anaml._headers = self._headers

        return new_anaml

    # Commits and Branches

    def get_current_commit(self, branch: Union[BranchName, str]) -> Commit:
        """Get the current commit for a branch.

        Args:
            branch: Name of the branch to inspect.

        Returns:
            The commit currently at the tip of the named branch.
        """
        r = self._get(f"/branch/{str(branch)}")
        result = self._json_or_handle_errors(r)
        return Commit.from_json(result)

    def get_branches(self) -> List[str]:
        """Get a list of all branches.

        Returns:
            A list of branch names
        """
        r = self._get("/branch")
        result = self._json_or_handle_errors(r)
        return result

    def get_recently_modified_branches(self) -> List[BranchRef]:
        """Get recently modified branches.

        Returns:
            A list of BranchRefs with created and updated timestamps
            associated with the given commit and recently modified.
        """
        # this would be nice
        # r = self._get("/blame/branch")
        # result = self._json_or_handle_errors(r)
        branch_commits = [(b['name'], b['head']['createdAt'][:10]) for b in self.get_branches()]
        recently_commited_branches = \
            [b[0] for b in branch_commits if (datetime.now() - datetime.strptime(b[1], "%Y-%m-%d")).days < 30]

        return recently_commited_branches

    # Feature-related non CRUD functions

    def get_generated_features(
        self,
        feature_store: Union[FeatureStoreName, str],
        primary_key
    ) -> GeneratedFeatures:
        """Get the features generated from a feature store for a particular primary key value.

        Args:
            feature_store: Name of the feature store.
            primary_key: Primary key of the entity to get.

        Returns:
            The features for the given primary key in the named feature store.
        """
        r = self._get("/generated-feature/" + feature_store + "/" + str(primary_key))
        result = self._json_or_handle_errors(r)
        return GeneratedFeatures.from_json(result)

    def get_online_features_with_id(
        self,
        name,
        feature_store_id: Union[FeatureStoreId, int],
        primary_key
    ) -> GeneratedFeatures:
        """Get the features generated from a feature store for a particular primary key value.

        Args:
            name: Name of the destination online feature store table.
            feature_store_id: Id of the feature store.
            primary_key: Primary key of the entity to get.

        Returns:
            The features for the given primary key in the named feature store.
        """
        r = self._get(f"/online-store/{int(feature_store_id)}" + "/" + str(name) + "/" + str(primary_key))
        result = self._json_or_handle_errors(r)
        return GeneratedFeatures.from_json(result)

    def preview_feature(
            self,
            feature: Feature,
            *,
            entity: Optional[EntityId] = None,
            snapshot_date: Optional[Union[str, date]] = None
    ) -> List[PreviewSummary]:
        """Returns list of feature statistics.

        Args:
            feature: a Feature object or list of feature objects.
            entity:  Entity Id to filter feature preview on.
            snapshot_date: Date to filter feature preview on.
        """
        req = {"feature": feature.to_json()}

        req["entity"] = entity

        if isinstance(snapshot_date, str):
            try:
                datetime.strptime(snapshot_date, "%Y-%m-%d")
                req["snapshotDate"] = snapshot_date
            except ValueError:
                raise ValueError(f"snapshotDate: {snapshot_date} provided is not of the format 'yyyy-mm-dd'")
        elif isinstance(snapshot_date, date):
            req["snapshotDate"] = snapshot_date.strftime("%Y-%m-%d")
        else:
            req["snapshotDate"] = None

        r = self._post("/feature-preview", json=req)
        result = self._json_or_handle_errors(r)
        return [
            PreviewSummary.from_json(fs)
            for fs in result.get('previewData', {}).get('featureStatistics', [])
        ]

    def preview_feature_and_plot(
            self,
            feature: Feature,
            *,
            entity: Optional[EntityId] = None,
            snapshot_date: Optional[Union[str, datetime.date]] = None
    ) -> None:
        """Show a matplotlib plot for the preview statistics of a feature.

        Args:
            feature: a Feature object
            entity:  Entity Id to filter feature previews on.
            snapshot_date: Date to filter feature preview on.
        """
        feature_stats = self.preview_feature(feature, entity=entity, snapshot_date=snapshot_date)
        for fs in feature_stats:
            for stats in fs.statistics:
                if isinstance(stats, EmptySummaryStatistics):
                    self._warn_empty_feature_stats([fs.featureName])
                self._build_feature_plots(stats)

    def sample_feature(self, feature: Feature) -> pandas.DataFrame:
        """Generate a sample of feature values.

        Arguments:
            feature: a Feature object

        Returns:
            a pandas dataframe of the feature sample values
        """
        import pandas

        r = self._post("/feature-sample", json={"feature": feature.to_json()})
        result = self._json_or_handle_errors(r)

        return pandas.DataFrame(result)

    def get_feature_run_summary(self, feature_id: Union[FeatureId, int]) -> FeatureRunSummary:
        """Get a summary of the most recent run of a feature.

        Args:
            feature_id: Unique identifier of the feature.

        Returns:
            A summary of the given feature from the most recent feature store run.
        """
        r = self._get(f"/feature/{int(feature_id)}/latest-run-statistics")
        result = self._json_or_handle_errors(r)
        return FeatureRunSummary.from_json(result)

    def preview_feature_set(
            self,
            feature_set: Union[FeatureSet, FeatureSetCreationRequest],
            *,
            entity: Optional[EntityId] = None,
            snapshot_date: Optional[Union[str, date]] = None
    ) -> pandas.DataFrame:
        """Returns a pandas dataframe of the feature set.

        Args:
            feature_set: a FeatureSet object.
            entity:  Entity Id to filter feature preview on.
            snapshot_date: Date to filter feature preview on.
        """
        import pandas
        req = {"featureSet": feature_set.to_json()}
        req["entity"] = entity
        if isinstance(snapshot_date, str):
            try:
                datetime.strptime(snapshot_date, "%Y-%m-%d")
                req["snapshotDate"] = snapshot_date
            except ValueError:
                raise ValueError(f"snapshotDate: {snapshot_date} provided is not of the format 'yyyy-mm-dd'")
        elif isinstance(snapshot_date, date):
            req["snapshotDate"] = snapshot_date.strftime("%Y-%m-%d")
        else:
            req["snapshotDate"] = None

        r = self._post("/feature-set-preview", json=req)
        result = self._json_or_handle_errors(r)
        table_preview = TablePreview.from_json(result.get('previewData', {}))

        # Convert to pandas
        col_names = [c.name for c in table_preview.headers]
        md_list = []
        for row in table_preview.rows:
            cell_list = []
            for cell in row.cells:
                if isinstance(cell, NullCell):
                    cell_list.append(None)
                else:
                    cell_list.append(cell.data)
            md_list.append(cell_list)

        return pandas.DataFrame(md_list, columns=col_names)

    def get_run_for_feature_set(self, feature_set_id: Union[FeatureSetId, int]) -> FeatureStoreRun:
        """Get the most recent feature store run for the given feature set.

        Args:
            feature_set_id: The unique identifier of the feature set.

        Returns:
            The most recent feature store run for that feature set.
        """
        r = self._get(f"/feature-set/{int(feature_set_id)}/latest-run-statistics")
        result = self._json_or_handle_errors(r)
        return FeatureStoreRun.from_json(result)

    def get_feature_store_runs(
        self,
        feature_store_id: Union[FeatureStoreId, int],
        num: Optional[int] = None
    ) -> List[FeatureStoreRun]:
        """Get a list of all runs of a given feature store from the Anaml server.

        Args:
            feature_store_id: The unique identifier of a feature store.
            num: Optional. Maximum number of results to return.

        Returns:
            A list of runs of the given feature store.
        """
        q = {}
        if num is not None:
            q['num'] = num
        r = self._get(f"/feature-store/{int(feature_store_id)}/run", query=q)
        result = self._json_or_handle_errors(r)
        return [FeatureStoreRun.from_json(r) for r in result]

    def get_feature_store_run(
        self,
        feature_store_id: Union[FeatureStoreId, int],
        run_id: Union[FeatureStoreRunId, int]
    ) -> FeatureStoreRun:
        """Get the details for a feature store run from the Anaml server.

        Args:
            feature_store_id: The unique identifier of a feature store.
            run_id: The unique identifier of a run of that feature store.

        Returns:
             Details of the given feature store run.
        """
        r = self._get(f"/feature-store/{int(feature_store_id)}/run/{int(run_id)}")
        result = self._json_or_handle_errors(r)
        return FeatureStoreRun.from_json(result)

    def get_latest_feature_store_run_by_name(self, feature_store_name: Union[FeatureStoreName, str]) -> FeatureStoreRun:
        """Get the most recent run of the named feature store from the Anaml server.

        Args:
            feature_store_name: The name of the feature store.

        Returns:
            Details of the feature store run.

        Raises:
            IndexError: When the named feature store has no runs.
        """
        feature_store = self.get_feature_store_by_name(feature_store_name)
        # TODO: Extend server to provide an end
        runs = self.get_feature_store_runs(feature_store_id=feature_store.id.value, num=1)
        return runs[0]

    # EventStore-related functions
    def get_event_stores(self) -> List[EventStore]:
        """Get a list of all event stores from the Anaml server.

        Returns:
            A list of event stores.
        """
        r = self._get("/event-store")
        result = self._json_or_handle_errors(r)
        return [EventStore.from_json(d) for d in result]

    def get_merge_request_comments(self, merge_request_id: Union[MergeRequestId, int]) -> List[MergeRequestComment]:
        """List merge requests from the Anaml server.

        Args:
            limit: The maximum number of objects to return.

        Returns:
            A list of merge requests.
        """
        r = self._get(f"/merge-request/{int(merge_request_id)}/comment")
        result = self._json_or_handle_errors(r)
        return [
            MergeRequestComment.from_json(r) for r in result
        ]

    def get_view_materialisation_runs(
        self,
        view_materialisation_id: Union[ViewMaterialisationJobId, int],
        num: Optional[int] = None
    ) -> List[ViewMaterialisationRun]:
        """Get a list of all runs of a given view materialisation from the Anaml server.

        Args:
            view_materialisation_id: The unique identifier of a view materialisation.
            num: Optional. Maximum number of results to return.

        Returns:
            A list of runs of the given view materialisation.
        """
        q = {}
        if num is not None:
            q['num'] = num
        r = self._get(f"/view-materialisation/{int(view_materialisation_id)}/run", query=q)
        result = self._json_or_handle_errors(r)
        return [ViewMaterialisationRun.from_json(r) for r in result]

    def get_view_materialisation_run(
        self,
        view_materialisation_id: Union[ViewMaterialisationJobId, int],
        run_id: Union[ViewMaterialisationRunId, int]
    ) -> ViewMaterialisationRun:
        """Get the details for a view materialisation run from the Anaml server.

        Args:
            view_materialisation_id: The unique identifier of a view materialisation.
            run_id: The unique identifier of a run of that view materialisation.

        Returns:
             Details of the given view materialisation run.
        """
        r = self._get(f"/view-materialisation/{int(view_materialisation_id)}/run/{int(run_id)}")
        result = self._json_or_handle_errors(r)
        return ViewMaterialisationRun.from_json(result)

    def get_merge_request_diff(self, merge_request_id: Union[MergeRequestId, int]) -> dict:
        """Gets a diff for a merge request.

        Args:
            merge_request_id: The merge request to diff.

        Returns:
            dict.
        """
        r = self._get(f"/merge-request/{str(merge_request_id)}/diff")
        result = self._json_or_handle_errors(r)
        return result

    def create_merge_request_comment(
            self,
            merge_request_id: Union[MergeRequestId, int],
            comment: MergeRequestCommentCreationRequest
    ) -> List[MergeRequestComment]:
        """Create a new Comment for a merge request.

        Args:
            merge_request_id: The merge request to comment on.
            comment: The comment to create.

        Returns:
            The new list of comments for the merge request.
        """
        r = self._post(f"/merge-request/{str(merge_request_id)}/comment", json=comment.to_json())
        self._int_or_handle_errors(r)
        return self.get_merge_request_comments(merge_request_id)

    def add_merge_request_reviewers(
            self,
            merge_request_id: Union[MergeRequestId, int],
            reviewers: dict
    ):
        """Add new Reviewers for a merge request.

        Args:
            merge_request_id: The merge request.
            reviewers: The reviewers to add.
        """
        r = self._post(f"/merge-request/{str(merge_request_id)}/reviewers", json=reviewers)
        self._handle_errors(r)

    # Checks
    def get_checks(self, commit_id: Union[CommitId, UUID]) -> List[Check]:
        """Get checks for a given commit from the Anaml server.

        Args:
            commit_id: Unique identifier of the commit.

        Returns:
            A list of checks associated with the given commit.
        """
        r = self._get(f"/checks/{str(commit_id)}")
        result = self._json_or_handle_errors(r)
        return [
            Check.from_json(r) for r in result
        ]

    def get_check(self, commit_id: Union[CommitId, UUID], check_id: Union[CheckId, int]) -> Check:
        """Get a specific check for given a commit_id from the Anaml server.

        Args:
            commit_id: Unique identifier of the commit.
            check_id: Unique identifier of the check.

        Returns:
            The check, if it exists.
        """
        r = self._get(f"/checks/{str(commit_id)}/{int(check_id)}")
        result = self._json_or_handle_errors(r)
        return Check.from_json(result)

    def create_check(self, commit: Union[CommitId, UUID], check: CheckCreationRequest) -> Check:
        """Create a new Check for a commit.

        Args:
            commit: The commit being checked.
            check: The details of the check.

        Returns:
            The check object, with unique identifier and other computed fields updated.
        """
        r = self._post(f"/checks/{str(commit)}", json=check.to_json())
        id = self._int_or_handle_errors(r)
        return self.get_check(commit, id)

    def update_check(self, check: Check) -> Check:
        """Get Checks from the Anaml server.

        Args:
            check: The check details to be saved.

        Returns:
            The check object, with unique identifier and other computed fields updated.
        """
        r = self._put("/checks/" + str(check.commit.value) + "/" + str(check.id.value), json=check.to_json())
        _ = self._json_or_handle_errors(r)
        # Let's re-load the saved check. Just to make sure it's all up to date.
        return self.get_check(check.commit, check.id)

    def get_latest_commit(self, branch: str) -> Commit:
        """Get the latest Commit for a branch.

        Args:
            branch: The branch name.

        Returns:
            The Commit object.
        """
        r = self._get(f"/branch/{branch}")
        result = self._json_or_handle_errors(r)
        return Commit.from_json(result)

    # Table Monitoring Functions
    def get_table_monitoring_result(
        self,
        run_id: Union[TableMonitoringRunId, int],
        table_name: Optional[Union[TableName, str]] = None,
        table_id: Optional[Union[TableId, int]] = None
    ) -> List[MonitoringResultPartial]:
        """Gets a monitoring result for a given run_id.

        Optionally, a table_name / table_id can be supplied to get a specific table's results for that run_id

        Args:
            run_id: run_id of the requested job run
            table_name [optional]: table_name in the requested job run
            table_id [optional]: table_id in the requested job run

        Returns:
            The PARTIAL monitoring result for a given run_id -> MonitoringResultPartial

            If a table name / id is supplied, the result will be for that table only.
        """
        if table_name:
            table_id = self.get_table_by_name(table_name).id.value

        if table_id:
            r = self._get(f"/table-monitoring/table/{int(table_id)}/results")
        else:
            r = self._get(f"/table-monitoring/run/{int(run_id)}/results")

        result = self._json_or_handle_errors(r)

        return [MonitoringResultPartial.from_json(r) for r in result]

    def get_latest_table_monitoring_result_by_table_name(
        self,
        table_name: Union[TableName, str],
        full_results: Optional[bool] = False
    ) -> Union[MonitoringResultPartial, MonitoringResult]:
        """Gets the latest monitoring result for a specified table name.

        Args:
            name: Name of the table

        Returns:
            Default:
                The PARTIAL monitoring result -> MonitoringResultPartial
            If full_result=True:
                The full monitoring result -> MonitoringResult
        """
        table_id = self.get_table_by_name(table_name).id.value

        r = self._get(f"/table-monitoring/table/{int(table_id)}/results")
        results = self._json_or_handle_errors(r)
        if len(results) == 0:
            raise ValueError(f"Latest results not found for {table_name}")

        latest_result_id = results[0]['id']
        r = self._get(f"/table-monitoring/results/{int(latest_result_id)}")
        latest_result = self._json_or_handle_errors(r)

        if full_results:
            return MonitoringResult.from_json(latest_result)
        else:
            return MonitoringResultPartial.from_json(latest_result)

    # User / User Group functions

    def get_users_for_group(
        self,
        user_group_name: Optional[Union[UserGroupName, str]] = None
    ) -> List(User):
        """Get a count of human users registered on the anaml deployment.

        Args:
            user_group_name : the name of the group that serves as the human user parent group.

        Returns:
            length of members attribute of provided group
        """
        members = self.get_user_group_by_name(user_group_name).members
        users = [self.get_user_from_id(m.userId.value) for m in members]

        return users

    def get_lineage_for_event_store(self, event_store_id: Union[EventStoreId, int]) -> Lineage:
        """Get lineage data relating to an event store from the Anaml server.

        Args:
            event_store_id: Unique identifier of the event store.

        Returns:
            The event store lineage data, if the event store exists.
        """
        r = self._get(f"/lineage/event-store/{int(event_store_id)}")
        result = self._json_or_handle_errors(r)
        return Lineage.from_json(result)

    # Builder functions
    def build_event_feature(
        self,
        *,
        name: str,
        table: typing.Union[int, str, Table],
        select: str,
        aggregate: AggregateExpression,
        window: EventWindow,
        description: str = "",
        labels: List[Label] = [],
        attributes: List[Attribute] = [],
        filter: str = None,
        postAggregateExpr: str = None,
        entityRestrictions: List[EntityId] = None,
        template: TemplateId = None
    ) -> EventFeatureCreationRequest:
        """Helper function for building event features."""
        if isinstance(table, Table):
            table_id = table.id
        elif isinstance(table, str):
            table_id = self.get_table_by_name(table).id
        else:
            table_id = table

        if filter is not None:
            filter = FilterExpression(filter)
        if postAggregateExpr is not None:
            postAggregateExpr = PostAggregateExpression(postAggregateExpr)

        return EventFeatureCreationRequest(
            name=FeatureName(name),
            description=description,
            attributes=attributes,
            labels=labels,
            table=table_id,
            select=SelectExpression(select),
            filter=filter,
            aggregate=aggregate,
            window=window,
            postAggregateExpr=postAggregateExpr,
            entityRestrictions=entityRestrictions,
            template=template
        )

    def build_feature_set(
        self,
        *,
        name: str,
        entity: typing.Union[int, str],
        description: str = "",
        labels: List[Label] = [],
        attributes: List[Attribute] = [],
        features: List[FeatureId] = []
    ) -> FeatureSetCreationRequest:
        """Helper function for building feature sets."""
        if isinstance(entity, Table):
            entity_id = entity.id
        elif isinstance(entity, str):
            entity_id = self.get_entity_by_name(entity).id
        else:
            entity_id = entity

        return FeatureSetCreationRequest(
            name=FeatureSetName(name),
            entity=entity_id,
            description=description,
            labels=labels,
            attributes=attributes,
            features=features)

    def build_external_table(
        self,
        *,
        name: str,
        description: str,
        labels: List[Label] = [],
        attributes: List[Attribute] = [],
        entities: typing.Dict[EntityId, str] = None,
        timestampColumn: str = None,
        timezone: str = None,
        source: typing.Union[int, str, Source]
    ) -> RootTableCreationRequest:
        """Helper function for building external tables."""
        if entities is not None and timestampColumn is not None:
            eventDescription = EventDescription(entities, TimestampInfo(timestampColumn, timezone))
        elif entities is not None and timestampColumn is None:
            raise ValueError("Please provide value for timestampColumn.")
        elif entities is None and timestampColumn is not None:
            raise ValueError("Please provide value for entities.")
        else:
            eventDescription = None

        if isinstance(source, Source):
            source_id = source.id
        elif isinstance(source, str):
            source_id = self.get_source_by_name(source).id
        else:
            source_id = source

        return RootTableCreationRequest(
            name=TableName(name),
            description=description,
            labels=labels,
            attributes=attributes,
            eventDescription=eventDescription,
            source=FolderSourceReference(source_id))

    def build_view_table(
        self,
        *,
        name: str,
        description: str,
        labels: List[Label] = [],
        attributes: List[Attribute] = [],
        entities: typing.Dict[EntityId, str] = None,
        timestampColumn: str = None,
        timezone: str = None,
        expression: str,
        sources: List[TableId] = []
    ) -> ViewTableCreationRequest:
        """Helper function for building view tables."""
        if entities is not None and timestampColumn is not None:
            eventDescription = EventDescription(entities, TimestampInfo(timestampColumn, timezone))
        elif entities is not None and timestampColumn is None:
            raise ValueError("Please provide value for timestampColumn.")
        elif entities is None and timestampColumn is not None:
            raise ValueError("Please provide value for entities.")
        else:
            eventDescription = None

        return ViewTableCreationRequest(
            name=TableName(name),
            description=description,
            labels=labels,
            attributes=attributes,
            eventDescription=eventDescription,
            expression=expression,
            sources=sources
        )

    #####################
    # Load feature data #
    #####################

    def load_features_to_pandas(self, run: FeatureStoreRun) -> pandas.DataFrame:
        """Load the data from a collection of features to a Pandas data frame.

        This method supports some but not all of the data stores available to
        the Anaml server. Where necessary, you may need to configure authentication
        to each data store separately using the appropriate configuration file,
        environment variables, or other mechanism.

        Args:
            run: A successful run of the feature store to be loaded.

        Warning: This method will attempt to load all of the data in the given
        feature store, whether or not your Python process has enough memory to
        store it.

        Returns:
            A Pandas dataframe.
        """
        return self._load_features_to_dataframe(run)

    def load_features_to_spark(
        self,
        run: FeatureStoreRun,
        *,
        spark_session: pyspark.sql.SparkSession
    ) -> pandas.DataFrame:
        """Load the data from a collection of features to a Spark data frame.

        This method supports some but not all of the data stores available to
        the Anaml server.

        Args:
            run: A successful run of the feature store to be loaded.
            spark_session: A running Spark session to load the data.

        The Spark session must have the appropriate libraries and configuration
        to access the underlying data store.

        Returns:
            A Spark dataframe object.
        """
        return self._load_features_to_dataframe(run, spark_session=spark_session)

    def _load_features_to_dataframe(
            self,
            run: FeatureStoreRun,
            *,
            spark_session: Optional[pyspark.sql.SparkSession] = None,
    ) -> Union[pandas.DataFrame, pyspark.sql.DataFrame]:
        """Load the data from a feature store into a data frame.

        Args:
            run: A run from a feature store.
            spark_session: Optional Spark session to load the data.

        Returns:
              When `spark_session` is given, a Spark data frame will be created and returned.
              Otherwise, a Pandas data frame will be created and returned.
        """
        if run.status != RunStatus.Completed:
            self._log.debug(
                f"Attempted to load data from feature store run id={run.id.value}, status={run.status.value}"
            )
            raise ValueError("The feature store run is not complete")

        # TODO: We should think about using Version here.
        store = self.get_feature_store_by_id(run.featureStoreId.value)

        # Loop through the destinations and attempt to load them. They should all contain the same data, so we'll
        # take the first one we find that actually returns a dataframe.
        dataframe = None
        for dest_ref in store.destinations:
            dest = self.get_destination_by_id(dest_ref.destinationId.value)
            if isinstance(dest_ref, TableDestinationReference):
                if isinstance(dest, BigQueryDestination) and spark_session is not None:
                    project, dataset = dest.path.split(":")
                    ref = "{project}.{dataset}.{table}".format(
                        project=project,
                        dataset=dataset,
                        table=dest_ref.tableName
                    )
                    dataframe = spark_session.read.format('bigquery').option('table', ref).load()
                elif isinstance(dest, BigQueryDestination) and spark_session is None:
                    # We're using the BigQuery client library instead of the Pandas support.
                    # More information: https://cloud.google.com/bigquery/docs/pandas-gbq-migration
                    from google.cloud import bigquery
                    project, dataset = dest.path.split(":")
                    ref = bigquery.TableReference(
                        dataset_ref=bigquery.DatasetReference(project=project, dataset_id=dataset),
                        table_id=dest_ref.tableName
                    )
                    dataframe = self._bigquery_client.list_rows(
                        table=ref,
                        # TODO: Should we restrict the columns we want to fetch?
                        selected_fields=None,
                    ).to_dataframe()
                # TODO: Implement support for loading data from Hive.
                # TODO: Implement support for loading data from HDBC.
                else:
                    self._log.debug(f"Cannot load table data from {type(dest).__name__}; skipping.")
            elif isinstance(dest_ref, FolderDestinationReference):
                if isinstance(dest, GCSDestination) and spark_session is not None:
                    url = "gs://{bucket}/{prefix}/".format(
                        bucket=dest.bucket,
                        prefix=f"{dest.path.strip('/')}/{dest_ref.folder.strip('/')}"
                    )
                    spark_options = {}
                    if isinstance(dest.fileFormat, CSV):
                        spark_options['header'] = dest.fileFormat.includeHeader
                    dataframe = spark_session.read.load(path=url, format=dest.fileFormat.adt_type, **spark_options)
                elif isinstance(dest, GCSDestination) and spark_session is None:
                    url = "gs://{bucket}/{prefix}/**{suffix}".format(
                        bucket=dest.bucket,
                        prefix=f"{dest.path.strip('/')}/{dest_ref.folder.strip('/')}",
                        suffix=self._file_format_suffix(dest.fileFormat)
                    )
                    dataframe = self._load_pandas_from_files(
                        urls=[url],
                        format=dest.fileFormat
                    )
                elif isinstance(dest, HDFSDestination) and spark_session is not None:
                    url = "hdfs://{path}".format(
                        path=f"{dest.path.strip('/')}/{dest_ref.folder.strip('/')}"
                    )
                    spark_options = {}
                    if isinstance(dest.fileFormat, CSV):
                        spark_options['header'] = dest.fileFormat.includeHeader
                    dataframe = spark_session.read.load(path=url, format=dest.fileFormat.adt_type, **spark_options)
                # TODO: Load Pandas data frame from HDFS.
                elif isinstance(dest, LocalDestination) and spark_session is not None:
                    url = f"/{dest.path.strip('/')}/{dest_ref.folder.strip('/')}"
                    spark_options = {}
                    if isinstance(dest.fileFormat, CSV):
                        spark_options['header'] = dest.fileFormat.includeHeader
                    dataframe = spark_session.read.load(path=url, format=dest.fileFormat.adt_type, **spark_options)
                elif isinstance(dest, LocalDestination) and spark_session is None:
                    url = "{prefix}/**/*{suffix}".format(
                        prefix=f"/{dest.path.strip('/')}/{dest_ref.folder.strip('/')}",
                        suffix=self._file_format_suffix(dest.fileFormat)
                    )
                    dataframe = self._load_pandas_from_files(
                        urls=filter(os.path.isfile, glob.iglob(url, recursive=True)),
                        format=dest.fileFormat
                    )
                elif isinstance(dest, S3ADestination) and spark_session is not None:
                    url = "s3a://{bucket}/{prefix}/".format(
                        bucket=dest.bucket,
                        prefix=f"{dest.path.strip('/')}/{dest_ref.folder.strip('/')}",
                    )
                    spark_options = {}
                    if isinstance(dest.fileFormat, CSV):
                        spark_options['header'] = dest.fileFormat.includeHeader
                    dataframe = spark_session.read.load(path=url, format=dest.fileFormat.adt_type, **spark_options)
                elif isinstance(dest, S3Destination) and spark_session is not None:
                    url = "s3://{bucket}/{prefix}/".format(
                        bucket=dest.bucket,
                        prefix=f"{dest.path.strip('/')}/{dest_ref.folder.strip('/')}"
                    )
                    spark_options = {}
                    if isinstance(dest.fileFormat, CSV):
                        spark_options['header'] = dest.fileFormat.includeHeader
                    dataframe = spark_session.read.load(path=url, format=dest.fileFormat.adt_type, **spark_options)
                elif isinstance(dest, S3Destination) or isinstance(dest, S3ADestination):
                    url = "{bucket}/{prefix}/**{suffix}".format(
                        bucket=dest.bucket,
                        prefix=f"{dest.path.strip('/')}/{dest_ref.folder.strip('/')}",
                        suffix=self._file_format_suffix(dest.fileFormat)
                    )
                    dataframe = self._load_pandas_from_files(
                        urls=self._s3fs_client.glob(path=url),
                        format=dest.fileFormat
                    )
                else:
                    self._log.debug(f"Cannot load folder data from {type(dest).__name__}; skipping.")
            else:
                self._log.debug(f"Cannot load data from {type(dest_ref).__name__} references; skipping.")
            if dataframe is not None:
                return dataframe

        # If we haven't returned, then there were no supported destinations.
        raise NotImplementedError("No supported data stores available.")

    @staticmethod
    def _load_pandas_from_files(
        urls: typing.Iterable[str],
        format: FileFormat
    ) -> Optional[pandas.DataFrame]:
        """Load a folder of datafiles in Google Cloud Storage into a Pandas data frame.

        Args:
            urls: Collection of paths/URLs to the data files.
            format: Format of the data files.

        Warning: This method makes no attempt to check that the requested data will fit into available memory.
        """
        import pandas
        if isinstance(format, Parquet):
            return pandas.concat(pandas.read_parquet(url) for url in urls)
        elif isinstance(format, Orc):
            return pandas.concat(pandas.read_orc(url) for url in urls)
        elif isinstance(format, CSV):
            return pandas.concat(pandas.read_csv(url) for url in urls)
        else:
            raise ValueError(f"Cannot load unsupported format: {format.adt_type}")

    def _build_feature_plots(self, summary_stats: SummaryStatistics) -> None:
        if isinstance(summary_stats, NumericalSummaryStatistics):
            self._build_numerical_plots(summary_stats.quantiles, summary_stats.featureName)
        elif isinstance(summary_stats, CategoricalSummaryStatistics):
            self._build_categorical_plots(summary_stats.categoryFrequencies, summary_stats.featureName)

    @staticmethod
    def _build_numerical_plots(qdata: List[float], title: str) -> None:
        import numpy
        import seaborn
        from matplotlib import pyplot
        seaborn.set_style('whitegrid')
        pyplot.subplot(211)
        seaborn.kdeplot(x=numpy.array(qdata))
        pyplot.title(title)
        pyplot.subplot(212)
        seaborn.boxplot(x=numpy.array(qdata))
        pyplot.tight_layout()
        pyplot.show()

    @staticmethod
    def _build_categorical_plots(qdata, title: str) -> None:
        from matplotlib import pyplot
        import seaborn
        import pandas
        seaborn.set_style('whitegrid')
        seaborn.catplot(x="category", y="frequency", kind="bar", data=pandas.DataFrame(qdata))
        pyplot.title(title)
        pyplot.show()

    A = typing.TypeVar('A')

    @staticmethod
    def _to_list(gotten: Optional[A]) -> List[A]:
        return [] if gotten is None else [gotten]

    def _get(self, path: str, query: Optional[dict] = None, exclude_default_ref: bool = False):
        """Send a GET request to the Anaml server."""
        if query is None:
            query = {}
        if exclude_default_ref:
            params = {**query}
        else:
            params = {**query, **self._ref}
        return requests.get(self._url + path, params=params, headers=self._headers)

    def _put(self, part: str, json):
        """Send a PUT request to the Anaml server."""
        return requests.put(self._url + part, params=self._ref, json=json, headers=self._headers)

    def _post(self, part, json, **kwargs):
        """Send a POST request to the Anaml server."""
        return requests.post(self._url + part, params=self._ref, json=json, headers=self._headers, **kwargs)

    def _delete(self, part, json, **kwargs):
        """Send a DELETE request to the Anaml server."""
        return requests.delete(self._url + part, params=self._ref, json=json, headers=self._headers, **kwargs)

    def _handle_errors(self, r):
        try:
            response_json = r.json()
            if "errors" in response_json:
                ex = AnamlError.from_json(response_json)
                raise ex
        except json.JSONDecodeError:
            # This is not unexpected. 404 responses, in particular, often have no JSON error message.
            pass
        r.raise_for_status()

    def _json_or_handle_errors(self, r: requests.Response, none_on_404=False):
        if r.ok:
            try:
                result = r.json()
                return result
            except json.JSONDecodeError:
                # Sorry, (no or invalid) JSON here
                self._log.error("No or invalid JSON received from server")
                self._log.error("Response content: " + r.text)
                raise AnamlError(errors=[Reason(message="Expected JSON but the server did not return any")])
        elif r.status_code == 404:
            if none_on_404:
                return None
            else:
                self._handle_errors(r)
        else:
            self._handle_errors(r)

    def _int_or_handle_errors(self, r):
        if r.ok:
            print(r.text)
            return int(r.text)
        else:
            self._handle_errors(r)

    def _warn_empty_feature_stats(self, features: List[str]):
        if features:
            self._log.warning(_NO_FEATURES.format(thefeatures=', '.join(features)))

    @staticmethod
    def _file_format_suffix(fmt: FileFormat):
        if isinstance(fmt, Parquet):
            return ".parquet"
        elif isinstance(fmt, Orc):
            return ".orc"
        elif isinstance(fmt, CSV):
            return ".csv"
        else:
            raise ValueError("Unknown file format: '{f}'".format(f=type(fmt).__name__))

    ###########################################
    # START GENERATED CODE - From here to EOF #
    ###########################################

    def get_entities(self) -> List[Entity]:
        """Get a list of all entities from the server.

        Returns:
            A list of entities.
        """
        r = self._get("/entity")
        result = self._json_or_handle_errors(r)
        return [Entity.from_json(d) for d in result]

    def get_recently_modified_entities(self) -> List[EntityCreatedUpdated]:
        """Get recently modified entity ids, with created and updated timestamps.

        Returns:
            A list of entity ids with created and updated timestamps
            associated with the given commit and recently modified.
        """
        r = self._get("/blame/entity")
        result = self._json_or_handle_errors(r)
        return [EntityCreatedUpdated.from_json(d) for d in result]

    def get_entity_by_id(
        self,
        entity_id: Union[EntityId, int],
        entity_version_id: Optional[Union[UUID, str]] = None
    ) -> Entity:
        """Get a entity from the server.

        Args:
            entity_id: Unique identifier of the entity to retrieve.

        Returns:
            The requested entity, if it exists.
        """
        if entity_version_id:
            r = self._get(f"/entity/{int(entity_id)}",
                          query={"id": str(entity_version_id)},
                          exclude_default_ref=True)
        else:
            r = self._get(f"/entity/{int(entity_id)}")
        result = self._json_or_handle_errors(r)
        return Entity.from_json(result)

    def try_get_entity_by_id(
        self,
        entity_id: Union[EntityId, int]
    ) -> Optional[Entity]:
        """Get a entity from the server.

        Args:
            entity_id: Unique identifier of the entity to retrieve.

        Returns:
            The requested entity, if it exists.
        """
        r = self._get(f"/entity/{int(entity_id)}")
        result = self._json_or_handle_errors(r, none_on_404=True)
        return Entity.from_json(result) if result else None

    def get_entity_by_name(self, name: Union[EntityName, str]) -> Entity:
        """Get a entity from the server.

        Args:
            name: Name of the entity to retrieve.

        Returns:
            The requested entity, if it exists.
        """
        r = self._get("/entity", query={'name': str(name)})
        result = self._json_or_handle_errors(r)
        return Entity.from_json(result)

    def try_get_entity_by_name(
        self,
        name: Union[EntityName, str]
    ) -> Optional[Entity]:
        """Get a entity from the server.

        Args:
            name: Name of the entity to retrieve.

        Returns:
            The requested entity, if it exists.
        """
        r = self._get("/entity", query={'name': str(name)})
        result = self._json_or_handle_errors(r, none_on_404=True)
        return Entity.from_json(result) if result else None

    def get_lineage_for_entity(
        self,
        entity_id: Union[EntityId, int]
    ) -> Lineage:
        """Get lineage data relating to a entity.

        Args:
            entity_id: Unique identifier of the entity.

        Returns:
            The lineage data, if the entity exists.
        """
        r = self._get(f"/lineage/entity/{int(entity_id)}")
        result = self._json_or_handle_errors(r)
        return Lineage.from_json(result)

    def create_entity(
        self,
        entity: EntityCreationRequest
    ) -> Entity:
        """Create a entity definition on the server.

        Args:
            entity: The entity definition.

        Returns:
            The new entity.
        """
        r = self._post("/entity", json=entity.to_json())
        if "entity" == "user_group":
            # Hack for user_group which currently doesn't return a single id!
            id = int(self._json_or_handle_errors(r)[0])
        else:
            id = self._int_or_handle_errors(r)
        return self.get_entity_by_id(id)

    def update_entity(self, entity: Entity) -> Entity:
        """Update an existing entity definition on the server.

        Args:
            entity: The entity definition.

        Returns:
            The entity definition, with its unique identifier and other computed
            fields updated.
        """
        r = self._put(f"/entity/{str(entity.id.value)}",
                      json=entity.to_json())
        _ = self._json_or_handle_errors(r)
        return self.get_entity_by_id(int(entity.id.value))

    def delete_entity_by_id(self, entity_id: Union[EntityId, int]):
        """Delete a entity from the server.

        Args:
            entity_id: Unique identifier of the entity to retrieve.

        Returns:
            The requested entity, if it exists.
        """
        r = self.delete(f"/entity/{int(entity_id)}")
        self._json_or_handle_errors(r)

    def get_entity_populations(self) -> List[EntityPopulation]:
        """Get a list of all entity_populations from the server.

        Returns:
            A list of entity_populations.
        """
        r = self._get("/entity-population")
        result = self._json_or_handle_errors(r)
        return [EntityPopulation.from_json(d) for d in result]

    def get_recently_modified_entity_populations(self) -> List[EntityPopulationCreatedUpdated]:
        """Get recently modified entity_population ids, with created and updated timestamps.

        Returns:
            A list of entity_population ids with created and updated timestamps
            associated with the given commit and recently modified.
        """
        r = self._get("/blame/entity-population")
        result = self._json_or_handle_errors(r)
        return [EntityPopulationCreatedUpdated.from_json(d) for d in result]

    def get_entity_population_by_id(
        self,
        entity_population_id: Union[EntityPopulationId, int],
        entity_population_version_id: Optional[Union[UUID, str]] = None
    ) -> EntityPopulation:
        """Get a entity_population from the server.

        Args:
            entity_population_id: Unique identifier of the entity_population to retrieve.

        Returns:
            The requested entity_population, if it exists.
        """
        if entity_population_version_id:
            r = self._get(f"/entity-population/{int(entity_population_id)}",
                          query={"id": str(entity_population_version_id)},
                          exclude_default_ref=True)
        else:
            r = self._get(f"/entity-population/{int(entity_population_id)}")
        result = self._json_or_handle_errors(r)
        return EntityPopulation.from_json(result)

    def try_get_entity_population_by_id(
        self,
        entity_population_id: Union[EntityPopulationId, int]
    ) -> Optional[EntityPopulation]:
        """Get a entity_population from the server.

        Args:
            entity_population_id: Unique identifier of the entity_population to retrieve.

        Returns:
            The requested entity_population, if it exists.
        """
        r = self._get(f"/entity-population/{int(entity_population_id)}")
        result = self._json_or_handle_errors(r, none_on_404=True)
        return EntityPopulation.from_json(result) if result else None

    def get_entity_population_by_name(self, name: Union[EntityPopulationName, str]) -> EntityPopulation:
        """Get a entity_population from the server.

        Args:
            name: Name of the entity_population to retrieve.

        Returns:
            The requested entity_population, if it exists.
        """
        r = self._get("/entity-population", query={'name': str(name)})
        result = self._json_or_handle_errors(r)
        return EntityPopulation.from_json(result)

    def try_get_entity_population_by_name(
        self,
        name: Union[EntityPopulationName, str]
    ) -> Optional[EntityPopulation]:
        """Get a entity_population from the server.

        Args:
            name: Name of the entity_population to retrieve.

        Returns:
            The requested entity_population, if it exists.
        """
        r = self._get("/entity_population", query={'name': str(name)})
        result = self._json_or_handle_errors(r, none_on_404=True)
        return EntityPopulation.from_json(result) if result else None

    def get_lineage_for_entity_population(
        self,
        entity_population_id: Union[EntityPopulationId, int]
    ) -> Lineage:
        """Get lineage data relating to a entity_population.

        Args:
            entity_population_id: Unique identifier of the entity_population.

        Returns:
            The lineage data, if the entity_population exists.
        """
        r = self._get(f"/lineage/entity-population/{int(entity_population_id)}")
        result = self._json_or_handle_errors(r)
        return Lineage.from_json(result)

    def create_entity_population(
        self,
        entity_population: EntityPopulationCreationRequest
    ) -> EntityPopulation:
        """Create a entity_population definition on the server.

        Args:
            entity_population: The entity_population definition.

        Returns:
            The new entity_population.
        """
        r = self._post("/entity-population", json=entity_population.to_json())
        if "entity_population" == "user_group":
            # Hack for user_group which currently doesn't return a single id!
            id = int(self._json_or_handle_errors(r)[0])
        else:
            id = self._int_or_handle_errors(r)
        return self.get_entity_population_by_id(id)

    def update_entity_population(self, entity_population: EntityPopulation) -> EntityPopulation:
        """Update an existing entity_population definition on the server.

        Args:
            entity_population: The entity_population definition.

        Returns:
            The entity_population definition, with its unique identifier and other computed
            fields updated.
        """
        r = self._put(f"/entity-population/{str(entity_population.id.value)}",
                      json=entity_population.to_json())
        _ = self._json_or_handle_errors(r)
        return self.get_entity_population_by_id(int(entity_population.id.value))

    def delete_entity_population_by_id(self, entity_population_id: Union[EntityPopulationId, int]):
        """Delete a entity_population from the server.

        Args:
            entity_population_id: Unique identifier of the entity_population to retrieve.

        Returns:
            The requested entity_population, if it exists.
        """
        r = self.delete(f"/entity-population/{int(entity_population_id)}")
        self._json_or_handle_errors(r)

    def get_tables(self) -> List[Table]:
        """Get a list of all tables from the server.

        Returns:
            A list of tables.
        """
        r = self._get("/table")
        result = self._json_or_handle_errors(r)
        return [Table.from_json(d) for d in result]

    def get_recently_modified_tables(self) -> List[TableCreatedUpdated]:
        """Get recently modified table ids, with created and updated timestamps.

        Returns:
            A list of table ids with created and updated timestamps
            associated with the given commit and recently modified.
        """
        r = self._get("/blame/table")
        result = self._json_or_handle_errors(r)
        return [TableCreatedUpdated.from_json(d) for d in result]

    def get_table_by_id(
        self,
        table_id: Union[TableId, int],
        table_version_id: Optional[Union[UUID, str]] = None
    ) -> Table:
        """Get a table from the server.

        Args:
            table_id: Unique identifier of the table to retrieve.

        Returns:
            The requested table, if it exists.
        """
        if table_version_id:
            r = self._get(f"/table/{int(table_id)}",
                          query={"id": str(table_version_id)},
                          exclude_default_ref=True)
        else:
            r = self._get(f"/table/{int(table_id)}")
        result = self._json_or_handle_errors(r)
        return Table.from_json(result)

    def try_get_table_by_id(
        self,
        table_id: Union[TableId, int]
    ) -> Optional[Table]:
        """Get a table from the server.

        Args:
            table_id: Unique identifier of the table to retrieve.

        Returns:
            The requested table, if it exists.
        """
        r = self._get(f"/table/{int(table_id)}")
        result = self._json_or_handle_errors(r, none_on_404=True)
        return Table.from_json(result) if result else None

    def get_table_by_name(self, name: Union[TableName, str]) -> Table:
        """Get a table from the server.

        Args:
            name: Name of the table to retrieve.

        Returns:
            The requested table, if it exists.
        """
        r = self._get("/table", query={'name': str(name)})
        result = self._json_or_handle_errors(r)
        return Table.from_json(result)

    def try_get_table_by_name(
        self,
        name: Union[TableName, str]
    ) -> Optional[Table]:
        """Get a table from the server.

        Args:
            name: Name of the table to retrieve.

        Returns:
            The requested table, if it exists.
        """
        r = self._get("/table", query={'name': str(name)})
        result = self._json_or_handle_errors(r, none_on_404=True)
        return Table.from_json(result) if result else None

    def get_lineage_for_table(
        self,
        table_id: Union[TableId, int]
    ) -> Lineage:
        """Get lineage data relating to a table.

        Args:
            table_id: Unique identifier of the table.

        Returns:
            The lineage data, if the table exists.
        """
        r = self._get(f"/lineage/table/{int(table_id)}")
        result = self._json_or_handle_errors(r)
        return Lineage.from_json(result)

    def create_table(
        self,
        table: TableCreationRequest
    ) -> Table:
        """Create a table definition on the server.

        Args:
            table: The table definition.

        Returns:
            The new table.
        """
        r = self._post("/table", json=table.to_json())
        if "table" == "user_group":
            # Hack for user_group which currently doesn't return a single id!
            id = int(self._json_or_handle_errors(r)[0])
        else:
            id = self._int_or_handle_errors(r)
        return self.get_table_by_id(id)

    def update_table(self, table: Table) -> Table:
        """Update an existing table definition on the server.

        Args:
            table: The table definition.

        Returns:
            The table definition, with its unique identifier and other computed
            fields updated.
        """
        r = self._put(f"/table/{str(table.id.value)}",
                      json=table.to_json())
        _ = self._json_or_handle_errors(r)
        return self.get_table_by_id(int(table.id.value))

    def delete_table_by_id(self, table_id: Union[TableId, int]):
        """Delete a table from the server.

        Args:
            table_id: Unique identifier of the table to retrieve.

        Returns:
            The requested table, if it exists.
        """
        r = self.delete(f"/table/{int(table_id)}")
        self._json_or_handle_errors(r)

    def get_features(self) -> List[Feature]:
        """Get a list of all features from the server.

        Returns:
            A list of features.
        """
        r = self._get("/feature")
        result = self._json_or_handle_errors(r)
        return [Feature.from_json(d) for d in result]

    def get_recently_modified_features(self) -> List[FeatureCreatedUpdated]:
        """Get recently modified feature ids, with created and updated timestamps.

        Returns:
            A list of feature ids with created and updated timestamps
            associated with the given commit and recently modified.
        """
        r = self._get("/blame/feature")
        result = self._json_or_handle_errors(r)
        return [FeatureCreatedUpdated.from_json(d) for d in result]

    def get_feature_by_id(
        self,
        feature_id: Union[FeatureId, int],
        feature_version_id: Optional[Union[UUID, str]] = None
    ) -> Feature:
        """Get a feature from the server.

        Args:
            feature_id: Unique identifier of the feature to retrieve.

        Returns:
            The requested feature, if it exists.
        """
        if feature_version_id:
            r = self._get(f"/feature/{int(feature_id)}",
                          query={"id": str(feature_version_id)},
                          exclude_default_ref=True)
        else:
            r = self._get(f"/feature/{int(feature_id)}")
        result = self._json_or_handle_errors(r)
        return Feature.from_json(result)

    def try_get_feature_by_id(
        self,
        feature_id: Union[FeatureId, int]
    ) -> Optional[Feature]:
        """Get a feature from the server.

        Args:
            feature_id: Unique identifier of the feature to retrieve.

        Returns:
            The requested feature, if it exists.
        """
        r = self._get(f"/feature/{int(feature_id)}")
        result = self._json_or_handle_errors(r, none_on_404=True)
        return Feature.from_json(result) if result else None

    def get_feature_by_name(self, name: Union[FeatureName, str]) -> Feature:
        """Get a feature from the server.

        Args:
            name: Name of the feature to retrieve.

        Returns:
            The requested feature, if it exists.
        """
        r = self._get("/feature", query={'name': str(name)})
        result = self._json_or_handle_errors(r)
        return Feature.from_json(result)

    def try_get_feature_by_name(
        self,
        name: Union[FeatureName, str]
    ) -> Optional[Feature]:
        """Get a feature from the server.

        Args:
            name: Name of the feature to retrieve.

        Returns:
            The requested feature, if it exists.
        """
        r = self._get("/feature", query={'name': str(name)})
        result = self._json_or_handle_errors(r, none_on_404=True)
        return Feature.from_json(result) if result else None

    def get_lineage_for_feature(
        self,
        feature_id: Union[FeatureId, int]
    ) -> Lineage:
        """Get lineage data relating to a feature.

        Args:
            feature_id: Unique identifier of the feature.

        Returns:
            The lineage data, if the feature exists.
        """
        r = self._get(f"/lineage/feature/{int(feature_id)}")
        result = self._json_or_handle_errors(r)
        return Lineage.from_json(result)

    def create_feature(
        self,
        feature: FeatureCreationRequest
    ) -> Feature:
        """Create a feature definition on the server.

        Args:
            feature: The feature definition.

        Returns:
            The new feature.
        """
        r = self._post("/feature", json=feature.to_json())
        if "feature" == "user_group":
            # Hack for user_group which currently doesn't return a single id!
            id = int(self._json_or_handle_errors(r)[0])
        else:
            id = self._int_or_handle_errors(r)
        return self.get_feature_by_id(id)

    def update_feature(self, feature: Feature) -> Feature:
        """Update an existing feature definition on the server.

        Args:
            feature: The feature definition.

        Returns:
            The feature definition, with its unique identifier and other computed
            fields updated.
        """
        r = self._put(f"/feature/{str(feature.id.value)}",
                      json=feature.to_json())
        _ = self._json_or_handle_errors(r)
        return self.get_feature_by_id(int(feature.id.value))

    def delete_feature_by_id(self, feature_id: Union[FeatureId, int]):
        """Delete a feature from the server.

        Args:
            feature_id: Unique identifier of the feature to retrieve.

        Returns:
            The requested feature, if it exists.
        """
        r = self.delete(f"/feature/{int(feature_id)}")
        self._json_or_handle_errors(r)

    def get_feature_templates(self) -> List[FeatureTemplate]:
        """Get a list of all feature_templates from the server.

        Returns:
            A list of feature_templates.
        """
        r = self._get("/feature-template")
        result = self._json_or_handle_errors(r)
        return [FeatureTemplate.from_json(d) for d in result]

    def get_recently_modified_feature_templates(self) -> List[FeatureTemplateCreatedUpdated]:
        """Get recently modified feature_template ids, with created and updated timestamps.

        Returns:
            A list of feature_template ids with created and updated timestamps
            associated with the given commit and recently modified.
        """
        r = self._get("/blame/feature-template")
        result = self._json_or_handle_errors(r)
        return [FeatureTemplateCreatedUpdated.from_json(d) for d in result]

    def get_feature_template_by_id(
        self,
        feature_template_id: Union[FeatureTemplateId, int],
        feature_template_version_id: Optional[Union[UUID, str]] = None
    ) -> FeatureTemplate:
        """Get a feature_template from the server.

        Args:
            feature_template_id: Unique identifier of the feature_template to retrieve.

        Returns:
            The requested feature_template, if it exists.
        """
        if feature_template_version_id:
            r = self._get(f"/feature-template/{int(feature_template_id)}",
                          query={"id": str(feature_template_version_id)},
                          exclude_default_ref=True)
        else:
            r = self._get(f"/feature-template/{int(feature_template_id)}")
        result = self._json_or_handle_errors(r)
        return FeatureTemplate.from_json(result)

    def try_get_feature_template_by_id(
        self,
        feature_template_id: Union[FeatureTemplateId, int]
    ) -> Optional[FeatureTemplate]:
        """Get a feature_template from the server.

        Args:
            feature_template_id: Unique identifier of the feature_template to retrieve.

        Returns:
            The requested feature_template, if it exists.
        """
        r = self._get(f"/feature-template/{int(feature_template_id)}")
        result = self._json_or_handle_errors(r, none_on_404=True)
        return FeatureTemplate.from_json(result) if result else None

    def get_feature_template_by_name(self, name: Union[FeatureTemplateName, str]) -> FeatureTemplate:
        """Get a feature_template from the server.

        Args:
            name: Name of the feature_template to retrieve.

        Returns:
            The requested feature_template, if it exists.
        """
        r = self._get("/feature-template", query={'name': str(name)})
        result = self._json_or_handle_errors(r)
        return FeatureTemplate.from_json(result)

    def try_get_feature_template_by_name(
        self,
        name: Union[FeatureTemplateName, str]
    ) -> Optional[FeatureTemplate]:
        """Get a feature_template from the server.

        Args:
            name: Name of the feature_template to retrieve.

        Returns:
            The requested feature_template, if it exists.
        """
        r = self._get("/feature_template", query={'name': str(name)})
        result = self._json_or_handle_errors(r, none_on_404=True)
        return FeatureTemplate.from_json(result) if result else None

    def get_lineage_for_feature_template(
        self,
        feature_template_id: Union[FeatureTemplateId, int]
    ) -> Lineage:
        """Get lineage data relating to a feature_template.

        Args:
            feature_template_id: Unique identifier of the feature_template.

        Returns:
            The lineage data, if the feature_template exists.
        """
        r = self._get(f"/lineage/feature-template/{int(feature_template_id)}")
        result = self._json_or_handle_errors(r)
        return Lineage.from_json(result)

    def create_feature_template(
        self,
        feature_template: FeatureTemplateCreationRequest
    ) -> FeatureTemplate:
        """Create a feature_template definition on the server.

        Args:
            feature_template: The feature_template definition.

        Returns:
            The new feature_template.
        """
        r = self._post("/feature-template", json=feature_template.to_json())
        if "feature_template" == "user_group":
            # Hack for user_group which currently doesn't return a single id!
            id = int(self._json_or_handle_errors(r)[0])
        else:
            id = self._int_or_handle_errors(r)
        return self.get_feature_template_by_id(id)

    def update_feature_template(self, feature_template: FeatureTemplate) -> FeatureTemplate:
        """Update an existing feature_template definition on the server.

        Args:
            feature_template: The feature_template definition.

        Returns:
            The feature_template definition, with its unique identifier and other computed
            fields updated.
        """
        r = self._put(f"/feature-template/{str(feature_template.id.value)}",
                      json=feature_template.to_json())
        _ = self._json_or_handle_errors(r)
        return self.get_feature_template_by_id(int(feature_template.id.value))

    def delete_feature_template_by_id(self, feature_template_id: Union[FeatureTemplateId, int]):
        """Delete a feature_template from the server.

        Args:
            feature_template_id: Unique identifier of the feature_template to retrieve.

        Returns:
            The requested feature_template, if it exists.
        """
        r = self.delete(f"/feature-template/{int(feature_template_id)}")
        self._json_or_handle_errors(r)

    def get_feature_sets(self) -> List[FeatureSet]:
        """Get a list of all feature_sets from the server.

        Returns:
            A list of feature_sets.
        """
        r = self._get("/feature-set")
        result = self._json_or_handle_errors(r)
        return [FeatureSet.from_json(d) for d in result]

    def get_recently_modified_feature_sets(self) -> List[FeatureSetCreatedUpdated]:
        """Get recently modified feature_set ids, with created and updated timestamps.

        Returns:
            A list of feature_set ids with created and updated timestamps
            associated with the given commit and recently modified.
        """
        r = self._get("/blame/feature-set")
        result = self._json_or_handle_errors(r)
        return [FeatureSetCreatedUpdated.from_json(d) for d in result]

    def get_feature_set_by_id(
        self,
        feature_set_id: Union[FeatureSetId, int],
        feature_set_version_id: Optional[Union[UUID, str]] = None
    ) -> FeatureSet:
        """Get a feature_set from the server.

        Args:
            feature_set_id: Unique identifier of the feature_set to retrieve.

        Returns:
            The requested feature_set, if it exists.
        """
        if feature_set_version_id:
            r = self._get(f"/feature-set/{int(feature_set_id)}",
                          query={"id": str(feature_set_version_id)},
                          exclude_default_ref=True)
        else:
            r = self._get(f"/feature-set/{int(feature_set_id)}")
        result = self._json_or_handle_errors(r)
        return FeatureSet.from_json(result)

    def try_get_feature_set_by_id(
        self,
        feature_set_id: Union[FeatureSetId, int]
    ) -> Optional[FeatureSet]:
        """Get a feature_set from the server.

        Args:
            feature_set_id: Unique identifier of the feature_set to retrieve.

        Returns:
            The requested feature_set, if it exists.
        """
        r = self._get(f"/feature-set/{int(feature_set_id)}")
        result = self._json_or_handle_errors(r, none_on_404=True)
        return FeatureSet.from_json(result) if result else None

    def get_feature_set_by_name(self, name: Union[FeatureSetName, str]) -> FeatureSet:
        """Get a feature_set from the server.

        Args:
            name: Name of the feature_set to retrieve.

        Returns:
            The requested feature_set, if it exists.
        """
        r = self._get("/feature-set", query={'name': str(name)})
        result = self._json_or_handle_errors(r)
        return FeatureSet.from_json(result)

    def try_get_feature_set_by_name(
        self,
        name: Union[FeatureSetName, str]
    ) -> Optional[FeatureSet]:
        """Get a feature_set from the server.

        Args:
            name: Name of the feature_set to retrieve.

        Returns:
            The requested feature_set, if it exists.
        """
        r = self._get("/feature_set", query={'name': str(name)})
        result = self._json_or_handle_errors(r, none_on_404=True)
        return FeatureSet.from_json(result) if result else None

    def get_lineage_for_feature_set(
        self,
        feature_set_id: Union[FeatureSetId, int]
    ) -> Lineage:
        """Get lineage data relating to a feature_set.

        Args:
            feature_set_id: Unique identifier of the feature_set.

        Returns:
            The lineage data, if the feature_set exists.
        """
        r = self._get(f"/lineage/feature-set/{int(feature_set_id)}")
        result = self._json_or_handle_errors(r)
        return Lineage.from_json(result)

    def create_feature_set(
        self,
        feature_set: FeatureSetCreationRequest
    ) -> FeatureSet:
        """Create a feature_set definition on the server.

        Args:
            feature_set: The feature_set definition.

        Returns:
            The new feature_set.
        """
        r = self._post("/feature-set", json=feature_set.to_json())
        if "feature_set" == "user_group":
            # Hack for user_group which currently doesn't return a single id!
            id = int(self._json_or_handle_errors(r)[0])
        else:
            id = self._int_or_handle_errors(r)
        return self.get_feature_set_by_id(id)

    def update_feature_set(self, feature_set: FeatureSet) -> FeatureSet:
        """Update an existing feature_set definition on the server.

        Args:
            feature_set: The feature_set definition.

        Returns:
            The feature_set definition, with its unique identifier and other computed
            fields updated.
        """
        r = self._put(f"/feature-set/{str(feature_set.id.value)}",
                      json=feature_set.to_json())
        _ = self._json_or_handle_errors(r)
        return self.get_feature_set_by_id(int(feature_set.id.value))

    def delete_feature_set_by_id(self, feature_set_id: Union[FeatureSetId, int]):
        """Delete a feature_set from the server.

        Args:
            feature_set_id: Unique identifier of the feature_set to retrieve.

        Returns:
            The requested feature_set, if it exists.
        """
        r = self.delete(f"/feature-set/{int(feature_set_id)}")
        self._json_or_handle_errors(r)

    def get_feature_stores(self) -> List[FeatureStore]:
        """Get a list of all feature_stores from the server.

        Returns:
            A list of feature_stores.
        """
        r = self._get("/feature-store")
        result = self._json_or_handle_errors(r)
        return [FeatureStore.from_json(d) for d in result]

    def get_recently_modified_feature_stores(self) -> List[FeatureStoreCreatedUpdated]:
        """Get recently modified feature_store ids, with created and updated timestamps.

        Returns:
            A list of feature_store ids with created and updated timestamps
            associated with the given commit and recently modified.
        """
        r = self._get("/blame/feature-store")
        result = self._json_or_handle_errors(r)
        return [FeatureStoreCreatedUpdated.from_json(d) for d in result]

    def get_feature_store_by_id(
        self,
        feature_store_id: Union[FeatureStoreId, int],
        feature_store_version_id: Optional[Union[UUID, str]] = None
    ) -> FeatureStore:
        """Get a feature_store from the server.

        Args:
            feature_store_id: Unique identifier of the feature_store to retrieve.

        Returns:
            The requested feature_store, if it exists.
        """
        if feature_store_version_id:
            r = self._get(f"/feature-store/{int(feature_store_id)}",
                          query={"id": str(feature_store_version_id)},
                          exclude_default_ref=True)
        else:
            r = self._get(f"/feature-store/{int(feature_store_id)}")
        result = self._json_or_handle_errors(r)
        return FeatureStore.from_json(result)

    def try_get_feature_store_by_id(
        self,
        feature_store_id: Union[FeatureStoreId, int]
    ) -> Optional[FeatureStore]:
        """Get a feature_store from the server.

        Args:
            feature_store_id: Unique identifier of the feature_store to retrieve.

        Returns:
            The requested feature_store, if it exists.
        """
        r = self._get(f"/feature-store/{int(feature_store_id)}")
        result = self._json_or_handle_errors(r, none_on_404=True)
        return FeatureStore.from_json(result) if result else None

    def get_feature_store_by_name(self, name: Union[FeatureStoreName, str]) -> FeatureStore:
        """Get a feature_store from the server.

        Args:
            name: Name of the feature_store to retrieve.

        Returns:
            The requested feature_store, if it exists.
        """
        r = self._get("/feature-store", query={'name': str(name)})
        result = self._json_or_handle_errors(r)
        return FeatureStore.from_json(result)

    def try_get_feature_store_by_name(
        self,
        name: Union[FeatureStoreName, str]
    ) -> Optional[FeatureStore]:
        """Get a feature_store from the server.

        Args:
            name: Name of the feature_store to retrieve.

        Returns:
            The requested feature_store, if it exists.
        """
        r = self._get("/feature_store", query={'name': str(name)})
        result = self._json_or_handle_errors(r, none_on_404=True)
        return FeatureStore.from_json(result) if result else None

    def get_lineage_for_feature_store(
        self,
        feature_store_id: Union[FeatureStoreId, int]
    ) -> Lineage:
        """Get lineage data relating to a feature_store.

        Args:
            feature_store_id: Unique identifier of the feature_store.

        Returns:
            The lineage data, if the feature_store exists.
        """
        r = self._get(f"/lineage/feature-store/{int(feature_store_id)}")
        result = self._json_or_handle_errors(r)
        return Lineage.from_json(result)

    def create_feature_store(
        self,
        feature_store: FeatureStoreCreationRequest
    ) -> FeatureStore:
        """Create a feature_store definition on the server.

        Args:
            feature_store: The feature_store definition.

        Returns:
            The new feature_store.
        """
        r = self._post("/feature-store", json=feature_store.to_json())
        if "feature_store" == "user_group":
            # Hack for user_group which currently doesn't return a single id!
            id = int(self._json_or_handle_errors(r)[0])
        else:
            id = self._int_or_handle_errors(r)
        return self.get_feature_store_by_id(id)

    def update_feature_store(self, feature_store: FeatureStore) -> FeatureStore:
        """Update an existing feature_store definition on the server.

        Args:
            feature_store: The feature_store definition.

        Returns:
            The feature_store definition, with its unique identifier and other computed
            fields updated.
        """
        r = self._put(f"/feature-store/{str(feature_store.id.value)}",
                      json=feature_store.to_json())
        _ = self._json_or_handle_errors(r)
        return self.get_feature_store_by_id(int(feature_store.id.value))

    def delete_feature_store_by_id(self, feature_store_id: Union[FeatureStoreId, int]):
        """Delete a feature_store from the server.

        Args:
            feature_store_id: Unique identifier of the feature_store to retrieve.

        Returns:
            The requested feature_store, if it exists.
        """
        r = self.delete(f"/feature-store/{int(feature_store_id)}")
        self._json_or_handle_errors(r)

    def get_view_materialisations(self) -> List[ViewMaterialisationJob]:
        """Get a list of all view_materialisations from the server.

        Returns:
            A list of view_materialisations.
        """
        r = self._get("/view-materialisation")
        result = self._json_or_handle_errors(r)
        return [ViewMaterialisationJob.from_json(d) for d in result]

    def get_recently_modified_view_materialisations(self) -> List[ViewMaterialisationJobCreatedUpdated]:
        """Get recently modified view_materialisation ids, with created and updated timestamps.

        Returns:
            A list of view_materialisation ids with created and updated timestamps
            associated with the given commit and recently modified.
        """
        r = self._get("/blame/view-materialisation")
        result = self._json_or_handle_errors(r)
        return [ViewMaterialisationJobCreatedUpdated.from_json(d) for d in result]

    def get_view_materialisation_by_id(
        self,
        view_materialisation_id: Union[ViewMaterialisationJobId, int],
        view_materialisation_version_id: Optional[Union[UUID, str]] = None
    ) -> ViewMaterialisationJob:
        """Get a view_materialisation from the server.

        Args:
            view_materialisation_id: Unique identifier of the view_materialisation to retrieve.

        Returns:
            The requested view_materialisation, if it exists.
        """
        if view_materialisation_version_id:
            r = self._get(f"/view-materialisation/{int(view_materialisation_id)}",
                          query={"id": str(view_materialisation_version_id)},
                          exclude_default_ref=True)
        else:
            r = self._get(f"/view-materialisation/{int(view_materialisation_id)}")
        result = self._json_or_handle_errors(r)
        return ViewMaterialisationJob.from_json(result)

    def try_get_view_materialisation_by_id(
        self,
        view_materialisation_id: Union[ViewMaterialisationJobId, int]
    ) -> Optional[ViewMaterialisationJob]:
        """Get a view_materialisation from the server.

        Args:
            view_materialisation_id: Unique identifier of the view_materialisation to retrieve.

        Returns:
            The requested view_materialisation, if it exists.
        """
        r = self._get(f"/view-materialisation/{int(view_materialisation_id)}")
        result = self._json_or_handle_errors(r, none_on_404=True)
        return ViewMaterialisationJob.from_json(result) if result else None

    def get_view_materialisation_by_name(self, name: Union[ViewMaterialisationJobName, str]) -> ViewMaterialisationJob:
        """Get a view_materialisation from the server.

        Args:
            name: Name of the view_materialisation to retrieve.

        Returns:
            The requested view_materialisation, if it exists.
        """
        r = self._get("/view-materialisation", query={'name': str(name)})
        result = self._json_or_handle_errors(r)
        return ViewMaterialisationJob.from_json(result)

    def try_get_view_materialisation_by_name(
        self,
        name: Union[ViewMaterialisationJobName, str]
    ) -> Optional[ViewMaterialisationJob]:
        """Get a view_materialisation from the server.

        Args:
            name: Name of the view_materialisation to retrieve.

        Returns:
            The requested view_materialisation, if it exists.
        """
        r = self._get("/view_materialisation", query={'name': str(name)})
        result = self._json_or_handle_errors(r, none_on_404=True)
        return ViewMaterialisationJob.from_json(result) if result else None

    def get_lineage_for_view_materialisation(
        self,
        view_materialisation_id: Union[ViewMaterialisationJobId, int]
    ) -> Lineage:
        """Get lineage data relating to a view_materialisation.

        Args:
            view_materialisation_id: Unique identifier of the view_materialisation.

        Returns:
            The lineage data, if the view_materialisation exists.
        """
        r = self._get(f"/lineage/view-materialisation/{int(view_materialisation_id)}")
        result = self._json_or_handle_errors(r)
        return Lineage.from_json(result)

    def create_view_materialisation(
        self,
        view_materialisation: ViewMaterialisationJobCreationRequest
    ) -> ViewMaterialisationJob:
        """Create a view_materialisation definition on the server.

        Args:
            view_materialisation: The view_materialisation definition.

        Returns:
            The new view_materialisation.
        """
        r = self._post("/view-materialisation", json=view_materialisation.to_json())
        if "view_materialisation" == "user_group":
            # Hack for user_group which currently doesn't return a single id!
            id = int(self._json_or_handle_errors(r)[0])
        else:
            id = self._int_or_handle_errors(r)
        return self.get_view_materialisation_by_id(id)

    def update_view_materialisation(self, view_materialisation: ViewMaterialisationJob) -> ViewMaterialisationJob:
        """Update an existing view_materialisation definition on the server.

        Args:
            view_materialisation: The view_materialisation definition.

        Returns:
            The view_materialisation definition, with its unique identifier and other computed
            fields updated.
        """
        r = self._put(f"/view-materialisation/{str(view_materialisation.id.value)}",
                      json=view_materialisation.to_json())
        _ = self._json_or_handle_errors(r)
        return self.get_view_materialisation_by_id(int(view_materialisation.id.value))

    def delete_view_materialisation_by_id(self, view_materialisation_id: Union[ViewMaterialisationJobId, int]):
        """Delete a view_materialisation from the server.

        Args:
            view_materialisation_id: Unique identifier of the view_materialisation to retrieve.

        Returns:
            The requested view_materialisation, if it exists.
        """
        r = self.delete(f"/view-materialisation/{int(view_materialisation_id)}")
        self._json_or_handle_errors(r)

    def get_sources(self) -> List[Source]:
        """Get a list of all sources from the server.

        Returns:
            A list of sources.
        """
        r = self._get("/source")
        result = self._json_or_handle_errors(r)
        return [Source.from_json(d) for d in result]

    def get_recently_modified_sources(self) -> List[SourceCreatedUpdated]:
        """Get recently modified source ids, with created and updated timestamps.

        Returns:
            A list of source ids with created and updated timestamps
            associated with the given commit and recently modified.
        """
        r = self._get("/blame/source")
        result = self._json_or_handle_errors(r)
        return [SourceCreatedUpdated.from_json(d) for d in result]

    def get_source_by_id(
        self,
        source_id: Union[SourceId, int],
        source_version_id: Optional[Union[UUID, str]] = None
    ) -> Source:
        """Get a source from the server.

        Args:
            source_id: Unique identifier of the source to retrieve.

        Returns:
            The requested source, if it exists.
        """
        if source_version_id:
            r = self._get(f"/source/{int(source_id)}",
                          query={"id": str(source_version_id)},
                          exclude_default_ref=True)
        else:
            r = self._get(f"/source/{int(source_id)}")
        result = self._json_or_handle_errors(r)
        return Source.from_json(result)

    def try_get_source_by_id(
        self,
        source_id: Union[SourceId, int]
    ) -> Optional[Source]:
        """Get a source from the server.

        Args:
            source_id: Unique identifier of the source to retrieve.

        Returns:
            The requested source, if it exists.
        """
        r = self._get(f"/source/{int(source_id)}")
        result = self._json_or_handle_errors(r, none_on_404=True)
        return Source.from_json(result) if result else None

    def get_source_by_name(self, name: Union[SourceName, str]) -> Source:
        """Get a source from the server.

        Args:
            name: Name of the source to retrieve.

        Returns:
            The requested source, if it exists.
        """
        r = self._get("/source", query={'name': str(name)})
        result = self._json_or_handle_errors(r)
        return Source.from_json(result)

    def try_get_source_by_name(
        self,
        name: Union[SourceName, str]
    ) -> Optional[Source]:
        """Get a source from the server.

        Args:
            name: Name of the source to retrieve.

        Returns:
            The requested source, if it exists.
        """
        r = self._get("/source", query={'name': str(name)})
        result = self._json_or_handle_errors(r, none_on_404=True)
        return Source.from_json(result) if result else None

    def get_lineage_for_source(
        self,
        source_id: Union[SourceId, int]
    ) -> Lineage:
        """Get lineage data relating to a source.

        Args:
            source_id: Unique identifier of the source.

        Returns:
            The lineage data, if the source exists.
        """
        r = self._get(f"/lineage/source/{int(source_id)}")
        result = self._json_or_handle_errors(r)
        return Lineage.from_json(result)

    def create_source(
        self,
        source: SourceCreationRequest
    ) -> Source:
        """Create a source definition on the server.

        Args:
            source: The source definition.

        Returns:
            The new source.
        """
        r = self._post("/source", json=source.to_json())
        if "source" == "user_group":
            # Hack for user_group which currently doesn't return a single id!
            id = int(self._json_or_handle_errors(r)[0])
        else:
            id = self._int_or_handle_errors(r)
        return self.get_source_by_id(id)

    def update_source(self, source: Source) -> Source:
        """Update an existing source definition on the server.

        Args:
            source: The source definition.

        Returns:
            The source definition, with its unique identifier and other computed
            fields updated.
        """
        r = self._put(f"/source/{str(source.id.value)}",
                      json=source.to_json())
        _ = self._json_or_handle_errors(r)
        return self.get_source_by_id(int(source.id.value))

    def delete_source_by_id(self, source_id: Union[SourceId, int]):
        """Delete a source from the server.

        Args:
            source_id: Unique identifier of the source to retrieve.

        Returns:
            The requested source, if it exists.
        """
        r = self.delete(f"/source/{int(source_id)}")
        self._json_or_handle_errors(r)

    def get_destinations(self) -> List[Destination]:
        """Get a list of all destinations from the server.

        Returns:
            A list of destinations.
        """
        r = self._get("/destination")
        result = self._json_or_handle_errors(r)
        return [Destination.from_json(d) for d in result]

    def get_recently_modified_destinations(self) -> List[DestinationCreatedUpdated]:
        """Get recently modified destination ids, with created and updated timestamps.

        Returns:
            A list of destination ids with created and updated timestamps
            associated with the given commit and recently modified.
        """
        r = self._get("/blame/destination")
        result = self._json_or_handle_errors(r)
        return [DestinationCreatedUpdated.from_json(d) for d in result]

    def get_destination_by_id(
        self,
        destination_id: Union[DestinationId, int],
        destination_version_id: Optional[Union[UUID, str]] = None
    ) -> Destination:
        """Get a destination from the server.

        Args:
            destination_id: Unique identifier of the destination to retrieve.

        Returns:
            The requested destination, if it exists.
        """
        if destination_version_id:
            r = self._get(f"/destination/{int(destination_id)}",
                          query={"id": str(destination_version_id)},
                          exclude_default_ref=True)
        else:
            r = self._get(f"/destination/{int(destination_id)}")
        result = self._json_or_handle_errors(r)
        return Destination.from_json(result)

    def try_get_destination_by_id(
        self,
        destination_id: Union[DestinationId, int]
    ) -> Optional[Destination]:
        """Get a destination from the server.

        Args:
            destination_id: Unique identifier of the destination to retrieve.

        Returns:
            The requested destination, if it exists.
        """
        r = self._get(f"/destination/{int(destination_id)}")
        result = self._json_or_handle_errors(r, none_on_404=True)
        return Destination.from_json(result) if result else None

    def get_destination_by_name(self, name: Union[DestinationName, str]) -> Destination:
        """Get a destination from the server.

        Args:
            name: Name of the destination to retrieve.

        Returns:
            The requested destination, if it exists.
        """
        r = self._get("/destination", query={'name': str(name)})
        result = self._json_or_handle_errors(r)
        return Destination.from_json(result)

    def try_get_destination_by_name(
        self,
        name: Union[DestinationName, str]
    ) -> Optional[Destination]:
        """Get a destination from the server.

        Args:
            name: Name of the destination to retrieve.

        Returns:
            The requested destination, if it exists.
        """
        r = self._get("/destination", query={'name': str(name)})
        result = self._json_or_handle_errors(r, none_on_404=True)
        return Destination.from_json(result) if result else None

    def get_lineage_for_destination(
        self,
        destination_id: Union[DestinationId, int]
    ) -> Lineage:
        """Get lineage data relating to a destination.

        Args:
            destination_id: Unique identifier of the destination.

        Returns:
            The lineage data, if the destination exists.
        """
        r = self._get(f"/lineage/destination/{int(destination_id)}")
        result = self._json_or_handle_errors(r)
        return Lineage.from_json(result)

    def create_destination(
        self,
        destination: DestinationCreationRequest
    ) -> Destination:
        """Create a destination definition on the server.

        Args:
            destination: The destination definition.

        Returns:
            The new destination.
        """
        r = self._post("/destination", json=destination.to_json())
        if "destination" == "user_group":
            # Hack for user_group which currently doesn't return a single id!
            id = int(self._json_or_handle_errors(r)[0])
        else:
            id = self._int_or_handle_errors(r)
        return self.get_destination_by_id(id)

    def update_destination(self, destination: Destination) -> Destination:
        """Update an existing destination definition on the server.

        Args:
            destination: The destination definition.

        Returns:
            The destination definition, with its unique identifier and other computed
            fields updated.
        """
        r = self._put(f"/destination/{str(destination.id.value)}",
                      json=destination.to_json())
        _ = self._json_or_handle_errors(r)
        return self.get_destination_by_id(int(destination.id.value))

    def delete_destination_by_id(self, destination_id: Union[DestinationId, int]):
        """Delete a destination from the server.

        Args:
            destination_id: Unique identifier of the destination to retrieve.

        Returns:
            The requested destination, if it exists.
        """
        r = self.delete(f"/destination/{int(destination_id)}")
        self._json_or_handle_errors(r)

    def get_clusters(self) -> List[Cluster]:
        """Get a list of all clusters from the server.

        Returns:
            A list of clusters.
        """
        r = self._get("/cluster")
        result = self._json_or_handle_errors(r)
        return [Cluster.from_json(d) for d in result]

    def get_recently_modified_clusters(self) -> List[ClusterCreatedUpdated]:
        """Get recently modified cluster ids, with created and updated timestamps.

        Returns:
            A list of cluster ids with created and updated timestamps
            associated with the given commit and recently modified.
        """
        r = self._get("/blame/cluster")
        result = self._json_or_handle_errors(r)
        return [ClusterCreatedUpdated.from_json(d) for d in result]

    def get_cluster_by_id(
        self,
        cluster_id: Union[ClusterId, int],
        cluster_version_id: Optional[Union[UUID, str]] = None
    ) -> Cluster:
        """Get a cluster from the server.

        Args:
            cluster_id: Unique identifier of the cluster to retrieve.

        Returns:
            The requested cluster, if it exists.
        """
        if cluster_version_id:
            r = self._get(f"/cluster/{int(cluster_id)}",
                          query={"id": str(cluster_version_id)},
                          exclude_default_ref=True)
        else:
            r = self._get(f"/cluster/{int(cluster_id)}")
        result = self._json_or_handle_errors(r)
        return Cluster.from_json(result)

    def try_get_cluster_by_id(
        self,
        cluster_id: Union[ClusterId, int]
    ) -> Optional[Cluster]:
        """Get a cluster from the server.

        Args:
            cluster_id: Unique identifier of the cluster to retrieve.

        Returns:
            The requested cluster, if it exists.
        """
        r = self._get(f"/cluster/{int(cluster_id)}")
        result = self._json_or_handle_errors(r, none_on_404=True)
        return Cluster.from_json(result) if result else None

    def get_cluster_by_name(self, name: Union[ClusterName, str]) -> Cluster:
        """Get a cluster from the server.

        Args:
            name: Name of the cluster to retrieve.

        Returns:
            The requested cluster, if it exists.
        """
        r = self._get("/cluster", query={'name': str(name)})
        result = self._json_or_handle_errors(r)
        return Cluster.from_json(result)

    def try_get_cluster_by_name(
        self,
        name: Union[ClusterName, str]
    ) -> Optional[Cluster]:
        """Get a cluster from the server.

        Args:
            name: Name of the cluster to retrieve.

        Returns:
            The requested cluster, if it exists.
        """
        r = self._get("/cluster", query={'name': str(name)})
        result = self._json_or_handle_errors(r, none_on_404=True)
        return Cluster.from_json(result) if result else None

    def create_cluster(
        self,
        cluster: ClusterCreationRequest
    ) -> Cluster:
        """Create a cluster definition on the server.

        Args:
            cluster: The cluster definition.

        Returns:
            The new cluster.
        """
        r = self._post("/cluster", json=cluster.to_json())
        if "cluster" == "user_group":
            # Hack for user_group which currently doesn't return a single id!
            id = int(self._json_or_handle_errors(r)[0])
        else:
            id = self._int_or_handle_errors(r)
        return self.get_cluster_by_id(id)

    def update_cluster(self, cluster: Cluster) -> Cluster:
        """Update an existing cluster definition on the server.

        Args:
            cluster: The cluster definition.

        Returns:
            The cluster definition, with its unique identifier and other computed
            fields updated.
        """
        r = self._put(f"/cluster/{str(cluster.id.value)}",
                      json=cluster.to_json())
        _ = self._json_or_handle_errors(r)
        return self.get_cluster_by_id(int(cluster.id.value))

    def delete_cluster_by_id(self, cluster_id: Union[ClusterId, int]):
        """Delete a cluster from the server.

        Args:
            cluster_id: Unique identifier of the cluster to retrieve.

        Returns:
            The requested cluster, if it exists.
        """
        r = self.delete(f"/cluster/{int(cluster_id)}")
        self._json_or_handle_errors(r)

    def get_merge_requests(self) -> List[MergeRequest]:
        """Get a list of all merge_requests from the server.

        Returns:
            A list of merge_requests.
        """
        r = self._get("/merge-request")
        result = self._json_or_handle_errors(r)
        return [MergeRequest.from_json(d) for d in result]

    def get_merge_request_by_id(
        self,
        merge_request_id: Union[MergeRequestId, int],
        merge_request_version_id: Optional[Union[UUID, str]] = None
    ) -> MergeRequest:
        """Get a merge_request from the server.

        Args:
            merge_request_id: Unique identifier of the merge_request to retrieve.

        Returns:
            The requested merge_request, if it exists.
        """
        if merge_request_version_id:
            r = self._get(f"/merge-request/{int(merge_request_id)}",
                          query={"id": str(merge_request_version_id)},
                          exclude_default_ref=True)
        else:
            r = self._get(f"/merge-request/{int(merge_request_id)}")
        result = self._json_or_handle_errors(r)
        return MergeRequest.from_json(result)

    def try_get_merge_request_by_id(
        self,
        merge_request_id: Union[MergeRequestId, int]
    ) -> Optional[MergeRequest]:
        """Get a merge_request from the server.

        Args:
            merge_request_id: Unique identifier of the merge_request to retrieve.

        Returns:
            The requested merge_request, if it exists.
        """
        r = self._get(f"/merge-request/{int(merge_request_id)}")
        result = self._json_or_handle_errors(r, none_on_404=True)
        return MergeRequest.from_json(result) if result else None

    def create_merge_request(
        self,
        merge_request: MergeRequestCreationRequest
    ) -> MergeRequest:
        """Create a merge_request definition on the server.

        Args:
            merge_request: The merge_request definition.

        Returns:
            The new merge_request.
        """
        r = self._post("/merge-request", json=merge_request.to_json())
        if "merge_request" == "user_group":
            # Hack for user_group which currently doesn't return a single id!
            id = int(self._json_or_handle_errors(r)[0])
        else:
            id = self._int_or_handle_errors(r)
        return self.get_merge_request_by_id(id)

    def update_merge_request(self, merge_request: MergeRequest) -> MergeRequest:
        """Update an existing merge_request definition on the server.

        Args:
            merge_request: The merge_request definition.

        Returns:
            The merge_request definition, with its unique identifier and other computed
            fields updated.
        """
        r = self._put(f"/merge-request/{str(merge_request.id.value)}",
                      json=merge_request.to_json())
        _ = self._json_or_handle_errors(r)
        return self.get_merge_request_by_id(int(merge_request.id.value))

    def delete_merge_request_by_id(self, merge_request_id: Union[MergeRequestId, int]):
        """Delete a merge_request from the server.

        Args:
            merge_request_id: Unique identifier of the merge_request to retrieve.

        Returns:
            The requested merge_request, if it exists.
        """
        r = self.delete(f"/merge-request/{int(merge_request_id)}")
        self._json_or_handle_errors(r)

    def get_users(self) -> List[User]:
        """Get a list of all users from the server.

        Returns:
            A list of users.
        """
        r = self._get("/user")
        result = self._json_or_handle_errors(r)
        return [User.from_json(d) for d in result]

    def get_user_by_id(
        self,
        user_id: Union[UserId, int],
        user_version_id: Optional[Union[UUID, str]] = None
    ) -> User:
        """Get a user from the server.

        Args:
            user_id: Unique identifier of the user to retrieve.

        Returns:
            The requested user, if it exists.
        """
        if user_version_id:
            r = self._get(f"/user/{int(user_id)}",
                          query={"id": str(user_version_id)},
                          exclude_default_ref=True)
        else:
            r = self._get(f"/user/{int(user_id)}")
        result = self._json_or_handle_errors(r)
        return User.from_json(result)

    def try_get_user_by_id(
        self,
        user_id: Union[UserId, int]
    ) -> Optional[User]:
        """Get a user from the server.

        Args:
            user_id: Unique identifier of the user to retrieve.

        Returns:
            The requested user, if it exists.
        """
        r = self._get(f"/user/{int(user_id)}")
        result = self._json_or_handle_errors(r, none_on_404=True)
        return User.from_json(result) if result else None

    def create_user(
        self,
        user: UserCreationRequest
    ) -> User:
        """Create a user definition on the server.

        Args:
            user: The user definition.

        Returns:
            The new user.
        """
        r = self._post("/user", json=user.to_json())
        if "user" == "user_group":
            # Hack for user_group which currently doesn't return a single id!
            id = int(self._json_or_handle_errors(r)[0])
        else:
            id = self._int_or_handle_errors(r)
        return self.get_user_by_id(id)

    def update_user(self, user: User) -> User:
        """Update an existing user definition on the server.

        Args:
            user: The user definition.

        Returns:
            The user definition, with its unique identifier and other computed
            fields updated.
        """
        r = self._put(f"/user/{str(user.id.value)}",
                      json=user.to_json())
        _ = self._json_or_handle_errors(r)
        return self.get_user_by_id(int(user.id.value))

    def delete_user_by_id(self, user_id: Union[UserId, int]):
        """Delete a user from the server.

        Args:
            user_id: Unique identifier of the user to retrieve.

        Returns:
            The requested user, if it exists.
        """
        r = self.delete(f"/user/{int(user_id)}")
        self._json_or_handle_errors(r)

    def get_user_groups(self) -> List[UserGroup]:
        """Get a list of all user_groups from the server.

        Returns:
            A list of user_groups.
        """
        r = self._get("/user-group")
        result = self._json_or_handle_errors(r)
        return [UserGroup.from_json(d) for d in result]

    def get_user_group_by_id(
        self,
        user_group_id: Union[UserGroupId, int],
        user_group_version_id: Optional[Union[UUID, str]] = None
    ) -> UserGroup:
        """Get a user_group from the server.

        Args:
            user_group_id: Unique identifier of the user_group to retrieve.

        Returns:
            The requested user_group, if it exists.
        """
        if user_group_version_id:
            r = self._get(f"/user-group/{int(user_group_id)}",
                          query={"id": str(user_group_version_id)},
                          exclude_default_ref=True)
        else:
            r = self._get(f"/user-group/{int(user_group_id)}")
        result = self._json_or_handle_errors(r)
        return UserGroup.from_json(result)

    def try_get_user_group_by_id(
        self,
        user_group_id: Union[UserGroupId, int]
    ) -> Optional[UserGroup]:
        """Get a user_group from the server.

        Args:
            user_group_id: Unique identifier of the user_group to retrieve.

        Returns:
            The requested user_group, if it exists.
        """
        r = self._get(f"/user-group/{int(user_group_id)}")
        result = self._json_or_handle_errors(r, none_on_404=True)
        return UserGroup.from_json(result) if result else None

    def get_user_group_by_name(self, name: Union[UserGroupName, str]) -> UserGroup:
        """Get a user_group from the server.

        Args:
            name: Name of the user_group to retrieve.

        Returns:
            The requested user_group, if it exists.
        """
        r = self._get("/user-group", query={'name': str(name)})
        result = self._json_or_handle_errors(r)
        return UserGroup.from_json(result)

    def try_get_user_group_by_name(
        self,
        name: Union[UserGroupName, str]
    ) -> Optional[UserGroup]:
        """Get a user_group from the server.

        Args:
            name: Name of the user_group to retrieve.

        Returns:
            The requested user_group, if it exists.
        """
        r = self._get("/user_group", query={'name': str(name)})
        result = self._json_or_handle_errors(r, none_on_404=True)
        return UserGroup.from_json(result) if result else None

    def create_user_group(
        self,
        user_group: UserGroupCreationRequest
    ) -> UserGroup:
        """Create a user_group definition on the server.

        Args:
            user_group: The user_group definition.

        Returns:
            The new user_group.
        """
        r = self._post("/user-group", json=user_group.to_json())
        if "user_group" == "user_group":
            # Hack for user_group which currently doesn't return a single id!
            id = int(self._json_or_handle_errors(r)[0])
        else:
            id = self._int_or_handle_errors(r)
        return self.get_user_group_by_id(id)

    def update_user_group(self, user_group: UserGroup) -> UserGroup:
        """Update an existing user_group definition on the server.

        Args:
            user_group: The user_group definition.

        Returns:
            The user_group definition, with its unique identifier and other computed
            fields updated.
        """
        r = self._put(f"/user-group/{str(user_group.id.value)}",
                      json=user_group.to_json())
        _ = self._json_or_handle_errors(r)
        return self.get_user_group_by_id(int(user_group.id.value))

    def delete_user_group_by_id(self, user_group_id: Union[UserGroupId, int]):
        """Delete a user_group from the server.

        Args:
            user_group_id: Unique identifier of the user_group to retrieve.

        Returns:
            The requested user_group, if it exists.
        """
        r = self.delete(f"/user-group/{int(user_group_id)}")
        self._json_or_handle_errors(r)

    ######################
    # END GENERATED CODE #
    ######################

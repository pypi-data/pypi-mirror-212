#
#  Copyright 2021 Simple Machines Pty Ltd - All Rights Reserved.
#
#  This file is part of Anaml.
#
#  Unauthorized copying and/or distribution of this file, via any medium
#  is strictly prohibited.
#
import os.path
import unittest
import uuid
from typing import Dict, Tuple, Optional

import pytest

from anaml_client.models import *
from base import IntegrationTestBase, fixed_uuid
from fixtures import cluster_json_fixture, featureset_json_fixture


BILLING_TABLE_COLUMNS = [
    'billing_account_id', 'service', 'sku', 'usage_start_time', 'usage_end_time', 'project', 'labels',
    'system_labels', 'location', 'export_time', 'cost', 'currency', 'currency_conversion_rate', 'usage',
    'credits', 'invoice', 'cost_type', 'adjustment_info'
]

BILLING_TABLE_RECORDS = 239876


def local_featurestore_json(
        test_id: str,
        cluster_id: int,
        destination_id: int,
        featureset_id: int,
        folder: Optional[str] = None,
        table: Optional[str] = None
) -> dict:
    if folder:
        dest = {
            "adt_type": "folder",
            "destinationId": destination_id,
            "folder": folder,
            "folderPartitioningEnabled": True,
            "saveMode": "overwrite",
            "options": []
        }
    else:
        dest = {
            "adt_type": "table",
            "destinationId": destination_id,
            "tableName": table,
            "saveMode": "overwrite",
            "options": []
        }
    return {
        "adt_type": "batch",
        "name": f"feature_store_{destination_id}_{test_id}",
        "description": f"Feature store for test {test_id}",
        "labels": [],
        "attributes": [],
        "featureSet": featureset_id,
        "enabled": False,
        "destinations": [dest],
        "cluster": cluster_id,
        "schedule": {"adt_type": "never"},
        "startDate": None,
        "endDate": None,
        "versionTarget": None
    }


@pytest.mark.usefixtures("spark_session")
@unittest.skip("Fix this (docker-compose spark broken)")
class TestLoadingDataPandasIntegration(IntegrationTestBase):
    """Test SDK functionality to load feature data."""

    test_id: str
    destinations: Dict[Tuple[str, str], int] = {}
    store_local_csv: int
    run_local_csv: int
    store_local_orc: int
    run_local_orc: int
    store_bigquery: int
    run_bigquery: int

    def setUp(self):
        self.test_id = fixed_uuid()
        self.cluster_id = int(self.client._post("/cluster", cluster_json_fixture(self.test_id)).text)
        self.featureset_id = int(
            self.client._post("/feature-set", featureset_json_fixture(self.test_id, self.entity_id)).text
        )
        self.store_local_csv, self.run_local_csv = self._create_feature_store_run(
            destination="local", folder="bands", format=CSV(
                sep=",",
                quoteAll=False,
                includeHeader=True,
                emptyValue="",
                compression="none",
                dateFormat="yyyy-MM-dd",
                timestampFormat="yyyy-MM-dd'T'HH:mm:ss[.SSS][XXX]",
                ignoreLeadingWhiteSpace=False,
                ignoreTrailingWhiteSpace=False,
                lineSep="\n"
            )
        )
        self.store_gcs_orc, self.run_gcs_orc = self._create_feature_store_run(
            destination="gcs", folder="transactions", format=Orc()
        )
        self.store_bigquery, self.run_bigquery = self._create_feature_store_run(
            destination="bigquery", table="test_python_bigquery"
        )

    def _get_destination(self, type: str, format: FileFormat) -> int:
        if (type, str(format)) not in self.destinations:
            if type == "local":
                self.destinations[(type, str(format))] = int(
                    self.client._post("/destination", LocalDestination(
                        id=DestinationId(123),
                        name=DestinationName(f"local_destination_{self.test_id}"),
                        description="",
                        attributes=[],
                        labels=[],
                        version=DestinationVersionId(uuid.uuid4()),
                        path=f"{os.path.dirname(__file__)}/data/{format.adt_type}",
                        fileFormat=format,
                        accessRules=[]
                    ).to_json()).text
                )
            elif type == "gcs":
                self.destinations[(type, str(format))] = int(
                    self.client._post("/destination", GCSDestination(
                        id=DestinationId(123),
                        name=DestinationName(f"gcs_destination_{self.test_id}"),
                        description="",
                        attributes=[],
                        labels=[],
                        version=DestinationVersionId(uuid.uuid4()),
                        bucket="anaml-dev-warehouse",
                        path="vapour",
                        fileFormat=format,
                        accessRules=[]
                    ).to_json()).text
                )
            elif type == "bigquery":
                self.destinations[(type, str(format))] = int(
                    self.client._post("/destination", BigQueryDestination(
                        id=DestinationId(123),
                        name=DestinationName(f"bigquery_destination_{self.test_id}"),
                        description="",
                        attributes=[],
                        labels=[],
                        version=DestinationVersionId(uuid.uuid4()),
                        path="anaml-dev-nonprod:anaml",
                        stagingArea=TemporaryGCSStagingArea("anaml-dev-nonprod-dataproc-staging"),
                        accessRules=[]
                    ).to_json()).text
                )
        return self.destinations[(type, str(format))]

    def _create_feature_store_run(
        self,
        destination: str,
        folder: Optional[str] = None,
        format: Optional[FileFormat] = None,
        table: Optional[str] = None
    ):
        destination_id = self._get_destination(destination, format)
        featurestore_id = int(self.client._post(
            "/feature-store",
            local_featurestore_json(
                test_id=self.test_id,
                cluster_id=self.cluster_id,
                destination_id=destination_id,
                featureset_id=self.featureset_id,
                folder=folder,
                table=table
            ),
        ).text)
        featurestore = self.client.get_feature_store_by_id(featurestore_id)
        commit = self.client.get_current_commit('official')
        run_id = int(self.client._post(
            f"/feature-store/{featurestore.id.value}/run",
            {
                "adt_type": "batch",
                "featureStoreId": featurestore.id.to_json(),
                "featureStoreVersionId": featurestore.version.to_json(),
                "commitId": commit.id.to_json(),
                "runStartDate": "2021-07-01",
                "runEndDate": "2021-07-02",
                "status": {"adt_type": "completed"},
                "error": None,
                "scheduleState": None,
                "statistics": None
            }
        ).text)
        return featurestore_id, run_id

    @unittest.skip("Requires external setup")
    def test_load_pandas_from_local_csv(self):
        run = self.client.get_feature_store_run(feature_store_id=self.store_local_csv, run_id=self.run_local_csv)
        df = self.client.load_features_to_pandas(run)
        self.assertEqual(len(df), 11)
        self.assertEqual(list(df.columns), ["pk", "band", "fname", "lname", "score"])

    @unittest.skip("Not implemented")
    def test_load_pandas_from_s3_parquet(self):
        run = self.client.get_feature_store_run(feature_store_id=self.store_s3_parquet, run_id=self.run_s3_parquet)
        df = self.client.load_features_to_pandas(run)
        self.assertEqual(list(df.columns), ['customer', 'sku', 'basket', 'store', 'time', 'cost'])
        self.assertGreaterEqual(df.count(), 10)

    @unittest.skip("Requires external setup")
    def test_load_pandas_from_gcs_orc(self):
        run = self.client.get_feature_store_run(feature_store_id=self.store_gcs_orc, run_id=self.run_gcs_orc)
        df = self.client.load_features_to_pandas(run)
        self.assertEqual(list(df.columns), ['customer', 'sku', 'basket', 'store', 'time', 'cost'])
        self.assertGreaterEqual(len(df), 1000)

    @unittest.skip("Requires external setup")
    def test_load_pandas_from_bigquery(self):
        run = self.client.get_feature_store_run(feature_store_id=self.store_bigquery, run_id=self.run_bigquery)
        df = self.client.load_features_to_pandas(run)
        self.assertEqual(list(df.columns), BILLING_TABLE_COLUMNS)
        self.assertEqual(len(df), BILLING_TABLE_RECORDS)

    @unittest.skip("Requires external setup")
    def test_load_spark_from_local_csv(self):
        run = self.client.get_feature_store_run(feature_store_id=self.store_local_csv, run_id=self.run_local_csv)
        df = self.client.load_features_to_spark(run, spark_session=self.spark_session)
        self.assertEqual(df.count(), 11)
        self.assertEqual(df.schema.fieldNames(), ["pk", "band", "fname", "lname", "score", "year"])

    @unittest.skip("Configuration required")
    def test_load_spark_from_gcs_orc(self):
        run = self.client.get_feature_store_run(feature_store_id=self.store_gcs_orc, run_id=self.run_gcs_orc)
        df = self.client.load_features_to_spark(run, spark_session=self.spark_session)
        self.assertGreaterEqual(df.count(), 1000)

    @unittest.skip("Requires external setup")
    def test_load_spark_from_bigquery(self):
        run = self.client.get_feature_store_run(feature_store_id=self.store_bigquery, run_id=self.run_bigquery)
        df = self.client.load_features_to_spark(run, spark_session=self.spark_session)
        # Ignore the synthetic partition information columns.
        df_columns = list(filter(lambda s: not s.startswith('_'), df.schema.fieldNames()))
        self.assertEqual(df_columns, BILLING_TABLE_COLUMNS)
        self.assertEqual(df.count(), BILLING_TABLE_RECORDS)

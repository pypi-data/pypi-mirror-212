"""Integration tests for handling of FeatureStore Runs."""

import datetime

from anaml_client.models import *
from base import IntegrationTestBase, fixed_uuid
from fixtures import destination_json_fixture, cluster_json_fixture, featurestore_json_fixture, featureset_json_fixture


class TestFeatureStoreRunIntegration(IntegrationTestBase):

    test_id: str
    cluster_id: int
    destination_id: int
    featureset_id: int
    featurestore_id: int
    commit: Commit

    def setUp(self) -> None:
        """Apply fixtures."""
        self.test_id = fixed_uuid()
        self.cluster_id = int(self.client._post("/cluster", cluster_json_fixture(self.test_id)).text)
        self.destination_id = int(self.client._post("/destination", destination_json_fixture(self.test_id)).text)
        self.featureset_id = int(
            self.client._post("/feature-set", featureset_json_fixture(self.test_id, self.entity_id)).text
        )
        self.featurestore_id = int(self.client._post(
            "/feature-store",
            featurestore_json_fixture(
                test_id=self.test_id,
                cluster_id=self.cluster_id,
                destination_id=self.destination_id,
                featureset_id=self.featureset_id,
            ),
        ).text)
        self.commit = self.client.get_current_commit('official')

    def test_get_feature_store_runs(self):
        featurestore = self.client.get_feature_store_by_id(self.featurestore_id)

        r = self.client.get_feature_store_runs(self.featurestore_id)
        self.assertEqual(0, len(r))

        dt = datetime.date(year=2021, month=7, day=1)
        for i in range(0, 7):
            one = datetime.timedelta(days=1)
            d = datetime.timedelta(days=i)
            self.client._post(
                f"/feature-store/{featurestore.id.value}/run",
                {
                    "adt_type": "batch",
                    "featureStoreId": featurestore.id.to_json(),
                    "featureStoreVersionId": featurestore.version.to_json(),
                    "commitId": self.commit.id.to_json(),
                    "runStartDate": str(dt + d),
                    "runEndDate": str(dt + d + one),
                    "status": {"adt_type": "failed"},
                    "error": {"message": "Just testing"},
                    "scheduleState": None,
                    "statistics": None
                }
            )
        runs = self.client.get_feature_store_runs(featurestore.id.value)
        self.assertEqual(7, len(runs))

    def test_get_feature_store_run(self):
        featurestore = self.client.get_feature_store_by_id(self.featurestore_id)
        run_id = int(self.client._post(
            f"/feature-store/{featurestore.id.value}/run",
            {
                "adt_type": "batch",
                "featureStoreId": featurestore.id.to_json(),
                "featureStoreVersionId": featurestore.version.to_json(),
                "commitId": self.commit.id.to_json(),
                "runStartDate": "2021-07-01",
                "runEndDate": "2021-07-02",
                "status": {"adt_type": "failed"},
                "error": {"message": f"Test {self.test_id}"},
                "scheduleState": None,
                "statistics": None
            }
        ).text)

        run = self.client.get_feature_store_run(featurestore.id.value, run_id)
        self.assertIsInstance(run, FeatureStoreRun)
        self.assertEqual(run.error.message, f"Test {self.test_id}")

    def test_get_latest_feature_store_run_by_name(self):
        featurestore = self.client.get_feature_store_by_id(self.featurestore_id)
        run_id = int(self.client._post(
            f"/feature-store/{featurestore.id.to_json()}/run",
            {
                "adt_type": "batch",
                "featureStoreId": featurestore.id.to_json(),
                "featureStoreVersionId": featurestore.version.to_json(),
                "commitId": self.commit.id.to_json(),
                "runStartDate": "2021-07-01",
                "runEndDate": "2021-07-02",
                "status": {"adt_type": "failed"},
                "error": {"message": f"Test {self.test_id}"},
                "scheduleState": None,
                "statistics": None
            }
        ).text)

        run = self.client.get_feature_store_run(featurestore.id.value, run_id)
        self.assertIsInstance(run, FeatureStoreRun)
        self.assertEqual(run.error.message, f"Test {self.test_id}")

        run2 = self.client.get_latest_feature_store_run_by_name(featurestore.name.value)
        self.assertIsInstance(run2, FeatureStoreRun)
        self.assertEqual(run, run2)

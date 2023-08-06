"""Integration tests for handling of FeatureStore."""

from anaml_client.models import *
from base import IntegrationTestBase, fixed_uuid
from fixtures import destination_json_fixture, cluster_json_fixture, featurestore_json_fixture, \
    featureset_json_fixture, kafka_source_json_fixture, kafka_destination_json_fixture, \
    streaming_featurestore_json_fixture, root_table_json_fixture


class TestFeatureStoreIntegration(IntegrationTestBase):
    test_id: str
    cluster_id: int
    destination_id: int
    featureset_id: int
    featurestore_id: int
    kafka_source_id: int
    kafka_table_id: int
    kafka_destination_id: int
    streaming_featurestore_id: int

    def setUp(self) -> None:
        """Apply fixtures."""
        self.test_id = fixed_uuid()
        self.cluster_id = int(self.client._post(
            "/cluster",
            cluster_json_fixture(self.test_id),
        ).text)
        self.destination_id = int(self.client._post(
            "/destination",
            destination_json_fixture(self.test_id),
        ).text)
        self.featureset_id = int(self.client._post(
            "/feature-set",
            featureset_json_fixture(self.test_id, self.entity_id),
        ).text)
        self.featurestore_id = int(self.client._post(
            "/feature-store",
            featurestore_json_fixture(
                test_id=self.test_id,
                cluster_id=self.cluster_id,
                destination_id=self.destination_id,
                featureset_id=self.featureset_id,
            ),
        ).text)
        self.kafka_source_id = int(self.client._post(
            "/source",
            kafka_source_json_fixture(self.test_id),
        ).text)
        self.kafka_table_id = int(self.client._post(
            "/table",
            root_table_json_fixture(self.test_id, self.kafka_source_id)
        ).text)
        self.kafka_destination_id = int(self.client._post(
            "/destination",
            kafka_destination_json_fixture(self.test_id),
        ).text)
        self.streaming_featurestore_id = int(self.client._post(
            "/feature-store",
            streaming_featurestore_json_fixture(
                test_id=self.test_id,
                cluster_id=self.cluster_id,
                destination_id=self.kafka_destination_id,
                featureset_id=self.featureset_id,
                table_id=self.kafka_table_id
            ),
        ).text)

    def test_get_feature_stores(self):
        r = self.client.get_feature_stores()
        self.assertEqual(2, len([fs for fs in r if self.test_id in fs.name.value]))

    def test_get_feature_store(self):
        actual = self.client.get_feature_store_by_id(self.featurestore_id)
        self.assertIsInstance(actual, BatchFeatureStore)

        another = self.client.get_feature_store_by_name(f"feature_store_{self.test_id}")
        self.assertIsInstance(another, BatchFeatureStore)
        self.assertEqual(another, actual)

    def test_get_streaming_feature_store(self):
        actual = self.client.get_feature_store_by_id(self.streaming_featurestore_id)
        self.assertIsInstance(actual, StreamingFeatureStore)

        another = self.client.get_feature_store_by_name(f"streaming_feature_store_{self.test_id}")
        self.assertIsInstance(another, StreamingFeatureStore)
        self.assertEqual(another, actual)

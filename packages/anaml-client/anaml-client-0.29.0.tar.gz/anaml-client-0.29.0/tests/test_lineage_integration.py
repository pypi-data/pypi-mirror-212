"""Integration tests for API methods relating to lineage."""
from base import IntegrationTestBase, fixed_uuid

from fixtures import destination_json_fixture, feature_json_fixture, featureset_json_fixture, \
    featurestore_json_fixture, cluster_json_fixture, eventstore_json_fixture, eventstore_table_json_fixture


class TestSourceIntegration(IntegrationTestBase):

    def setUp(self) -> None:
        self.test_id = fixed_uuid()

        self.cluster_id = int(self.client._post("/cluster", cluster_json_fixture(self.test_id)).text)

        self.eventstore_id = int(self.client._post(
            "/event-store",
            eventstore_json_fixture(self.test_id, self.cluster_id)
        ).text)
        self.eventstore_table_id = int(self.client._post(
            "/table",
            eventstore_table_json_fixture(self.test_id, self.eventstore_id, self.entity_id)
        ).text)
        self.eventstore_feature_id = int(self.client._post(
            "/feature",
            feature_json_fixture("eventstore_" + self.test_id, self.eventstore_table_id)
        ).text)
        self.feature_id = int(self.client._post(
            "/feature",
            feature_json_fixture(self.test_id, self.table_id)
        ).text)
        self.featureset_id = int(self.client._post(
            "/feature-set",
            featureset_json_fixture(self.test_id, self.entity_id, self.feature_id, self.eventstore_feature_id)
        ).text)
        self.destination_id = int(self.client._post(
            "/destination",
            destination_json_fixture(self.test_id)
        ).text)
        self.featurestore_id = int(self.client._post(
            "/feature-store",
            featurestore_json_fixture(self.test_id, self.cluster_id, self.destination_id, self.featureset_id)
        ).text)

    def test_get_lineage_for_eventstore(self):
        lineage = self.client.get_lineage_for_event_store(self.eventstore_id)

        self.assertEqual(1, len(lineage.eventStores))
        self.assertEqual(0, len(lineage.sources))
        self.assertTrue(any(eventstore.id.value == self.eventstore_id for eventstore in lineage.eventStores))
        self.assertTrue(any(table.id.value == self.eventstore_table_id for table in lineage.tables))
        self.assertTrue(any(feature.id.value == self.eventstore_feature_id for feature in lineage.features))
        self.assertTrue(any(featureset.id.value == self.featureset_id for featureset in lineage.featureSets))
        self.assertTrue(any(featurestore.id.value == self.featurestore_id for featurestore in lineage.featureStores))
        self.assertTrue(any(destination.id.value == self.destination_id for destination in lineage.destinations))

    def test_get_lineage_for_source(self):
        lineage = self.client.get_lineage_for_source(self.source_id)

        self.assertEqual(0, len(lineage.eventStores))
        self.assertEqual(1, len(lineage.sources))
        self.assertTrue(any(source.id.value == self.source_id for source in lineage.sources))
        self.assertTrue(any(table.id.value == self.table_id for table in lineage.tables))
        self.assertTrue(any(feature.id.value == self.feature_id for feature in lineage.features))
        self.assertTrue(any(featureset.id.value == self.featureset_id for featureset in lineage.featureSets))
        self.assertTrue(any(featurestore.id.value == self.featurestore_id for featurestore in lineage.featureStores))
        self.assertTrue(any(destination.id.value == self.destination_id for destination in lineage.destinations))

    def test_get_lineage_for_table(self):
        lineage = self.client.get_lineage_for_table(self.table_id)

        self.assertEqual(1, len(lineage.tables))
        self.assertTrue(any(source.id.value == self.source_id for source in lineage.sources))
        self.assertTrue(any(table.id.value == self.table_id for table in lineage.tables))
        self.assertTrue(any(feature.id.value == self.feature_id for feature in lineage.features))
        self.assertTrue(any(featureset.id.value == self.featureset_id for featureset in lineage.featureSets))
        self.assertTrue(any(featurestore.id.value == self.featurestore_id for featurestore in lineage.featureStores))
        self.assertTrue(any(destination.id.value == self.destination_id for destination in lineage.destinations))

    def test_get_lineage_for_feature(self):
        lineage = self.client.get_lineage_for_feature(self.feature_id)

        self.assertEqual(1, len(lineage.features))
        self.assertTrue(any(source.id.value == self.source_id for source in lineage.sources))
        self.assertTrue(any(table.id.value == self.table_id for table in lineage.tables))
        self.assertTrue(any(feature.id.value == self.feature_id for feature in lineage.features))
        self.assertTrue(any(featureset.id.value == self.featureset_id for featureset in lineage.featureSets))
        self.assertTrue(any(featurestore.id.value == self.featurestore_id for featurestore in lineage.featureStores))
        self.assertTrue(any(destination.id.value == self.destination_id for destination in lineage.destinations))

    def test_get_lineage_for_featureset(self):
        lineage = self.client.get_lineage_for_feature_set(self.featureset_id)

        self.assertEqual(1, len(lineage.featureSets))
        self.assertTrue(any(source.id.value == self.source_id for source in lineage.sources))
        self.assertTrue(any(table.id.value == self.table_id for table in lineage.tables))
        self.assertTrue(any(feature.id.value == self.feature_id for feature in lineage.features))
        self.assertTrue(any(featureset.id.value == self.featureset_id for featureset in lineage.featureSets))
        self.assertTrue(any(featurestore.id.value == self.featurestore_id for featurestore in lineage.featureStores))
        self.assertTrue(any(destination.id.value == self.destination_id for destination in lineage.destinations))

    def test_get_lineage_for_featurestore(self):
        lineage = self.client.get_lineage_for_feature_store(self.featurestore_id)

        self.assertEqual(1, len(lineage.featureStores))
        self.assertTrue(any(source.id.value == self.source_id for source in lineage.sources))
        self.assertTrue(any(table.id.value == self.table_id for table in lineage.tables))
        self.assertTrue(any(feature.id.value == self.feature_id for feature in lineage.features))
        self.assertTrue(any(featureset.id.value == self.featureset_id for featureset in lineage.featureSets))
        self.assertTrue(any(featurestore.id.value == self.featurestore_id for featurestore in lineage.featureStores))
        self.assertTrue(any(destination.id.value == self.destination_id for destination in lineage.destinations))

    def test_get_lineage_for_destination(self):
        lineage = self.client.get_lineage_for_destination(self.destination_id)

        self.assertEqual(1, len(lineage.destinations))
        self.assertEqual(0, len(lineage.sources))
        self.assertEqual(0, len(lineage.tables))
        self.assertEqual(0, len(lineage.features))
        self.assertEqual(0, len(lineage.featureSets))
        self.assertTrue(any(featurestore.id.value == self.featurestore_id for featurestore in lineage.featureStores))
        self.assertTrue(any(destination.id.value == self.destination_id for destination in lineage.destinations))

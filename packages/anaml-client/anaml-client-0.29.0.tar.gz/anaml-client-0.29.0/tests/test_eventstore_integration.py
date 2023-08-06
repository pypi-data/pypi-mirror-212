"""Integration tests for handling of EventStore."""

from base import IntegrationTestBase, fixed_uuid
from fixtures import cluster_json_fixture, eventstore_json_fixture


class TestEventStoreIntegration(IntegrationTestBase):
    test_id: str
    cluster_id: int
    eventstore_id: int

    def setUp(self) -> None:
        """Apply fixtures."""
        self.test_id = fixed_uuid()
        self.cluster_id = int(self.client._post(
            "/cluster",
            cluster_json_fixture(self.test_id),
        ).text)
        self.eventstore_id = int(self.client._post(
            "/event-store",
            eventstore_json_fixture(
                test_id=self.test_id,
                cluster_id=self.cluster_id,
            ),
        ).text)

    def test_get_event_stores(self):
        r = self.client.get_event_stores()
        self.assertEqual(1, len([fs for fs in r if self.test_id in fs.name.value]))

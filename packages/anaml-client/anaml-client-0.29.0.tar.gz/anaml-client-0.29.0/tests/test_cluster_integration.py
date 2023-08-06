"""Integration tests for cluster information."""

from anaml_client.models import *
from base import IntegrationTestBase, fixed_uuid
from fixtures import cluster_json_fixture


class TestClusterIntegration(IntegrationTestBase):

    test_id: str
    cluster_id: int
    destination_id: int

    def setUp(self) -> None:
        """Apply fixtures."""
        self.test_id = fixed_uuid()
        self.cluster_id = int(self.client._post(
            "/cluster",
            cluster_json_fixture(self.test_id),
        ).text)

    def test_get_clusters(self):
        r = self.client.get_clusters()
        self.assertEqual(1, len([fs for fs in r if self.test_id in fs.name.value]))

    def test_get_cluster_by_id(self):
        r = self.client.get_cluster_by_id(self.cluster_id)
        self.assertIsInstance(r, Cluster)
        self.assertIsInstance(r, LocalCluster)
        self.assertTrue(self.test_id in r.name.value)

    def test_get_cluster_by_name(self):
        r = self.client.get_cluster_by_name(f"cluster_{self.test_id}")
        self.assertIsInstance(r, Cluster)
        self.assertIsInstance(r, LocalCluster)
        self.assertTrue(self.test_id in r.name.value)

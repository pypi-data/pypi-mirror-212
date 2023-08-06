"""Integration tests for API methods relating to source."""

from base import IntegrationTestBase, fixed_uuid

from fixtures import source_json_fixture


class TestSourceIntegration(IntegrationTestBase):

    def setUp(self) -> None:
        self.test_id = fixed_uuid()
        self.source_id = int(self.client._post("/source", source_json_fixture(self.test_id)).text)

    def test_get_source_id(self):
        source = self.client.get_source_by_id(self.source_id)
        self.assertEqual(source.name.value, f"test_source_{self.test_id}")

    def test_get_source_name(self):
        source = self.client.get_source_by_name(f"test_source_{self.test_id}")
        self.assertEqual(source.id.value, self.source_id)

"""Integration tests for the Destination APIs."""

from anaml_client.models import *
from base import IntegrationTestBase, fixed_uuid

from fixtures import destination_json_fixture, kafka_destination_json_fixture


class TestDestinationIntegration(IntegrationTestBase):
    destination_id: int

    def setUp(self) -> None:
        self.test_id = fixed_uuid()
        self.destination_id = int(self.client._post("/destination", destination_json_fixture(self.test_id)).text)

    def test_list_destinations(self):
        destinations = self.client.get_destinations()
        self.assertGreaterEqual(len(destinations), 1)
        self.assertTrue(
            len([d for d in destinations if self.test_id in d.name.value]) == 1,
            msg="Expected exactly one destination."
        )

    def test_get_destination(self):
        destination = self.client.get_destination_by_id(self.destination_id)
        self.assertIsInstance(destination, LocalDestination)

    def test_create_kafka_destination(self):
        id = fixed_uuid()
        kafka_d_id = int(self.client._post("/destination", kafka_destination_json_fixture(id)).text)
        dest = self.client.get_destination_by_id(kafka_d_id)
        self.assertEqual(dest.name.value, f'kafka_destination_{id}')

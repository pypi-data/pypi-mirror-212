#
# Copyright 2021 Simple Machines Pty Ltd - All Rights Reserved.
#
# This file is part of Anaml.
#
# Unauthorized copying and/or distribution of this file, via any medium is
# strictly prohibited.
#

#
# Tests for Anaml Table functionality
#

from random import choice
from requests import get

from anaml_client.models import *

from base import IntegrationTestBase, fixed_uuid

from fixtures import entity_mapping_json_fixture, feature_json_fixture

# The goal of these tests is to confirm that we can
# 1) retrieve all tables from the Anaml server, as a list
# 2) retrieve an arbitrarily select table from that list
# 3) that the elements of (2) retrieved via HTTP GET are correctly
#    specified in the object returned by the client
# 3) create each Table type
# 4) catch Table-specific exceptions


class IntegrationTest(IntegrationTestBase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.source_id = SourceId(cls.source_id)
        cls.table_id = TableId(cls.table_id)

    def setUp(self) -> None:
        self.test_id = fixed_uuid()
        feature_id = int(
            self.client._post("/feature", feature_json_fixture(self.test_id, self.table_id.value)).text
        )
        entity_mapping_id = int(
            self.client._post("/entity-mapping", entity_mapping_json_fixture(
                self.entity_id, self.entity_id, feature_id)).text
        )
        self.entity_mapping_id = EntityMappingId(entity_mapping_id)
        self.entity_id = EntityId(self.entity_id)

    def test_get_all_tables(self):
        allT = IntegrationTest.client.get_tables()
        self.assertTrue(len(allT) > 0, "Is the Anaml server running?")
        gotten = get(IntegrationTest.url + "/table",
                     headers=IntegrationTest.headers)
        self.assertEqual(gotten.status_code, 200)
        self.assertEqual(len(allT), len(gotten.json()))

    def test_get_random_table(self):
        allT = IntegrationTest.client.get_tables()
        randTable = choice(allT)
        self.assertIsInstance(randTable, Table)

        gotten = IntegrationTest.client.get_table_by_id(randTable.id.value)
        self.assertEqual(randTable, gotten)
        self.assertEqual(type(randTable), type(gotten))

        another = IntegrationTest.client.get_table_by_name(randTable.name.value)
        self.assertEqual(randTable, another)
        self.assertEqual(type(randTable), type(another))

    def test_create_root_table_no_eventdescription(self):
        self._test_create_get_table(RootTableCreationRequest(
            name=TableName(f"root_table_{fixed_uuid()}"),
            description="A sample table",
            labels=[],
            attributes=[],
            eventDescription=None,
            source=FolderSourceReference(sourceId=self.source_id, folder="data_usage"),
        ))

    def test_create_root_table_with_eventdescription(self):
        self._test_create_get_table(RootTableCreationRequest(
            name=TableName(f"root_table_{fixed_uuid()}"),
            description="A sample table",
            labels=[],
            attributes=[],
            eventDescription=EventDescription({self.entity_id: "customerNumber"}, TimestampInfo("current_date", None)),
            source=FolderSourceReference(sourceId=self.source_id, folder="data_usage"),
        ))

    def test_create_view_table_no_eventdescription(self): 
        root_table = self.client.get_table_by_id(self.table_id)
        self._test_create_get_table(ViewTableCreationRequest(
            name=TableName(f"view_table_{fixed_uuid()}"),
            description="A sample table",
            labels=[],
            attributes=[],
            eventDescription=None,
            expression=f"select * from {root_table.name} where mbUsed > 1000",
            sources=[self.table_id],
        ))

    def test_create_pivot_table_no_eventdescription(self):
        self._test_create_get_table(PivotTableCreationRequest(
            name=TableName(f"view_table_{fixed_uuid()}"),
            description="A sample table",
            labels=[],
            attributes=[],
            entityMapping=self.entity_mapping_id,
            extraFeatures=[],
        ))

    def _test_create_get_table(self, table: TableCreationRequest):
        table = self.client.create_table(table)
        # TODO: Assert fields are the same.

        actual = self.client.get_table_by_id(table.id.value)
        self.assertEqual(actual, table)

        another = self.client.get_table_by_id(table.id.value)
        self.assertEqual(another, table)

        features = self.client.get_tables()
        self.assertIn(table, features)

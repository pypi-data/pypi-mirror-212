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

import uuid

from jsonschema import ValidationError
from hypothesis import given

from anaml_client.models import *

from base import TestBase
from generators import TableGen

# The goal of these tests is to confirm that we can
# 1) retrieve all tables from the Anaml server, as a list
# 2) retrieve an arbitrarily select table from that list
# 3) that the elements of (2) retrieved via HTTP GET are correctly
#    specified in the object returned by the client
# 3) create each Table type
# 4) catch Table-specific exceptions


# adt_type to object lookup

adtToTable = {"root": RootTable, "view": ViewTable, "pivot": PivotTable}

# generic table elements
genericFields: dict = {
    "id": None,
    "name": None,
    "description": None,
    "version": None,
    "adt_type": None,
    "labels": None,
    "attributes": None
}


class TestTables(TestBase):
    @given(TableGen)
    def test_round_trip(self, table):
        assert table == Table.from_json(table.to_json())

    def test_table_types(self):
        with self.assertRaises(ValidationError):
            Table.from_json({})

        with self.assertRaises(ValidationError):
            Table.from_json({"adt_type": ""})

        with self.assertRaises(ValidationError):
            baredict = {"adt_type": "this is unsupported"}
            Table.from_json(baredict)

        with self.assertRaises(ValidationError):
            Table.from_json({
                "adt_type": "root",
                "id": 123,
                "name": "example",
                "description": None,
                "version": str(uuid.uuid4()),
                "labels": [],
                "attributes": [],
                "source": {
                    "sourceId": 234,
                }
            })

        with self.assertRaises(ValidationError):
            genericFields["id"] = 1
            genericFields["name"] = "this is a name"
            genericFields["version"] = str(uuid.uuid4())
            genericFields["labels"] = []
            genericFields["attributes"] = []
            Table.from_json(genericFields)

        with self.assertRaises(ValidationError):
            genericFields['adt_type'] = 'wot'
            Table.from_json(genericFields)

        rootTableFields = {
            "adt_type": "root",
            "id": 1,
            "name": "this is a name",
            "version": str(uuid.uuid4()),
            "labels": [],
            "attributes": [],
            "source": {"adt_type": "folder", "sourceId": 12, "folder": "/tmp/foo"}
        }
        newRootTable = Table.from_json(rootTableFields)
        self.assertIsInstance(newRootTable, RootTable)

        rootTableFields["eventDescription"] = {
            "timestampInfo": {
                "timestampColumn": "example",
            },
            "entities": {"123": "customer_id"},
        }
        newRootTable = Table.from_json(rootTableFields)
        self.assertIsInstance(newRootTable, RootTable)

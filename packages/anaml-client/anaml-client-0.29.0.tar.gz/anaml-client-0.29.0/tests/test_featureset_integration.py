"""Integration tests for API methods relating to feature sets."""

from datetime import datetime
import unittest
import pandas as pd
from pandas.testing import assert_frame_equal
import pytz

from anaml_client.models import *

from base import IntegrationTestBase, fixed_uuid

from fixtures import feature_json_fixture, featureset_json_fixture


class TestFeatureSetIntegration(IntegrationTestBase):

    test_id: str
    featureset_id: int

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.table_id = TableId(cls.table_id)

    def setUp(self) -> None:
        self.test_id = fixed_uuid()
        feature_id = int(
            self.client._post("/feature", feature_json_fixture(self.test_id, self.table_id.value)).text
        )
        self.featureset_id = int(
            self.client._post("/feature-set", featureset_json_fixture(self.test_id, self.entity_id)).text
        )
        self.featureset_with_feature_id = int(
            self.client._post(
                "/feature-set", featureset_json_fixture(fixed_uuid(), self.entity_id, feature_id)
            ).text
        )
        self.entity_id = EntityId(self.entity_id)
        self.feature_id = FeatureId(feature_id)

    def test_get_featuresets(self):
        feature_sets = self.client.get_feature_sets()
        current = [fs for fs in feature_sets if self.test_id in fs.name.value]
        self.assertEqual(len(current), 1)

    def test_get_featureset(self):
        feature_set = self.client.get_feature_set_by_id(self.featureset_id)
        self.assertIsInstance(feature_set, FeatureSet)
        self.assertTrue(self.test_id in feature_set.name.value)

        another = self.client.get_feature_set_by_name(f"featureset_{self.test_id}")
        self.assertIsInstance(another, FeatureSet)
        self.assertEqual(feature_set, another)

    @unittest.skip("Fix this (docker-compose spark broken)")
    def test_preview_featureset(self):
        feature_set = self.client.get_feature_set_by_id(self.featureset_with_feature_id)
        result = self.client.preview_feature_set(feature_set)

        tz = pytz.timezone('Australia/Sydney')
        curr_date = datetime.utcnow().date().strftime("%Y-%m-%d")
        feature = self.client.get_feature_by_id(self.feature_id)
        expected_result = pd.DataFrame(data={
            'phoneNumber': ['12345678', '12345789', '12345981'],
            'date': [curr_date] * 3,
            feature.name.value: [1, 0, 0]
        })
        result_sorted = result.sort_values("phoneNumber")
        expected_result_sorted = expected_result.sort_values("phoneNumber")
        assert_frame_equal(result_sorted.reset_index(drop=True), expected_result_sorted.reset_index(drop=True))

    def test_create_featureset(self):
        self._test_create_get_featureset(FeatureSetCreationRequest(
            name=FeatureSetName(f"featureset_{fixed_uuid()}"),
            entity=EntityId(self.entity_id),
            description="A Sample Feature Set",
            labels=[],
            attributes=[],
            features=[self.feature_id]
        ))

    def test_create_update_featureset(self):
        feature_set = self.client.create_feature_set(FeatureSetCreationRequest(
            name=FeatureSetName(f"featureset_{fixed_uuid()}"),
            entity=EntityId(self.entity_id),
            description="A Sample Feature Set",
            labels=[],
            attributes=[],
            features=[self.feature_id]
        ))

        updated_description = "Updated description"
        updated_fs = self.client.update_feature_set(FeatureSet(
            id=feature_set.id,
            name=feature_set.name,
            description=updated_description,
            entity=feature_set.entity,
            labels=feature_set.labels,
            attributes=feature_set.attributes,
            features=feature_set.features,
            version=feature_set.version
        ))

        actual = self.client.get_feature_set_by_id(updated_fs.id.value)

        self.assertEqual(actual.description, updated_description)

    def _test_create_get_featureset(self, featureset: FeatureSetCreationRequest):
        feature_set = self.client.create_feature_set(featureset)
        # TODO: Assert fields are the same.

        actual = self.client.get_feature_set_by_id(feature_set.id.value)
        self.assertEqual(actual, feature_set)

        another = self.client.get_feature_set_by_name(feature_set.name.value)
        self.assertEqual(another, feature_set)

        features = self.client.get_feature_sets()
        self.assertIn(feature_set, features)

#
# Copyright 2020 Simple Machines Pty Ltd - All Rights Reserved.
#
# This file is part of Anaml.
#
# Unauthorized copying and/or distribution of this file, via any medium
# is strictly prohibited.
#

import unittest
import uuid
from datetime import datetime

from parameterized import parameterized

from anaml_client.exceptions import AnamlError
from anaml_client.models import *

from base import fixed_uuid, IntegrationTestBase

from fixtures import customer_number_entity_json_fixture, table_multiple_entities_json_fixture, \
    preview_cluster_json_fixture

SIMPLE_AGGREGATE_EXPRESSIONS = [(a.value, a) for a in AggregateExpression if a.value not in ['basketsum', 'basketlast', 'maxby', 'minby']]
BASKET_AGGREGATE_EXPRESSIONS = [(a.value, a) for a in AggregateExpression if a.value in ['basketsum', 'basketlast']]
MAXBY_MINBY_AGGREGATE_EXPRESSIONS = [(a.value, a) for a in AggregateExpression if a.value in ['maxby', 'minby']]

class TestFeatureIntegration(IntegrationTestBase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.source_id = SourceId(cls.source_id)
        cls.entity_id = EntityId(cls.entity_id)
        cls.table_id = TableId(cls.table_id)

        cls.cluster_id = int(cls.client._post(
            "/cluster",
            preview_cluster_json_fixture("test_preview_cluster_" + fixed_uuid())
        ).text)

    def setUp(self) -> None:
        self.test_id = fixed_uuid()
        customer_entity_id = int(self.client._post("/entity", customer_number_entity_json_fixture(self.test_id)).text)
        self.table_multiple_entities_id = TableId(int(self.client._post(
            "/table",
            table_multiple_entities_json_fixture(
                test_id=self.test_id,
                source_id=self.source_id.value,
                entity_id=self.entity_id.value,
                customer_entity_id=customer_entity_id
            )
        ).text))
        self.customer_entity_id = EntityId(customer_entity_id)

    def test_create_get_feature_with_optional(self):
        self._test_create_get_feature(EventFeatureCreationRequest(
            name=FeatureName("feature_%s" % fixed_uuid()),
            description="A sample feature",
            attributes=[],
            labels=[],
            table=self.table_id,
            window=DayWindow(7),
            select=SelectExpression("mbUsed"),
            filter=FilterExpression("mbUsed > 1000"),
            aggregate=AggregateExpression.Count,
            postAggregateExpr=PostAggregateExpression("x -> x > 5"),
            entityRestrictions=None,
            template=None
        ))

    def test_create_update_get_feature(self):
        feature = EventFeatureCreationRequest(
            name=FeatureName("feature_%s" % fixed_uuid()),
            description="A sample feature",
            labels=[],
            attributes=[],
            table=self.table_id,
            window=DayWindow(7),
            select=SelectExpression("mbUsed"),
            filter=FilterExpression("mbUsed > 1000"),
            aggregate=AggregateExpression.Count,
            postAggregateExpr=PostAggregateExpression("x -> x > 5"),
            entityRestrictions=None,
            template=None,
        )
        actual = self.client.create_feature(feature)
        self.assertIsInstance(actual, EventFeature)
        # TODO: Compare the fields.

        features = self.client.get_features()
        tt = [fs for fs in features if fs.id == actual.id]
        self.assertEqual(len(tt), 1)

        self.assertIn(actual, features, msg=f"Did not find {actual.id} in {len(features)} features.")

        # TODO
        # feature.description = "An updated sample feature"
        # self.client.create_feature(feature)
        # actual = self.client.get_feature_by_id(feature.id)
        # self.assertEqual(actual, feature)

        features = self.client.get_features()
        self.assertIn(actual, features)

    def test_create_get_feature_without_post_aggregate(self):
        self._test_create_get_feature(EventFeatureCreationRequest(
            name=FeatureName("feature_%s" % fixed_uuid()),
            description="A sample feature",
            labels=[],
            attributes=[],
            table=self.table_id,
            window=DayWindow(7),
            select=SelectExpression("mbUsed"),
            filter=FilterExpression("mbUsed > 1000"),
            aggregate=AggregateExpression.Count,
            postAggregateExpr=None,
            entityRestrictions=None,
            template=None
        ))

    def test_create_get_feature_without_filter(self):
        self._test_create_get_feature(EventFeatureCreationRequest(
            name=FeatureName("feature_%s" % fixed_uuid()),
            description="A sample feature",
            labels=[],
            attributes=[],
            table=self.table_id,
            window=DayWindow(7),
            select=SelectExpression("mbUsed"),
            filter=None,
            aggregate=AggregateExpression.Sum,
            postAggregateExpr=PostAggregateExpression("x -> x > 10000"),
            entityRestrictions=None,
            template=None
        ))

    def test_create_get_feature_without_optional(self):
        self._test_create_get_feature(EventFeatureCreationRequest(
            name=FeatureName("feature_%s" % fixed_uuid()),
            description="A sample feature",
            labels=[],
            attributes=[],
            table=self.table_id,
            window=DayWindow(7),
            select=SelectExpression("mbUsed"),
            filter=None,
            aggregate=AggregateExpression.Sum,
            postAggregateExpr=None,
            entityRestrictions=None,
            template=None
        ))

    def test_create_get_feature_with_row_window(self):
        self._test_create_get_feature(EventFeatureCreationRequest(
            name=FeatureName("feature_%s" % fixed_uuid()),
            description="A sample feature",
            labels=[],
            attributes=[],
            table=self.table_id,
            window=RowWindow(7),
            select=SelectExpression("mbUsed"),
            filter=FilterExpression("mbUsed > 1000"),
            aggregate=AggregateExpression.Count,
            postAggregateExpr=PostAggregateExpression("x -> x > 5"),
            entityRestrictions=None,
            template=None
        ))

    def test_create_get_feature_with_open_window(self):
        self._test_create_get_feature(EventFeatureCreationRequest(
            name=FeatureName("feature_%s" % fixed_uuid()),
            description="A sample feature",
            labels=[],
            attributes=[],
            table=self.table_id,
            window=OpenWindow(),
            select=SelectExpression("mbUsed"),
            filter=FilterExpression("mbUsed > 1000"),
            aggregate=AggregateExpression.Count,
            postAggregateExpr=PostAggregateExpression("x -> x > 5"),
            entityRestrictions=None,
            template=None
        ))

    @parameterized.expand(SIMPLE_AGGREGATE_EXPRESSIONS)
    def test_create_get_feature_with_simple_aggregate_expressions(self, name, aggregate_expression):
        self._test_create_get_feature(EventFeatureCreationRequest(
            name=FeatureName("feature_%s" % fixed_uuid()),
            description="A sample feature",
            labels=[],
            attributes=[],
            table=self.table_id,
            window=OpenWindow(),
            select=SelectExpression("mbUsed"),
            filter=FilterExpression("mbUsed > 1000"),
            aggregate=aggregate_expression,
            postAggregateExpr=None, #PostAggregateExpression("x -> x > 5"),
            entityRestrictions=None,
            template=None
        ))

    @parameterized.expand(BASKET_AGGREGATE_EXPRESSIONS)
    def test_create_get_feature_with_basket_aggregate_expressions(self, name, aggregate_expression):
        self._test_create_get_feature(EventFeatureCreationRequest(
            name=FeatureName("feature_%s" % fixed_uuid()),
            description="A sample feature",
            labels=[],
            attributes=[],
            table=self.table_id,
            window=OpenWindow(),
            select=SelectExpression("named_struct('key', customerNumber, 'value', mbUsed)"),
            filter=FilterExpression("mbUsed > 1000"),
            aggregate=aggregate_expression,
            postAggregateExpr=PostAggregateExpression("x -> max_basket(x).key"),
            entityRestrictions=None,
            template=None
        ))

    @parameterized.expand(MAXBY_MINBY_AGGREGATE_EXPRESSIONS)
    def test_create_get_feature_with_maxby_minby_aggregate_expressions(self, name, aggregate_expression):
        self._test_create_get_feature(EventFeatureCreationRequest(
            name=FeatureName("feature_%s" % fixed_uuid()),
            description="A sample feature",
            labels=[],
            attributes=[],
            table=self.table_id,
            window=OpenWindow(),
            select=SelectExpression("named_struct('value', customerNumber, 'ordering', mbUsed)"),
            filter=FilterExpression("mbUsed > 1000"),
            aggregate=aggregate_expression,
            postAggregateExpr=None,
            entityRestrictions=None,
            template=None
        ))

    def test_create_get_row_feature(self):
        feature0 = EventFeatureCreationRequest(
            name=FeatureName("feature_%s" % fixed_uuid()),
            description="A sample feature",
            labels=[],
            attributes=[],
            table=self.table_id,
            window=DayWindow(7),
            select=SelectExpression("mbUsed"),
            filter=FilterExpression("mbUsed > 1000"),
            aggregate=AggregateExpression.Count,
            postAggregateExpr=None,
            entityRestrictions=None,
            template=None
        )
        feature1 = EventFeatureCreationRequest(
            name=FeatureName("feature_%s" % fixed_uuid()),
            description="A sample feature",
            labels=[],
            attributes=[],
            table=self.table_id,
            window=DayWindow(7),
            select=SelectExpression("mbUsed"),
            filter=FilterExpression("mbUsed > 1000"),
            aggregate=AggregateExpression.Count,
            postAggregateExpr=None,
            entityRestrictions=None,
            template=None
        )
        feature0 = self.client.create_feature(feature0)
        feature1 = self.client.create_feature(feature1)
        self._test_create_get_feature(RowFeatureCreationRequest(
            name=FeatureName("feature_%s" % fixed_uuid()),
            description="A sample feature",
            labels=[],
            attributes=[],
            over=[feature0.id, feature1.id],
            select=SelectExpression("{f0} + {f1}".format(
                f0=feature0.name, f1=feature1.name)
            ),
            entityId=self.entity_id,
            template=None
        ))

    def test_create_get_row_feature_template(self):
        feature0 = EventFeatureCreationRequest(
            name=FeatureName("feature_%s" % fixed_uuid()),
            description="A sample feature",
            labels=[],
            attributes=[],
            table=self.table_id,
            window=DayWindow(7),
            select=SelectExpression("mbUsed"),
            filter=FilterExpression("mbUsed > 1000"),
            aggregate=AggregateExpression.Count,
            postAggregateExpr=None,
            entityRestrictions=None,
            template=None
        )
        feature1 = EventFeatureCreationRequest(
            name=FeatureName("feature_%s" % fixed_uuid()),
            description="A sample feature",
            labels=[],
            attributes=[],
            table=self.table_id,
            window=DayWindow(7),
            select=SelectExpression("mbUsed"),
            filter=FilterExpression("mbUsed > 1000"),
            aggregate=AggregateExpression.Count,
            postAggregateExpr=None,
            entityRestrictions=None,
            template=None
        )
        feature0 = self.client.create_feature(feature0)
        feature1 = self.client.create_feature(feature1)
        self._test_create_get_feature_template(RowFeatureTemplateCreationRequest(
            name=TemplateName("feature_%s" % fixed_uuid()),
            description="A sample feature",
            labels=[],
            attributes=[],
            over=[feature0.id, feature1.id],
            select=SelectExpression("{f0} + {f1}".format(
                f0=feature0.name, f1=feature1.name
            )),
            entityId=self.entity_id,
        ))

    def test_create_get_feature_template_with_optional(self):
        self._test_create_get_feature_template(EventFeatureTemplateCreationRequest(
            name=TemplateName("feature_%s" % fixed_uuid()),
            description="A sample feature",
            labels=[],
            attributes=[],
            table=self.table_id,
            window=OpenWindow(),
            select=SelectExpression("data_usage"),
            filter=FilterExpression("data_usage > 1000"),
            aggregate=AggregateExpression.Count,
            postAggregateExpr=PostAggregateExpression("x -> count > 10"),
            entityRestrictions=None
        ))

    def test_create_get_feature_template_without_filter(self):
        self._test_create_get_feature_template(EventFeatureTemplateCreationRequest(
            name=TemplateName("feature_%s" % fixed_uuid()),
            description="A sample feature",
            labels=[],
            attributes=[],
            table=self.table_id,
            window=OpenWindow(),
            select=SelectExpression("data_usage"),
            filter=None,
            aggregate=AggregateExpression.Count,
            postAggregateExpr=PostAggregateExpression("x -> count > 10"),
            entityRestrictions=None
        ))

    def test_create_get_feature_template_without_aggregate(self):
        self._test_create_get_feature_template(EventFeatureTemplateCreationRequest(
            name=TemplateName("feature_%s" % fixed_uuid()),
            description="A sample feature",
            labels=[],
            attributes=[],
            table=self.table_id,
            window=OpenWindow(),
            select=SelectExpression("data_usage"),
            filter=FilterExpression("data_usage > 1000"),
            aggregate=None,
            postAggregateExpr=PostAggregateExpression("x -> x > 10"),
            entityRestrictions=None
        ))

    def test_create_get_feature_template_without_post_aggregate(self):
        self._test_create_get_feature_template(EventFeatureTemplateCreationRequest(
            name=TemplateName("feature_%s" % fixed_uuid()),
            description="A sample feature",
            labels=[],
            attributes=[],
            table=self.table_id,
            window=OpenWindow(),
            select=SelectExpression("data_usage"),
            filter=FilterExpression("data_usage > 1000"),
            aggregate=AggregateExpression.Count,
            postAggregateExpr=None,
            entityRestrictions=None
        ))

    def test_create_get_feature_template_without_optional(self):
        self._test_create_get_feature_template(EventFeatureTemplateCreationRequest(
            name=TemplateName("feature_%s" % fixed_uuid()),
            description="A sample feature",
            labels=[],
            attributes=[],
            table=self.table_id,
            window=OpenWindow(),
            select=SelectExpression("data_usage"),
            filter=None,
            aggregate=None,
            postAggregateExpr=None,
            entityRestrictions=None
        ))

    @parameterized.expand(SIMPLE_AGGREGATE_EXPRESSIONS)
    def test_create_get_feature_template_with_simple_aggregate_expressions(self, name, aggregate_expression):
        self._test_create_get_feature_template(EventFeatureTemplateCreationRequest(
            name=TemplateName("feature_%s" % fixed_uuid()),
            description="A sample feature",
            labels=[],
            attributes=[],
            table=self.table_id,
            window=OpenWindow(),
            select=SelectExpression("data_usage"),
            filter=FilterExpression("data_usage > 1000"),
            aggregate=aggregate_expression,
            postAggregateExpr=None,
            entityRestrictions=None
        ))

    @parameterized.expand(BASKET_AGGREGATE_EXPRESSIONS)
    def test_create_get_feature_template_with_basket_aggregate_expressions(self, name, aggregate_expression):
        self._test_create_get_feature_template(EventFeatureTemplateCreationRequest(
            name=TemplateName("feature_%s" % fixed_uuid()),
            description="A sample feature",
            labels=[],
            attributes=[],
            table=self.table_id,
            window=OpenWindow(),
            select=SelectExpression("named_struct('key', customerNumber, 'value', mbUsed)"),
            filter=FilterExpression("mbUsed > 1000"),
            aggregate=aggregate_expression,
            postAggregateExpr=PostAggregateExpression("x -> max_basket(x).key"),
            entityRestrictions=None
        ))


    @parameterized.expand(MAXBY_MINBY_AGGREGATE_EXPRESSIONS)
    def test_create_get_feature_template_with_maxby_minby_aggregate_expressions(self, name, aggregate_expression):
        self._test_create_get_feature_template(EventFeatureTemplateCreationRequest(
            name=TemplateName("feature_%s" % fixed_uuid()),
            description="A sample feature",
            labels=[],
            attributes=[],
            table=self.table_id,
            window=OpenWindow(),
            select=SelectExpression("named_struct('key', customerNumber, 'value', mbUsed)"),
            filter=FilterExpression("mbUsed > 1000"),
            aggregate=aggregate_expression,
            postAggregateExpr=None,
            entityRestrictions=None
        ))

    @unittest.skip("Requires external setup (to create online feature store and populate with values)")
    def test_get_generated_features(self):
        self.client.get_generated_features("core_customer_daily", 1)

    @unittest.skip("Requires external setup (to create online feature store and populate with values)")
    def test_get_online_features_with_id(self):
        self.client.get_online_features_with_id("test_table", 1, 1)

    @unittest.skip("Fix this (docker-compose spark broken)")
    def test_preview_feature(self):
        id = uuid.uuid4()
        feature = EventFeature(
            id=FeatureId(1),
            version=FeatureVersionId(id),
            name=FeatureName("feature_%s" % id),
            description="A sample feature",
            labels=[],
            attributes=[],
            table=self.table_id,
            window=DayWindow(7),
            select=SelectExpression("mbUsed"),
            filter=FilterExpression("mbUsed > 1000"),
            aggregate=AggregateExpression.Count,
            postAggregateExpr=None,
            entityRestrictions=None,
            template=None
        )
        preview_data = self.client.preview_feature(feature)
        # TODO : Assert result is as expected
        entity = self.client.get_entity_by_id(self.entity_id)
        preview_data_entity_name = [p.entityName for p in preview_data]
        self.assertListEqual([entity.name], preview_data_entity_name)

    @unittest.skip("Fix this (docker-compose spark broken)")
    def test_preview_feature_with_multiple_entities(self):
        id = uuid.uuid4()
        feature = EventFeature(
            id=FeatureId(1),
            version=FeatureVersionId(id),
            name=FeatureName("feature_%s" % id),
            description="A sample feature",
            labels=[],
            attributes=[],
            table=self.table_multiple_entities_id,
            window=DayWindow(7),
            select=SelectExpression("mbUsed"),
            filter=FilterExpression("mbUsed > 1000"),
            aggregate=AggregateExpression.Count,
            postAggregateExpr=None,
            entityRestrictions=None,
            template=None
        )
        preview_data = self.client.preview_feature(feature)
        # TODO : Assert result is as expected
        entity = self.client.get_entity_by_id(self.entity_id)
        customer_entity = self.client.get_entity_by_id(self.customer_entity_id)
        preview_data_entity_name = [p.entityName for p in preview_data]
        self.assertListEqual([customer_entity.name, entity.name], preview_data_entity_name)

    @unittest.skip("Fix this (docker-compose spark broken)")
    def test_preview_feature_entity_filter(self):
        id = uuid.uuid4()
        feature = EventFeature(
            id=FeatureId(1),
            version=FeatureVersionId(id),
            name=FeatureName("feature_%s" % id),
            description="A sample feature",
            labels=[],
            attributes=[],
            table=self.table_multiple_entities_id,
            window=DayWindow(7),
            select=SelectExpression("mbUsed"),
            filter=FilterExpression("mbUsed > 1000"),
            aggregate=AggregateExpression.Count,
            postAggregateExpr=None,
            entityRestrictions=None,
            template=None
        )
        preview_data = self.client.preview_feature(feature, entity=self.entity_id.value)
        # TODO : Assert result is as expected
        entity = self.client.get_entity_by_id(self.entity_id)
        preview_data_entity_name = [p.entityName for p in preview_data]
        self.assertListEqual([entity.name], preview_data_entity_name)

    @unittest.skip("Fix this (docker-compose spark broken)")
    def test_preview_feature_incorrect_entity_filter(self):
        id = uuid.uuid4()
        feature = EventFeature(
            id=FeatureId(1),
            version=FeatureVersionId(id),
            name=FeatureName("feature_%s" % id),
            description="A sample feature",
            labels=[],
            attributes=[],
            table=self.table_id,
            window=DayWindow(7),
            select=SelectExpression("mbUsed"),
            filter=FilterExpression("mbUsed > 1000"),
            aggregate=AggregateExpression.Count,
            postAggregateExpr=None,
            entityRestrictions=None,
            template=None
        )
        with self.assertRaises(AnamlError) as context:
            self.client.preview_feature(feature, entity=self.customer_entity_id.value)
        entity = self.client.get_entity_by_id(self.customer_entity_id)
        self.assertTrue(
            f"Preview could not be generated for Entity: {entity.name}." in
            [m.message for m in context.exception.errors]
        )

    @unittest.skip("Fix this (docker-compose spark broken)")
    def test_preview_feature_date_filter(self):
        id = uuid.uuid4()
        feature = EventFeature(
            id=FeatureId(1),
            version=FeatureVersionId(id),
            name=FeatureName("feature_%s" % id),
            description="A sample feature",
            labels=[],
            attributes=[],
            table=self.table_id,
            window=OpenWindow(),
            select=SelectExpression("mbUsed"),
            filter=FilterExpression("mbUsed > 1000"),
            aggregate=AggregateExpression.Sum,
            postAggregateExpr=None,
            entityRestrictions=None,
            template=None
        )
        preview_data = self.client.preview_feature(feature, snapshot_date=datetime(2021, 9, 10))
        entity = self.client.get_entity_by_id(self.entity_id)
        preview_data_entity_name = [p.entityName for p in preview_data]
        self.assertListEqual([entity.name], preview_data_entity_name)
        self.assertIsInstance(preview_data[0].statistics[0], EmptySummaryStatistics)

    @unittest.skip("Fix this (docker-compose spark broken)")
    def test_preview_feature_date_entity_filter(self):
        id = uuid.uuid4()
        feature = EventFeature(
            id=FeatureId(1),
            version=FeatureVersionId(id),
            name=FeatureName("feature_%s" % id),
            description="A sample feature",
            labels=[],
            attributes=[],
            table=self.table_id,
            window=OpenWindow(),
            select=SelectExpression("mbUsed"),
            filter=FilterExpression("mbUsed > 1000"),
            aggregate=AggregateExpression.Sum,
            postAggregateExpr=None,
            entityRestrictions=None,
            template=None
        )
        preview_data = self.client.preview_feature(
            feature,
            entity=self.entity_id.value,
            snapshot_date="2021-10-09"
        )
        entity = self.client.get_entity_by_id(self.entity_id)
        preview_data_entity_name = [p.entityName for p in preview_data]
        self.assertListEqual([entity.name], preview_data_entity_name)

    @unittest.skip("Requires external setup (to create test data for source table)")
    def test_sample_feature(self):
        id = str(uuid.uuid4()).replace('-', '_')
        feature = EventFeature(
            name=FeatureName("feature_%s" % id),
            description="A sample feature",
            labels=[],
            attributes=[],
            table=self.table_id,
            window=DayWindow(7),
            select=SelectExpression("mbUsed"),
            filter=FilterExpression("mbUsed > 1000"),
            aggregate=AggregateExpression.Count,
            postAggregateExpr=None,
            entityRestrictions=None,
            template=None
        )
        self.client.sample_feature(feature)

    def test_create_get_feature_with_entity_restrictions(self):
        self._test_create_get_feature(EventFeatureCreationRequest(
            name=FeatureName("feature_%s" % fixed_uuid()),
            description="A sample feature",
            labels=[],
            attributes=[],
            table=self.table_id,
            window=DayWindow(7),
            select=SelectExpression("mbUsed"),
            filter=FilterExpression("mbUsed > 1000"),
            aggregate=AggregateExpression.Count,
            postAggregateExpr=None,
            entityRestrictions=[self.entity_id],
            template=None
        ))

    def _test_create_get_feature(self, feature: FeatureCreationRequest):
        feature = self.client.create_feature(feature)
        # TODO: Assert fields are the same.
        
        actual = self.client.get_feature_by_id(feature.id.value)
        self.assertEqual(actual, feature)

        another = self.client.get_feature_by_name(feature.name.value)
        self.assertEqual(another, feature)

        features = self.client.get_features()
        self.assertIn(feature, features)

    def _test_update_get_feature(self, feature):
        feature = self.client.create_feature(feature)
        actual = self.client.get_feature_by_id(feature.id.value)
        self.assertEqual(actual, feature)

        another = self.client.get_feature_by_name(feature.name.value)
        self.assertEqual(another, feature)

        features = self.client.get_features()
        self.assertIn(feature, features)

    def _test_create_get_feature_template(self, feature_template: FeatureTemplateCreationRequest):
        feature_template = self.client.create_feature_template(feature_template)

        actual = self.client.get_feature_template_by_id(feature_template.id.value)
        self.assertEqual(actual, feature_template)

        another = self.client.get_feature_template_by_name(feature_template.name.value)
        self.assertEqual(another, feature_template)

        feature_templates = self.client.get_feature_templates()
        self.assertIn(feature_template, feature_templates)

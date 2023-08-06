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

from anaml_client.models import *

class TestValidator(unittest.TestCase):
    def test_validator(self):
        self.__round_trip_feature(EventFeature(
            id=FeatureId(1),
            name=FeatureName("sum_gb_used"),
            description="Total data usage in GB",
            version=FeatureVersionId(uuid.uuid4()),
            labels=[],
            attributes=[],
            table=TableId(1),
            window=OpenWindow(),
            select=SelectExpression("mbUsed / 1000"),
            filter=None,
            aggregate=AggregateExpression.Sum,
            postAggregateExpr=None,
            entityRestrictions=None,
            template=None,
        ))
        self.__round_trip_feature(EventFeature(
            id=FeatureId(2),
            name=FeatureName("gb_used_sum_7_days"),
            version=FeatureVersionId(uuid.uuid4()),
            description="Total data usage in GB over 7 days",
            labels=[],
            attributes=[],
            table=TableId(1),
            window=DayWindow(7),
            select=SelectExpression("mbUsed / 1000"),
            filter=None,
            aggregate=AggregateExpression.Sum,
            postAggregateExpr=None,
            entityRestrictions=None,
            template=None
        ))

    def __round_trip_feature(self, feature):
        actual = Feature.from_json(feature.to_json())
        self.assertEqual(actual, feature)

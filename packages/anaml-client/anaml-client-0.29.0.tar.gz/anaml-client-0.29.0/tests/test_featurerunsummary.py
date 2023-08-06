#
#  Copyright 2021 Simple Machines Pty Ltd - All Rights Reserved.
#
#  This file is part of Anaml.
#
#  Unauthorized copying and/or distribution of this file, via any medium is strictly prohibited.
#
from hypothesis import given

from anaml_client.models import *

from generators import FeatureRunSummaryGen


@given(FeatureRunSummaryGen)
def test_feature_run_summary_round_trip(summary: FeatureRunSummary):
    assert summary == FeatureRunSummary.from_json(summary.to_json())

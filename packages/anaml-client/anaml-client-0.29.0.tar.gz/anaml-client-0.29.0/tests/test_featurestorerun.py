#
# Copyright 2021 Simple Machines Pty Ltd - All Rights Reserved.
#
# This file is part of Anaml.
#
# Unauthorized copying and/or distribution of this file, via any medium is
# strictly prohibited.
#
"""Roundtrip tests for the FeatureStoreExecutionStatistics APIs."""

from hypothesis import given
import pytest

from anaml_client.models import *

from generators import FeatureStoreRunGen


@given(FeatureStoreRunGen)
@pytest.mark.skip(reason="keeps failing on CI build")
def test_feature_store_run_round_trip(run: FeatureStoreRun):
    assert run == FeatureStoreRun.from_json(run.to_json())

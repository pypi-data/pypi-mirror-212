#
# Copyright 2021 Simple Machines Pty Ltd - All Rights Reserved.
#
# This file is part of Anaml.
#
# Unauthorized copying and/or distribution of this file, via any medium is
# strictly prohibited.
#
"""Roundtrip tests for the SummaryStatistics APIs."""

from hypothesis import given

from anaml_client.models import *

from generators import JobMetricsGen, SummaryStatisticsGen, ExecutionStatisticsGen


@given(SummaryStatisticsGen)
def test_summary_statistics_round_trip(stats: SummaryStatistics):
    assert stats == SummaryStatistics.from_json(stats.to_json())


@given(JobMetricsGen)
def test_task_statistics_round_trip(stats: JobMetrics):
    assert stats == JobMetrics.from_json(stats.to_json())


@given(ExecutionStatisticsGen)
def test_execution_statistics_round_trip(stats: ExecutionStatistics):
    assert stats == ExecutionStatistics.from_json(stats.to_json())

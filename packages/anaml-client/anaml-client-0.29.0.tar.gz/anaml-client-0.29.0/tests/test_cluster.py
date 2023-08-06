"""Integration tests for the Destination APIs."""

from hypothesis import given, settings

from anaml_client.models import *

from base import TestBase
from generators import ClusterGen


class TestCluster(TestBase):
    @settings(deadline=1000)
    @given(ClusterGen)
    def test_round_trip(self, cluster: Cluster):
        assert cluster == Cluster.from_json(cluster.to_json())

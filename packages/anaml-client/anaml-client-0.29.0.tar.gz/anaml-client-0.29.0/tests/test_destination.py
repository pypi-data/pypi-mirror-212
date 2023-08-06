"""Integration tests for the Destination APIs."""

from hypothesis import given, settings

from anaml_client import Destination

from generators import DestinationGen


@given(DestinationGen)
@settings(deadline=None)
def test_destination_round_trip(destination: Destination):
    assert destination == Destination.from_json(destination.to_json())

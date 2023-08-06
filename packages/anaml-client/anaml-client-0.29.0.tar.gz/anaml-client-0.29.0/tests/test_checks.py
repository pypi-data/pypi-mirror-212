"""Tests for the Checks APIs."""
from hypothesis import given  # , settings, HealthCheck, Verbosity

from anaml_client import Check, CheckCreationRequest

from base import TestBase
from generators import CheckGen, CheckCreationRequestGen


class TestCheck(TestBase):
    # @settings(
    #     suppress_health_check=(HealthCheck.too_slow,),
    #     max_examples=100,
    #     verbosity=Verbosity.verbose
    # )
    @given(CheckGen)
    def test_round_trip_check(self, check: Check):
        assert check == Check.from_json(check.to_json())

    @given(CheckCreationRequestGen)
    def test_round_trip_creation_request(self, req: CheckCreationRequest):
        assert req == CheckCreationRequest.from_json(req.to_json())

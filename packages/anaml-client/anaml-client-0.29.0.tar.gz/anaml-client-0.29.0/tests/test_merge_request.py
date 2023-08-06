"""Tests for the Merge Request APIs."""

from hypothesis import given

from anaml_client.models import *

from generators import MergeRequestGen, MergeRequestCreationRequestGen, MergeRequestCommentGen, \
    MergeRequestCommentCreationRequestGen


@given(MergeRequestGen)
def test_merge_request_round_trip(req: MergeRequest):
    assert req == MergeRequest.from_json(req.to_json())


@given(MergeRequestCreationRequestGen)
def test_merge_request_creation_request_round_trip(req: MergeRequestCreationRequest):
    assert req == MergeRequestCreationRequest.from_json(req.to_json())


@given(MergeRequestCommentGen)
def test_merge_request_comment_round_trip(req: MergeRequestComment):
    assert req == MergeRequestComment.from_json(req.to_json())


@given(MergeRequestCommentCreationRequestGen)
def test_merge_request_comment_creation_request_round_trip(req: MergeRequestCommentCreationRequest):
    assert req == MergeRequestCommentCreationRequest.from_json(req.to_json())

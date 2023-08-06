from hypothesis import given

from anaml_client import Commit

from generators import CommitGen


@given(CommitGen)
def test_round_trip_commit(commit: Commit):
    assert commit == Commit.from_json(commit.to_json())

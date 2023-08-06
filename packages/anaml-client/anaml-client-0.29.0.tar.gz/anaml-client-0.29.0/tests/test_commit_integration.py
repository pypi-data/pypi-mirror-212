from anaml_client import Commit

from base import IntegrationTestBase


class TestCommitIntegration(IntegrationTestBase):
    def test_get_commit_for_branch(self):
        commit = self.client.get_current_commit("official")
        self.assertIsInstance(commit, Commit)

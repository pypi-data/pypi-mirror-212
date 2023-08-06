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
from datetime import datetime

from parameterized import parameterized

from anaml_client.exceptions import AnamlError
from anaml_client.models import *

from base import fixed_uuid, IntegrationTestBase


class TestUserGroupIntegration(IntegrationTestBase):

    def test_create_update_get_user_group(self):
        user = UserCreationRequest(UserEmail("%s@anaml.io" % fixed_uuid()), "password", "Test User %s" % fixed_uuid(), "Test", "User", roles=[Role.Author])
        actual = self.client.create_user(user)
        self.assertIsInstance(actual, User)
        # TODO: Compare the fields.

        users = self.client.get_users()
        tt = [u for u in users if u.id == actual.id]
        self.assertEqual(len(tt), 1)

        self.assertIn(actual, users, msg=f"Did not find {actual.id} in {len(users)} users.")

        # TODO
        # feature.description = "An updated sample feature"
        # self.client.create_feature(feature)
        # actual = self.client.get_feature_by_id(feature.id)
        # self.assertEqual(actual, feature)

        user_group = UserGroupCreationRequest(UserGroupName("test group %s" % fixed_uuid()), "test group desc", roles=[], members=[UserGroupMember(tt[0].id, UserGroupMemberSource.Anaml)], externalGroupId=None)
        actual = self.client.create_user_group(user_group)
        self.assertIsInstance(actual, UserGroup)
        # TODO: Compare the fields.

        user_groups = self.client.get_user_groups()
        tt = [ug for ug in user_groups if ug.id == actual.id]
        self.assertEqual(len(tt), 1)

        self.assertIn(actual, user_groups, msg=f"Did not find {actual.id} in {len(user_groups)} user_groups.")

#
#  Copyright 2021 Simple Machines Pty Ltd - All Rights Reserved.
#
#  This file is part of Anaml.
#
#  Unauthorized copying and/or distribution of this file, via any medium is strictly prohibited.
#
import pytest as pytest
import requests as requests

from base import IntegrationTestBase
from anaml_client.models import *


class TestFeatureStoreRunIntegration(IntegrationTestBase):

    def testGetFeatureSummaryForMissingFeature(self):
        with pytest.raises(requests.exceptions.HTTPError) as ex:
            self.client.get_feature_by_id(99999)
        self.assertEqual(ex.value.response.status_code, 404)
        with pytest.raises(requests.exceptions.HTTPError) as ex:
            self.client.get_feature_run_summary(99999)
        self.assertEqual(ex.value.response.status_code, 404)

    def testGetFeatureSummaryForFeatureWithNoRuns(self):
        fs = self.client.get_features()
        ft = fs[0]
        self.assertIsInstance(ft, Feature)
        with pytest.raises(requests.exceptions.HTTPError) as ex:
            self.client.get_feature_run_summary(1)
        self.assertEqual(ex.value.response.status_code, 404)

    def testGetFeatureSummary(self):
        # TODO: How should we arrange for summary to be available.
        self.skipTest("Requires external setup (to create runs with summaries to read)")

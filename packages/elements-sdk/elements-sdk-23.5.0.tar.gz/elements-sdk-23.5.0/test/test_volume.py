"""
    ELEMENTS API

    No description provided (generated by Openapi Generator https://github.com/openapitools/openapi-generator)  # noqa: E501

    The version of the OpenAPI document: 2
    Generated by: https://openapi-generator.tech
"""


import sys
import unittest

import elements_sdk
from elements_sdk.model.backend import Backend
from elements_sdk.model.fs_properties import FSProperties
from elements_sdk.model.volume_status import VolumeStatus
globals()['Backend'] = Backend
globals()['FSProperties'] = FSProperties
globals()['VolumeStatus'] = VolumeStatus
from elements_sdk.model.volume import Volume


class TestVolume(unittest.TestCase):
    """Volume unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testVolume(self):
        """Test Volume"""
        # FIXME: construct object with mandatory attributes with example values
        # model = Volume()  # noqa: E501
        pass


if __name__ == '__main__':
    unittest.main()

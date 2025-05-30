# -*- coding: utf-8 -*-

import os
import unittest

from tests import utils
from vsg import vhdlFile
from vsg.rules import generic_map

sTestDir = os.path.dirname(__file__)

lFile, eError = vhdlFile.utils.read_vhdlfile(os.path.join(sTestDir, "rule_601_test_input.vhd"))


class test_generic_map_rule(unittest.TestCase):
    def setUp(self):
        self.oFile = vhdlFile.vhdlFile(lFile)
        self.assertIsNone(eError)

    def test_rule_601(self):
        oRule = generic_map.rule_601()
        self.assertTrue(oRule)
        self.assertEqual(oRule.name, "generic_map")
        self.assertEqual(oRule.identifier, "601")

        lExpected = [46, 53, 54, 55, 65, 74, 83]

        oRule.analyze(self.oFile)
        self.assertEqual(lExpected, utils.extract_violation_lines_from_violation_object(oRule.violations))

    def test_rule_600_g_uppercase(self):
        oRule = generic_map.rule_601()
        oRule.suffixes = ["_G"]
        self.assertTrue(oRule)
        self.assertEqual(oRule.name, "generic_map")
        self.assertEqual(oRule.identifier, "601")

        lExpected = [46, 53, 54, 55, 65, 74, 83]

        oRule.analyze(self.oFile)
        self.assertEqual(lExpected, utils.extract_violation_lines_from_violation_object(oRule.violations))

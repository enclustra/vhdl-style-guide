# -*- coding: utf-8 -*-

import os
import unittest

from tests import utils
from vsg import vhdlFile
from vsg.rules import generic_map

sTestDir = os.path.dirname(__file__)

lFile, eError = vhdlFile.utils.read_vhdlfile(os.path.join(sTestDir, "rule_002_test_input.vhd"))

lExpected_lower = []
lExpected_lower.append("")
utils.read_file(os.path.join(sTestDir, "rule_002_test_input.fixed_lower.vhd"), lExpected_lower)

lExpected_upper = []
lExpected_upper.append("")
utils.read_file(os.path.join(sTestDir, "rule_002_test_input.fixed_upper.vhd"), lExpected_upper)


class test_generic_map_rule(unittest.TestCase):
    def setUp(self):
        self.oFile = vhdlFile.vhdlFile(lFile)
        self.assertIsNone(eError)

    def test_rule_002_lower(self):
        oRule = generic_map.rule_002()
        self.assertTrue(oRule)
        self.assertEqual(oRule.name, "generic_map")
        self.assertEqual(oRule.identifier, "002")

        lExpected = [53, 54, 55, 62, 63, 64, 71, 72, 73, 87, 88, 89]

        oRule.analyze(self.oFile)
        self.assertEqual(utils.extract_violation_lines_from_violation_object(oRule.violations), lExpected)

    def test_rule_002_upper(self):
        oRule = generic_map.rule_002()
        oRule.case = "upper"
        self.assertTrue(oRule)
        self.assertEqual(oRule.name, "generic_map")
        self.assertEqual(oRule.identifier, "002")

        lExpected = [4, 5, 6, 13, 14, 15, 22, 23, 24, 38, 39, 40]
        oRule.analyze(self.oFile)
        self.assertEqual(utils.extract_violation_lines_from_violation_object(oRule.violations), lExpected)

    def test_fix_rule_002_lower(self):
        oRule = generic_map.rule_002()

        oRule.fix(self.oFile)

        lActual = self.oFile.get_lines()

        self.assertEqual(lExpected_lower, lActual)

        oRule.analyze(self.oFile)
        self.assertEqual(oRule.violations, [])

    def test_fix_rule_002_upper(self):
        oRule = generic_map.rule_002()
        oRule.case = "upper"

        oRule.fix(self.oFile)

        lActual = self.oFile.get_lines()

        self.assertEqual(lExpected_upper, lActual)

        oRule.analyze(self.oFile)
        self.assertEqual(oRule.violations, [])

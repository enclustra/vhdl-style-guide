# -*- coding: utf-8 -*-

import os
import unittest

from tests import utils
from vsg import vhdlFile
from vsg.rules import delay_mechanism

sTestDir = os.path.dirname(__file__)

lFile, eError = vhdlFile.utils.read_vhdlfile(os.path.join(sTestDir, "rule_502_test_input.vhd"))

lExpected_lower = []
lExpected_lower.append("")
utils.read_file(os.path.join(sTestDir, "rule_502_test_input.fixed_lower.vhd"), lExpected_lower)

lExpected_upper = []
lExpected_upper.append("")
utils.read_file(os.path.join(sTestDir, "rule_502_test_input.fixed_upper.vhd"), lExpected_upper)


class test_delay_mechanism_rule(unittest.TestCase):
    def setUp(self):
        self.oFile = vhdlFile.vhdlFile(lFile)
        self.assertIsNone(eError)

    def test_rule_502_lower(self):
        oRule = delay_mechanism.rule_502()
        self.assertTrue(oRule)
        self.assertEqual(oRule.name, "delay_mechanism")
        self.assertEqual(oRule.identifier, "502")

        lExpected = [8]

        oRule.analyze(self.oFile)
        self.assertEqual(utils.extract_violation_lines_from_violation_object(oRule.violations), lExpected)

    def test_rule_502_upper(self):
        oRule = delay_mechanism.rule_502()
        oRule.case = "upper"
        self.assertTrue(oRule)
        self.assertEqual(oRule.name, "delay_mechanism")
        self.assertEqual(oRule.identifier, "502")

        lExpected = [6]
        oRule.analyze(self.oFile)
        self.assertEqual(utils.extract_violation_lines_from_violation_object(oRule.violations), lExpected)

    def test_fix_rule_502_lower(self):
        oRule = delay_mechanism.rule_502()

        oRule.fix(self.oFile)

        lActual = self.oFile.get_lines()

        self.assertEqual(lExpected_lower, lActual)

        oRule.analyze(self.oFile)
        self.assertEqual(oRule.violations, [])

    def test_fix_rule_502_upper(self):
        oRule = delay_mechanism.rule_502()
        oRule.case = "upper"

        oRule.fix(self.oFile)

        lActual = self.oFile.get_lines()

        self.assertEqual(lExpected_upper, lActual)

        oRule.analyze(self.oFile)
        self.assertEqual(oRule.violations, [])

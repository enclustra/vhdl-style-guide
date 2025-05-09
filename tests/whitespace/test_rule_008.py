# -*- coding: utf-8 -*-

import os
import unittest

from tests import utils
from vsg import vhdlFile
from vsg.rules import whitespace

sTestDir = os.path.dirname(__file__)

lFile, eError = vhdlFile.utils.read_vhdlfile(os.path.join(sTestDir, "rule_008_test_input.vhd"))
lExpected = []
lExpected.append("")
utils.read_file(os.path.join(sTestDir, "rule_008_test_input.fixed.vhd"), lExpected)


class test_whitespace_rule(unittest.TestCase):
    def setUp(self):
        self.oFile = vhdlFile.vhdlFile(lFile)
        self.assertIsNone(eError)

    def test_rule_008(self):
        oRule = whitespace.rule_008()
        self.assertTrue(oRule)
        self.assertEqual(oRule.name, "whitespace")
        self.assertEqual(oRule.identifier, "008")
        self.assertEqual(oRule.groups, ["whitespace"])

        lExpected = [21, 28]

        oRule.analyze(self.oFile)
        self.assertEqual(lExpected, utils.extract_violation_lines_from_violation_object(oRule.violations))

    def test_fix_rule_008(self):
        oRule = whitespace.rule_008()

        oRule.fix(self.oFile)

        lActual = self.oFile.get_lines()

        self.assertEqual(lExpected, lActual)

        oRule.analyze(self.oFile)
        self.assertEqual(oRule.violations, [])

# -*- coding: utf-8 -*-

import os
import unittest

from tests import utils
from vsg import vhdlFile
from vsg.rules import subprogram_instantiation

sTestDir = os.path.dirname(__file__)

lFile, eError = vhdlFile.utils.read_vhdlfile(os.path.join(sTestDir, "rule_001_test_input.vhd"))

dIndentMap = utils.read_indent_file()

lExpected = []
lExpected.append("")
utils.read_file(os.path.join(sTestDir, "rule_001_test_input.fixed.vhd"), lExpected)


class test_rule(unittest.TestCase):
    def setUp(self):
        self.oFile = vhdlFile.vhdlFile(lFile)
        self.assertIsNone(eError)
        self.oFile.set_indent_map(dIndentMap)

    def test_rule_001(self):
        oRule = subprogram_instantiation.rule_001()
        self.assertTrue(oRule)
        self.assertEqual(oRule.name, "subprogram_instantiation")
        self.assertEqual(oRule.identifier, "001")

        lExpected = [20]

        oRule.analyze(self.oFile)
        self.assertEqual(lExpected, utils.extract_violation_lines_from_violation_object(oRule.violations))

    def test_fix_rule_001(self):
        oRule = subprogram_instantiation.rule_001()

        oRule.fix(self.oFile)

        lActual = self.oFile.get_lines()

        self.assertEqual(lExpected, lActual)

        oRule.analyze(self.oFile)
        self.assertEqual(oRule.violations, [])

# -*- coding: utf-8 -*-

from vsg import token
from vsg.rules import token_case

lTokens = []
lTokens.append(token.interface_incomplete_type_declaration.type_keyword)


class rule_500(token_case):
    """
    This rule checks the **type** keyword has proper case.

    |configuring_uppercase_and_lowercase_rules_link|

    **Violation**

    .. code-block:: vhdl

       generic (
         TYPE generic_data_type

    **Fix**

    .. code-block:: vhdl

       generic (
         type generic_data_type
    """

    def __init__(self):
        super().__init__(lTokens)
        self.groups.append("case::keyword")

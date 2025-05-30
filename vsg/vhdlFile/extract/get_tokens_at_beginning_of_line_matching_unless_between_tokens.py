# -*- coding: utf-8 -*-

from vsg import parser
from vsg.vhdlFile.extract import tokens, utils


def get_tokens_at_beginning_of_line_matching_unless_between_tokens(lTokens, lUnless, lAllTokens, oTokenMap):
    lIndexes = utils.get_indexes_of_token_list(lTokens, oTokenMap)
    lIndexes = utils.filter_indexes_in_unless_regions(lIndexes, lUnless, oTokenMap)

    lReturn = []
    for iIndex in lIndexes:
        if oTokenMap.is_token_at_index(parser.carriage_return, iIndex - 1):
            iLine = oTokenMap.get_line_number_of_index(iIndex)
            lReturn.append(tokens.New(iIndex, iLine, [lAllTokens[iIndex]]))
        elif oTokenMap.is_token_at_index(parser.carriage_return, iIndex - 2) and utils.is_token_at_index_whitespace(oTokenMap, iIndex - 1):
            iLine = oTokenMap.get_line_number_of_index(iIndex)
            lReturn.append(tokens.New(iIndex - 1, iLine, lAllTokens[iIndex - 1 : iIndex + 1]))

    return lReturn

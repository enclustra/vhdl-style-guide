# -*- coding: utf-8 -*-

import bisect
import pprint

from vsg import parser, token


class New:
    def __init__(self, dMap):
        self.dMap = dMap
        self.maxTokenNum = None

    def get_token_indexes(self, oToken, bCopy=False):
        sBase, sSub = extract_unique_id(oToken)
        try:
            if bCopy:
                return self.dMap[sBase][sSub].copy()
            else:
                return self.dMap[sBase][sSub]
        except KeyError:
            return []

    def get_token_indexes_between_indexes(self, oToken, iStart, iEnd):
        lReturn = []
        lIndexes = self.get_token_indexes(oToken)
        for iIndex in lIndexes:
            if iIndex > iStart and iIndex < iEnd:
                lReturn.append(iIndex)
        return lReturn

    def get_line_number_of_index(self, iIndex):
        iLine = bisect.bisect_left(self.dMap["parser"]["carriage_return"], iIndex) + 1
        return iLine

    def get_index_of_carriage_return_after_index(self, iIndex):
        iTemp = bisect.bisect_right(self.dMap["parser"]["carriage_return"], iIndex)
        return self.dMap["parser"]["carriage_return"][iTemp]

    def get_index_of_carriage_return_before_index(self, iIndex):
        if iIndex == 0:
            return None
        iTemp = bisect.bisect_left(self.dMap["parser"]["carriage_return"], iIndex) - 1
        if iIndex < self.dMap["parser"]["carriage_return"][iTemp]:
            return iIndex
        return self.dMap["parser"]["carriage_return"][iTemp]

    def get_index_of_token_after_index(self, oToken, iIndex):
        sBase, sSub = extract_unique_id(oToken)
        try:
            iTemp = bisect.bisect_right(self.dMap[sBase][sSub], iIndex)
            return self.dMap[sBase][sSub][iTemp]
        except IndexError:
            return None
        except KeyError:
            return None

    def get_token_pair_indexes(self, oStart, oEnd):
        lStartIndexes = self.get_token_indexes(oStart)
        lEndIndexes = self.get_token_indexes(oEnd)
        return extract_start_end_indexes(lStartIndexes, lEndIndexes)

    def get_index_of_next_non_whitespace_token(self, iIndex, bExcludeComments=False):
        iStartIndex = iIndex + 1
        lTokens = [None, None, None, None]
        lBaseKeys = list(self.dMap.keys())
        for sBaseKey in lBaseKeys:
            lSubKeys = list(self.dMap[sBaseKey].keys())
            if sBaseKey == "parser":
                if "whitespace" in lSubKeys:
                    lSubKeys.remove("whitespace")
                if "carriage_return" in lSubKeys:
                    lSubKeys.remove("carriage_return")
                if "blank_line" in lSubKeys:
                    lSubKeys.remove("blank_line")
                if bExcludeComments and "comment" in lSubKeys:
                    lSubKeys.remove("comment")
            for sSubKey in lSubKeys:
                for iIdx in range(0, 4):
                    iSearchIdx = iStartIndex + iIdx
                    if iSearchIdx in self.dMap[sBaseKey][sSubKey]:
                        lTokens[iIdx] = iSearchIdx
                        continue

        for iToken in lTokens:
            if iToken is not None:
                return iToken

    def get_index_of_previous_non_whitespace_token_before_index(self, iIndex):
        iStartIndex = iIndex - 1
        for i in range(iStartIndex, 0, -1):
            if not self.is_token_at_index_whitespace(i):
                return i

    def get_index_of_next_non_whitespace_token_after_index_ignoring_comments(self, iIndex):
        iStartIndex = iIndex + 1
        for i in range(iStartIndex, self.iMaxToken):
            if not self.is_token_at_index_whitespace_or_comment(i):
                return i

    def get_index_of_previous_non_whitespace_token(self, iIndex):
        iStartIndex = iIndex - 1
        for i in range(iStartIndex, 0, -1):
            if not self.is_token_at_index_whitespace_or_comment(i):
                return i

    def is_token_at_index(self, oToken, iIndex):
        try:
            sBase, sSub = extract_unique_id(oToken)
            if iIndex in self.dMap[sBase][sSub]:
                return True
            return False
        except KeyError:
            return False

    def is_token_at_index_whitespace(self, iIndex):
        if self.is_token_at_index(parser.whitespace, iIndex):
            return True
        if self.is_token_at_index(parser.carriage_return, iIndex):
            return True
        if self.is_token_at_index(parser.blank_line, iIndex):
            return True
        return False

    def is_token_at_index_whitespace_or_comment(self, iIndex):
        if self.is_token_at_index(parser.whitespace, iIndex):
            return True
        if self.is_token_at_index(token.pragma.pragma, iIndex):
            return True
        if self.is_token_at_index(parser.comment, iIndex):
            return True
        if self.is_token_at_index(parser.carriage_return, iIndex):
            return True
        if self.is_token_at_index(parser.blank_line, iIndex):
            return True
        return False

    def is_previous_non_whitespace_token(self, iIndex, oToken):
        index = self.get_index_of_previous_non_whitespace_token_before_index(iIndex)
        return self.is_token_at_index(oToken, index)

    def pretty_print(self):
        pp = pprint.PrettyPrinter(indent=4)
        pp.pprint(self.dMap)

    def get_index_of_line(self, iLine):
        return self.dMap["parser"]["carriage_return"][iLine - 2] + 1


def extract_unique_id(oToken):
    lDoc = oToken.__doc__.split()
    for iDoc, sDoc in enumerate(lDoc):
        if sDoc == "unique_id":
            return lDoc[iDoc + 2], lDoc[iDoc + 4]
    return None, None


def process_tokens(lTokens):
    dMap = build_default_map()
    for iToken, oToken in enumerate(lTokens):
        sBase, sSub = oToken.get_unique_id()
        if sBase is not None:
            try:
                dMap[sBase][sSub].append(iToken)
            except KeyError:
                try:
                    dMap[sBase][sSub] = []
                    dMap[sBase][sSub].append(iToken)
                except KeyError:
                    dMap[sBase] = {}
                    dMap[sBase][sSub] = []
                    dMap[sBase][sSub].append(iToken)
        if sBase == "logical_operator":
            try:
                dMap[sBase][sBase].append(iToken)
            except KeyError:
                try:
                    dMap[sBase][sBase] = []
                    dMap[sBase][sBase].append(iToken)
                except KeyError:
                    dMap[sBase] = {}
                    dMap[sBase][sBase] = []
                    dMap[sBase][sBase].append(iToken)
            continue
        if sSub == "comma":
            try:
                if iToken not in dMap["parser"]["comma"]:
                    dMap["parser"]["comma"].append(iToken)
            except KeyError:
                try:
                    dMap["parser"]["comma"] = []
                    dMap["parser"]["comma"].append(iToken)
                except KeyError:
                    dMap["parser"] = {}
                    dMap["parser"]["comma"] = []
                    dMap["parser"]["comma"].append(iToken)
            continue
        if sSub == "open_parenthesis":
            try:
                if iToken not in dMap["parser"]["open_parenthesis"]:
                    dMap["parser"]["open_parenthesis"].append(iToken)
            except KeyError:
                try:
                    dMap["parser"]["open_parenthesis"] = []
                    dMap["parser"]["open_parenthesis"].append(iToken)
                except KeyError:
                    dMap["parser"] = {}
                    dMap["parser"]["open_parenthesis"] = []
                    dMap["parser"]["open_parenthesis"].append(iToken)
            continue

    oNew = New(dMap)
    oNew.iMaxToken = len(lTokens)
    return oNew


def build_default_map():
    dMap = {}
    return dMap


def extract_start_end_indexes(lStartIndexes, lEndIndexes):
    mylStartIndexes = lStartIndexes.copy()
    mylEndIndexes = lEndIndexes.copy()
    lPairs = extract_pairs(mylStartIndexes, mylEndIndexes)
    return extract_indexes_from_pairs(lPairs)


def extract_pairs(lStartIndexes, lEndIndexes):
    lMyPairs = []
    while len(lEndIndexes) > 0 and len(lStartIndexes) > 0:
        iMin = lEndIndexes[-1] + 1
        lPair = []
        for iStart in lStartIndexes:
            lPair = extract_closest_pair(iStart, lEndIndexes, lPair, iMin)

        if pair_is_empty(lPair):
            break

        lMyPairs.append(lPair)

        lStartIndexes.remove(lPair[0])
        lEndIndexes.remove(lPair[1])

    return lMyPairs


def extract_closest_pair(iStart, lEndIndexes, lPair, iMin):
    for iEnd in lEndIndexes:
        if iStart > iEnd:
            continue
        if iEnd - iStart < iMin:
            lPair = [iStart, iEnd]
            iMin = iEnd - iStart
    return lPair


def extract_indexes_from_pairs(lPairs):
    lStartIndexes = []
    lPairs = remove_any_empty_pairs(lPairs)
    for pair in lPairs:
        lStartIndexes.append(pair[0])

    lStartIndexes.sort()

    lReturnStartIndexes = []
    lReturnEndIndexes = []
    for iStartIndex in lStartIndexes:
        lReturnStartIndexes.append(iStartIndex)
        for pair in lPairs:
            if pair[0] == iStartIndex:
                lReturnEndIndexes.append(pair[1])

    return lReturnStartIndexes, lReturnEndIndexes


def pair_is_empty(lPair):
    if len(lPair) == 0:
        return True
    return False


def remove_any_empty_pairs(lPairs):
    return [x for x in lPairs if x != []]

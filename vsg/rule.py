# -*- coding: utf-8 -*-


from vsg import severity, utils


class Rule:
    def __init__(self):
        self.name = get_rule_name(self)
        self.identifier = get_rule_identifier(self)
        self.unique_id = str(self.name) + "_" + str(self.identifier)
        self.solution = None
        self.violations = []
        self.had_violations = False
        self.indent_style = "spaces"
        self.indent_size = 2
        self.phase = None
        self.subphase = 1
        self.disable = False
        self.fixable = True
        self.severity = severity.error("Error")
        self.user_error_message = ""
        self.debug = False
        self.dFix = {}
        self.dFix["violations"] = {}
        self.configuration = ["indent_style", "indent_size", "phase", "disable", "fixable", "severity", "user_error_message"]
        self.deprecated = False
        self.proposed = False
        self.groups = []
        self.options = []
        self.configuration_documentation_link = None
        self.prerequisites = []
        self.remap = True

    def configure(self, oConfig):
        """Configures attributes on rules using a dictionary of the following form:

          dConfiguration['rule'] = {}
          dConfiguration['rule']['xyz_001'] = {}
          dConfiguration['rule']['xyz_001']['disable'] = True
          dConfiguration['rule']['xyz_001']['solution'] = 'This is the new solution'
          dConfiguration['rule']['xyz_002'] = {}
          dConfiguration['rule']['xyz_002']['disable'] = False
          dConfiguration['rule']['global'] = {}
          dConfiguration['rule']['global']['indent_size'] = 4

        The rule:global dictionary will apply to all rules.
        Individual rule attributes can be modified with [self.name_self.identifier].
        """
        if self.deprecated and self.unique_id in oConfig.dConfig["rule"]:
            return self.print_output()

        dConfiguration = oConfig.dConfig
        configure_global_rule_attributes(self, oConfig)
        configure_group_rule_attributes(self, oConfig)
        configure_rule_attributes(self, oConfig)
        return []

    def has_violations(self):
        if len(self.violations) == 0:
            return False
        return True

    def _build_violation_dict_from_violation_object(self, violation):
        dViolation = {}
        dViolation["severity"] = {}
        dViolation["severity"]["name"] = self.severity.name
        dViolation["severity"]["type"] = self.severity.type
        dViolation["rule"] = self.get_unique_id()
        dViolation["lineNumber"] = str(violation.get_line_number())
        dViolation["solution"] = violation.get_solution()
        return dViolation

    def get_unique_id(self):
        return self.name + "_" + self.identifier

    def get_violations_at_linenumber(self, iLineNumber):
        """
        Returns a list of formatted violations.

        Parameters:

          iLineNumber (integer)

        Returns: (list of dictionaries)
        """
        lReturn = []

        for violation in self.violations:
            if violation.get_line_number() == iLineNumber:
                lReturn.append(self._build_violation_dict_from_violation_object(violation))

        return lReturn

    def get_violations(self):
        lReturn = []

        for violation in self.violations:
            lReturn.append(self._build_violation_dict_from_violation_object(violation))

        return lReturn

    def fix(self, oFile, dFixOnly=None):
        """
        Applies fixes for any rule violations.
        """
        if self.fixable:
            self.analyze(oFile)
            self._print_debug_message("Fixing rule: " + self.unique_id)
            self._filter_out_fix_only_violations(dFixOnly)
            for oViolation in self.violations[::-1]:
                self._fix_violation(oViolation)
                self.had_violations = True
            oFile.update(self.violations, self.remap)
            self.clear_violations()

    def _filter_out_fix_only_violations(self, dFixOnly):
        if dFixOnly is None:
            return

        try:
            if "all" in dFixOnly["fix"]["rule"][self.unique_id]:
                return
        except KeyError:
            self.violations = []

        lTemp = []
        for oViolation in self.violations:
            if oViolation.get_line_number() in dFixOnly["fix"]["rule"][self.unique_id]:
                lTemp.append(oViolation)
        self.violations = lTemp

    def add_violation(self, violation):
        """
        Adds a linenumber to a violations list.
        """
        if not violation.has_code_tag(self.unique_id):
            if self.user_error_message != "":
                violation.sSolution = violation.sSolution + " [user_error_message: " + self.user_error_message + "]"
            self.violations.append(violation)

    def analyze(self, oFile):
        """
        Performs the analysis.
        """
        self._print_debug_message("Analyzing rule: " + self.unique_id)
        lToi = self._get_tokens_of_interest(oFile)
        self._analyze(lToi)

    def get_configuration(self):
        """
        Returns a dictionary of every configurable attribute of the rule.
        """
        dConfig = {}
        for sParameter in self.configuration:
            dConfig[sParameter] = getattr(self, sParameter)
        dConfig["severity"] = self.severity.name
        return dConfig

    def _get_solution(self, iLineNumber):
        """
        Returns the solution for a violation.
        """
        return utils.get_violation_solution_at_line_number(self.violations, iLineNumber)

    def clear_violations(self):
        self.violations = []

    def set_debug(self):
        """
        This method sets the debug attribute to True.
        """
        self.debug = True

    def _print_debug_message(self, sString):
        """
        Prints a debug message to stdio.

        Parameters:

          sString : (string)

        Returns: Nothing
        """
        if self.debug:
            print("INFO: " + sString)

    def _fix_violation(self, oViolation):
        """
        Default if rule is not fixable
        """
        return

    def _sort_violations(self):
        """
        Sorts self.violations based on the start index of each violation.
        Sort order is increasing start index.
        """
        if not self.violations:
            return
        lNewViolations = []
        lNewViolations.append(self.violations[0])
        for oViolation in self.violations[1:]:
            iStartIndex = oViolation.get_start_index()
            for iInsertIndex, oNewViolation in enumerate(lNewViolations):
                iNewIndex = oNewViolation.get_start_index()
                if iStartIndex < iNewIndex:
                    lNewViolations.insert(iInsertIndex, oViolation)
                    break
            else:
                lNewViolations.append(oViolation)
        self.violations = lNewViolations

    def add_option(self, oOption):
        self.options.append(oOption)
        self.configuration.append(oOption.name)
        setattr(self, oOption.name, oOption.value)


def configure_group_rule_attributes(self, oConfig):
    """
    Updates rule attributes based on configuration input files
    """
    try:
        for sGroupName in oConfig.dConfig["rule"]["group"]:
            if sGroupName in self.groups:
                configure_attribute(self, oConfig, sGroupName)
    except KeyError:
        pass


def configure_attribute(self, oConfig, sGroupName):
    try:
        for sAttributeName in oConfig.dConfig["rule"]["group"][sGroupName]:
            if sAttributeName == "severity":
                self.severity = oConfig.severity_list.get_severity_named(oConfig.dConfig["rule"]["group"][sGroupName]["severity"])
            elif sAttributeName in self.__dict__:
                self.__dict__[sAttributeName] = oConfig.dConfig["rule"]["group"][sGroupName][sAttributeName]
    except KeyError:
        pass


def configure_global_rule_attributes(self, oConfig):
    """
    Updates rule attributes based on configuration input files
    """
    try:
        for sAttributeName in oConfig.dConfig["rule"]["global"]:
            if sAttributeName == "severity":
                self.severity = oConfig.severity_list.get_severity_named(oConfig.dConfig["rule"]["global"]["severity"])
            elif sAttributeName in self.configuration:
                self.__dict__[sAttributeName] = oConfig.dConfig["rule"]["global"][sAttributeName]
    except KeyError:
        pass


def configure_rule_attributes(self, oConfig):
    """
    Updates rule attributes based on configuration input files
    """
    try:
        for sAttributeName in oConfig.dConfig["rule"][self.get_unique_id()]:
            if sAttributeName == "severity":
                self.severity = oConfig.severity_list.get_severity_named(oConfig.dConfig["rule"][self.get_unique_id()]["severity"])
            elif sAttributeName in self.__dict__:
                self.__dict__[sAttributeName] = oConfig.dConfig["rule"][self.get_unique_id()][sAttributeName]
            for oOption in self.options:
                if sAttributeName == oOption.name:
                    oOption.value = oConfig.dConfig["rule"][self.get_unique_id()][sAttributeName]
    except KeyError:
        pass


def get_rule_identifier(self):
    """
    Extracts the rule's identifier from the name of the class.
    """
    sReturn = None
    if self.__class__.__name__.startswith("rule_"):
        sReturn = self.__class__.__name__[-3:]
    return sReturn


def get_rule_name(self):
    """
    Extracts the rule's name from the name of the module.
    """
    sReturn = None
    if self.__module__.startswith("vsg.rules."):
        rule_group_name = self.__module__.split(".")[2]
        # Cater for exceptions where the name of the rule doesn't match the name of the module.
        if rule_group_name == "assert_statement":
            sReturn = "assert"
        elif rule_group_name == "file_statement":
            sReturn = "file"
        elif rule_group_name == "if_statement":
            sReturn = "if"
        elif rule_group_name == "ranges":
            sReturn = "range"
        elif rule_group_name == "type_definition":
            sReturn = "type"
        elif rule_group_name == "with_statement":
            sReturn = "with"
        else:
            sReturn = rule_group_name
    return sReturn

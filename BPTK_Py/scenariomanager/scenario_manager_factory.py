#                                                       /`-
# _                                  _   _             /####`-
# | |                                | | (_)           /########`-
# | |_ _ __ __ _ _ __  ___  ___ _ __ | |_ _ ___       /###########`-
# | __| '__/ _` | '_ \/ __|/ _ \ '_ \| __| / __|   ____ -###########/
# | |_| | | (_| | | | \__ \  __/ | | | |_| \__ \  |    | `-#######/
# \__|_|  \__,_|_| |_|___/\___|_| |_|\__|_|___/  |____|    `- # /
#
# Copyright (c) 2018 transentis labs GmbH
# MIT License


import glob
import json
import os

import BPTK_Py.config.config as config
from ..modelmonitor import JsonMonitor
from ..logger import log
from ..modelmonitor import ModelMonitor
from ..scenariomanager import ScenarioManagerABM

from .scenario import SimulationScenario
from .scenario_manager_sd import ScenarioManagerSD



####################################
### Class ScenarioManagerFactory ###
####################################


class ScenarioManagerFactory():
    """
    This class manages all scenario of all scenario managers and exposes methods to look them up, read from filesystem and flush them
    """

    def __init__(self):
        """
        Initialize object and reserve namespaces for scenario managers, monitors, scenarios and JSON file path (scenario storage)
        """

        self.scenario_managers = {}

        self.scenarios = {}
        self.model_monitors = {}
        self.json_monitors = {}
        self.path = ""
        self.scenario_files = []

    def __readScenario(self, filename=""):
        """
        Reads the specified JSON file and generates the scenario_manager and scenario objects
        Pretty large method that does the following:
         - read scenarios from file
         - update the scenario managers in case a new scenario is detected.
         - If you actually updated a scenario, first you need to pop it from a scenario manager's scenarios dict
        :param filename: filename of JSON file to parse
        :return:  self.scenario_managers
        """

        if filename.lower().endswith(".json") and not filename in self.json_monitors.keys():
            self.json_monitors[filename] = JsonMonitor(json_file=filename,
                                                       update_func=self.__refresh_scenarios_for_json)

        if len(filename) > 0 and filename.lower().endswith(".json"):

            json_data = open(filename, encoding="utf-8").read()
            try:
                json_dict = dict(json.loads(json_data))
            except ValueError as e:
                log("[ERROR] Problem reading {}. Error message: {}".format(filename, str(e)))
                return None

            # ScenarioManager ->
            for scenario_manager_name in json_dict.keys():

                # HANDLE ABM SCENARIOS
                if "type" in json_dict[scenario_manager_name].keys() and json_dict[scenario_manager_name][
                    "type"].lower() == "abm":

                    self.scenario_managers[scenario_manager_name] = ScenarioManagerABM(json_dict[scenario_manager_name],
                                                                                       scenario_manager_name,
                                                                                       filenames=[filename])
                    self.scenario_managers[scenario_manager_name].instantiate_model()

                # HANDLE SD SCENARIOS _ COMPLEX STUFF WITH ALL THE BASE CONSTANTS / BASE POINTS AND POSSIBLE DISTRIBUTION OVER FILES
                else:
                    if scenario_manager_name not in self.scenario_managers.keys():
                        self.scenario_managers[scenario_manager_name] = ScenarioManagerSD(base_points=None,
                                                                                          base_constants=None,
                                                                                          scenarios={},
                                                                                          name=scenario_manager_name)

                    manager = self.scenario_managers[scenario_manager_name]

                    if filename not in manager.filenames:
                        manager.filenames += [filename]

                    # Lookup base constants across all json files with the scenarios/ directory
                    manager.base_constants = self.__get_all_base_constants(scenario_manager_name, self.scenario_files)
                    manager.base_points = self.__get_all_base_points(scenario_manager_name, self.scenario_files)


                    # ScenarioManager -> "scenarios" ->
                    scen_dict = json_dict[scenario_manager_name]["scenarios"]
                    model_file = json_dict[scenario_manager_name]["model"]
                    source= None

                    try:
                        source=json_dict[scenario_manager_name]["source"]
                    except:
                        pass



                    # Create simulation scenarios from structure
                    manager.load_scenarios(scen_dict=scen_dict,model_file=model_file,source=source)


                    # Start monitor for source file
                    if "source" in json_dict[scenario_manager_name].keys():

                        if not source in self.model_monitors.keys() and os.path.isfile(source):
                            self.__add_monitor(manager.source, manager.model_file)
                        elif not os.path.isfile(manager.source):
                            log(
                                "[ERROR] ABMModel monitor: Source model file not found: \"{}\". Not attempting to monitor changes to it.".format(
                                    str(manager.source)))


                    manager.instantiate_model()

            return self.scenario_managers
        else:
            print("[ERROR] Attempted to load a scenario manager without giving a filename. Skipping!")

    def get_scenario_managers(self, path=config.configuration["scenario_storage"], scenario_managers_to_filter=[],
                              type=""):
        """
        If self.scenario_managers is empty, this method attempts to load all scenario managers from disk in the specified path
        :param path: path to look for JSON files containing scenario managers and scenarios
        :param scenario_managers_to_filter: only look for certain scenario managers
        :return: self.scenario_managers
        """

        self.path = path
        # a) Only load scenarios if we do not already have them
        if len(self.scenario_managers.keys()) == 0:
            log("[INFO] New scenario manager or reset. Reading in all scenarios from storage!")
            self.scenario_files = glob.glob(os.path.join(path, '*.json'))

            for infile in glob.glob(os.path.join(path, '*.json')):
                self.__readScenario(filename=infile)

            log("[INFO] Successfully loaded all scenarios!")

        scenario_managers = self.scenario_managers

        if type != "":
            scenario_managers = {k: v for k, v in scenario_managers.copy().items() if v.type == type}

        if len(scenario_managers_to_filter) > 0:
            scenario_managers = {k: v for k, v in scenario_managers.copy().items() if k in scenario_managers_to_filter}

        return scenario_managers

    def reset_scenario(self, scenario_manager, scenario):
        """
        Reloads exactly one scenario. For lookup, requires scenario manager's name and the scenario's name
        :param scenario_manager: name of scenario manager
        :param scenario: name of scenario
        :return: None
        """
        log("[INFO] Reloading scenario {} from {}".format(scenario, scenario_manager))

        manager = self.get_scenario_managers()[scenario_manager]
        manager_filenames = manager.filenames
        manager.scenarios.pop(scenario)

        for filename in manager_filenames:
            self.__readScenario(filename=filename)

        log("[INFO] Successfully reloaded scenario {} for ABMModel Manager {}".format(scenario, scenario_manager))

    def reset_all_scenarios(self):
        """
        Flushes all scenario managers and attempts to reload them
        :return: self.scenario_managers
        """
        self.scenario_managers = {}
        return self.get_scenario_managers()

    def get_scenario(self, scenario_manager, scenario):
        """
        Returns exactly one scenario object specified by the scenario_manager and scenario
        :param scenario_manager: Name of the scenario_manager to lookup
        :param scenario: Name of the scenario to lookup
        :return:
        """
        return self.scenario_managers[scenario_manager].scenarios[scenario]

    def get_scenarios(self, scenario_managers=[], scenarios=[], type=""):
        """
        Get an arbitrary amount of scenario objects, depending on the parameters
        :param scenario_managers:  Names of the scenario_managers to lookup
        :param scenarios: Names of the scenarios to lookup
        :param type: Type of simulation models to return
        :return:
        """

        managers = self.get_scenario_managers(scenario_managers_to_filter=scenario_managers, type=type)

        scenarios_objects = {}
        if len(managers) > 1:

            for manager_name, manager in managers.items():
                for scenario_name, scenario in manager.scenarios.items():

                    scenarios_objects[manager_name + "_" + scenario_name] = scenario
                    if scenario_name in scenarios:
                        scenarios += [manager_name + "_" + scenario_name]

        else:
            for manager_name, manager in managers.items():
                for scenario_name, scenario in manager.scenarios.items():

                    scenarios_objects[scenario_name] = scenario
                    if scenario_name in scenarios:
                        scenarios += [scenario_name]

        if len(scenarios) > 0:
            filtered_scenarios = {}
            for key in scenarios:
                if key in scenarios_objects.keys():
                    filtered_scenarios[key] = scenarios_objects[key]
            scenarios_objects = filtered_scenarios

        return scenarios_objects

    def add_scenario(self, scenario, scenario_manager, source="", model=None):
        """
        Add a scenario object during runtime
        :param scenario: scenario object to add
        :param scenario_manager: scenario_manager's name to add scenario to
        :param source: source file of the itmx file (optional)
        :param model: model name of the python file containing the python code for the model
        :return: None
        """
        if scenario_manager not in self.get_scenario_managers().keys():
            self.scenario_managers[scenario_manager] = ScenarioManagerSD(scenarios={scenario.name: scenario},
                                                                         name=scenario_manager,
                                                                         model_file=model)
            self.scenario_managers[scenario_manager].instantiate_model()


        else:
            log("[WARN] Model Manager already existing. Not overwriting the model!")
            self.scenario_managers[scenario_manager].add_scenarios(scenario)

        if len(source) > 0:
            self.__add_monitor(source, model)

    def __add_monitor(self, source, model):
        """
        Add a file monitor for a source model
        :param source:  itmx file link (String)
        :param model:  output file link (without .py)
        :return:  None
        """
        if not source in self.model_monitors.keys():
            self.model_monitors[source] = ModelMonitor(source, str(
                model), update_func=self.refresh_scenarios_for_source_model)

    def destroy(self):
        """
        Kill all file monitor threads
        :return:
        """
        values = self.model_monitors.keys()
        for scenario in values:
            scenario.kill()

        self.model_monitors = {}

    def create_scenario(self, filename="/Users/dominikschroeck/Code/sd_py_simulator/BPTK_Py/scenarios/scenario.json",
                        dictionary={}):
        """
        Method for writing scenarios to JSON file
        :param filename: filename to write to
        :param dictionary: dictionary to parse to JSON
        :return:
        """
        with open(filename, 'w', encoding="utf-8") as outfile:
            json.dump(dictionary, outfile, indent=4)

    def refresh_scenarios_for_source_model(self, filename):
        """
        Refreshes all scenarios that use the given source file (e.g. itmx)
        :param filename:
        :return:
        """
        # Obtain all scenarios
        managers = self.get_scenario_managers()

        for manager_name, manager in managers.items():
            if manager.source == filename:
                for scenario_name in manager.scenarios.keys():
                    self.reset_scenario(scenario=scenario_name, scenario_manager=manager_name)

        log("[INFO] Reset scenarios for all scenarios that require {}".format(filename))

    def __refresh_scenarios_for_json(self, filename):
        """
        Refresh all scenario managers that use this filename as source (JSON!)
        Also update for scenarios that are spread over multiple files
        :param filename: JSON file name
        :return: None
        """
        managers = self.get_scenario_managers()

        managers = list(managers.values())

        for manager in managers:
            if filename in manager.filenames:
                for json_file in manager.filenames:
                    self.__readScenario(json_file)

    def __get_all_base_constants(self, scenario_manager, filenames):
        """
        This method loads all base constants for a given scenario manager. It looks them up in all the files given
        If a scenario manager spreads over multiple files and you define base constants in different files for the same
        manager, just don't! You will definitely lose data!!
        :param scenario_manager:
        :param filenames:
        :return: Base constants, merged from multiple files into one dict!
        """
        base_constants = {}
        for filename in filenames:
            json_data = open(filename, encoding="utf-8").read()

            try:
                json_dict = dict(json.loads(json_data))
            except ValueError as e:
                log("[ERROR] Problem reading {}. Error message: {}".format(filename, str(e)))
                return None

            if scenario_manager in json_dict.keys():
                scenario_manager_dict = json_dict[scenario_manager]

                if "base_constants" in scenario_manager_dict.keys():
                    for key, value in scenario_manager_dict["base_constants"].items():
                        base_constants[key] = value

        return base_constants

    def __get_all_base_points(self, scenario_manager, filenames):
        """
        This method loads all base points for a given scenario manager. It looks them up in all the files given
        If a scenario manager spreads over multiple files and you define base constants in different files for the same
        manager, just don't! You will definitely lose data!!
        :param scenario_manager:
        :param filenames:
        :return: Base constants, merged from multiple files into one dict!
        """
        base_points = {}
        for filename in filenames:
            json_data = open(filename, encoding="utf-8").read()

            try:
                json_dict = dict(json.loads(json_data))
            except ValueError as e:
                log("[ERROR] Problem reading {}. Error message: {}".format(filename, str(e)))
                return None

            if scenario_manager in json_dict.keys():
                scenario_manager_dict = json_dict[scenario_manager]

                if "base_points" in scenario_manager_dict.keys():
                    for key, value in scenario_manager_dict["base_points"].items():
                        base_points[key] = value

        return base_points

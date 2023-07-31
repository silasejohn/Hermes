import configparser  # to parse config files


class Poseidon:  # "parsing" module
    def __init__(self,
                 config_file_name: str) -> None:
        # logger variable initialization
        self._CONFIG_FILE_NAME = config_file_name
        self._CONFIG_OBJ = None

    def setup_parser(self):
        self._CONFIG_OBJ = configparser.ConfigParser()
        self._CONFIG_OBJ.read(self._CONFIG_FILE_NAME)

    def print_valid_sections(self):
        print("Sections Identified in", self._CONFIG_FILE_NAME)
        for section in self._CONFIG_OBJ:
            print(section)
        print(f"\n{self._CONFIG_OBJ.sections()}")

    def get_config_value(self,
                         section_name: str,
                         key_name: str) -> str:
        if section_name in self._CONFIG_OBJ:
            value = self._CONFIG_OBJ[section_name][key_name]
            # print(f"Retrieved value {value} for key {key_name} in section {section_name} "
            #       f"of config_file {self._CONFIG_FILE_NAME}")
            return value
        else:
            # print(f"NO VALUE FOUND for key {key_name} in section {section_name} "
            #       f"of config_file {self._CONFIG_FILE_NAME}")
            return "ERROR!"

    def get_bool_config_value(self,
                              section_name: str,
                              key_name: str) -> str:
        if section_name in self._CONFIG_OBJ:
            value = self._CONFIG_OBJ.getboolean(section_name, key_name)
            # print(f"Retrieved value {value} for key {key_name} in section {section_name} "
            #       f"of config_file {self._CONFIG_FILE_NAME}")
            return value
        else:
            # print(f"NO VALUE FOUND for key {key_name} in section {section_name} "
            #       f"of config_file {self._CONFIG_FILE_NAME}")
            return "ERROR!"

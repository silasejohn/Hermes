import argparse  # for reading + parsing command line args
from ConfigParserUtility import Poseidon  # to read and parse a script-specific configuration file
from dotenv import load_dotenv  # to read and store sensitive/critical variables from a local source
from Hermes import Hermes  # to create and manage customized MQTT clients
from LoggingUtility import Aristotle  # to enable a customized logging service
import os  # used in conjunction w/ dotenv to pull sensitive info from a local serve


def setup_argument_parser(log_file_name: str) -> argparse.Namespace:  # argparse setup
    parser = argparse.ArgumentParser(description="[TEST] Simple Python script for testing purposes")
    parser.add_argument("-d", "--debug", help=f"log debugging information to {log_file_name}", action="store_true")
    parser.add_argument("-v", "--version", help="specifies current program version", action="store_true")
    parser.add_argument("-c", "--clean", help=f"cleanses {log_file_name}", action="store_true")
    arg_options = parser.parse_args()
    return arg_options


def parse_arg_options(arg_options: argparse.Namespace) -> None:
    if arg_options.version:  # console output program version (based on version argument)
        print(f"Current Program Version: {PROJECT_VERSION}")
        exit(0)


def process_execution_arguments(log_file_name: str):
    arg_options = setup_argument_parser(log_file_name)
    parse_arg_options(arg_options)
    return arg_options


def parse_config_file(config_file_name: str, python_file_name: str) -> int:
    # config file setup goes here
    config_obj = Poseidon(config_file_name)
    config_obj.setup_parser()
    # config_obj.print_valid_sections()

    # pull out log values from the config files
    log_to_file = config_obj.get_bool_config_value(python_file_name, "LogToFile")
    log_to_console = config_obj.get_bool_config_value(python_file_name, "LogToConsole")

    # logic to determine logging mode
    logging_method = -1  # both (0), console (1), file (2), invalid (-1)
    if log_to_file and log_to_console:
        logging_method = 0
    elif log_to_console:
        logging_method = 1
    elif log_to_file:
        logging_method = 2
    else:
        pass  # unreachable code

    return logging_method


if __name__ == '__main__':
    # [GLOBAL VARS, local env] global constants for this python script
    load_dotenv()  # load local variables and information
    CONFIG_FILE_NAME = os.getenv('CONFIG_FILE_NAME')
    PROJECT_VERSION = os.getenv('PROJECT_VERSION')
    PYTHON_FILE_NAME = "example.py"
    LOG_FILE_NAME = os.getenv('EXAMPLE_LOG_FILE_NAME')  # creates log file if it does not previously exist

    # [FILE ARGS] read & parse file execution arguments, return all arguments specified
    arg_options_obj = process_execution_arguments(LOG_FILE_NAME)

    # [CONFIG]read & parse config file, set LOGGING_METHOD
    LOGGING_METHOD = parse_config_file(CONFIG_FILE_NAME, PYTHON_FILE_NAME)  # both (0), console (1), file (2)

    # [LOGGING] create custom logger, initialize logger, clean log file if needed
    myLog = Aristotle(__name__, LOG_FILE_NAME, arg_options_obj.debug, arg_options_obj.clean, LOGGING_METHOD)
    myLog.initialize_logger()
    myLog.clean_log_file()  # clean the specified log file (based on clean argument)
    myLog.restart_log_message(PYTHON_FILE_NAME, PROJECT_VERSION)  # log a program restart
    myLog.create_log_event("info", f"LOGGING METHOD: {LOGGING_METHOD} "
                                   f"at threshold of {myLog.get_logging_threshold_str()} "
                                   f"({myLog.get_logging_threshold_int()})")  # log the current LOGGING method
    myLog.create_log_event("info", f"Script Setup Complete")  # log end of script setup

    # [HERMES CLIENT INITIALIZATION]
    myLog.create_log_event("info", f"Initializing Test Client 1 from Hermes Module")
    client_sub_one = Hermes("client_sub_one", True, True)

    # loops forever
    client_sub_one.connect_to_broker_and_loop()




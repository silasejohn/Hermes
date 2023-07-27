# This is a test Python script
import argparse  # to review command line arguments
from ConfigParserUtility import Poseidon  # to parse config file and pull out configuration values
from dotenv import load_dotenv  # to import project hidden environment variables
from LoggingUtility import Aristotle  # to use the utility logging wrapper module
import os  # access environment variables
import requests  # to identify a client IP_ADDR


def find_client_ip_addr(url: str) -> int:
    response = requests.get(url)
    print('Your Client IP for {0} is {1}'.format(url, response.json()['origin']))
    return 0  # successful return indicated by Exit Code 0 (no problems)


def setup_argument_parser(test_log_file_name: str) -> argparse.Namespace:  # argparse setup
    parser = argparse.ArgumentParser(description="[TEST] Simple Python script for testing purposes")
    parser.add_argument("-d", "--debug", help=f"log debugging information to {test_log_file_name}", action="store_true")
    parser.add_argument("-v", "--version", help="specifies current program version", action="store_true")
    parser.add_argument("-c", "--clean", help=f"cleanses {test_log_file_name}", action="store_true")
    arg_options = parser.parse_args()
    return arg_options


if __name__ == '__main__':
    load_dotenv()  # load local variables and information

    # define some inter-file constants
    PYTHON_FILE_NAME = "test.py"
    LOGGING_METHOD = -1
    # LOGGING_METHOD = 2  # both (0), console (1), file (2)

    # specify constants from environment file
    CONFIG_FILE_NAME = os.getenv('CONFIG_FILE_NAME')
    PROJECT_VERSION = os.getenv('PROJECT_VERSION')
    TEST_LOG_FILE_NAME = os.getenv('TEST_LOG_FILE_NAME')  # creates log file if it does not previously exist

    # setup arguments of the python scripting tools
    arg_options_obj = setup_argument_parser(TEST_LOG_FILE_NAME)

    # console output program version (based on version argument)
    if arg_options_obj.version:
        print(f"Current Program Version: {PROJECT_VERSION}")
        exit(0)

    # config file setup goes here
    myConfig = Poseidon(CONFIG_FILE_NAME)
    myConfig.setup_parser()
    myConfig.print_valid_sections()

    # pull out log values from the config files
    log_to_file = myConfig.get_bool_config_value(PYTHON_FILE_NAME, "LogToFile")
    log_to_console = myConfig.get_bool_config_value(PYTHON_FILE_NAME, "LogToConsole")

    # logic to determine logging mode
    # both (0), console (1), file (2)
    if log_to_file and log_to_console:
        LOGGING_METHOD = 0
    elif log_to_console:
        LOGGING_METHOD = 1
    elif log_to_file:
        LOGGING_METHOD = 2
    else:
        pass  # unreachable code

    # logging setup
    myLog = Aristotle(__name__, TEST_LOG_FILE_NAME, arg_options_obj.debug, arg_options_obj.clean, LOGGING_METHOD)
    myLog.initialize_logger()

    # clean the specified log file (based on clean argument)
    myLog.clean_log_file()

    # restart log message block to identify the new program run in the specified logging location
    myLog.restart_log_message(PYTHON_FILE_NAME, PROJECT_VERSION)

    # simple function that tests logging all function types (ensure that the correct threshold is set)
    myLog.create_log_event("info", f"LOGGING METHOD: {LOGGING_METHOD}")

    # calls default ip function
    rv = find_client_ip_addr('https://httpbin.org/ip')

    # exit code logging
    if rv != 0:
        myLog.create_log_event("error", f"Problems detected. Unsuccessful Exit Code {rv} ")
    else:
        myLog.create_log_event("info", "Client IP Addr successfully identified ")

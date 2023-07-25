# This is a test Python script
import argparse  # to review command line arguments
from dotenv import load_dotenv  # to import project hidden environment variables
import os  # access environment variables
import requests  # to identify a client IP_ADDR
from LoggingUtility import *  # to use the utility logging wrapper module


def find_client_ip_addr(url: str) -> int:
    response = requests.get(url)
    print('Your Client IP for {0} is {1}'.format(url, response.json()['origin']))
    return 0  # successful return indicated by Exit Code 0 (no problems)


if __name__ == '__main__':
    load_dotenv()  # load project environment variables

    # specify constants from environment file
    PROJECT_VERSION = os.getenv('PROJECT_VERSION')
    # will create log file if it does not previously exists, appends info if previously exists
    TEST_LOG_FILE_NAME = os.getenv('TEST_LOG_FILE_NAME')


    # argparse setup
    parser = argparse.ArgumentParser(description="[TEST] Simple Python script to identify IP_ADDR given a URL")
    parser.add_argument("-d", "--debug", help=f"log debugging information to {TEST_LOG_FILE_NAME}", action="store_true")
    parser.add_argument("-v", "--version", help="specifies current program version", action="store_true")
    parser.add_argument("-c", "--clean", help=f"cleanses {TEST_LOG_FILE_NAME}", action="store_true")
    arg_options = parser.parse_args()

    # configure logging level (based on debug argument)
    if arg_options.debug:
        configure_logging(TEST_LOG_FILE_NAME, "debug")  # lowest logging level
    else:
        configure_logging(TEST_LOG_FILE_NAME, "info")  # second lowest logging level

    # clean the specified log file (based on clean argument)
    if arg_options.clean:
        with open(TEST_LOG_FILE_NAME, 'w') as file:
            pass

    logging_info("\n\n[NEW PROGRAM IN EXECUTION] ~ ~ ~ ~ ~ ~", True)  # indicate program start in logfile
    logging_info(f" Version: {PROJECT_VERSION}", True)  # indicate program start in logfile

    # console output program version (based on version argument)
    if arg_options.version:
        print(f"Current Program Version: {PROJECT_VERSION}")
        exit(0)

    curr_local_time = time.ctime(time.time())
    logging_info(f" Current Timestamp: [{curr_local_time}] ", True)  # log program start time in logfile

    # calls default ip function
    rv = find_client_ip_addr('https://httpbin.org/ip')

    # exit code logging
    if rv != 0:
        logging_error(f"Problems detected. Unsuccessful Exit Code {rv} ")
    else:
        logging_info("Client IP Addr successfully identified ")

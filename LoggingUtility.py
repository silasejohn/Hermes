import logging  # logging of program execution
import sys
import time  # determine seconds since epoch

# __{LOGGING LEVELS}__
# Debug (10): debug log messages
# Info (20): common programs actions / checkpoints
# Warning (30): not an error, but an unexpected program action
# Error (40): program failure to perform essential task or function
# Critical (50): critical, application-defining error

# Default Logger is named ROOT (when logger functions are directly called)
# Custom Loggers are named off the file name


# named after a famous scribe (records information, captures any new information)
class Aristotle:
    def __init__(self,
                 logger_name: str,
                 log_file_name: str,
                 debug: bool = False,
                 cleanse: bool = False,
                 default_logging_method: int = 0) -> None:

        # logger naming initialization
        self._FILE_LOGGER_NAME = logger_name
        self._CONSOLE_LOGGER_NAME = f"[{logger_name}]"
        self._LOG_FILE_NAME = str(log_file_name)

        # logger objects empty initialization
        self._CONSOLE_LOGGER_OBJ = None
        self._FILE_LOGGER_OBJ = None

        # handler / formatter empty initializer
        self._STDOUT_HANDLER = None
        self._FILE_HANDLER = None
        self._STDOUT_FORMAT = None
        self._FILE_FORMAT = None

        # corresponds to the options in obj initialization
        self._DEFAULT_LOGGING_METHOD = default_logging_method
        self._DEBUG = debug
        self._CLEANSE = cleanse

    def create_file_handler(self) -> None:
        self._FILE_HANDLER = logging.FileHandler(self._LOG_FILE_NAME)
        if self._DEBUG:
            self._FILE_HANDLER.setLevel(logging.DEBUG)
        else:
            self._FILE_HANDLER.setLevel(logging.INFO)

    def create_file_formatter(self) -> None:
        # 8.8s refers to minimum and max 8 chars of a string
        self._FILE_FORMAT = logging.Formatter('%(levelname)8.8s:%(name)s [%(asctime)s] ~> %(message)s',
                                              '%H:%M:%S %a | %b %d %Y')
        self._FILE_HANDLER.setFormatter(self._FILE_FORMAT)

    def create_console_handler(self) -> None:
        self._STDOUT_HANDLER = logging.StreamHandler(sys.stdout)
        if self._DEBUG:
            self._STDOUT_HANDLER.setLevel(logging.DEBUG)
        else:
            self._STDOUT_HANDLER.setLevel(logging.INFO)

    def create_console_formatter(self) -> None:
        self._STDOUT_FORMAT = logging.Formatter('%(levelname)8.8s:%(name)s [%(asctime)s] ~> %(message)s',
                                                '%H:%M:%S')
        self._STDOUT_HANDLER.setFormatter(self._STDOUT_FORMAT)

    def create_handlers_and_formatters(self) -> None:
        if self._DEFAULT_LOGGING_METHOD == 2:
            self.create_file_handler()
            self.create_file_formatter()
        elif self._DEFAULT_LOGGING_METHOD == 1:
            self.create_console_handler()
            self.create_console_formatter()
        elif self._DEFAULT_LOGGING_METHOD == 0:
            self.create_file_handler()
            self.create_file_formatter()
            self.create_console_handler()
            self.create_console_formatter()
        else:
            pass  # unreachable code

    def create_logger_objects(self) -> None:
        # create up to 2 logger objects for console and/or file logging
        if self._DEFAULT_LOGGING_METHOD == 2:
            self._FILE_LOGGER_OBJ = logging.getLogger(self._FILE_LOGGER_NAME)
        elif self._DEFAULT_LOGGING_METHOD == 1:
            self._CONSOLE_LOGGER_OBJ = logging.getLogger(self._CONSOLE_LOGGER_NAME)
        elif self._DEFAULT_LOGGING_METHOD == 0:
            self._CONSOLE_LOGGER_OBJ = logging.getLogger(self._CONSOLE_LOGGER_NAME)
            self._FILE_LOGGER_OBJ = logging.getLogger(self._FILE_LOGGER_NAME)
        else:
            pass  # unreachable code

        # set logging thresholds for the file logging object
        if self._DEBUG and (self._DEFAULT_LOGGING_METHOD == 0 or self._DEFAULT_LOGGING_METHOD == 2):
            self._FILE_LOGGER_OBJ.setLevel(logging.DEBUG)
        elif (not self._DEBUG) and (self._DEFAULT_LOGGING_METHOD == 0 or self._DEFAULT_LOGGING_METHOD == 2):
            self._FILE_LOGGER_OBJ.setLevel(logging.INFO)
        else:
            pass

        # set logging thresholds for the console logging object
        if self._DEBUG and (self._DEFAULT_LOGGING_METHOD == 0 or self._DEFAULT_LOGGING_METHOD == 1):
            self._CONSOLE_LOGGER_OBJ.setLevel(logging.DEBUG)
        elif (not self._DEBUG) and (self._DEFAULT_LOGGING_METHOD == 0 or self._DEFAULT_LOGGING_METHOD == 1):
            self._CONSOLE_LOGGER_OBJ.setLevel(logging.INFO)
        else:
            pass

    def assign_handlers_and_formatters(self) -> None:
        # assign appropriate handlers and formatters to the right logging object
        if self._DEFAULT_LOGGING_METHOD == 2:
            print("Logging to a FILE STREAM...")
            self._FILE_LOGGER_OBJ.addHandler(self._FILE_HANDLER)
            print("self._FILE_HANDLER 2 is", self._FILE_HANDLER, "and type is", type(self._FILE_HANDLER))
        elif self._DEFAULT_LOGGING_METHOD == 1:
            print("Logging to a CONSOLE STREAM...")
            self._CONSOLE_LOGGER_OBJ.addHandler(self._STDOUT_HANDLER)
            print("self._STDOUT_HANDLER 2 is", self._STDOUT_HANDLER, "and type is", type(self._STDOUT_HANDLER))
        elif self._DEFAULT_LOGGING_METHOD == 0:
            print("Logging to a FILE STREAM...")
            print("Logging to a CONSOLE STREAM...")
            self._FILE_LOGGER_OBJ.addHandler(self._FILE_HANDLER)
            self._CONSOLE_LOGGER_OBJ.addHandler(self._STDOUT_HANDLER)
            print("self._FILE_HANDLER 2 is", self._FILE_HANDLER, "and type is", type(self._FILE_HANDLER))
            print("self._STDOUT_HANDLER 2 is", self._STDOUT_HANDLER, "and type is", type(self._STDOUT_HANDLER))
        else:
            pass  # unreachable code

    # last parameter is (apart from default logging, you want to specifically print something to console or file)
    def create_log_event(self,
                         log_type: str,
                         formatted_message: str,
                         logging_method: int = -1) -> None:

        # creative method of using a class variable as a default value to a class method
        if logging_method == -1:
            logging_method = self._DEFAULT_LOGGING_METHOD

        # if you need to log to the console
        if logging_method == 0 or logging_method == 1:
            match log_type:
                case "debug":
                    self._CONSOLE_LOGGER_OBJ.debug(formatted_message)
                case "info":
                    self._CONSOLE_LOGGER_OBJ.info(formatted_message)
                case "warning":
                    self._CONSOLE_LOGGER_OBJ.warning(formatted_message)
                case "error":
                    self._CONSOLE_LOGGER_OBJ.error(formatted_message)
                case "critical":
                    self._CONSOLE_LOGGER_OBJ.critical(formatted_message)
                case _:  # default case
                    self._CONSOLE_LOGGER_OBJ.debug(formatted_message)

        # if you need to log to a specified file
        if logging_method == 0 or logging_method == 2:
            match log_type:
                case "debug":
                    self._FILE_LOGGER_OBJ.debug(formatted_message)
                case "info":
                    self._FILE_LOGGER_OBJ.info(formatted_message)
                case "warning":
                    self._FILE_LOGGER_OBJ.warning(formatted_message)
                case "error":
                    self._FILE_LOGGER_OBJ.error(formatted_message)
                case "critical":
                    self._FILE_LOGGER_OBJ.critical(formatted_message)
                case _:  # default case
                    self._FILE_LOGGER_OBJ.debug(formatted_message)

    def upper_wrapper(self) -> None:
        self.create_log_event("info", "--------------------------")

    def lower_wrapper(self) -> None:
        self.create_log_event("info", "--------------------------\n")

    def test_all_log_message_types(self) -> None:
        self.create_log_event("info", "[Testing Five (5) Different Logging Thresholds]")
        self.upper_wrapper()
        self.create_log_event("debug", f"[TEST] Logging a DEBUG Log Message...")
        self.create_log_event("info", f"[TEST] Logging a INFO Log Message...")
        self.create_log_event("warning", f"[TEST] Logging a WARNING Log Message...")
        self.create_log_event("error", f"[TEST] Logging a ERROR Log Message...")
        self.create_log_event("critical", f"[TEST] Logging a CRITICAL Log Message...")
        self.lower_wrapper()

    def restart_log_message(self,
                            python_file_name: str = "unknown.py",
                            python_project_version: str = "[X.X.X]") -> None:
        self.create_log_event("info", "Restarting Program...\n")
        self.upper_wrapper()
        self.create_log_event("info", f"| [{python_file_name} IN EXECUTION] |")
        self.create_log_event("info", f"| [Version: {python_project_version}] |")
        self.lower_wrapper()

    def initialize_logger(self) -> None:
        # set up special logger object(s)
        self.create_logger_objects()

        # based on DEFAULT_LOGGING_METHOD, will log to the file or console or both
        self.create_handlers_and_formatters()

        # assign appropriate handlers and formatters to 1 or 2 logger objects
        self.assign_handlers_and_formatters()

        # self.test_all_log_message_types() # for debugging purposes

    def clean_log_file(self) -> None:  # clean the specified log file on program start if specified
        if self._CLEANSE:
            with open(self._LOG_FILE_NAME, 'w') as file:
                pass

    def get_file_logger_name(self) -> str:
        return self._FILE_LOGGER_NAME

    def get_console_logger_name(self) -> str:
        return self._CONSOLE_LOGGER_NAME

    def get_console_logger_obj(self) -> logging.Logger:
        return self._CONSOLE_LOGGER_OBJ

    def get_file_logger_obj(self) -> logging.Logger:
        return self._FILE_LOGGER_OBJ


# TODO:
# (1) rewrite utility class to a logger class - w/ handler and have options to write to file or stdout or both
# - maybe some inheritance? base abstract logger class w/ sub logger classes derived and implemented
# (2) think about incorporating colored text for terminal output
# (3) rewrite 5 functions into 1 function w/ an added parameter for log level - should writing log messages
# be a static method?
# (4) Rewrite all variables into proper names (w/ underscores)
# (5) Split the logger obj creation for a file and for the console (different handlers), then create a macro static
# function where you can specify to use the console log or a file log or both at the same time as well as the
# appropriate log level for both (setting log level needs to be an input - debug if debug option, info otherwise)
# (6) raise and throw exceptions out of functions if problems could arise instead of doing return codes...
# https://coralogix.com/blog/python-logging-best-practices-tips/

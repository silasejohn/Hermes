import logging  # logging of program execution
import time  # determine seconds since epoch

# __{LOGGING LEVELS}__
# Debug (10): debug log messages
# Info (20): common programs actions / checkpoints
# Warning (30): not an error, but an unexpected program action
# Error (40): program failure to perform essential task or function
# Critical (50): critical, application-defining error


def configure_logging(log_file_name: str, log_type: str):
    match log_type:
        case "debug":
            logging.basicConfig(level=logging.DEBUG, filename=log_file_name)
        case "info":
            logging.basicConfig(level=logging.INFO, filename=log_file_name)
        case "warning":
            logging.basicConfig(level=logging.WARNING, filename=log_file_name)
        case "error":
            logging.basicConfig(level=logging.ERROR, filename=log_file_name)
        case "critical":
            logging.basicConfig(level=logging.CRITICAL, filename=log_file_name)


def logging_debug(formatted_message: str, startup=False):
    if startup:
        logging.debug(formatted_message)  # indicate program start in logfile
    else:  # if not a startup logging message
        curr_time = time.ctime(time.time())
        logging.debug(f"[{curr_time}] {formatted_message}")


def logging_info(formatted_message: str, startup=False):
    if startup:
        logging.info(formatted_message)  # indicate program start in logfile
    else:  # if not a startup logging message
        curr_time = time.ctime(time.time())
        logging.info(f"[{curr_time}] {formatted_message}")


def logging_warning(formatted_message: str, startup=False):
    if startup:
        logging.warning(formatted_message)  # indicate program start in logfile
    else:  # if not a startup logging message
        curr_time = time.ctime(time.time())
        logging.warning(f"[{curr_time}] {formatted_message}")


def logging_error(formatted_message: str, startup=False):
    if startup:
        logging.error(formatted_message)  # indicate program start in logfile
    else:  # if not a startup logging message
        curr_time = time.ctime(time.time())
        logging.error(f"[{curr_time}] {formatted_message}")


def logging_critical(formatted_message: str, startup=False):
    if startup:
        logging.critical(formatted_message)  # indicate program start in logfile
    else:  # if not a startup logging message
        curr_time = time.ctime(time.time())
        logging.critical(f"[{curr_time}] {formatted_message}")


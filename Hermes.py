# create Hermes class here
# MQTT Links:
# http://www.steves-internet-guide.com/python-notes/
# http://www.steves-internet-guide.com/into-mqtt-python-client/
# https://www.emqx.com/en/blog/how-to-use-mqtt-in-python
# https://www.emqx.com/en/blog/advanced-features-of-mqtt-topics
from ConfigParserUtility import Poseidon  # to read and parse a script-specific configuration file
from dotenv import load_dotenv  # to read and store sensitive/critical variables from a local source
from LoggingUtility import Aristotle  # to enable a customized logging service
import paho.mqtt.client as mqtt  # to complete mqtt related activities
import os  # used in conjunction w/ dotenv to pull sensitive info from a local serve


class Hermes:
    def __init__(self, client_name: str, clean_log: bool = True, debug_log: bool = False):
        self._CLIENT_NAME = client_name
        self._CLEAN_LOG = clean_log
        self._DEBUG_LOG = debug_log

        # [CONFIG FILE SETUP]
        load_dotenv()  # load local variables and information
        self._PYTHON_FILE_NAME = "hermes.py"
        self._CONFIG_FILE_NAME = os.getenv('CONFIG_FILE_NAME')
        self._CONFIG_OBJ = Poseidon(self._CONFIG_FILE_NAME)
        self._LOGGING_METHOD = self.parse_config_file()  # both (0), console (1), file (2)

        # [DEFINE LOGGING VARIABLES]
        self._LOG_FILE_NAME = os.getenv('HERMES_LOG_FILE_NAME')
        self._PROJECT_VERSION = os.getenv('PROJECT_VERSION')

        # [LOGGING SETUP]
        self._MQTT_LOG = Aristotle(__name__, self._LOG_FILE_NAME, self._DEBUG_LOG, self._CLEAN_LOG, self._LOGGING_METHOD)
        self._MQTT_LOG.initialize_logger()
        self._MQTT_LOG.clean_log_file()
        self._MQTT_LOG.restart_log_message(self._PYTHON_FILE_NAME, self._PROJECT_VERSION)
        self._MQTT_LOG.create_log_event("info", f"LOGGING METHOD: {self._LOGGING_METHOD} "
                                        f"at threshold of {self._MQTT_LOG.get_logging_threshold_str()} "
                                        f"({self._MQTT_LOG.get_logging_threshold_int()})")
        self._MQTT_LOG.create_log_event("info", f"MQTT Logger Setup Complete")  # log end of script setup

        # [Define MQTT Client]
        self._MQTT_LOG.create_log_event("info", f"Creating up MQTT Client [{self._CLIENT_NAME}]")
        self._MQTT_CLIENT = mqtt.Client(self._CLIENT_NAME)
        self.setup_mqtt_callbacks()
        self._MQTT_LOG.create_log_event("info", f"MQTT Client [{self._CLIENT_NAME}] Creation Complete")

        # [Obtain Broker Info]
        self._BROKER_HOSTNAME = None
        self._BROKER_PORT_NUM = None
        self._KEEP_ALIVE = None
        self.obtain_broker_info()

    def parse_config_file(self) -> int:
        # config file setup goes here
        self._CONFIG_OBJ.setup_parser()

        # pull out log values from the config files
        log_to_file = self._CONFIG_OBJ.get_bool_config_value(self._PYTHON_FILE_NAME, "LogToFile")
        log_to_console = self._CONFIG_OBJ.get_bool_config_value(self._PYTHON_FILE_NAME, "LogToConsole")

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

    # callback for when the client receives a [CONNACK] response from the server
    def on_connect(self, client, userdata, flags, rc):
        self._MQTT_LOG.create_log_event("info", f"[{self._CLIENT_NAME}] connected to MQTT BROKER w/ result code {rc}")

        # by subscribing in on_connect, we re-subscribe to same topics if we lose cnnxtn and reconnect
        topic_mqtt_broker_sys = "$SYS/#"
        client.subscribe(topic_mqtt_broker_sys)  # subscribe to MQTT Broker $SYS topic
        self._MQTT_LOG.create_log_event("info", f"[{self._CLIENT_NAME}] subscribed to topic [{topic_mqtt_broker_sys}]")

    # callback for when a [PUBLISH] message is received from the MQTT Broker
    def on_message(self, client, userdata, msg):
        self._MQTT_LOG.create_log_event("info", f"[{self._CLIENT_NAME}] received from topic [{msg.topic}] "
                                                f"~> {str(msg.payload)}", 2)  # log to file AND print to console

    def setup_mqtt_callbacks(self):
        self._MQTT_CLIENT.on_connect = self.on_connect
        self._MQTT_LOG.create_log_event("info", f"MQTT Client [{self._CLIENT_NAME}] has a callback for on_connect")
        self._MQTT_CLIENT.on_message = self.on_message
        self._MQTT_LOG.create_log_event("info", f"MQTT Client [{self._CLIENT_NAME}] has a callback for on_message")

    def obtain_broker_info(self):
        self._MQTT_LOG.create_log_event("info", f"Obtaining MQTT Broker Information...")
        self._BROKER_HOSTNAME = self._CONFIG_OBJ.get_config_value(self._PYTHON_FILE_NAME, "BrokerHostname")
        self._BROKER_PORT_NUM = self._CONFIG_OBJ.get_config_value(self._PYTHON_FILE_NAME, "BrokerPort")
        self._KEEP_ALIVE = self._CONFIG_OBJ.get_config_value(self._PYTHON_FILE_NAME, "KeepAlive")
        self._MQTT_LOG.create_log_event("info", f"MQTT Broker with hostname [{self._BROKER_HOSTNAME}] and "
                                                f"port [{self._BROKER_PORT_NUM}] and "
                                                f"KeepAlive of [{self._KEEP_ALIVE}] has been identified")

    def connect_to_broker_and_loop(self):
        # [Setup MQTT Connection]
        self._MQTT_LOG.create_log_event("debug", f"type of self._BROKER_HOSTNAME [{self._BROKER_HOSTNAME}] "
                                                 f"is {type(self._BROKER_HOSTNAME)}")
        self._MQTT_LOG.create_log_event("debug", f"type of self._BROKER_PORT_NUM [{self._BROKER_PORT_NUM}] "
                                                 f"is {type(self._BROKER_PORT_NUM)}")
        self._MQTT_LOG.create_log_event("debug", f"type of self._KEEP_ALIVE [{self._KEEP_ALIVE}] "
                                                 f"is {type(self._KEEP_ALIVE)}")
        self._MQTT_LOG.create_log_event("debug", f"type of self._BROKER_PORT_NUM [{self._BROKER_PORT_NUM}] "
                                                 f"is {type(int(self._BROKER_PORT_NUM))}")
        self._MQTT_LOG.create_log_event("debug", f"type of self._KEEP_ALIVE [{self._KEEP_ALIVE}] "
                                                 f"is {type(int(self._KEEP_ALIVE))}")

        self._MQTT_LOG.create_log_event("info", f"[{self._CLIENT_NAME}] connecting to MQTT Broker...")
        self._MQTT_CLIENT.connect(self._BROKER_HOSTNAME, int(self._BROKER_PORT_NUM), int(self._KEEP_ALIVE))
        self._MQTT_LOG.create_log_event("info", f"[{self._CLIENT_NAME}] is CONNECTED to MQTT Broker")

        # blocking call to process network traffic, reconnections, and callbacks
        self._MQTT_CLIENT.loop_forever()


# split the private vs public parameters into .env and .ini config files appropriately
# clean up MQTT Log code so that everything runs inside the initialization() function
# instead of passing a million objs into obj initialization functions, create some sort of data structure w/
#   multiple flags (such as "cleanse" or "debug")

import logging
from typing import Dict

from openfabric_pysdk.context import Ray, State, StateStatus
from openfabric_pysdk.loader import ConfigClass, InputClass, OutputClass, \
    config_callback_function, \
    execution_callback_function
from openfabric_pysdk.loader.config import manifest, state_config
from openfabric_pysdk.store import KeyValueDB


#######################################################
#  App
#######################################################
class App:
    state: State = None

    # ------------------------------------------------------------------------
    def __init__(self):
        self.state = State()

    # ------------------------------------------------------------------------
    def set_status(self, status: StateStatus):
        self.state.status = status

    # ------------------------------------------------------------------------
    def execution_callback_function(self, input: InputClass, ray: Ray) -> OutputClass:
        return execution_callback_function(input, ray, self.state)

    # ------------------------------------------------------------------------
    def config_callback_function(self, config: Dict[str, ConfigClass]):
        logging.info(f"Openfabric - apply APP configuration")
        if config_callback_function is not None:
            try:
                config_callback_function(config, self.state)
            except Exception as e:
                logging.error(f"Openfabric - invalid configuration can\'t restored : {e}")
        else:
            logging.warning(f"Openfabric - no configuration callback available")

    # ------------------------------------------------------------------------
    def get_manifest(self) -> KeyValueDB:
        return manifest

    # ------------------------------------------------------------------------
    def get_state_config(self) -> KeyValueDB:
        return state_config

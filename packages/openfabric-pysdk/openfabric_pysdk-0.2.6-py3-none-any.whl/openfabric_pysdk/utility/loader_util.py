import importlib
from pydoc import locate

from openfabric_pysdk.loader.config import execution
from openfabric_pysdk.benchmark import MeasureBlockTime


#######################################################
# Class loader utility class
#######################################################
class LoaderUtil:

    @staticmethod
    def import_class(name):
        return locate(name.__module__ + "." + name.__name__)

    @staticmethod
    def get_class(name):
        with MeasureBlockTime("Loader::get_class"):
            class_config = execution.get(name)
            if class_config is None:
                return None
            clazz = class_config['class']
            package = class_config['package']
            if clazz is None or package is None:
                return None
            module = importlib.import_module(package)
            return locate(module.__name__ + "." + clazz)

    @staticmethod
    def get_function(name):
        with MeasureBlockTime("Loader::get_function"):
            function_config = execution.get(name)
            if function_config is None:
                return None
            function = function_config['function']
            package = function_config['package']
            if function is None or package is None:
                return None
            module = importlib.import_module(package)
            # print(module.__name__ + "." + function)
            return locate(module.__name__ + "." + function)

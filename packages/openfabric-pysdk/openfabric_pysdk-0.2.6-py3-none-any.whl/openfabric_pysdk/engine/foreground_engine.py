import logging
import os
import traceback
import uuid
from typing import Any, Dict, List

from openfabric_pysdk.app import App
from openfabric_pysdk.benchmark import MeasureBlockTime
from openfabric_pysdk.context import MessageType, Ray, RaySchema, RayStatus, State
from openfabric_pysdk.loader import InputSchema, OutputSchema
from openfabric_pysdk.store import Store

# TODO: should not exist as it:
#    - creates inconsistent usage ('submitted' message not published, nor periodical 'progress')
#    - adds a way to kill the instance by overloading the system
# Would make more sense to have instead a priority queue and process only one or at most a limited number of requests at a time.
#######################################################
#  Foreground Engine
#######################################################
class ForegroundEngine:
    __app: App = None
    __store: Store = None
    __rays: Dict[str, Ray] = None

    # ------------------------------------------------------------------------
    def __init__(self):
        self.__rays = dict()
        self.__store = Store(path=f"{os.getcwd()}/datastore")

    # ------------------------------------------------------------------------
    def prepare(self, app: App, data: Any, qid=None, sid=None, uid=None, rid=None) -> str:
        if qid is None:
            qid: str = uuid.uuid4().hex
        ray = self.ray(qid)
        ray.status = RayStatus.QUEUED
        ray.sid = sid
        ray.uid = uid
        ray.rid = rid
        self.write(qid, 'ray', ray, RaySchema().dump)
        self.write(qid, 'in', data)
        self.__app = app
        return qid

    # ------------------------------------------------------------------------
    def ray(self, qid: str):
        if self.__rays.get(qid) is None:
            ray = Ray(qid=qid)
            self.__rays[qid] = ray
        return self.__rays[qid]

    # ------------------------------------------------------------------------
    def rays(self, criteria=None) -> List[Ray]:
        rays: List[Ray] = []
        for qid, ray in self.__rays.items():
            if criteria is None or criteria(ray):
                rays.append(ray)
        return rays

    # ------------------------------------------------------------------------
    def process(self, qid):

        with MeasureBlockTime("Engine::execution_callback_function"):

            output = None
            ray = self.ray(qid)
            try:
                data = self.read(qid, 'in', InputSchema().load)
                if data is None:
                    return None

                ray.status = RayStatus.RUNNING
                self.write(qid, 'ray', ray, RaySchema().dump)

                # Callback execution method
                output = self.__app.execution_callback_function(data, ray)

                ray.status = RayStatus.COMPLETED
            except:
                error = f"Openfabric - failed executing: [{qid}]\n{traceback.format_exc()}"
                logging.error(error)
                ray.message(MessageType.ERROR, error)
                ray.status = RayStatus.FAILED
        ray.complete()
        self.write(qid, 'ray', ray, RaySchema().dump)
        self.write(qid, 'out', output, OutputSchema().dump)

        return output

    # ------------------------------------------------------------------------
    def read(self, qid: str, key: str, deserializer=None) -> Any:
        output = self.__store.get(qid, key)
        if output is None:
            return None
        output = deserializer(output) if deserializer is not None else output
        return output

    # ------------------------------------------------------------------------
    def write(self, qid: str, key: str, val: Any, serializer=None):
        if val is not None:
            val = serializer(val) if serializer is not None else val
        self.__store.set(qid, key, val)

    # ------------------------------------------------------------------------
    def delete(self, qid: str) -> Ray:
        ray = self.ray(qid)
        self.__store.drop(qid)
        ray.status = RayStatus.REMOVED
        return ray


foreground = ForegroundEngine()

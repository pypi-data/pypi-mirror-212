import logging
import threading
import traceback
from time import sleep
from typing import Any, List

from openfabric_pysdk.context import Ray, RaySchema
from openfabric_pysdk.task import Task
from openfabric_pysdk.app import App
from .foreground_engine import foreground


#######################################################
#  Background Engine
#######################################################
class BackgroundEngine:
    __task: Task = None
    __instances: int = 0
    __running: bool = False
    __current_qid: str = None
    __worker: threading.Thread = None
    __lock: threading.Condition = threading.Condition()

    # ------------------------------------------------------------------------
    def __init__(self):
        self.__lock.acquire()
        if self.__instances == 0:
            self.__task = Task()
            self.__worker = threading.Thread(target=self.__process, args=())
            self.__worker.start()

        self.__instances = self.__instances + 1
        self.__lock.release()

        # Wait for processing thread to start
        while not self.__running:
            sleep(0.1)

    # ------------------------------------------------------------------------
    def __del__(self):
        self.__lock.acquire()
        if self.__instances > 0:
            self.__lock.release()
            return

        self.__running = False

        self.__lock.notify_all()
        self.__lock.release()

    # ------------------------------------------------------------------------
    def __process(self):
        self.__running = True
        while self.__running:
            self.__lock.acquire()
            self.__current_qid = None
            while self.__running and self.__task.empty():
                self.__lock.wait()
            try:
                self.__current_qid = self.__task.next()
            except:
                logging.warning("Openfabric - queue empty!")
                traceback.print_exc()
            finally:
                self.__lock.release()

            if self.__running and self.__current_qid is not None:
                foreground.process(self.__current_qid)

    # ------------------------------------------------------------------------
    def prepare(self, app: App, data: str, qid=None, sid=None, uid=None, rid=None) -> str:
        self.__lock.acquire()
        qid: str = foreground.prepare(app, data, qid=qid, sid=sid, uid=uid, rid=rid)
        self.__task.add(qid)
        self.__lock.notify_all()
        self.__lock.release()
        return qid

    # ------------------------------------------------------------------------
    def ray(self, qid: str) -> Ray:
        return foreground.ray(qid)

    # ------------------------------------------------------------------------
    def rays(self, criteria=None) -> List[str]:
        rays: List[str] = []
        for qid in self.__task.all():
            ray = foreground.read(qid, 'ray', RaySchema().load)
            if ray is None:
                continue
            if criteria is None or criteria(ray):
                rays.append(ray)
        rays.sort(key=lambda r: r.created_at)
        return rays

    # ------------------------------------------------------------------------
    def delete(self, qid: str) -> Ray:
        self.__lock.acquire()
        self.__task.rem(qid)
        ray = foreground.delete(qid)
        self.__lock.notify_all()
        self.__lock.release()
        return ray

    # ------------------------------------------------------------------------
    def read(self, qid: str, key: str, deserializer=None) -> Any:
        return foreground.read(qid, key, deserializer)

    # ------------------------------------------------------------------------
    def write(self, qid: str, key: str, val: Any, serializer=None):
        return foreground.write(qid, key, val, serializer)


background = BackgroundEngine()

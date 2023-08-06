from datetime import datetime
from enum import Enum
from typing import Dict, Set

from tqdm.asyncio import tqdm, tqdm_asyncio

from .bar import Bar
from .message import Message, MessageType


#######################################################
#  Ray Status
#######################################################
class RayStatus(Enum):
    QUEUED = 'queued',
    PENDING = 'pending',
    COMPLETED = 'completed',
    RUNNING = 'running',
    CANCELED = 'canceled',
    REMOVED = 'removed',
    UNKNOWN = 'unknown',
    FAILED = 'failed'

    # ------------------------------------------------------------------------
    def __str__(self):
        return self.name


#######################################################
#  Ray
#######################################################
class Ray:
    uid: str = None
    sid: str = None
    qid: str = None
    rid: str = None
    finished: bool = None
    bars: Dict[str, Bar] = None
    status: RayStatus = None
    created_at: datetime = None
    updated_at: datetime = None
    messages: Set[Message] = None
    __tqdms: Dict[str, tqdm_asyncio] = None

    # ------------------------------------------------------------------------
    def __init__(self, qid):
        self.__tqdms = dict()
        self.qid = qid
        self.bars = dict(default=Bar())
        self.finished = False
        self.status = RayStatus.UNKNOWN
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
        self.messages = set()

    # ------------------------------------------------------------------------
    def update(self, other):
        for name, value in vars(other).items():
            if name in ["qid", "sid", "uid", "rid"]:
                continue
            setattr(self, name, value)

    # ------------------------------------------------------------------------
    def complete(self, name='default'):
        self.finished = True
        bar = self.bars.get(name, Bar())
        self.bars[name] = bar
        bar.remaining = 0
        bar.percent = 100

    # ------------------------------------------------------------------------
    def progress(self, name='default', step=1, total=100) -> tqdm_asyncio:
        if self.__tqdms.get(name) is None:
            self.__tqdms[name] = tqdm(total=total)
        tqdm_bar = self.__tqdms[name]
        # --
        bar = self.bars.get(name, Bar())
        self.bars[name] = bar
        f_dict = tqdm_bar.format_dict
        rate = f_dict.get("rate")
        total = tqdm_bar.total
        n = tqdm_bar.n
        remaining = (total - n) / rate if rate and total else 0
        bar.remaining = max(0, remaining)
        bar.percent = n
        # --
        tqdm_bar.update(step)
        return tqdm_bar

    # ------------------------------------------------------------------------
    def message(self, message_type: MessageType, content: str):
        message = Message()
        message.type = message_type
        message.content = content
        self.messages.add(message)

    # ------------------------------------------------------------------------
    def clear_messages(self):
        self.messages.clear()

    # ------------------------------------------------------------------------
    def tqdms(self):
        return self.__tqdms

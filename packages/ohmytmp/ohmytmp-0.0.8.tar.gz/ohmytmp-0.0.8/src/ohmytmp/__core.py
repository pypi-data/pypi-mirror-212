import os
import json
from copy import deepcopy as dcp
from typing import Callable

from .__constant import EVENT, Info
from .__plugin import PluginBase
from .__predict import predict


class Ohmytmp:
    def __init__(self, sv: str = None) -> None:
        self.func = {i: list() for i in EVENT.to_dict().values()}
        self.reg_f(predict, EVENT.GUESSTYPE)
        if sv:
            self.sv = os.path.abspath(os.path.expanduser(sv))
            self.reg_f(self.__save)

    def __save(self, info: Info) -> None:
        open(self.sv, 'a').write(
            json.dumps(info.to_dict(), skipkeys=True) + '\n'
        )

    def register(self, a: PluginBase) -> None:
        try:
            event = a.event
        except AttributeError:
            event = EVENT.AFTER
        if event is None:
            event = EVENT.AFTER

        try:
            level = a.level
        except AttributeError:
            level = -1

        self.reg_f(a.func, event, level)

    def reg_f(self, func: Callable, event: str = EVENT.AFTER, level: int = -1) -> None:
        if level == -1:
            self.func[event].append(func)
            return
        if level < 0:
            level += 1
        self.func[event] = self.func[event][:level] + \
            [func,] + self.func[event][level:]

    def reg_handle(self, event: str = EVENT.AFTER, level: int = -1) -> Callable:
        def __get_f(f: Callable) -> Callable:
            def __new_f(*args, **kwds):
                return f(*args, **kwds)
            self.reg_f(__new_f, event, level)
            return __new_f
        return __get_f

    def __event(self, info: Info) -> Info:
        for i in sorted(self.func):
            if i < EVENT.AFTER:
                for j in self.func[i]:
                    j(info)
            else:
                for j in self.func[i]:
                    j(dcp(info))
        return info

    def init_file(self, src: str = None, j: dict = None) -> Info:
        info = Info(src, j)
        return self.__event(info)

    def walk(self, d: str):
        for p, _, f in os.walk(d):
            for i in f:
                self.init_file(src=os.path.join(p, i))

    def load(self, ld: str) -> None:
        with open(os.path.abspath(os.path.expanduser(ld)), 'r') as f:
            line = f.readline()
            while line:
                self.init_file(j=json.loads(line))
                line = f.readline()


__all__ = ('Ohmytmp',)

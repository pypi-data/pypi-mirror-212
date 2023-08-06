import os

from .__constant import Info, EVENT, TYPE


class PluginBase:
    def __init__(self, event: int = None, level: int = -1) -> None:
        self.event = event
        self.level = level

    def func(self, info: Info) -> None:
        pass


class PluginPredictType(PluginBase):
    def __init__(self, level: int = -1) -> None:
        super().__init__(EVENT.GUESSTYPE, level)

    def predict(self, info: Info) -> str:
        return TYPE.UNKNOWN

    def func(self, info: Info) -> None:
        info.TYPE = self.predict(info)


class PluginAnalysis(PluginBase):
    def __init__(self, level: int = -1) -> None:
        super().__init__(EVENT.ANALYSIS, level)

    def func(self, info: Info) -> None:
        pass


class PluginAddTags(PluginBase):
    def __init__(self, level: int = -1) -> None:
        super().__init__(EVENT.ADDTAGS, level)

    def get_tags(self, info: Info) -> set:
        return set()

    def func(self, info: Info) -> None:
        info.TAGS.extend(self.get_tags(info))


class PluginDestination(PluginBase):
    def __init__(self, dst: str, level: int = -1) -> None:
        super().__init__(EVENT.DESTINATION, level)
        self.dst = os.path.abspath(os.path.expanduser(dst))
        self.flag = False

    def start(self) -> None:
        if not self.flag:
            self.mkdirs()
            self.flag = True

    def join(self, *paths) -> str:
        return os.path.abspath(os.path.join(self.dst, *paths))

    def mkdir(self, path: str) -> None:
        if os.path.exists(path):
            if not os.path.isdir(path):
                raise FileExistsError(path)
        else:
            os.makedirs(path)

    def mkdirs(self) -> None:
        self.mkdir(self.dst)

    def get_dst(self, info: Info) -> str:
        return self.dst

    def func(self, info: Info) -> None:
        info.DST = self.get_dst(info)


class PluginAfter(PluginBase):
    def __init__(self, level: int = -1) -> None:
        super().__init__(EVENT.AFTER, level)

    def func(self, _info: Info) -> None:
        pass


__all__ = ('PluginBase', 'PluginPredictType', 'PluginAnalysis',
           'PluginAddTags', 'PluginDestination', 'PluginAfter')

import os


CONSTCHAR = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_'
CONSTCHAR0 = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ_'


def is_const(v: str) -> bool:
    return 0 < len(v) < 255 and v[0] in CONSTCHAR0 and all([i in CONSTCHAR for i in v[1:]])


class Const:
    def __init__(self) -> None:
        pass

    def to_dict(self) -> dict:
        ans = dict()
        for i in dir(self):
            if is_const(i):
                ans[i] = eval('self.%s' % i)
        return ans


class __event(Const):
    def __init__(self) -> None:
        super().__init__()
        self.GUESSTYPE = 0x08
        self.ANALYSIS = 0x18
        self.ADDTAGS = 0x28
        self.DESTINATION = 0x38
        self.AFTER = 0x48


EVENT = __event()


class __type(Const):
    def __init__(self) -> None:
        super().__init__()
        self.UNKNOWN = 'unknown'
        self.ARCHIVE = 'archive'
        self.VIDEO = 'video'
        self.AUDIO = 'audio'
        self.IMAGE = 'image'
        self.GIF = 'image/gif'
        self.SVG = 'image/svg'
        self.OFFICE = 'office'
        self.EXECUTABLE = 'executable'
        self.TEXT = 'text'
        self.CONFIG = 'text/config'
        self.CODE = 'text/code'


TYPE = __type()


class Info(Const):
    def __init__(self, src: str = None, j: dict = None) -> None:
        super().__init__()
        if not src and not j:
            raise ValueError(src, j)

        if src:
            self.SRC = os.path.abspath(os.path.expanduser(src))
        else:
            self.SRC = j['SRC']

        self.TYPE = TYPE.UNKNOWN
        self.TAGS = list()

        self.ID = None
        self.MD5 = None
        self.SHA256 = None
        self.DST = None

        if j:
            for i in j:
                if is_const(i):
                    exec('self.%s = j["%s"]' % (i, i))

        self.BASE = os.path.basename(self.SRC)
        self.EXT = os.path.splitext(self.BASE)[1][1:]

    def to_tagset(self, addlist: tuple = ('EXT', 'TYPE')) -> set:
        ans = set(self.TAGS)
        d = self.to_dict()
        for i in addlist:
            if i in d and isinstance(d[i], str):
                ans.add('%s_%s' % (i, d[i]))
        return ans


__all__ = ('EVENT', 'TYPE', 'Info')

from Entity.EnumMagSize import EnumMagSize


class Mag:
    def __init__(self, title: str, counts: int, penality: bool, resize: bool, fastLoad: bool, ids:[]):
        self._title: EnumMagSize = EnumMagSize.from_value(title)
        self._counts: int = counts
        self._penality: bool = penality
        self._resize: bool = resize
        self._fastLoad: bool = fastLoad
        self._ids: [] = ids

    @property
    def title(self) -> str:
        return self._title.value

    @property
    def counts(self) -> int:
        return self._counts

    @property
    def penality(self) -> bool:
        return self._penality

    @property
    def resize(self) -> bool:
        return self._resize

    @property
    def ids(self) -> []:
        return self._ids

    @property
    def fastLoad(self) -> []:
        return self._fastLoad

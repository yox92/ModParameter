class Buff:
    def __init__(self, **buff):
        self._absolute_value = buff.get("AbsoluteValue", None)
        self._buff_type = buff.get("BuffType", None)
        self._chance = buff.get("Chance", None)
        self._delay = buff.get("Delay", None)
        self._duration = buff.get("Duration", None)
        self._skill_name = buff.get("SkillName", None)
        self._value = buff.get("Value", None)
        self._change = buff.get("change", None)
        self._add = buff.get("add", None)

    @property
    def absolute_value(self) -> bool:
        return self._absolute_value

    @property
    def buff_type(self) -> str:
        return self._buff_type

    @property
    def chance(self) -> float:
        return self._chance

    @property
    def delay(self) -> float:
        return self._delay

    @property
    def duration(self) -> float:
        return self._duration

    @property
    def skill_name(self) -> str:
        return self._skill_name

    @property
    def value(self) -> float:
        return self._value

    @property
    def change(self) -> bool:
        return self._change

    @property
    def add(self) -> bool:
        return self._add

    @classmethod
    def from_data(cls, data: dict):
        return cls(**data)

    def __iter__(self):
        return (key for key in self.__dict__.keys())

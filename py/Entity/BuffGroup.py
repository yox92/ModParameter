from Entity.Buff import Buff
from Entity.EnumBuff import EnumBuff
from typing import List


class BuffGroup:
    def __init__(self, name: EnumBuff, buffs: List[Buff]):
        self._name = name
        self._buffs = buffs

    @property
    def name(self) -> EnumBuff:
        return self._name

    @property
    def buffs(self) -> List[Buff]:
        return self._buffs

    def find_buff(self, buff_type: str, skill_name: str) -> Buff | None:
        for buff in self._buffs:
            if buff.buff_type == buff_type and buff.skill_name == skill_name:
                return buff
        return None

    @staticmethod
    def get_all_buffs(buff_groups: list["BuffGroup"]):
        return [buff for group in buff_groups for buff in group.buffs]

    @classmethod
    def from_data(cls, name: str, buffs_data: list[dict]):
        buffs = [Buff.from_data(b) for b in buffs_data]
        return cls(name=EnumBuff(name), buffs=buffs)

    def __repr__(self):
        return f"<BuffGroup {self.name.value} ({len(self.buffs)} buffs)>"

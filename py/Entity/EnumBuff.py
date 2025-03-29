from enum import Enum

class EnumBuff(str, Enum):
    BuffsAdrenaline = "BuffsAdrenaline"
    BuffsGoldenStarBalm = "BuffsGoldenStarBalm"
    BuffsPropital = "BuffsPropital"
    BuffsSJ1TGLabs = "BuffsSJ1TGLabs"
    BuffsSJ6TGLabs = "BuffsSJ6TGLabs"
    BuffsZagustin = "BuffsZagustin"
    Buffs_2A2bTG = "Buffs_2A2bTG"
    Buffs_3bTG = "Buffs_3bTG"
    Buffs_AHF1M = "Buffs_AHF1M"
    Buffs_Antidote = "Buffs_Antidote"
    Buffs_KultistsToxin = "Buffs_KultistsToxin"
    Buffs_L1 = "Buffs_L1"
    Buffs_MULE = "Buffs_MULE"
    Buffs_Meldonin = "Buffs_Meldonin"
    Buffs_Obdolbos = "Buffs_Obdolbos"
    Buffs_Obdolbos2 = "Buffs_Obdolbos2"
    Buffs_P22 = "Buffs_P22"
    Buffs_PNB = "Buffs_PNB"
    Buffs_Perfotoran = "Buffs_Perfotoran"
    Buffs_SJ12_TGLabs = "Buffs_SJ12_TGLabs"
    Buffs_Trimadol = "Buffs_Trimadol"

    @property
    def label(self) -> str:
        return self.value

    @classmethod
    def count(cls) -> int:
        return len(cls)

    @classmethod
    def enumerate_buffs(cls):
        return list(cls)

    @classmethod
    def enumerate_labels(cls) -> list[tuple[str, str]]:
        return [
            (member.value, member.value.replace("Buffs_", "").replace("Buffs", "").replace("TGLabs", ""))
            for member in cls
        ]
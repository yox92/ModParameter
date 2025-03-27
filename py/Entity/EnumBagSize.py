from enum import Enum

class EnumBagSize(Enum):
    CAT_S = "1-18"
    CAT_M1 = "19-24"
    CAT_M2 = "25-30"
    CAT_L = "31-36"
    CAT_XL = "37-48"

    @classmethod
    def list_values(cls):
        return [member.value for member in cls]

    @classmethod
    def from_value(cls, value: str):
        for member in cls:
            if member.value == value:
                return member
        raise ValueError(f"{value} n'est pas une valeur valide pour EnumBackpackSize")

from enum import Enum

class EnumMagSize(Enum):
    CAT_01_09 = "01–09"
    CAT_10_19 = "10–19"
    CAT_20_29 = "20–29"
    CAT_30_39 = "30–39"
    CAT_40_49 = "40–49"
    CAT_50_59 = "50–59"
    CAT_60_69 = "60–69"
    CAT_70_79 = "70–79"
    CAT_80_89 = "80–89"
    CAT_90_100 = "90–100"
    CAT_GT_100 = ">100"

    @classmethod
    def list_values(cls):
        return [member.value for member in cls]
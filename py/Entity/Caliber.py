from enum import Enum


class Caliber(Enum):
    MAKAROV_9x18 = "9x18mm Makarov", "Caliber9x18PM", "pistol"
    PARABELLUM_9x19 = "9x19mm Para", "Caliber9x19PARA", "pistol"
    GYURZA_9x21 = "9x21mm Gyurza", "Caliber9x21", "pistol"
    TT_762x25 = "762x25mm TT", "Caliber762x25TT", "pistol"
    ACP_45 = ".45 ACP", "Caliber1143x23ACP", "pistol"
    ACTION_EXPRESS_50 = ".50 AE", "Caliber127x33", "pistol"
    MAGNUM_357 = ".357 Magnum", "Caliber9x33R", "pistol"

    HK_46x30 = "4.6x30mm (mp7)", "Caliber46x30", "rifle"
    FN_57x28 = "5.7x28mm (p90)", "Caliber57x28", "rifle"
    RUSSIAN_545x39 = "5.45x39mm", "Caliber545x39", "rifle"
    NATO_556x45 = "5.56x45mm NATO", "Caliber556x45NATO", "rifle"
    BLACKOUT_300 = ".300 Blackout", "Caliber762x35", "rifle"
    RUSSIAN_762x39 = "7.62x39mm", "Caliber762x39", "rifle"
    NATO_762x51 = "7.62x51mm NATO", "Caliber762x51", "rifle"
    MAGNUM_68x51 = "6.8x51mm (Spear)", "Caliber68x51", "rifle"

    RUSSIAN_9x39 = "9x39mm", "Caliber9x39", "heavy"
    RUSSIAN_762x54 = "7.62x54mmR", "Caliber762x54R", "heavy"
    RUSSIAN_127x55 = "12.7x55mm", "Caliber127x55", "heavy"
    TKM_366 = ".366 TKM", "Caliber366TKM", "heavy"
    LAPUA_338_MAGNUM = ".338 Lapua", "Caliber86x70", "heavy"

    SHOTGUN_12_70 = "12x70mm", "Caliber12g", "explosive"
    SHOTGUN_23x75 = "23x75mm KS23", "Caliber23x75", "explosive"
    GRENADE_40x46 = "40x46mm HE + VOG", "Caliber40x46", "explosive"
    Caliber40mmRU = "VOG", "Caliber40mmRU", "explosive"
    UTYOS_AGS = "Utyos + AGS", "UTYOS_AGS", "explosive"

    @property
    def label(self):
        return self.value[0]

    @property
    def code(self):
        return self.value[1]

    @property
    def categorie(self):
        return self.value[2]

    @classmethod
    def count(cls):
        return len(cls)

    @classmethod
    def enumerate_calibers(cls):
        return [
            (caliber.label,
             caliber.code,
             caliber.categorie) for caliber in cls
        ]

    def to_tuple(self):
        return self.value


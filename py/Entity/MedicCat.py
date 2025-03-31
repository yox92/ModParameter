from enum import Enum


class MedicalCat(Enum):
    MEDKIT = "MedKit","5448f39d4bdc2d0a728b4568"
    DRUGS = "Drugs","5448f3a14bdc2d27728b4569"
    STIMULATOR = "Stimulator" ,"5448f3a64bdc2d60728b456a",
    MEDICAL = "Medical" ,"5448f3ac4bdc2dce718b4569",
    BUFF = "Buff" ,"",

    @property
    def label(self):
        return self.value[0]

    @property
    def code(self):
        return self.value[1]

    @classmethod
    def count(cls):
        return len(cls)

    @classmethod
    def enumerate_medical(cls):
        return [
            (medic.label,
             medic.code) for medic in cls
        ]

    def to_tuple(self):
        return self.value


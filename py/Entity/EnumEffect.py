from enum import Enum

class EnumEffect(Enum):
    DURATION = ("duration","Duration of the effect (seconds) (0, 2000) ")
    FADEOUT = ("fadeOut","Time it takes for the debuff to fade out \n(seconds) (0-100)")
    COST = ("cost","Resource cost to remove the effect \n (e.g., stop bleeding with a Salewa) (0-250)")
    HEALTHPENALTYMIN = ("healthPenaltyMin","Minimum % of health removed \n from the treated body part (0-100)")
    HEALTHPENALTYMAX = ("healthPenaltyMax","Maximum percentage of health removed \n from the treated body part (1-99)")

    @property
    def label(self):
        return self.value[0]

    @property
    def code(self):
        return self.value[1]

    @classmethod
    def get_code_by_label(cls, label):
        for prop in cls:
            if prop.label == label:
                return prop.code
        raise ValueError(f"Aucun 'code' trouvé pour le label : {label}")

    @classmethod
    def get_label_by_code(cls, code):
        for prop in cls:
            if prop.code == code:
                return prop.label
        raise ValueError(f"Aucun 'code' trouvé pour le label : {code}")

    def __str__(self):
        return f"{self.label} ({self.code})"

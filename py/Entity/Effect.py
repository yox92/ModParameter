class Effect:
    def __init__(self,
                 delay=None,
                 duration=None,
                 fadeOut=None,
                 cost=None,
                 healthPenaltyMin=None,
                 healthPenaltyMax=None):
        self.delay = delay
        self.duration = duration
        self.fadeOut = fadeOut
        self.cost = cost
        self.healthPenaltyMin = healthPenaltyMin
        self.healthPenaltyMax = healthPenaltyMax

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            delay=data.get("delay"),
            duration=data.get("duration"),
            fadeOut=data.get("fadeOut"),
            cost=data.get("cost"),
            healthPenaltyMin=data.get("healthPenaltyMin"),
            healthPenaltyMax=data.get("healthPenaltyMax")
        )

    def __repr__(self):
        return f"Effect(delay={self.delay}, duration={self.duration}, fadeOut={self.fadeOut}, cost={self.cost}, healthPenaltyMin={self.healthPenaltyMin}, healthPenaltyMax={self.healthPenaltyMax})"

    def __eq__(self, other):
        if not isinstance(other, Effect):
            return False
        return vars(self) == vars(other)
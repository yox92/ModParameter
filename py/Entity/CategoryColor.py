from enum import Enum

class CategoryColor(Enum):
    PISTOL = "dodgerblue"
    RIFLE = "peru"
    HEAVY = "mediumseagreen"
    EXPLOSIVE = "khaki"
    NERF = "FireBrick"

    @classmethod
    def get(cls, category: str):
        return cls.__members__.get(category.upper(), cls.NERF).value


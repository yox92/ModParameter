
class Locale:
    def __init__(self, name: str = None, short_name: str = None):
        self.Name = name
        self.ShortName = short_name

    @property
    def name(self) -> str:
        return self.Name

    @name.setter
    def name(self, name: str):
        self.Name = name

    @property
    def short_name(self) -> str:
        return self.ShortName

    @short_name.setter
    def short_name(self, short_name: str):
        self.ShortName = short_name

    @classmethod
    def from_data(cls, data: dict):
        return Locale(
            name=data.get("Name"),
            short_name=data.get("ShortName")
        )

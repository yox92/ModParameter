class Locale:
    def __init__(self, name: str = None, short_name: str = None):
        self.Name = name
        self.ShortName = short_name

    def get_name(self) -> str:
        return self.Name

    def set_name(self, name: str):
        self.Name = name

    def get_short_name(self) -> str:
        return self.ShortName

    def set_short_name(self, short_name: str):
        self.ShortName = short_name

    @classmethod
    def from_data(cls, data: dict):
        return Locale(
            name=data.get("Name"),
            short_name=data.get("ShortName")
        )

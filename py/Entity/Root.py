from Entity import Locale, Item


class Root:
    def __init__(self, locale: Locale, item: Item):
        self.Locale = locale
        self.Item = item

    @property
    def locale(self) -> Locale:
        return self.Locale

    @property
    def item(self) -> Item:
        return self.Item

    @staticmethod
    def from_data(data: dict):
        return Root(
            locale=Locale.from_data(data.get("locale", {})),
            item=Item.from_data(data.get("item", {}))
        )

    def __repr__(self):
        return f"Root(locale={self.locale}, item={self.item})"

from CustomWeapon.py.Entity.Item import Item
from CustomWeapon.py.Entity.Locale import Locale


class Root:
    def __init__(self, locale: Locale, item: Item):
        self.locale = locale
        self.item = item

    def get_locale(self) -> Locale:
        return self.locale

    def set_locale(self, locale: Locale):
        self.locale = locale

    def get_item(self) -> Item:
        return self.item

    def set_item(self, item: Item):
        self.item = item

    @staticmethod
    def from_data(data: dict):
        return Root(
            locale=Locale.from_data(data.get("locale", {})),
            item=Item.from_data(data.get("item", {}))
        )

    def __repr__(self):
        return f"Root(locale={self.locale}, item={self.item})"


from Entity.Locale import Locale
from Entity.Item import Item
from Entity.WindowType import WindowType


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
    def from_data(data: dict, wt):
        if wt == WindowType.WEAPON:
            return Root(
                locale=Locale.from_data(data.get("locale", {})),
                item=Item.from_data_weapon(data.get("item", {})))
        elif wt == WindowType.AMMO:
            return Root(
                locale=Locale.from_data(data.get("locale", {})),
                item=Item.from_data_ammo(data.get("item", {})))
        elif wt == WindowType.MEDIC:
            return Root(
                locale=Locale.from_data(data.get("locale", {})),
                item=Item.from_data_medic(data.get("item", {})))

    def __repr__(self):
        return f"Root(locale={self.locale}, item={self.item})"

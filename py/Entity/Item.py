from CustomWeapon.py.Entity.ItemProps import ItemProps


class Item:
    def __init__(self, id: str, name: str, props: ItemProps = None):
        self._id = id
        self._name = name
        self._props = props

    def get_id(self) -> str:
        return self._id

    def set_id(self, id: str):
        self._id = id

    def get_name(self) -> str:
        return self._name

    def set_name(self, name: str):
        self._name = name

    def get_props(self) -> ItemProps:
        return self._props

    def set_props(self, props: ItemProps):
        self._props = props

    @staticmethod
    def from_data(data: dict):
        return Item(
            id=data.get("_id"),
            name=data.get("_name"),
            props=ItemProps.from_data(data.get("_props", {}))
        )

    def __repr__(self):
        return f"Item(_id={self._id}, _name={self._name}, _props={self._props})"


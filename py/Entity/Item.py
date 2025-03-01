from py.Entity.ItemProps import ItemProps


class Item:
    def __init__(self, id: str, name: str, props: ItemProps = None):
        self._id = id
        self._name = name
        self._props = props

    @property
    def id(self) -> str:
        return self._id

    @id.setter
    def id(self, id: str):
        self._id = id

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, name: str):
        self._name = name

    @property
    def props(self) -> ItemProps:
        return self._props

    @props.setter
    def props(self, props: ItemProps):
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

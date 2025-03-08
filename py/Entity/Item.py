from typing import Union

from Entity.Ammo import Ammo
from Entity.ItemProps import ItemProps

class Item:
    def __init__(self, id: str, name: str, props: Union[ItemProps, Ammo]):
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
    def props(self) -> Union[ItemProps, Ammo]:
        return self._props

    @props.setter
    def props(self, props: Union[ItemProps, Ammo]):
        if not isinstance(props, (ItemProps, Ammo)):
            raise ValueError("props must be an instance of ItemProps or Ammo")
        self._props = props

    @staticmethod
    def from_data_weapon(data: dict):
        return Item(
            id=data.get("_id"),
            name=data.get("_name"),
            props=ItemProps.from_data(data.get("_props", {}))
        )

    @staticmethod
    def from_data_ammo(data: dict):
        return Item(
            id=data.get("_id"),
            name=data.get("_name"),
            props=Ammo.from_data(data.get("_props", {}))
        )

    def __repr__(self):
        return f"Item(_id={self._id}, _name={self._name}, _props={self._props})"

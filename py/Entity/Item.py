from typing import Union

from Entity.Ammo import Ammo
from Entity.ItemProps import ItemProps
from Entity.Medic import Medic


class Item:
    def __init__(self, id: str, name: str, parent: str, props: Union[ItemProps, Ammo]):
        self._id = id
        self._name = name
        self._parent = parent
        self._props = props

    @property
    def id(self) -> str:
        return self._id

    @id.setter
    def id(self, id: str):
        self._id = id

    @property
    def parent(self) -> str:
        return self._parent


    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, name: str):
        self._name = name

    @name.setter
    def name(self, parent: str):
        self._parent = parent

    @property
    def props(self) -> Union[ItemProps, Ammo, Medic]:
        return self._props

    @props.setter
    def props(self, props: Union[ItemProps, Ammo, Medic]):
        if not isinstance(props, (ItemProps, Ammo, Medic)):
            raise ValueError("props must be an instance of ItemProps, Ammo or Medic")
        self._props = props

    @staticmethod
    def from_data_weapon(data: dict):
        return Item(
            id=data.get("_id"),
            name=data.get("_name"),
            parent=data.get("_parent"),
            props=ItemProps.from_data(data.get("_props", {}))
        )

    @staticmethod
    def from_data_ammo(data: dict):
        return Item(
            id=data.get("_id"),
            name=data.get("_name"),
            parent=data.get("_parent"),
            props=Ammo.from_data(data.get("_props", {}))
        )

    @staticmethod
    def from_data_medic(data: dict):
        return Item(
            id=data.get("_id"),
            name=data.get("_name"),
            parent=data.get("_parent"),
            props=Medic.from_data(data.get("_props", {}))
        )

    def __repr__(self):
        return f"Item(_id={self._id}, _name={self._name}, _props={self._props})"

from enum import Enum
from typing import Union, Iterable, Optional, Any

from dt_maps.types.commons import EntityHelper, FieldPath
from dt_maps.types.frames import Frame

COLOR = "color"


class CitizenType(Enum):
    YELLOW = "yellow"
    RED = "red"
    GREEN = "green"
    GRAY = "grey"


class Citizen(EntityHelper):

    def _get_property_values(self, name: str) -> Optional[Iterable[Any]]:
        return {
            COLOR: [w.value for w in CitizenType]
        }[name]

    def _get_property_types(self, name: str) -> Union[type, Iterable[type]]:
        return {
            COLOR: str
        }[name]

    def _get_layer_name(self) -> str:
        return "citizens"

    def _set_property(self, name: FieldPath, types: Union[type, Iterable[type]], value: Any):
        # CitizenType -> str
        if name == COLOR and isinstance(value, CitizenType):
            value = value.value
        # ---
        super(Citizen, self)._set_property(name, types, value)

    def _get_property(self, name: FieldPath) -> Any:
        value = super(Citizen, self)._get_property(name)
        # str -> CitizenType
        if name == COLOR:
            value = CitizenType(value)
        # ---
        return value

    @property
    def frame(self) -> Frame:
        return Frame.create(self._map, self._key)

    @property
    def color(self) -> CitizenType:
        return CitizenType(self._get_property(COLOR))

    @color.setter
    def color(self, value: Union[str, CitizenType]):
        self._set_property(COLOR, str, value)

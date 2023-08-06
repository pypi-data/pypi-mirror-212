from enum import Enum
from typing import Union, Iterable, Optional, Any

from dt_maps.types.commons import EntityHelper, FieldPath
from dt_maps.types.frames import Frame

CONFIGURATION = "configuration"
ID = "id"
COLOR = "color"


class ColorType(Enum):
    BLUE = "blue"
    RED = "red"
    GREEN = "green"
    GRAY = "grey"


class VehicleType(Enum):
    # duckiebot
    DB18: str = "DB18"
    DB19: str = "DB19"
    DB21M: str = "DB21M"
    DB21J: str = "DB21J"
    DBR4: str = "DBR4"
    # duckiedrone
    DD18: str = "DD18"
    DD21: str = "DD21"


class Vehicle(EntityHelper):

    def _get_property_values(self, name: str) -> Optional[Iterable[Any]]:
        return {
            CONFIGURATION: [w.value for w in VehicleType],
            ID: None,
            COLOR: [w.value for w in ColorType]
        }[name]

    def _get_property_types(self, name: str) -> Union[type, Iterable[type]]:
        return {
            CONFIGURATION: str,
            ID: (type(None), str),
            COLOR: str
        }[name]

    def _get_layer_name(self) -> str:
        return "vehicles"

    def _set_property(self, name: FieldPath, types: Union[type, Iterable[type]], value: Any):
        # VehicleType -> str or ColorType -> str
        if (name == CONFIGURATION and isinstance(value, VehicleType)) or \
                (name == COLOR and isinstance(value, ColorType)):
            value = value.value
        # ---
        super(Vehicle, self)._set_property(name, types, value)

    def _get_property(self, name: FieldPath) -> Any:
        value = super(Vehicle, self)._get_property(name)
        # str -> VehicleType
        if name == CONFIGURATION:
            value = VehicleType(value)
        # str -> ColorType
        if name == COLOR:
            value = ColorType(value)
        # ---
        return value

    @property
    def frame(self) -> Frame:
        return Frame.create(self._map, self._key)

    @property
    def configuration(self) -> VehicleType:
        return VehicleType(self._get_property(CONFIGURATION))

    @property
    def id(self) -> Optional[str]:
        return self._get_property(ID)

    @property
    def color(self) -> ColorType:
        return ColorType(self._get_property(COLOR))

    @configuration.setter
    def configuration(self, value: Union[str, VehicleType]):
        self._set_property(CONFIGURATION, str, value)

    @id.setter
    def id(self, value: Optional[str]):
        self._set_property(ID, (type(None), str), value)

    @color.setter
    def color(self, value: Union[str, ColorType]):
        self._set_property(COLOR, str, value)

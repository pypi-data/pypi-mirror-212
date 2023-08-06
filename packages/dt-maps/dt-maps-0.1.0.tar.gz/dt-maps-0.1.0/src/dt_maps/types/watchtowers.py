from enum import Enum
from typing import Union, Iterable, Optional, Any

from dt_maps.types.commons import EntityHelper, FieldPath
from dt_maps.types.frames import Frame

CONFIGURATION = "configuration"
ID = "id"


class WatchtowerType(Enum):
    WT18: str = "WT18"
    WT19: str = "WT19"


class Watchtower(EntityHelper):

    def _get_property_values(self, name: str) -> Optional[Iterable[Any]]:
        return {
            CONFIGURATION: [w.value for w in WatchtowerType],
            ID: None
        }[name]

    def _get_property_types(self, name: str) -> Union[type, Iterable[type]]:
        return {
            CONFIGURATION: str,
            ID: (type(None), str)
        }[name]

    def _get_layer_name(self) -> str:
        return "watchtowers"

    def _set_property(self, name: FieldPath, types: Union[type, Iterable[type]], value: Any):
        # WatchtowerType -> str
        if name == CONFIGURATION and isinstance(value, WatchtowerType):
            value = value.value
        # ---
        super(Watchtower, self)._set_property(name, types, value)

    def _get_property(self, name: FieldPath) -> Any:
        value = super(Watchtower, self)._get_property(name)
        # str -> WatchtowerType
        if name == CONFIGURATION:
            value = WatchtowerType(value)
        # ---
        return value

    @property
    def frame(self) -> Frame:
        return Frame.create(self._map, self._key)

    @property
    def configuration(self) -> WatchtowerType:
        return WatchtowerType(self._get_property(CONFIGURATION))

    @property
    def id(self) -> Optional[str]:
        return self._get_property(ID)

    @configuration.setter
    def configuration(self, value: Union[str, WatchtowerType]):
        self._set_property(CONFIGURATION, str, value)

    @id.setter
    def id(self, value: Optional[str]):
        self._set_property(ID, (type(None), str), value)

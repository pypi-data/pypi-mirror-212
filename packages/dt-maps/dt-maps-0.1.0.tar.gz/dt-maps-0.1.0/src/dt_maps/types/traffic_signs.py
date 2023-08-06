from enum import Enum
from typing import Union, Iterable, Optional, Any

from dt_maps.types.commons import EntityHelper, FieldPath
from dt_maps.types.frames import Frame

TYPE = "type"
ID = "id"
FAMILY = "family"


class TrafficSignType(Enum):
    FOUR_WAY_INTERSECT = "four_way_intersect"
    DO_NOT_ENTER = "do_not_enter"
    DUCK_CROSSING = "duck_crossing"
    LEFT_T_INTERSECT = "left_t_intersect"
    NO_LEFT_TURN = "no_left_turn"
    NO_RIGHT_TURN = "no_right_turn"
    ONEWAY_LEFT = "oneway_left"
    ONEWAY_RIGHT = "oneway_right"
    PARKING = "parking"
    PEDESTRIAN = "pedestrian"
    RIGHT_T_INTERSECT = "right_t_intersect"
    STOP = "stop"
    T_INTERSECTION = "t_intersection"
    T_LIGHT_AHEAD = "t_light_ahead"
    YIELD = "yield"


class TrafficSign(EntityHelper):

    def _get_property_values(self, name: str) -> Optional[Iterable[Any]]:
        return {
            TYPE: [w.value for w in TrafficSignType],
            ID: None,
            FAMILY: None
        }[name]

    def _get_property_types(self, name: str) -> Union[type, Iterable[type]]:
        return {
            TYPE: str,
            ID: int,
            FAMILY: str
        }[name]

    def _get_layer_name(self) -> str:
        return "traffic_signs"

    def _set_property(self, name: FieldPath, types: Union[type, Iterable[type]], value: Any):
        # TrafficSignType -> str
        if name == TYPE and isinstance(value, TrafficSignType):
            value = value.value
        # ---
        super(TrafficSign, self)._set_property(name, types, value)

    def _get_property(self, name: FieldPath) -> Any:
        value = super(TrafficSign, self)._get_property(name)
        # str -> TrafficSignType
        if name == TYPE:
            value = TrafficSignType(value)
        # ---
        return value

    @property
    def frame(self) -> Frame:
        return Frame.create(self._map, self._key)

    @property
    def type(self) -> TrafficSignType:
        return TrafficSignType(self._get_property(TYPE))

    @property
    def id(self) -> int:
        return self._get_property(ID)

    @property
    def family(self) -> str:
        return self._get_property(FAMILY)

    @type.setter
    def type(self, value: Union[str, TrafficSignType]):
        self._set_property(TYPE, str, value)

    @id.setter
    def id(self, value: int):
        self._set_property(ID, int, value)

    @family.setter
    def family(self, value: str):
        self._set_property(FAMILY, str, value)

from typing import Union, Iterable, Optional, Any

from dt_maps.types.commons import EntityHelper, FieldPath
from dt_maps.types.frames import Frame

SIZE = "size"
ID = "id"
FAMILY = "family"


class GroundTag(EntityHelper):

    def _get_property_values(self, name: str) -> Optional[Iterable[Any]]:
        return {
            SIZE: None,
            ID: None,
            FAMILY: None
        }[name]

    def _get_property_types(self, name: str) -> Union[type, Iterable[type]]:
        return {
            SIZE: float,
            ID: int,
            FAMILY: str
        }[name]

    def _get_layer_name(self) -> str:
        return "ground_tags"

    def _set_property(self, name: FieldPath, types: Union[type, Iterable[type]], value: Any):
        super(GroundTag, self)._set_property(name, types, value)

    def _get_property(self, name: FieldPath) -> Any:
        value = super(GroundTag, self)._get_property(name)
        return value

    @property
    def frame(self) -> Frame:
        return Frame.create(self._map, self._key)

    @property
    def size(self) -> float:
        return self._get_property(SIZE)

    @property
    def id(self) -> int:
        return self._get_property(ID)

    @property
    def family(self) -> str:
        return self._get_property(FAMILY)

    @size.setter
    def size(self, value: float):
        self._set_property(SIZE, float, value)

    @id.setter
    def id(self, value: int):
        self._set_property(ID, int, value)

    @family.setter
    def family(self, value: str):
        self._set_property(FAMILY, str, value)

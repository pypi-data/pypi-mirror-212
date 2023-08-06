from typing import Optional, Any, Union, Iterable

from dt_maps.exceptions import EntityNotFound
from dt_maps.types.commons import EntityHelper
from dt_maps.types.geometry import Pose3D


class Frame(EntityHelper):

    def _get_property_types(self, name: str) -> Union[type, Iterable[type]]:
        return {
            "pose": dict,
            "relative_to": str
        }[name]

    def _get_layer_name(self) -> str:
        return "frames"

    def _get_property_values(self, name: str) -> Optional[Iterable[Any]]:
        return {
            "pose": None,
            "relative_to": None
        }[name]

    @property
    def parent(self) -> 'Optional[Frame]':
        parts = self.key.split('/')[:-1]
        current = []
        parent = None
        for part in parts:
            current += [part]
            parent_key = '/'.join(current)
            try:
                parent = self._map.layers.frames[parent_key]
            except EntityNotFound:
                pass
        # ---
        return parent

    @property
    def pose(self) -> Pose3D:
        return Pose3D.create(self._map, self._key)

    @property
    def relative_to(self) -> Optional[str]:
        return self._get_property("relative_to")

    @relative_to.setter
    def relative_to(self, value: Optional[str]):
        self._set_property("relative_to", (str, None), value)

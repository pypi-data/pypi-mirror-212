from typing import Optional, Iterable, Any, Union

from dt_maps.types.commons import EntityHelper


class TileSize(EntityHelper):

    def _get_property_types(self, name: str) -> Union[type, Iterable[type]]:
        return {
            "x": float,
            "y": float,
        }[name]

    def _get_layer_name(self) -> str:
        return "tile_maps"

    def _get_property_values(self, name: str) -> Optional[Iterable[Any]]:
        return {
            "x": None,
            "y": None
        }[name]

    @property
    def x(self) -> float:
        return self._get_property(("tile_size", "x"))

    @property
    def y(self) -> float:
        return self._get_property(("tile_size", "y"))

    @x.setter
    def x(self, value: float):
        self._set_property(("tile_size", "x"), float, value)

    @y.setter
    def y(self, value: float):
        self._set_property(("tile_size", "y"), float, value)


class TileMap(EntityHelper):

    def _get_property_types(self, name: str) -> Union[type, Iterable[type]]:
        return {
            "tile_size": dict,
        }[name]

    def _get_layer_name(self) -> str:
        return "tile_maps"

    def _get_property_values(self, name: str) -> Optional[Iterable[Any]]:
        return {
            "tile_size": None,
        }[name]

    @property
    def tile_size(self) -> TileSize:
        return TileSize.create(self._map, self._key)

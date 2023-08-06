from typing import Optional, Iterable

import networkx as nx
import numpy as np

from dt_maps import Map
from dt_maps.exceptions import EntityNotFound
from dt_maps.graph.tiles import get_tile_graph
from dt_maps.graph.utils import densify_graph
from dt_maps.types.tile_maps import TileMap
from dt_maps.types.tiles import TileCoordinates, Tile
from dt_maps.utils.tiles import get_tile


def get_tile_map_graph(m: Map, tile_map: TileMap, subdivision_steps: int = 0) -> nx.DiGraph:
    # create empty graph
    G = nx.DiGraph()
    # populate graph
    for i, j in get_tile_map_tiles(m, tile_map.key):
        tile: Optional[Tile] = get_tile(m, i, j)
        if tile is None:
            raise EntityNotFound("tiles", i=i, j=j)
        # get tile graph
        tile_G = get_tile_graph(tile, tile_map)
        # move tile graph
        for _, node in tile_G.nodes.data():
            tx, ty, tz = node["position"]
            pose = tile.frame.pose
            node["position"] = [
                (tx * np.cos(pose.yaw) - ty * np.sin(pose.yaw)) + tile.frame.pose.x,
                (tx * np.sin(pose.yaw) + ty * np.cos(pose.yaw)) + tile.frame.pose.y,
                tz + tile.frame.pose.z,
            ]
        # add tile graph to tile_map graph
        G = nx.compose(G, tile_G)
    # subdivide graph
    densify_graph(G, subdivision_steps)
    # ---
    return G


def get_tile_map_tiles(m: Map, tile_map: str) -> Iterable[TileCoordinates]:
    for tile_key, tile in m.layers.tiles.items():
        if tile_key.startswith(tile_map):
            yield tile["i"], tile["j"]

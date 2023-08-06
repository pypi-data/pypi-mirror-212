from typing import Callable, Dict

import networkx as nx
import numpy as np

from dt_maps.constants import YELLOW_TAPE, CENTER_OF_LANE_NORMALIZED
from dt_maps.graph.utils import find_nodes, node_id, node_attributes
from dt_maps.types.tile_maps import TileSize, TileMap
from dt_maps.types.tiles import Tile, TileType


def _populate_tile_straight(g: nx.DiGraph, tile: Tile, tile_map: TileMap):
    tile_size: TileSize = tile_map.tile_size
    # get tapes and points of interest
    half_yellow = YELLOW_TAPE.width / 2.0
    distance_to_lane_center = half_yellow + CENTER_OF_LANE_NORMALIZED * tile_size.x
    half_tile = tile_size.x / 2.0
    # left lane (direction: north to south)
    left_top_id = node_id(tile.key, "left", "in")
    left_top = node_attributes(
        position=[-distance_to_lane_center, half_tile, 0.0],
        lane="left",
        direction="in",
        tile=tile,
        tile_map=tile_map
    )
    left_bottom_id = node_id(tile.key, "left", "out")
    left_bottom = node_attributes(
        position=[-distance_to_lane_center, -half_tile, 0.0],
        lane="left",
        direction="out",
        tile=tile,
        tile_map=tile_map
    )
    # right lane (direction: south to north)
    right_bottom_id = node_id(tile.key, "right", "in")
    right_bottom = node_attributes(
        position=[distance_to_lane_center, -half_tile, 0.0],
        lane="right",
        direction="in",
        tile=tile,
        tile_map=tile_map
    )
    right_top_id = node_id(tile.key, "right", "out")
    right_top = node_attributes(
        position=[distance_to_lane_center, half_tile, 0.0],
        lane="right",
        direction="out",
        tile=tile,
        tile_map=tile_map
    )
    # add nodes
    g.add_node(left_top_id, **left_top)
    g.add_node(left_bottom_id, **left_bottom)
    g.add_node(right_bottom_id, **right_bottom)
    g.add_node(right_top_id, **right_top)
    # add edges
    g.add_edge(left_top_id, left_bottom_id)
    g.add_edge(right_bottom_id, right_top_id)


# TODO: need to remove it
def _populate_tile_curve_right(g: nx.DiGraph, tile: Tile, tile_map: TileMap):
    _populate_tile_straight(g, tile, tile_map)
    # get 'left in' node, aka top-left node
    left_in_id = find_nodes(g, direction="in", lane="left")[0]
    left_in = g.nodes[left_in_id]
    # get 'right out' node, aka bottom-right node
    right_out_id = find_nodes(g, direction="out", lane="right")[0]
    right_out = g.nodes[right_out_id]
    # rotate nodes
    for node in [left_in, right_out]:
        tx, ty, tz = node["position"]
        node["position"] = [
            (tx * np.cos(np.deg2rad(-90)) - ty * np.sin(np.deg2rad(-90))),
            (tx * np.sin(np.deg2rad(-90)) + ty * np.cos(np.deg2rad(-90))),
            tz
        ]


# TODO: need to remove it
def _populate_tile_curve_left(g: nx.DiGraph, tile: Tile, tile_map: TileMap):
    _populate_tile_curve_right(g, tile, tile_map)
    # rotate nodes
    alpha = 180
    for _, node in g.nodes(data=True):
        tx, ty, tz = node["position"]
        node["position"] = [
            (tx * np.cos(np.deg2rad(alpha)) - ty * np.sin(np.deg2rad(alpha))),
            (tx * np.sin(np.deg2rad(alpha)) + ty * np.cos(np.deg2rad(alpha))),
            tz
        ]


def _populate_tile_3way(g: nx.DiGraph, tile: Tile, tile_map: TileMap):
    graphs = [
        (_populate_tile_straight, 0),
        (_populate_tile_curve_right, 0),
        (_populate_tile_curve_right, 90),
    ]
    # make graphs
    for populate, alpha in graphs:
        g1 = nx.DiGraph()
        populate(g1, tile, tile_map)
        # rotate nodes
        for _, node in g1.nodes(data=True):
            tx, ty, tz = node["position"]
            node["position"] = [
                (tx * np.cos(np.deg2rad(alpha)) - ty * np.sin(np.deg2rad(alpha))),
                (tx * np.sin(np.deg2rad(alpha)) + ty * np.cos(np.deg2rad(alpha))),
                tz
            ]
        # copy g1 into g
        g.add_edges_from(g1.edges(data=True))
        g.add_nodes_from(g1.nodes(data=True))


# It's the copy of fun "_populate_tile_curve_right"
def _populate_tile_curve(g: nx.DiGraph, tile: Tile, tile_map: TileMap):
    _populate_tile_straight(g, tile, tile_map)
    # get 'left in' node, aka top-left node
    left_in_id = find_nodes(g, direction="in", lane="left")[0]
    left_in = g.nodes[left_in_id]
    # get 'right out' node, aka bottom-right node
    right_out_id = find_nodes(g, direction="out", lane="right")[0]
    right_out = g.nodes[right_out_id]
    # rotate nodes
    for node in [left_in, right_out]:
        tx, ty, tz = node["position"]
        node["position"] = [
            (tx * np.cos(np.deg2rad(-90)) - ty * np.sin(np.deg2rad(-90))),
            (tx * np.sin(np.deg2rad(-90)) + ty * np.cos(np.deg2rad(-90))),
            tz
        ]


def _populate_tile_no_graph(_: nx.DiGraph, __: Tile, ___: TileMap):
    pass


tile_type_to_populate_fcn: Dict[TileType, Callable[[nx.DiGraph, Tile, TileMap], None]] = {
    TileType.STRAIGHT: _populate_tile_straight,
    TileType.CURVE: _populate_tile_curve,
    TileType.FLOOR: _populate_tile_no_graph,
    TileType.GRASS: _populate_tile_no_graph,
    TileType.ASPHALT: _populate_tile_no_graph,
    TileType.THREE_WAY: _populate_tile_3way
}


def get_tile_graph(tile: Tile, tile_map: TileMap) -> nx.DiGraph:
    # get tile
    tile_type = tile["type"]
    # create empty graph
    G = nx.DiGraph()
    # get function to populate the graph
    populate = tile_type_to_populate_fcn.get(tile_type, None)
    if populate is None:
        raise NotImplementedError("Function 'get_tile_graph' is not implemented for tile "
                                  f"of type {tile_type}")
    else:
        # populate graph
        populate(G, tile, tile_map)
    # ---
    return G

import os
import uuid
from typing import List, Optional

import networkx as nx
import numpy as np

from dt_maps.types.tile_maps import TileMap
from dt_maps.types.tiles import Tile, TileType


def node_id(tile_key: str, lane: str, *args) -> str:
    # TODO: fix this
    return str(uuid.uuid4())
    args = list(map(str, args))
    return os.path.join(tile_key, f"lane_{lane}", *args).replace("/", "__")


def node_attributes(tile: Tile, tile_map: TileMap, position: list, lane: str,
                    direction: Optional[str] = None) -> dict:
    return {
        "position": position,
        "lane": lane,
        "direction": direction,
        "tile": tile,
        "tile_map": tile_map
    }


def find_nodes(g: nx.DiGraph, **attrs):
    result: List[str] = []
    for node_id, node_data in g.nodes.data():
        bad: bool = False
        for k, v in attrs.items():
            if k not in node_data:
                bad = True
                break
            if node_data[k] != v:
                bad = True
                break
        if not bad:
            result.append(node_id)
    return result


def densify_graph(g: nx.DiGraph, steps: int):
    node_prefix = []
    for step in range(steps):
        node_prefix.append(step)
        edges = list(g.edges)
        for node_u_id, node_v_id in edges:
            # get nodes
            node_u = g.nodes[node_u_id]
            node_v = g.nodes[node_v_id]
            # get nodes' position
            ux, uy, uz = node_u["position"]
            vx, vy, vz = node_v["position"]
            tile_map, tile, lane = node_u["tile_map"], node_u["tile"], node_u["lane"]
            # direction of the bump as a function of the current lane
            lane_mirror = 0 if lane == "right" else 180
            # find angle of the bump
            yaw = np.arctan2(vy - uy, vx - ux) + np.deg2rad(lane_mirror)
            # direction of the bump
            dr = np.array([-np.sin(yaw), np.cos(yaw), 0])
            # distance between nodes
            d = np.linalg.norm([ux - vx, uy - vy, uz - vz]) / 2.0
            # apply a bump only to segments that are not straight
            bump_enabler = 0.0 if np.allclose([ux], [vx]) or np.allclose([uy], [vy]) else 1.0
            # smooth the bump as we keep subdividing
            bump_smooth = 1.0 / float(step + 1)
            # compute by how much we have to move orthogonally to the line (u, v)
            bump_magnitude = d * 0.5 * bump_enabler * bump_smooth
            # compute the midpoint along the line (u, v)
            cx = (ux + vx) / 2
            cy = (uy + vy) / 2
            cz = (uz + vz) / 2
            c = np.array([cx, cy, cz])
            # find new node position
            p = c + bump_magnitude * dr
            # make attributes for the new node
            mid_node_attrs = node_attributes(
                position=p.tolist(),
                lane=lane,
                direction=None,
                tile=tile,
                tile_map=tile_map
            )
            # get an ID for the new node
            mid_node_id = node_id(tile.key, lane, *node_prefix)
            # add new node
            g.add_node(mid_node_id, **mid_node_attrs)
            # link (u, mid), and (mid, v)
            g.add_edge(node_u_id, mid_node_id)
            g.add_edge(mid_node_id, node_v_id)
            # unlink (u, v)
            g.remove_edge(node_u_id, node_v_id)

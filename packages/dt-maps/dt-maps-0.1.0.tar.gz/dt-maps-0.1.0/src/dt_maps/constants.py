from collections import namedtuple

Tape = namedtuple('Tape', ['width', 'color'])


WHITE_TAPE = Tape(0.048, [255, 255, 255])
YELLOW_TAPE = Tape(0.024, [255, 255, 0])
RED_TAPE = Tape(0.048, [255, 0, 0])

TILE_SIZE = 0.585
LANE_WIDTH = 0.21
LANE_WIDTH_NORMALIZED = LANE_WIDTH / TILE_SIZE

# This is the distance between the edge of yellow tape and the center of the lane
# normalized with respect to the tile size,
CENTER_OF_LANE_NORMALIZED = (LANE_WIDTH / 2.0) / TILE_SIZE

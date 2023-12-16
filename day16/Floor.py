from pathlib import Path
import numpy as np
import numpy.typing as npt
import sys
from operator import add

from enum import Enum
GLOBAL_I = 0
np.set_printoptions(threshold=sys.maxsize)

class Direction(Enum):
    NORTH = [-1, 0]
    EAST = [0, 1]
    SOUTH = [1, 0]
    WEST = [0, -1]
    
    
def parse_input(file_path: Path) -> npt.NDArray:
    with open(file_path, "r") as f:
        data = [list(line.rstrip()) for line in f.read().splitlines()]
    return np.array(data)

def visit_laser(old_direction: Direction, index: [int, int], layout: npt.NDArray, energized_map: npt.NDArray):
    # check if still in bounds
    if index[0]<0 or index[0] >= layout.shape[0] or index[1]<0 or index[1] >= layout.shape[1]:
        return
    actual_tile = layout[index[0]][index[1]]
    
    energized_map[index[0], index[1]] = True
    # TODO debugging
    global GLOBAL_I
    GLOBAL_I += 1
    print("i: ", GLOBAL_I ,"coord: ", index[0], ",", index[1], "direction:", old_direction)
    if actual_tile == '.':
        visit_laser(old_direction, list(map(add, index, old_direction.value)), layout, energized_map)
    elif actual_tile == "\\":
        if old_direction == Direction.EAST:
            new_direction = Direction.SOUTH
        elif old_direction == Direction.SOUTH:
            new_direction = Direction.EAST
        elif old_direction == Direction.WEST:
            new_direction = Direction.NORTH
        elif old_direction == Direction.NORTH:
            new_direction = Direction.WEST
        new_position = list(map(add, index, new_direction.value))
        if not energized_map[new_position[0]][new_position[1]]:
            visit_laser(new_direction, new_position, layout, energized_map)
    elif actual_tile == "/":
        if old_direction == Direction.EAST:
            new_direction = Direction.NORTH
        elif old_direction == Direction.SOUTH:
            new_direction = Direction.WEST
        elif old_direction == Direction.WEST:
            new_direction = Direction.SOUTH
        elif old_direction == Direction.NORTH:
            new_direction = Direction.EAST
        new_position = list(map(add, index, new_direction.value))
        if not energized_map[new_position[0]][new_position[1]]:
            visit_laser(new_direction, new_position, layout, energized_map)
    elif actual_tile == "|":
        if old_direction == Direction.NORTH or old_direction == Direction.SOUTH:
            new_position = list(map(add, index, old_direction.value))
            visit_laser(old_direction, new_position, layout, energized_map)
        else:
            #split laser
            new_position = list(map(add, index, Direction.NORTH.value))
            if not energized_map[new_position[0]][new_position[1]]:
                visit_laser(Direction.NORTH,new_position, layout, energized_map)
            new_position = list(map(add, index, Direction.SOUTH.value))
            if not energized_map[new_position[0]][new_position[1]]:
                visit_laser(Direction.SOUTH, new_position, layout, energized_map)
    elif actual_tile == "-":
        if old_direction == Direction.WEST or old_direction == Direction.EAST:
            new_position = list(map(add, index, old_direction.value))
            visit_laser(old_direction, new_position, layout, energized_map)
        else:
            #split laser
            new_position = list(map(add, index, Direction.WEST.value))
            if not energized_map[new_position[0]][new_position[1]]:
                visit_laser(Direction.WEST, new_position, layout, energized_map)
            new_position = list(map(add, index, Direction.EAST.value))
            if not energized_map[new_position[0]][new_position[1]]:
                visit_laser(Direction.EAST,new_position, layout, energized_map)


if __name__ == "__main__":
    layout = parse_input(Path("day16/input.txt"))
    energized = np.full(layout.shape, False)
    visit_laser(Direction.EAST, (0,0), layout, energized)
    print(energized)
    print("energized tiles: ",energized.sum())
    pass

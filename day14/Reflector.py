from pathlib import Path
import numpy as np
import numpy.typing as npt
from enum import Enum
import sys

np.set_printoptions(threshold=sys.maxsize)


class Direction(Enum):
    NORTH = [-1, 0]
    EAST = [0, 1]
    SOUTH = [1, 0]
    WEST = [0, -1]


def parse_input(file_path: Path) -> list:
    map = []
    with open(file_path, "r") as f:
        for line in f:
            map.append(list(line.rstrip()))

    return np.array(map)


def find_next_free_position(
    map: npt.NDArray, start: list, direction: Direction
) -> list:
    coordinate = [start[0], start[1]]
    while 0 <= coordinate[0] < map.shape[0] and 0 <= coordinate[1] < map.shape[1]:
        new_coordinate = np.add(coordinate, direction.value)
        # next place is a cube rock
        if (
            map[new_coordinate[0]][new_coordinate[1]] == "#"
            or map[new_coordinate[0]][new_coordinate[1]] == "O"
        ):
            return coordinate
        coordinate = new_coordinate
    return np.subtract(coordinate, direction.value)


def tilt(map: npt.NDArray, direction: Direction) -> npt.NDArray:
    tilted_map = np.copy(map)
    for y in range(map.shape[0]):
        for x in range(map.shape[1]):
            if tilted_map[x][y] == "O":
                new_position = find_next_free_position(tilted_map, [x, y], direction)
                tilted_map[x][y] = "."
                tilted_map[new_position[0]][new_position[1]] = "O"
    return tilted_map


def calculate_load(map: npt.NDArray) -> int:
    length = map.shape[0]
    load = 0
    for i, line in enumerate(map):
        count = np.count_nonzero(line == "O")
        load += (length - i) * count

    return load


if __name__ == "__main__":
    map = parse_input(Path("day14/input.txt"))
    new_map = tilt(map, Direction.NORTH)

    load = calculate_load(new_map)
    # print(new_map)
    print("load: ", load)

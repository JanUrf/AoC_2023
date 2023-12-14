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
    last_coordinate = [start[0], start[1]]
    new_coordinate = np.add(last_coordinate, direction.value)
    while (
        0 <= new_coordinate[0] < map.shape[0] and 0 <= new_coordinate[1] < map.shape[1]
    ):

        # next place is a cube rock
        if (
            map[new_coordinate[0]][new_coordinate[1]] == "#"
            or map[new_coordinate[0]][new_coordinate[1]] == "O"
        ):
            return last_coordinate
        last_coordinate = new_coordinate
        new_coordinate = np.add(last_coordinate, direction.value)

    return last_coordinate


def tilt(map: npt.NDArray, direction: Direction) -> npt.NDArray:
    tilted_map = np.copy(map)
    for y in (
        range(map.shape[0])
        if direction == Direction.NORTH or direction == Direction.WEST
        else reversed(range(map.shape[0]))
    ):
        for x in (
            range(map.shape[1])
            if direction == Direction.NORTH or direction == Direction.WEST
            else reversed(range(map.shape[1]))
        ):
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
    new_map = parse_input(Path("day14/input.txt"))

    cycles = 1000000000

    history = [new_map]
    reached_cycle = False
    for i in range(cycles):
        new_map = tilt(new_map, Direction.NORTH)
        new_map = tilt(new_map, Direction.WEST)
        new_map = tilt(new_map, Direction.SOUTH)
        new_map = tilt(new_map, Direction.EAST)

        print("spin cycle: ", i)
        for j, hist in enumerate(history):
            if np.array_equal(hist, new_map):
                # first cycle element is visited again
                reached_cycle = True
                break

        if not reached_cycle:
            history.append(new_map)
        else:
            break

    remaining_iterations = cycles - (i + 1)
    cycle = history[j:]
    # skip all cycles and only go the remaining ones in the cached value
    final_map_index = remaining_iterations % len(cycle)
    load = calculate_load(cycle[final_map_index])

    print("load: ", load)

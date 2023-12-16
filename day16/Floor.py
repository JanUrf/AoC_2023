from pathlib import Path
import numpy as np
import numpy.typing as npt
import sys
from operator import add

from enum import Enum

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


def visit_laser(
    old_direction: Direction,
    index: [int, int],
    layout: npt.NDArray,
    energized_map: npt.NDArray,
):
    current_position = index
    # check if still in bounds
    while is_in_bounds(current_position, layout):

        actual_tile = layout[current_position[0]][current_position[1]]

        # enertgize maps stores the direction which each cell was visited
        energized_map[current_position[0], current_position[1]].add(old_direction)

        if actual_tile == ".":
            # keep direction and move to next cell
            current_position = list(map(add, current_position, old_direction.value))

        elif actual_tile == "\\":
            if old_direction == Direction.EAST:
                new_direction = Direction.SOUTH
            elif old_direction == Direction.SOUTH:
                new_direction = Direction.EAST
            elif old_direction == Direction.WEST:
                new_direction = Direction.NORTH
            elif old_direction == Direction.NORTH:
                new_direction = Direction.WEST

            # change position and update changed direction by 90 degree
            current_position = list(map(add, current_position, new_direction.value))
            old_direction = new_direction

        elif actual_tile == "/":
            if old_direction == Direction.EAST:
                new_direction = Direction.NORTH
            elif old_direction == Direction.SOUTH:
                new_direction = Direction.WEST
            elif old_direction == Direction.WEST:
                new_direction = Direction.SOUTH
            elif old_direction == Direction.NORTH:
                new_direction = Direction.EAST

            # change position and update changed direction by 90 degree
            current_position = list(map(add, current_position, new_direction.value))
            old_direction = new_direction

        elif actual_tile == "|":
            if old_direction == Direction.NORTH or old_direction == Direction.SOUTH:
                # case: pointy end of a splitter
                current_position = list(map(add, current_position, old_direction.value))
            else:
                # split laser
                # visit in north direction first
                visit_laser(
                    Direction.NORTH,
                    list(map(add, current_position, Direction.NORTH.value)),
                    layout,
                    energized_map,
                )
                # continue with the second (South) direction
                # update position and direction
                current_position = list(
                    map(add, current_position, Direction.SOUTH.value)
                )
                old_direction = Direction.SOUTH
                # check if following cell was already visited in same direction to avoid circles
                if (
                    is_in_bounds(current_position, layout)
                    and old_direction
                    in energized_map[current_position[0]][current_position[1]]
                ):
                    return

        elif actual_tile == "-":
            if old_direction == Direction.WEST or old_direction == Direction.EAST:
                # case: pointy end of a splitter
                current_position = list(map(add, current_position, old_direction.value))
            else:
                # split laser
                # visit in west direction first
                visit_laser(
                    Direction.WEST,
                    list(map(add, current_position, Direction.WEST.value)),
                    layout,
                    energized_map,
                )
                # continue with the second (east) direction
                # update position and direction
                current_position = list(
                    map(add, current_position, Direction.EAST.value)
                )
                old_direction = Direction.EAST
                # check if following cell was already visited in same direction to avoid circles
                if (
                    is_in_bounds(current_position, layout)
                    and old_direction
                    in energized_map[current_position[0]][current_position[1]]
                ):
                    return


def is_in_bounds(index: [int, int], layout: npt.NDArray) -> bool:
    return not (
        index[0] < 0
        or index[0] >= layout.shape[0]
        or index[1] < 0
        or index[1] >= layout.shape[1]
    )


if __name__ == "__main__":
    layout = parse_input(Path("day16/input.txt"))
    energized = np.array([set() for _ in range(layout.size)]).reshape(layout.shape)
    visit_laser(Direction.EAST, (0, 0), layout, energized)
    # print(energized)
    print("energized tiles: ", np.count_nonzero(energized != set()))

    best = 0
    start_point = ()

    for i in range(layout.shape[1]):
        # check for first row
        energized = np.array([set() for _ in range(layout.size)]).reshape(layout.shape)
        visit_laser(Direction.SOUTH, (0, i), layout, energized)
        new_energy = np.count_nonzero(energized != set())
        if new_energy > best:
            best = new_energy
            start_point = (0, i)
            best_dir = Direction.SOUTH

        # check for last row
        energized = np.array([set() for _ in range(layout.size)]).reshape(layout.shape)
        visit_laser(Direction.NORTH, (layout.shape[0] - 1, i), layout, energized)
        new_energy = np.count_nonzero(energized != set())
        if new_energy > best:
            best = new_energy
            start_point = (layout.shape[0] - 1, i)
            best_dir = Direction.NORTH

    for i in range(layout.shape[0]):
        # check for first column
        energized = np.array([set() for _ in range(layout.size)]).reshape(layout.shape)
        visit_laser(Direction.EAST, (i, 0), layout, energized)
        new_energy = np.count_nonzero(energized != set())
        if new_energy > best:
            best = new_energy
            start_point = (i, 0)
            best_dir = Direction.EAST

        # check for last column
        energized = np.array([set() for _ in range(layout.size)]).reshape(layout.shape)
        visit_laser(Direction.WEST, (i, layout.shape[1] - 1), layout, energized)
        new_energy = np.count_nonzero(energized != set())
        if new_energy > best:
            best = new_energy
            start_point = (i, layout.shape[1] - 1)
            best_dir = Direction.WEST

    print(
        "best starting position would be: ",
        start_point,
        " in direction: ",
        best_dir.name,
        " with energy of: ",
        best,
    )

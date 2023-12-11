from pathlib import Path
import numpy as np
import numpy.typing as npt
from itertools import combinations
import sys

np.set_printoptions(threshold=sys.maxsize)


def parse_input(file_path: Path) -> (npt.NDArray, int):
    universe = []

    with open(file_path, "r") as f:
        id = -1
        for line in f:
            no_galaxies = True
            sliced_universe = list(line.rstrip())
            for i, point in enumerate(sliced_universe):
                # Add numbers to the galaxies
                if point == "#":
                    id += 1
                    sliced_universe[i] = id
                    no_galaxies = False

            universe.append(sliced_universe)
            if no_galaxies:
                # in this case add this line again.
                universe.append(sliced_universe)
        columns = []

        universe = np.array(universe)
        for i in range(0, universe.shape[1]):
            vertical_row = universe[:, i]
            # empty column
            if all(point == "." for point in vertical_row):
                columns.append(i)

        # use numpy ndarray, because it's easier to insert at some index
        empty_column = ["."] * len(universe)

        # insert empty column. Reversed to avoid index shifting
        for column in reversed(columns):
            universe = np.insert(universe, column, empty_column, axis=1)
    return universe, id


def create_position_lookup(universe: npt.NDArray, max_galaxy_id: int) -> dict:
    positions = {}
    for id in range(max_galaxy_id + 1):
        coordinate = np.argwhere(universe == str(id))
        positions[id] = coordinate[0]

    return positions


def calculate_distance(positions: dict, max_galaxy_id: int) -> (dict, int):
    distances = {}
    total_distance = 0
    for pair in combinations(range(max_galaxy_id + 1), 2):
        coordinate_1 = positions[pair[0]]
        coordinate_2 = positions[pair[1]]
        distance = np.sum(np.abs(np.subtract(coordinate_2, coordinate_1)))
        total_distance += distance

        # save values in dict
        if not distances.get(pair[0], None):
            distances[pair[0]] = {}
        if not distances.get(pair[1], None):
            distances[pair[1]] = {}

        distances[pair[0]][pair[1]] = distance
        distances[pair[1]][pair[0]] = distance

    return distances, total_distance


if __name__ == "__main__":
    universe, max_galaxy_id = parse_input(Path("day11/input.txt"))
    positions = create_position_lookup(universe, max_galaxy_id)
    distances, total_distance = calculate_distance(positions, max_galaxy_id)
    print(total_distance)

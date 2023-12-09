from pathlib import Path
import numpy as np
from enum import Enum


class Direction(Enum):
    FRONT = 0
    LAST = -1


def parse_input(file_path: Path) -> list:
    # [ith inputline][jth derivation] = [column/steps]
    report = []

    with open(file_path, "r") as f:
        for line in f:
            current_line = []
            last_line = np.array([int(x) for x in line.rstrip().split()])
            current_line.append(last_line)

            # calculate derivations
            while True:
                diff = np.diff(last_line)
                current_line.append(diff)
                last_line = diff
                # append derivation
                if not diff.any():
                    break
            report.append(current_line)
    return report


def calculate_next(report: list, direction: Direction = Direction.LAST):
    """
    Direction defines at which index the new values should be appended.
    """
    for i in range(len(report)):
        last_element_below = 0

        # iterate backwards from 0 derivation upwards
        for j in reversed(range(len(report[i]))):
            if direction == Direction.FRONT:
                last_element_below *= -1
                index_insert = 0
            else:
                index_insert = report[i][j].size

            last_element_below = report[i][j][direction.value] + last_element_below
            report[i][j] = np.insert(report[i][j], index_insert, last_element_below)


def calculate_sum(report: list, index: Direction = Direction.LAST) -> int:
    return np.sum([row[0][index.value] for row in report])


if __name__ == "__main__":
    report = parse_input(Path("day9/input.txt"))
    direction = Direction.FRONT
    calculate_next(report, direction)
    sum = calculate_sum(report, direction)
    print(sum)

from pathlib import Path
import numpy as np
import numpy.typing as npt
from enum import Enum
import sys

np.set_printoptions(threshold=sys.maxsize)


def holiday_hash(input: str) -> int:
    current_value = 0
    for character in list(input):
        current_value += ord(character)
        current_value *= 17
        current_value = current_value % 256

    return current_value


def parse_input(file_path: Path) -> list:
    with open(file_path, "r") as f:
        return f.read().rstrip().split(",")


if __name__ == "__main__":
    input = parse_input(Path("day15/input.txt"))
    sum = 0
    for sequence in input:
        sum += holiday_hash(sequence)
    print("sum: ", sum)
from pathlib import Path
import numpy as np
import numpy.typing as npt


def parse_input(file_path: Path) -> list:
    data = []
    with open(file_path, "r") as f:
        for pattern in f.read().split("\n\n"):
            pattern_list = []
            for line in pattern.split("\n"):
                pattern_list.append(list(line.rstrip()))
            data.append(pattern_list)

    return data


def check_for_horizontal_symmetry(pattern: list, line_number: int) -> bool:
    first_half = line_number -1
    second_half = line_number + 2

    while 0 <= first_half and second_half < len(pattern):
        if pattern[first_half] == pattern[second_half]:
            first_half -= 1
            second_half += 1
        else:
            # not symetrical
            return False
    # One half ended and up to here there were symmetrical.
    return True


def check_for_vertical_symmetry(pattern: npt.NDArray, column_number: int) -> bool:
    first_half = column_number -1
    second_half = column_number + 2

    while 0 <= first_half and second_half < pattern[0].shape[0]:
        if (pattern[:, first_half] == pattern[:, second_half]).all():
            first_half -= 1
            second_half += 1
        else:
            # not symetrical
            return False

    # One half ended and up to here there were symmetrical.
    return True


def find_horizontal_symmetry(pattern: list) -> int:
    for i, line in enumerate(pattern):
        # to stop at the second last line
        if i < len(pattern) - 1:
            if line == pattern[i + 1]:
                if check_for_horizontal_symmetry(pattern, i):
                    # in this case we have found the axis
                    return i
                # else case two same lines but not complete symmetrical

    # no horizontal symmetry
    return -1


def find_vertical_symmetry(pattern: list) -> int:
    pattern = np.array(pattern)
    columns = pattern[0].shape[0]
    for i in range(columns):
        if i < columns - 1:
            if (pattern[:, i] == pattern[:, i + 1]).all():
                if check_for_vertical_symmetry(pattern, i):
                    # in this case we have found the axis
                    return i
                # else case two same columns but not complete symmetrical
    # no vertical symmetry
    return -1


if __name__ == "__main__":
    map = parse_input(Path("day13/input.txt"))
    score = 0
    for pattern in map:
        # check for hoirzontal symmetry
        # add 1 because first line starts with 1
        h_axis = find_horizontal_symmetry(pattern)

        # check for vertical symmetry
        v_axis = find_vertical_symmetry(pattern)
        print("h:", h_axis + 1, "  v:", v_axis + 1)
        score += (h_axis + 1) * 100
        score += v_axis + 1
    print("score: ", score)

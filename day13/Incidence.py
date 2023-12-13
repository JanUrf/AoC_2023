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
    first_half = line_number
    second_half = line_number + 1
    pattern = np.array(pattern)
    correct_smud_already = False

    while 0 <= first_half and second_half < pattern.shape[0]:
        differences = (pattern[first_half, :] != pattern[second_half, :]).sum()
        if not correct_smud_already or differences == 0:
            if differences == 1:
                correct_smud_already = True

            if differences <= 1:
                first_half -= 1
                second_half += 1
            else:
                # not symetrical
                return False
        else:
            return False
    # One half ended and up to here there were symmetrical.
    return correct_smud_already


def check_for_vertical_symmetry(pattern: npt.NDArray, column_number: int) -> bool:
    first_half = column_number
    second_half = column_number + 1

    correct_smud_already = False
    while 0 <= first_half and second_half < pattern[0].shape[0]:
        differences = (pattern[:, first_half] != pattern[:, second_half]).sum()
        if not correct_smud_already or differences == 0:
            if differences == 1:
                correct_smud_already = True
            if differences <= 1:
                first_half -= 1
                second_half += 1
            else:
                # not symetrical
                return False

        else:
            return False

    # One half ended and up to here there were symmetrical.
    return correct_smud_already


def find_horizontal_symmetry(pattern: list) -> int:
    for i, line in enumerate(pattern):
        # to stop at the second last line
        if i < len(pattern) - 1:
            if (np.array(line) != np.array(pattern[i + 1])).sum() <= 1:
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
            if (pattern[:, i] != pattern[:, i + 1]).sum() <= 1:
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

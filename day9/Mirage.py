from pathlib import Path
import re
import numpy as np
import math



def parse_input(file_path: Path) -> list:
    # [ith inputline][jth derivation] = [column/steps]
    report = []

    with open(file_path, "r") as f:
        for line in f:
            current_line = []
            input_line = np.array([int(x) for x in line.rstrip().split()])
            current_line.append(input_line)
            
            # calculate derivations            
            last_line = input_line
            while True:
                diff = np.diff(last_line)
                current_line.append(diff)
                last_line = diff
                # append derivation
                if not diff.any():
                    break
            report.append(current_line)
    return report


def calculate_next(report: list):
    for i in range(len(report)):
        last_element_below = 0
        # iterate backwards from 0 derivation upwards
        for j in reversed(range(len(report[i]))):
            if j == len(report[i])-1:
                report[i][j]=np.append(report[i][j], last_element_below)
            else:
                new_value= report[i][j][-1]+ last_element_below
                report[i][j]=np.append(report[i][j], new_value)
                last_element_below = new_value


def calculate_sum(report: list) -> int:
    # TODO do this with reduce function
    sum = 0
    for i in range(len(report)):
        sum += report[i][0][-1]
    return sum

if __name__ == "__main__":
    report = parse_input(Path("day9/input.txt"))
    calculate_next(report)
    sum=calculate_sum(report)
    print(sum)
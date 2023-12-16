from pathlib import Path


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


def calculate_focusing_power(boxes: list) -> int:
    focusing_power = 0
    for box_number, box in enumerate(boxes):
        slot_number = 1
        for lense_label in box:
            focusing_power += (box_number + 1) * slot_number * box[lense_label]
            slot_number += 1

    return focusing_power


if __name__ == "__main__":
    input = parse_input(Path("day15/input.txt"))
    boxes = [{} for _ in range(256)]

    for sequence in input:
        sequence = sequence.split("=")
        dash = False
        if len(sequence) == 1:
            # operator was a '-'
            dash = True
            label = sequence[0][:-1]
        else:
            label = sequence[0]
            focal_length = sequence[1]

        box = holiday_hash(label)

        if dash:
            boxes[box].pop(label, None)

        else:
            boxes[box][label] = int(focal_length)

    power = calculate_focusing_power(boxes)
    print("focusing power: ", power)

from pathlib import Path


def parse_input(file_path: Path) -> (list, list):
    with open(file_path, "r") as f:
        data = f.read().split("\n")
        time = [int(x) for x in data[0].replace("Time:", "").rstrip().lstrip().split()]
        distance = [
            int(x) for x in data[1].replace("Distance:", "").rstrip().lstrip().split()
        ]

    return (time, distance)


def calculate_distance(whole_time: int, button_time: int) -> int:
    # button time is equals speed because increase of 1 mm/ms
    return button_time * (whole_time - button_time)


if __name__ == "__main__":
    times, distances = parse_input(Path("day6/input.txt"))
    product = 1
    already_beat_record = False
    for idx, time in enumerate(times):
        _possible_trials = 0
        record = distances[idx]
        for i in range(time):
            if calculate_distance(time, i) > record:
                already_beat_record = True
                _possible_trials += 1

            # once the record can't be beat anymore we don't have to calculate the rest.
            elif already_beat_record:
                break

        product *= _possible_trials
    print(product)

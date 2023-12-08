from pathlib import Path
import re

node_format = re.compile(r"([A-Z]{3}) = \(([A-Z]{3}), ([A-Z]{3})\)")


def parse_input(file_path: Path) -> (list, dict):
    network = {}

    with open(file_path, "r") as f:
        data = f.read()
        data = data.split("\n\n")
        navigation = list(data[0])
        for node in data[1].split("\n"):
            result = node_format.search(node).groups()
            network[result[0]] = {"L": result[1], "R": result[2]}
    return navigation, network


def walk(start_node: str, target: str, navigation: list, network: dict) -> str:
    steps = 0
    current_node = start_node
    for step in navigation:
        current_node = network[current_node][step]
        steps += 1
        # if target is reached we can abort
        if re.match(current_node, target):
            return current_node, steps
    return current_node, steps


if __name__ == "__main__":
    navigation, network = parse_input(Path("day8/input.txt"))
    steps = 0
    current_node = "AAA"
    target = "ZZZ"
    # Do the steps again until you reach your target
    while current_node != target:
        current_node, iteration_steps = walk(current_node, target, navigation, network)
        steps += iteration_steps
    print("steps: ", steps)

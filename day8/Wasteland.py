from pathlib import Path
import re
import numpy as np
import math

node_format = re.compile(r"(\w{3}) = \((\w{3}), (\w{3})\)")


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


def walk(start_node: str, target: list, navigation: list, network: dict) -> str:
    steps = 0
    current_node = start_node
    for step in navigation:
        current_node = network[current_node][step]
        steps += 1
        # if target is reached we can abort
        if current_node in target:
            return current_node, steps
    return current_node, steps


def find_end(start: str, navigation: list, network: dict, end_notes: list) -> int:
    steps = 0
    current_node = start
    # Do the steps again until you reach your target
    while current_node not in end_nodes:
        current_node, iteration_steps = walk(
            current_node, end_nodes, navigation, network
        )
        steps += iteration_steps
    print(start, " need ", steps, "steps")
    return steps


if __name__ == "__main__":
    navigation, network = parse_input(Path("day8/input.txt"))

    start_nodes = list(filter(lambda node: re.match(r"\w{2}A", node), network.keys()))
    end_nodes = list(filter(lambda node: re.match(r"\w{2}Z", node), network.keys()))

    shortes_way_per_start = [0] * len(start_nodes)

    # find out how long it takes reaching the first from every start node
    for i, node in enumerate(start_nodes):
        steps = find_end(node, navigation, network, end_nodes)
        shortes_way_per_start[i] = steps

    # to synchronize we have to calculate the least common multiple from all nodes
    # including the len of our navigation series, because if other nodes aren't finished
    # they'll continue with the series.
    shortes_way_per_start.append(len(navigation))
    lcm = math.lcm(*shortes_way_per_start)

    print("steps: ", shortes_way_per_start)
    print("lcm: ", lcm)

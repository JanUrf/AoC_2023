from pathlib import Path
import numpy as np
import re

#[r,g,b]
distribution = np.array([12, 13, 14])

red_cubes = r"(\d+) red"
green_cubes = r"(\d+) green"
blue_cubes = r"(\d+) blue"

possible = lambda a: np.all(a <= distribution)

def parse_input(file_path: Path) -> list:
    # [
    #   [[r,g,b],[r,g,b],...,],
    #   [[r,g,b],[r,g,b],...,],
    #     ...
    # ]
    data = []
    with open(file_path, 'r') as f:
        for line in f:
            game = re.sub(r"Game \d*: ", "", line.rstrip()).split(";")
            normalized_game = []
            for reveal in game:
                r_match = re.search(red_cubes, reveal)
                g_match = re.search(green_cubes, reveal)
                b_match = re.search(blue_cubes, reveal)

                # If a colour wasn't drawn it becomes 0
                r = 0 if r_match is None else r_match.group(1)
                g = 0 if g_match is None else g_match.group(1)
                b = 0 if b_match is None else b_match.group(1)
                normalized_game.append(np.array([int(r), int(g), int(b)]))

            data.append(np.array(normalized_game))
    return data

def count_games(games: list) -> int:
    sum = 0
    power = 0
    for i, game in enumerate(games):
        if (all(possible(reveal) for reveal in game)):
            sum += i+1
        power += np.prod(game.max(axis=0))

    return sum, power

if __name__ ==  '__main__':
    game = parse_input(Path("day2/input.txt"))
    sum, power = count_games(game)
    print(sum)
    print(power)
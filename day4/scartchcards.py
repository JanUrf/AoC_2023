from pathlib import Path


def parse_input(file_path: Path) -> (list, list):
    winning_numbers = []
    my_numbers = []
    with open(file_path, "r") as f:
        for line in f:
            # removes the "Card x:"
            data = line.rstrip().split(":")[1]

            numbers = data.split("|")
            winning_numbers.append(set([int(x) for x in numbers[0].split()]))
            my_numbers.append(set([int(x) for x in numbers[1].split()]))

    return (winning_numbers, my_numbers)


def calculate_points(winning_numbers: list[set], my_numbers: list[set]) -> (list, list):
    points = []
    matches = []
    for card_i in range(len(winning_numbers)):
        # calculate intersection
        matches.append(winning_numbers[card_i].intersection(my_numbers[card_i]))
        # double the points depending on number of matches
        if len(matches[card_i]) == 0:
            points.append(0)
        else:
            points.append(2 ** (len(matches[card_i]) - 1))

    return (points, matches)


def new_cards(look_up: list, card_number: int) -> int:
    matches = look_up[card_number - 1]
    # recursive end. If no new winning cards exists.
    # Not needed necessarily, but will save the rest of the function.
    if len(matches) == 0:
        return 1

    # count for itself
    card_count = 1

    child_cards = [x + 1 + card_number for x in range(len(matches))]
    # TODO check if childcards doesn't contain anything > len(look_up)
    # But this is guaranteed.

    # recursion. Calculate child cards
    for new_card in child_cards:
        card_count += new_cards(look_up, new_card)

    return card_count


if __name__ == "__main__":
    winning_numbers, my_numbers = parse_input(Path("day4/input.txt"))
    points, matches = calculate_points(winning_numbers, my_numbers)
    print("points: ", sum(points))
    sum_of_cards = 0
    for i in range(len(winning_numbers)):
        sum_of_cards += new_cards(matches, i + 1)

    print("Amount of cards: ", sum_of_cards)

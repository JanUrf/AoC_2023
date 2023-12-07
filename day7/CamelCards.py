from pathlib import Path
from enum import Enum
import numpy as np


class Card(Enum):
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5
    SIX = 6
    SEVEN = 7
    EIGHT = 8
    NINE = 9
    TEN = 10
    J = 1
    Q = 12
    K = 13
    A = 14


class CardSet(Enum):
    HIGH_CARD = 0
    ONE_PAIR = 1
    TWO_PAIR = 2
    THREE_OF_A_KIND = 3
    FULL_HOUSE = 4
    FOUR_OF_A_KIND = 5
    FIVE_OF_A_KIND = 6


compare_set = lambda hand: hand["set"].value
highest = lambda hand: [card.value for card in hand["values"]]


def parse_input(file_path: Path) -> list:
    data = []
    with open(file_path, "r") as f:
        for line in f:
            hand = line.rstrip().split()
            card_set = determine_card_set(hand[0])
            data.append(
                {
                    "name": hand[0],
                    "bid": int(hand[1]),
                    "set": card_set,
                    "values": card_values(hand[0]),
                }
            )
    return data


def determine_card_set(cards: str) -> CardSet:
    # count occurrence
    hist, distribution = np.unique(list(cards), return_counts=True)
    joker_num = 0
    if "J" in hist:
        index = hist.tolist().index("J")
        joker_num = distribution[index]
        hist = np.delete(hist, index)
        distribution = np.delete(distribution, index)
    if 5 - joker_num in distribution:
        return CardSet.FIVE_OF_A_KIND
    elif 4 - joker_num in distribution:
        return CardSet.FOUR_OF_A_KIND
    elif (2 in distribution and 3 in distribution) or (
        np.count_nonzero(distribution == 2) == 2 and joker_num == 1
    ):
        # For the case 1, 2 and two joker four of a kind is better than Full house and handled before
        return CardSet.FULL_HOUSE
    elif 3 - joker_num in distribution:
        return CardSet.THREE_OF_A_KIND
    elif np.count_nonzero(distribution == 2) == 2:
        return CardSet.TWO_PAIR
    elif np.count_nonzero(distribution == 2) == 1:
        return CardSet.ONE_PAIR
    else:
        if joker_num == 5:
            return CardSet.FIVE_OF_A_KIND
        if joker_num == 1:
            return CardSet.ONE_PAIR
        return CardSet.HIGH_CARD


def card_values(hand: str) -> list:
    values = list(hand)
    for i, value in enumerate(values):
        if value.isnumeric():
            values[i] = Card(int(value))
        elif value == "T":
            values[i] = Card.TEN
        elif value == "J":
            values[i] = Card.J
        elif value == "Q":
            values[i] = Card.Q
        elif value == "K":
            values[i] = Card.K
        elif value == "A":
            values[i] = Card.A

    return values


if __name__ == "__main__":
    hands = parse_input(Path("day7/input.txt"))
    # first sort key is the set and second the highest card
    hands.sort(key=lambda element: (compare_set(element), highest(element)))
    # sum up winnings
    winnings = 0
    for i, hand in enumerate(hands):
        winnings += (i + 1) * hand["bid"]
    print("winnings: ", winnings)

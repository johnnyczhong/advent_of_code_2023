from typing import List, NamedTuple, Set


class Card(NamedTuple):
    id: int
    winning_numbers: Set
    candidate_numbers: Set


def parse_card(line: str) -> Card:
    """
    :param line: "Card 179: 73 43  9 40 72 71 | 47 17 74 40 60  2  5..."
    :return: Card
    """
    card_id, numbers = line.split(": ")
    winning, candidate = numbers.strip().split(" | ")
    winning = " ".join(winning.split()).split(" ")
    candidate = " ".join(candidate.split()).split(" ")
    _, _id = " ".join(card_id.split()).split(" ")
    return Card(id=_id, winning_numbers=set(winning), candidate_numbers=set(candidate))


def count_matches(card: Card) -> int:
    return len(card.candidate_numbers.intersection(card.winning_numbers))


def part1(cards: List[Card]) -> int:
    points = 0
    for card in cards:
        num_matches = count_matches(card)
        points += 2 ** (num_matches - 1) if num_matches > 0 else 0
    return points


def part2(cards: List[Card]) -> int:
    copies = [1] * len(cards)
    total_copies = 0
    while cards:
        card = cards.pop(0)
        num_copies = copies.pop(0)
        total_copies += num_copies
        for i in range(count_matches(card)):
            copies[i] += num_copies

    return total_copies


if __name__ == "__main__":
    filename = "data/day4"
    with open(filename, "r") as file:
        lines = [line.rstrip() for line in file]
    cards = [parse_card(line) for line in lines]
    print(part1(cards))
    print(part2(cards))

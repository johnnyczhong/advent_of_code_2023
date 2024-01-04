from collections import Counter
from typing import Dict, List, NamedTuple, Optional


class HandTypes(NamedTuple):
    five_of_a_kind: List[str]
    four_of_a_kind: List[str]
    full_house: List[str]
    three_of_a_kind: List[str]
    two_pair: List[str]
    one_pair: List[str]
    high_card: List[str]


def sort_hands(hands, rank_order: str, wildcard: str = None) -> HandTypes:
    types = {key: [] for key in HandTypes._fields}
    checks = {
        HandTypes._fields[i]: function
        for i, function in enumerate(
            [
                is_five_of_a_kind,
                is_four_of_a_kind,
                is_full_house,
                is_three_of_a_kind,
                is_two_pair,
                is_pair,
            ]
        )
    }
    for hand in hands:
        counts = optimize_wildcard_outcome(hand=hand, wildcard=wildcard)
        for key, check_function in checks.items():
            if check_function(counts):
                types[key].append(hand)
                break
        else:
            types["high_card"].append(hand)
    for name, hands in types.items():
        types[name] = ranking(types[name], rank_order=rank_order)
    return HandTypes(**types)


def optimize_wildcard_outcome(hand: str, wildcard: str = None) -> List[int]:
    if not wildcard or wildcard not in list(hand):
        return count_cards(hand)

    counter = Counter(hand)
    num_wildcards = counter[wildcard]
    if len(counter) == 1:
        return [counter[wildcard]]

    del counter[wildcard]
    remaining_card_count = sorted(list(counter.values()), reverse=True)
    remaining_card_count[0] += num_wildcards
    return remaining_card_count


def count_cards(hand: str) -> List[int]:
    return list(Counter(hand).values())


def is_five_of_a_kind(count: List[int]) -> bool:
    return 5 in count


def is_four_of_a_kind(count: List[int]) -> bool:
    return 4 in count


def is_full_house(count: List[int]) -> bool:
    return 3 in count and 2 in count


def is_three_of_a_kind(count: List[int]) -> bool:
    return [1, 1, 3] == sorted(count)


def is_two_pair(count: List[int]) -> bool:
    return [1, 2, 2] == sorted(count)


def is_pair(count: List[int]) -> bool:
    return len(count) == 4


def is_high_card(count: List[int]) -> bool:
    return len(count) == 5


def ranking(hands: List[str], rank_order: str) -> List[str]:
    mapping = {card: chr(ord("a") + i) for i, card in enumerate(rank_order)}
    reverse_mapping = {value: key for key, value in mapping.items()}
    enumerated_hands = ["".join([mapping[card] for card in hand]) for hand in hands]
    return [
        "".join([reverse_mapping[card] for card in hand])
        for hand in sorted(enumerated_hands)
    ]


def score(hand_types: HandTypes) -> int:
    ranked_hands = reversed([hand for hand_type in hand_types for hand in hand_type])
    return sum([(i + 1) * plays[hand] for i, hand in enumerate(ranked_hands)])


def evaluate_plays(
    plays: Dict[str, int], rank_order: str, wildcard: Optional[str] = None
) -> int:
    hand_types: HandTypes = sort_hands(
        list(plays.keys()), rank_order=rank_order, wildcard=wildcard
    )
    return score(hand_types)


if __name__ == "__main__":
    filename = "data/day7"
    with open(filename, "r") as file:
        plays = {
            hand: int(bet) for hand, bet in [line.rstrip().split() for line in file]
        }

    # part 1
    rank_order = "AKQJT98765432"
    print(evaluate_plays(plays=plays, rank_order=rank_order, wildcard=None))

    # part 2
    rank_order = "AKQT98765432J"
    print(evaluate_plays(plays=plays, rank_order=rank_order, wildcard="J"))

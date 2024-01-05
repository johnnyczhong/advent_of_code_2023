from typing import List


def get_sequence_differences(sequence: List[int]) -> List[int]:
    offset_sequence = sequence[1:]
    return [
        _next - value
        for _next, value in zip(offset_sequence, sequence)
    ]


def create_sequence_cluster(sequence: List[int]) -> List[List[int]]:
    sequence_cluster = [sequence]
    while not all(element == 0 for element in sequence_cluster[-1]):
        sequence_cluster.append(get_sequence_differences(sequence_cluster[-1]))
    return sequence_cluster


def predict_next_value(sequence: List[int]) -> int:
    sequence_cluster = list(reversed(create_sequence_cluster(sequence=sequence)))
    add_this = 0
    for sequence in sequence_cluster:
        sum = sequence[-1] + add_this
        sequence.append(sum)
        add_this = sum

    return sequence_cluster[-1][-1]


def predict_previous_value(sequence: List[int]) -> int:
    sequence_cluster = list(reversed(create_sequence_cluster(sequence=sequence)))
    subtract_this = 0
    for sequence in sequence_cluster:
        difference = sequence[0] - subtract_this
        sequence.insert(0, difference)
        subtract_this = difference

    return sequence_cluster[-1][0]


def oasis(sequences: List[List[int]]) -> int:
    # Oasis And Sand Instability Sensor
    # aka part 1
    total = 0
    for sequence in sequences:
        total += predict_next_value(sequence)
    return total


def oasis_extrapolator(sequences: List[List[int]]) -> int:
    # aka part 2
    total = 0
    for sequence in sequences:
        total += predict_previous_value(sequence)
    return total


def main():
    filename = "data/day9"
    with open(filename, "r") as file:
        lines = [line.rstrip().split() for line in file]
        sequences = [[int(val) for val in line] for line in lines]
    print(oasis(sequences))
    print(oasis_extrapolator(sequences))


if __name__ == "__main__":
    main()

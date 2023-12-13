from typing import Dict

NUMBERS: Dict[str, str] = {
    "one": "1",
    "two": "2",
    "three": "3",
    "four": "4",
    "five": "5",
    "six": "6",
    "seven": "7",
    "eight": "8",
    "nine": "9",
}


def find_number(chars: str, reversed_string: bool = False) -> str:
    # returns the first string or numeric number encountered
    buffer = ""
    for char in chars:
        if char.isnumeric():
            return char

        if reversed_string:
            buffer = char + buffer
        else:
            buffer += char

        for k, v in NUMBERS.items():
            if k in buffer:
                return v


def evaluate_file(filename: str) -> int:
    with open(filename, "r") as fp:
        lines = [line.rstrip() for line in fp]

    total = 0
    for line in lines:
        first = find_number(line)
        last = find_number(line[::-1], reversed_string=True)
        total += int(first + last)

    return total


if __name__ == "__main__":
    filename = "data/day1"
    print(evaluate_file(filename=filename))

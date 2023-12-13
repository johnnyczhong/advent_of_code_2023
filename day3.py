"""
part numbers determined by adjacency to a symbol
symbols are values that are not periods (.) and other numbers.
adjacency defined as left/right/up/down/diagonal.
initial approach is to treat the file as a grid.
find positions of symbols, then search in 8 directions for a number
if we find a number, walk left and right to assemble full number.
stop when we reach a non-numeric character.
"""
import string
from typing import List, Tuple

DIRECTIONS = (
    (0, 1),  # up
    (0, -1),  # down
    (-1, 0),  # left
    (1, 0),  # right
    (1, 1),  # up-right
    (-1, 1),  # up-left
    (1, -1),  # down-right
    (-1, -1),  # down-left
)
NON_SYMBOLS = set("." + string.digits)
GEAR_RATIO_ADJACENCY_COUNT = 2


def get_part_number_positions(line: str, position: int) -> (int, int):
    """
    :param line: line where we've found the number.
    :param position: position adjacent to the symbol
    :return: index of the start of the number and index of the end of the number.
    """
    width = len(line)
    left, right = position, position
    while left - 1 in range(width) and line[left - 1].isnumeric():
        left -= 1
    while right + 1 in range(width) and line[right + 1].isnumeric():
        right += 1
    return left, right


def find_part_number_total(lines: List[str]) -> int:
    total = 0
    visited = set()

    for y, line in enumerate(lines):
        for x, char in enumerate(line):
            if char not in NON_SYMBOLS:
                for direction_x, direction_y in DIRECTIONS:
                    new_x, new_y = x + direction_x, y + direction_y
                    if (
                        lines[new_y][new_x].isnumeric()
                        and (new_y, new_x) not in visited
                    ):
                        number_line = lines[new_y]

                        start, end = get_part_number_positions(
                            line=number_line, position=new_x
                        )
                        visited.add((new_y, new_x))
                        for i in range(start, end + 1):
                            visited.add((new_y, i))
                        total += int(number_line[start : end + 1])
    return total


def find_gear_ratio(lines: List[str]) -> int:
    total = 0
    visited = set()

    for y, line in enumerate(lines):
        for x, char in enumerate(line):
            if char == "*":
                adjacent_number_positions: List[Tuple[int, Tuple[int, int]]] = []
                for direction_x, direction_y in DIRECTIONS:
                    new_x, new_y = x + direction_x, y + direction_y
                    if (
                        lines[new_y][new_x].isnumeric()
                        and (new_y, new_x) not in visited
                    ):
                        start, end = get_part_number_positions(
                            line=lines[new_y], position=new_x
                        )
                        # fmt: off
                        adjacent_number_positions.append(
                            (
                                new_y,
                                (start, end,),
                            )
                        )
                        # fmt: on
                        visited.add((new_y, new_x))
                        for i in range(start, end + 1):
                            visited.add((new_y, i))

                if len(adjacent_number_positions) == GEAR_RATIO_ADJACENCY_COUNT:
                    number = 1
                    for position in adjacent_number_positions:
                        row, indices = position
                        start, end = indices
                        number *= int(lines[row][start : end + 1])
                    total += int(number)
    return total


if __name__ == "__main__":
    filename = "data/day3"
    with open(filename, "r") as file:
        lines = [line.rstrip() for line in file]

    print(find_part_number_total(lines=lines))
    print(find_gear_ratio(lines=lines))

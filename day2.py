from typing import List, Dict, Any
from typing import NamedTuple
from operator import mul
from functools import reduce


MAXES = {"red": 12, "green": 13, "blue": 14}


class Cube(NamedTuple):
    count: int
    color: str


def evaluate_games(
    filename: str,
    mode: str,
) -> int:
    with open(filename, "r") as file:
        games = [line.rstrip() for line in file]
    total = 0

    if mode == "is_possible":
        for game in games:
            game_id = int(game.split(" ")[1].strip(":"))
            pulls = get_pulls(game)
            total += game_id if is_possible(pulls) else 0

    if mode == "min_cubes":
        for game in games:
            pulls = get_pulls(game)
            total += min_cubes(pulls)

    return total


def is_possible(pulls: List[List[Cube]]) -> bool:
    for pull in pulls:
        for cube in pull:
            if MAXES[cube.color] < cube.count:
                return False
    return True


def min_cubes(pulls: List[List[Cube]]) -> Dict[str, Any]:
    minimums = {}
    for pull in pulls:
        for cube in pull:
            minimums.update({cube.color: max(minimums.get(cube.color, 0), cube.count)})

    return reduce(mul, list(minimums.values()))


def get_pulls(game_text: str) -> List[List[Cube]]:
    game_id_text, content = game_text.split(": ")
    plays = content.split("; ")
    pulls = []
    for play in plays:
        cube_combination = play.split(", ")
        cubes = []
        for cube_details in cube_combination:
            count, color = cube_details.split(" ")
            cubes.append(Cube(count=int(count), color=color))
        pulls.append(cubes)
    return pulls


if __name__ == "__main__":
    print(evaluate_games(filename="data/day2", mode="is_possible"))
    print(evaluate_games(filename="data/day2", mode="min_cubes"))

from typing import List


def get_distance_ms(button_held_ms: int, race_time_ms: int) -> int:
    return button_held_ms * (race_time_ms - button_held_ms)


def distance_curve(race_time_ms: int):
    # +1ms = +1mm/ms
    # return a list of distances
    # where the index is the number of seconds held
    # and the value is the total distance traveled for the rest of duration of the race.
    # total time = held time + travel time
    # i = hold time, max_duration - i
    return [
        get_distance_ms(button_held_ms=button_held_ms, race_time_ms=race_time_ms)
        for button_held_ms in range(race_time_ms + 1)
    ]


def parse_values(line: str) -> List[int]:
    return [int(character) for character in line.split(":")[1].split()]


def part1(times: List[int], records: List[int]) -> int:
    ways_to_beat = 1
    for time, record in zip(times, records):
        distances = distance_curve(time)
        ways_to_beat *= sum(1 for distance in distances if distance > record)

    return ways_to_beat


def part2(times: List[int], records: List[int]) -> int:
    time = int("".join([str(time) for time in times]))
    record = int("".join([str(record) for record in records]))
    # search for left and right bounds
    left = find_bound(
        center_ms=int(time/2),
        edge_ms=0,
        midpoint_ms=int((0 + int(time/2))/2),
        race_time_ms=time,
        record_ms=record,
    )
    right = find_bound(
        center_ms=int(time/2),
        edge_ms=time,
        midpoint_ms=int((time + int(time/2))/2),
        race_time_ms=time,
        record_ms=record,
    )
    # need to be inclusive.
    return right - left + 1


def find_bound(
        center_ms: int,
        edge_ms: int,
        midpoint_ms: int,
        race_time_ms: int,
        record_ms: int,
) -> int:
    """
    We expect that the overall distance travelled is some kind of bell curve
    So the record/distance to beat just modifies how much of that bell curve is seen.
    Visually, this would be like drawing a horizontal line on a gaussian distribution
      and pulling it up or down.
    The higher the distance to beat, the higher the bar in our visualization, the fewer values beat the given record.
    We're looking for where the gaussian distribution touches that horizontal axis.
    """
    # center, edge, middle.
    center_beats_record = get_distance_ms(button_held_ms=center_ms, race_time_ms=race_time_ms) > record_ms
    edge_beats_record = get_distance_ms(button_held_ms=edge_ms, race_time_ms=race_time_ms) > record_ms
    midpoint_beats_record = get_distance_ms(button_held_ms=midpoint_ms, race_time_ms=race_time_ms) > record_ms
    if center_beats_record and not edge_beats_record and (center_ms + 1 == edge_ms or center_ms == edge_ms + 1):
        return center_ms
    if midpoint_beats_record:
        # too close to the center, go outwards.
        return find_bound(
            center_ms=midpoint_ms,
            edge_ms=edge_ms,
            midpoint_ms=int((midpoint_ms + edge_ms)/2),
            race_time_ms=race_time_ms,
            record_ms=record_ms,
        )
    if not midpoint_beats_record:
        # too far out, go back towards center.
        return find_bound(
            center_ms=center_ms,
            edge_ms=midpoint_ms,
            midpoint_ms=int((midpoint_ms + center_ms) / 2),
            race_time_ms=race_time_ms,
            record_ms=record_ms,
        )


if __name__ == "__main__":
    filename = "data/day6"
    with open(filename, "r") as file:
        times = parse_values(file.readline())
        records = parse_values(file.readline())

    print(part1(times, records))
    print(part2(times, records))
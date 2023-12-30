from typing import Dict, List, NamedTuple, Tuple, Optional, Union


class Map(NamedTuple):
    destination: int
    source: int
    range: int

    @property
    def source_end(self):
        return self.source + self.range

    @property
    def source_start(self):
        return self.source

    @property
    def destination_end(self):
        return self.destination + self.range

    @property
    def destination_start(self):
        return self.destination


class Bound(NamedTuple):
    start: int
    end: int


class SeedMap(NamedTuple):
    seed_to_soil: List[Map]
    soil_to_fertilizer: List[Map]
    fertilizer_to_water: List[Map]
    water_to_light: List[Map]
    light_to_temperature: List[Map]
    temperature_to_humidity: List[Map]
    humidity_to_location: List[Map]

    @classmethod
    def from_file(cls, filename):
        # split along \n\n
        with open(filename, "r") as file:
            data = file.read()

        sections = data.split("\n\n")
        categories = {}
        for section in sections[1:]:
            lines = section.split("\n")
            header, _ = lines[0].split(" ")
            header = header.replace("-", "_")

            maps = []
            for line in lines[1:]:
                if line == "":
                    continue

                destination, source, range = line.split(" ")
                maps.append(
                    Map(
                        destination=int(destination),
                        source=int(source),
                        range=int(range),
                    )
                )
            maps = sorted(maps, key=lambda map: map.source)
            categories[header] = maps
        return cls(**categories)


def find_location_number(seed: int, seed_map: SeedMap) -> int:
    _source = seed
    for categories in seed_map:
        for map in categories:
            if map.source <= _source < (map.source + map.range):
                diff = _source - map.source
                _source = map.destination + diff
                break

    return _source


def map_range(bound: Bound, map: Map) -> Bound:
    return Bound(
        start=map.destination_start + (bound.start - map.source_start),
        end=map.destination_start + (bound.end - map.source_start),
    )


def find_maps(bound: Bound, map: Map) -> Dict[str, Union[Bound, List[Bound]]]:
    if map.source_start <= bound.start < bound.end <= map.source_end:
        return {
            "mapped": Bound(
                start=map.source_start + (bound.start - map.source_start),
                end=map.source_start + (bound.end - map.source_start),
            ),
            "unmapped": [],
        }

    if bound.start <= map.source_start < map.source_end <= bound.end:
        return {
            "mapped": Bound(start=map.source_start, end=map.source_end),
            "unmapped": [
                Bound(start=bound.start, end=map.source_start),
                Bound(start=map.source_end, end=bound.end),
            ],
        }

    if bound.start <= map.source_start < bound.end <= map.source_end:
        return {
            "mapped": Bound(
                start=map.source_start,
                end=map.source_start + (bound.end - map.source_start),
            ),
            "unmapped": [Bound(start=bound.start, end=map.source_start)],
        }

    if map.source_start <= bound.start < map.source_end <= bound.end:
        return {
            "mapped": Bound(
                start=(bound.start - map.source_start) + map.source_start,
                end=map.source_end,
            ),
            "unmapped": [Bound(start=map.source_end, end=bound.end)],
        }

    return {"mapped": None, "unmapped": [bound]}


def traverse_seed_map(_maps: Map, unmapped_ranges: List[Bound]):
    mapped_ranges = []
    for _map in _maps:
        mapped, unmapped_ranges = traverse_map(_map, unmapped_ranges)
        mapped_ranges += mapped
        if not unmapped_ranges:
            break
    unmapped_ranges += mapped_ranges
    return unmapped_ranges


def traverse_map(_map: Map, bounds: List[Bound]) -> Tuple[Optional[List[Bound]], Optional[List[Bound]]]:
    unmapped = []
    mapped = []
    for bound in bounds:
        results = find_maps(bound, _map)
        unmapped += results["unmapped"]
        mapped += (
            [map_range(results["mapped"], _map)] if results["mapped"] else []
        )
    return mapped, unmapped


def get_lowest(seed_range: Bound, seed_map: SeedMap) -> int:
    unmapped_ranges = [seed_range]
    for _maps in seed_map:
        unmapped_ranges = traverse_seed_map(_maps, unmapped_ranges)
    return sorted(unmapped_ranges, key=lambda unmapped_range: unmapped_range.start)[0].start


if __name__ == "__main__":
    filename = "data/day5"
    with open(filename, "r") as file:
        seeds = file.readline().split(": ")[1].split(" ")
    seed_map = SeedMap.from_file(filename)

    # part 1
    lowest = None
    for seed in seeds:
        destination = find_location_number(int(seed), seed_map)
        if not lowest or destination < lowest:
            lowest = destination
    print(lowest)

    # part 2
    # the number of iterations is too large.
    # instead, we have to work with the ranges.
    # ie. we have 1-1000, which maps to 5000-5500 and 300-800, so we keep track of these ranges.
    # now we have 5000-5500 and 300-800. we then use these as our sources for the next mapping.
    lowest_v2 = None
    seed_ranges = [
        Bound(start=int(seeds[i]), end=(int(seeds[i]) + int(seeds[i + 1])))
        for i in range(0, len(seeds), 2)
    ]
    for seed_range in seed_ranges:
        seed_lowest = get_lowest(seed_range=seed_range, seed_map=seed_map)
        lowest_v2 = min(lowest_v2, seed_lowest) if lowest_v2 else seed_lowest

    print(lowest_v2)

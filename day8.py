from typing import Dict, List
from copy import deepcopy
from math import lcm


def create_node(node: str) -> Dict[str, Dict[str, str]]:
    # example: DRM = (DLQ, BGR)
    source, destinations = node.split(" = ")
    left, right = destinations.strip("()").split(", ")
    return {source: {"L": left, "R": right}}


def create_graph(nodes: List[str]) -> Dict[str, Dict[str, str]]:
    """
    alternative ways to code this:
    graph = {}
    for node in nodes:
        graph.update(create_node(node=node))
        or
        graph = {**graph, **create_node(node=node)}
    return graph
    """
    return {k: v for node in nodes for k, v in create_node(node=node).items()}


def traverse_graph(
    source: str, graph: Dict[str, Dict[str, str]], instruction: str
) -> str:
    return graph[source][instruction]


def find_destination(
    instructions: List[str],
    graph: Dict[str, Dict[str, str]],
    source: str = "AAA",
    destination: str = "ZZZ",
) -> int:
    # aka part 1
    current_node = source
    steps = 0
    while current_node != destination:
        steps += 1
        instruction = instructions.pop(0)
        instructions.append(instruction)
        current_node = traverse_graph(
            source=current_node, graph=graph, instruction=instruction
        )

    return steps


def find_destinations_simultaneously(
    instructions: List[str],
    graph: Dict[str, Dict[str, str]],
    source: str = "A",
    destination: str = "Z",
):
    # aka part 2
    paths = {node: [node] for node in graph.keys() if node.endswith("A")}

    z_positions = []
    for origin, path in paths.items():
        current_instruction_set = deepcopy(instructions)
        while not path[-1].endswith("Z"):
            current_instruction = current_instruction_set.pop(0)
            current_instruction_set.append(current_instruction)
            path.append(
                traverse_graph(
                    source=path[-1], graph=graph, instruction=current_instruction
                )
            )
        z_positions.append(len(path) - 1)

    return lcm(*z_positions)


def main():
    filename = "data/day8"
    with open(filename, "r") as file:
        lines = [line.rstrip() for line in file]
    instructions = lines[0]
    nodes = lines[2:]

    instructions: List[str] = list(instructions)
    graph: Dict[str, Dict[str, str]] = create_graph(nodes=nodes)
    print(find_destination(instructions=instructions, graph=graph))
    print(find_destinations_simultaneously(instructions=instructions, graph=graph))


if __name__ == "__main__":
    main()

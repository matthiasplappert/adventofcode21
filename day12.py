from typing import Dict
from collections import Counter


def parse_line(l: str):
    lhs, rhs = l.strip().split("-")
    return (lhs.strip(), rhs.strip())


def find_path(
    node: str, graph: Dict[str, set], path: list, part2: bool = False
):
    if node == "end":
        # Found the end.
        return path + ["end"]
    if node == "start" and "start" in path:
        # Cannot visit start more than once.
        return path
    if node not in graph:
        # No more children.
        return path

    # Now for the more complex: visiting small caves at most
    # once, except a single one which can be visited twice.
    if node.islower() and node in path:
        if not part2:
            return path

        only_unique_small_cave_visits = all([
            v == 1
            for k, v in Counter(path).items()
            if k.islower()
        ])
        if not only_unique_small_cave_visits:
            # Already visited a single small cave more than once.
            return path

    # Recurse to all children.
    paths = []
    for child in graph[node]:
        paths.append(find_path(child, graph, path + [node], part2))
    return paths


def filter_complete_paths(l: list):
    out = []
    for x in l:
        if x[0] == "start" and x[-1] == "end":
            out.append(x)
        if isinstance(x, list):
            out.extend(filter_complete_paths(x))
    return out


with open("day12.txt", "r") as f:
    data = map(parse_line, f.readlines())

graph: Dict[str, set] = {}
for lhs, rhs in data:
    if lhs not in graph:
        graph[lhs] = set()
    if rhs not in graph:
        graph[rhs] = set()
    graph[lhs].add(rhs)
    graph[rhs].add(lhs)
assert "start" in graph

# Part 1
all_paths = find_path("start", graph, [])
print(len(filter_complete_paths(all_paths)))

# Part 2
all_paths = find_path("start", graph, [], part2=True)
print(len(filter_complete_paths(all_paths)))

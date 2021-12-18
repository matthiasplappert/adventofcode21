import math
import json
from typing import Optional
from copy import deepcopy


class Node:
    parent: Optional["Pair"] = None

    @property
    def depth(self):
        if self.parent is None:
            return 0
        return self.parent.depth + 1

    @property
    def magnitude(self) -> int:
        return 0


class Pair(Node):
    left: Node
    right: Node

    def __init__(self, left: Node, right: Node):
        left.parent = self
        self.left = left

        right.parent = self
        self.right = right

    def __repr__(self) -> str:
        return f"[{self.left}, {self.right}]"

    @property
    def magnitude(self) -> int:
        return 3 * self.left.magnitude + 2 * self.right.magnitude


class Number(Node):
    value: int

    def __init__(self, value: int):
        self.value = value

    def __repr__(self) -> str:
        return str(self.value)

    @property
    def magnitude(self) -> int:
        return self.value


def parse_line(data) -> Node:
    if isinstance(data, list):
        assert len(data) == 2, len(data)
        return Pair(left=parse_line(data[0]), right=parse_line(data[1]))
    else:
        return Number(value=data)


def add(left: Node, right: Node) -> Pair:
    node = Pair(left=deepcopy(left), right=deepcopy(right))
    reduce(node)
    return node


def iter(node: Node):
    yield node
    if isinstance(node, Number):
        return
    assert isinstance(node, Pair)
    yield from iter(node.left)
    yield from iter(node.right)


def reduce(node: Node):
    while reduce_step(node):
        pass


def reduce_step(node: Node) -> bool:
    # Step 1: explode (and return True if explode as applied)
    for child in iter(node):
        if not isinstance(child, Pair):
            continue
        assert isinstance(child, Pair)
        if child.depth < 4:
            continue
        explode(child)
        return True

    # Step 2: split (and return True if split as applied)
    for child in iter(node):
        if not isinstance(child, Number):
            continue
        assert isinstance(child, Number)
        if child.value < 10:
            continue
        split(child)
        return True

    # Nothing happened.
    return False


def find_left_number(node: Node) -> Number:
    if isinstance(node, Number):
        return node
    assert isinstance(node, Pair)
    return find_left_number(node.left)


def find_right_number(node: Node) -> Number:
    if isinstance(node, Number):
        return node
    assert isinstance(node, Pair)
    return find_right_number(node.right)


def find_right_root(pair: Pair):
    assert isinstance(pair, Pair)
    parent = pair.parent
    if parent is None:
        return None
    if parent.right != pair:
        return parent
    return find_right_root(parent)


def find_left_root(pair: Pair):
    assert isinstance(pair, Pair)
    parent = pair.parent
    if parent is None:
        return None
    if parent.left != pair:
        return parent
    return find_left_root(parent)


def explode(pair: Pair):
    assert isinstance(pair.left, Number)
    assert isinstance(pair.right, Number)
    new_number = Number(value=0)

    left_root = find_left_root(pair)
    if left_root is not None:
        find_right_number(left_root.left).value += pair.left.value
    right_root = find_right_root(pair)
    if right_root is not None:
        find_left_number(right_root.right).value += pair.right.value
    new_number.parent = pair.parent

    assert pair.parent
    if pair.parent.left == pair:
        pair.parent.left = new_number
    elif pair.parent.right == pair:
        pair.parent.right = new_number
    else:
        raise Exception("unexpected")


def split(number: Number):
    assert isinstance(number, Number)
    left_value = int(math.floor(number.value / 2))
    right_value = int(math.ceil(number.value / 2))
    new_pair = Pair(left=Number(left_value), right=Number(right_value))
    new_pair.parent = number.parent

    assert number.parent
    if number.parent.left == number:
        number.parent.left = new_pair
    elif number.parent.right == number:
        number.parent.right = new_pair
    else:
        raise Exception("unexpected")


with open("day18.txt") as f:
    data = [parse_line(json.loads(l)) for l in f.readlines()]


# Part 1
out = data[0]
for x in data[1:]:
    out = add(out, x)
print(out.magnitude)

# Part 2
max_magnitude = 0
for idx in range(len(data) - 1):
    for idx2 in range(idx + 1, len(data)):
        a = data[idx]
        b = data[idx2]
        m1 = add(a, b).magnitude
        m2 = add(b, a).magnitude
        max_magnitude = max(max_magnitude, m1, m2)
print(max_magnitude)

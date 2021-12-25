from typing import List
from tqdm import tqdm
from copy import copy
from functools import lru_cache
import time


@lru_cache
def cached_to_int(s: str) -> int:
    return int(s)


def load_or_literal(state, b):
    registers, _ = state
    if b in "wxyz":
        return registers[b]
    return cached_to_int(b)


def inp(state, a):
    registers, inputs = state
    registers[a] = inputs[-1]


def add(state, a, b):
    registers, _ = state
    registers[a] += load_or_literal(state, b)


def mul(state, a, b):
    registers, _ = state
    registers[a] *= load_or_literal(state, b)


def div(state, a, b):
    registers, _ = state
    registers[a] //= load_or_literal(state, b)


def mod(state, a, b):
    registers, _ = state
    registers[a] %= load_or_literal(state, b)


def eql(state, a, b):
    registers, _ = state
    registers[a] = int(registers[a] == load_or_literal(state, b))


OPS = {
    "inp": inp,
    "add": add,
    "mul": mul,
    "div": div,
    "mod": mod,
    "eql": eql,
}


def eval(state, instruction: List[str]):
    name, *args = instruction
    OPS[name](state, *args)


def parse_instruction(i: str) -> List[str]:
    return i.strip().split(" ")


def reduce_alus(alus):
    alu_groups = {}
    for alu in alus:
        key = (alu[0]["w"], alu[0]["x"], alu[0]["y"], alu[0]["z"])
        if key not in alu_groups:
            alu_groups[key] = alu
        else:
            if inputs > alu_groups[key][1]:
                alu_groups[key] = alu
    return alu_groups.values()


with open("day24.txt", "r") as f:
    instructions = list(map(parse_instruction, f.readlines()))

# This implementation does not use classes since the overhead of creating
# them when branching is too large.
alus = [({"x": 0, "y": 0, "z": 0, "w": 0}, [])]
for idx, instruction in enumerate(instructions):
    print(idx)

    name, *_ = instruction
    new_alus = []

    if name == "inp":
        print(f"  branching ALUs ... ", end="", flush=True)
        start_time = time.time()
        for registers, inputs in alus:
            for possible_input in range(1, 10):
                new_alu = (copy(registers), inputs + [possible_input])
                new_alus.append(new_alu)
        alus = new_alus
        duration = time.time() - start_time
        print(f"expanded to {len(alus)} ({duration:.3f}s)")

    print("  evaluating ALUs ... ", end="", flush=True)
    start_time = time.time()
    for alu in alus:
        eval(alu, instruction)
    duration = time.time() - start_time
    print(f"evaluated {len(alus)} ({duration:.3f}s)")

    # Reduce
    num_alus_before = len(alus)
    print(f"  reducing ALUs ... ", end="", flush=True)
    start_time = time.time()
    alus = reduce_alus(alus)
    duration = time.time() - start_time
    num_alus_after = len(alus)
    print(f"reduced {num_alus_before} -> {num_alus_after} ({duration:.3f}s)")
    print()

filtered_alus = [alu for alu in alus if alu[0]["z"] == 0]
sorted_inputs = list(sorted(map(lambda x: x[1], filtered_alus)))
print(sorted_inputs[-1])
print(sorted_inputs[0])

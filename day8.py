import itertools
from tqdm import tqdm


DIGITS = {
    0: "abcefg",
    1: "cf",
    2: "acdeg",
    3: "acdfg",
    4: "bcdf",
    5: "abdfg",
    6: "abdefg",
    7: "acf",
    8: "abcdefg",
    9: "abcdfg",
}


def permutations_iter():
    inputs = "abcdefg"
    for outputs in itertools.permutations(inputs):
        mapping = dict(zip(inputs, outputs))
        mapped_digits = {
            "".join(
                sorted(
                    map(lambda x: mapping[x], v)
                )
            ): k
            for k, v in DIGITS.items()
        }
        yield mapped_digits


def parse_line(l):
    lhs, rhs = l.strip().split(" | ")
    lhs = [x.strip() for x in lhs.split()]
    rhs = [x.strip() for x in rhs.split()]
    return lhs, rhs


with open("day8.txt", "r") as f:
    lines = [parse_line(l) for l in f.readlines()]

# Decode the outputs. The basic approach is:
# 1. Standardize the pattern and outputs by sorting them.
#    This is necessary because the order of abcdefg is arbitrary
#    and we'll need to compare. For the patterns, also sort across.
# 2. Enumerate all possible permutations in the same standardized form.
# 3. For each line, find the match (there should be exactly one).
#    Since we remembered the mapping that produced the permutation, we
#    can now use it to decode the output.
decoded_outputs = []
for patterns, outputs in tqdm(lines):
    sorted_patterns = sorted(["".join(sorted(x)) for x in patterns])
    sorted_outputs = ["".join(sorted(x)) for x in outputs]
    mapping = None
    for p in permutations_iter():
        sorted_ref_patterns = sorted(p.keys())
        assert len(sorted_ref_patterns) == len(sorted_patterns)
        if sorted_patterns == sorted_ref_patterns:
            mapping = p
            break
    assert mapping
    decoded_output = [mapping[x] for x in sorted_outputs]
    decoded_outputs.append(decoded_output)

# Part 1
counts = 0
for decoded_output in decoded_outputs:
    for target_digit in [1, 4, 7, 8]:
        counts += decoded_output.count(target_digit)
print(counts)

# Part 2
outputs_sum = 0
for decoded_output in decoded_outputs:
    number = int("".join([str(x) for x in decoded_output]))
    outputs_sum += number
print(outputs_sum)

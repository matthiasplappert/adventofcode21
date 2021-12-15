from collections import Counter, defaultdict
from types import new_class
from tqdm import tqdm


def parse_rule(rule):
    lhs, rhs = rule.strip().split(" -> ")
    return lhs, rhs


with open("day14.txt", "r") as f:
    template, rules = f.read().split("\n\n")
    template = template.strip()
    rules = dict(map(parse_rule, rules.split("\n")))


def simulate(template, rules, iters):
    counts = defaultdict(int)
    for x, y in zip(template[:-1], template[1:]):
        counts[(x, y)] += 1
    for _ in range(iters):
        new_counts = defaultdict(int)
        for (x, y), count in counts.items():
            new_letter = rules[x + y]
            new_counts[x + new_letter] += count
            new_counts[new_letter + y] += count
        counts = new_counts

    letter_counts = defaultdict(int)
    for (x, y), count in counts.items():
        letter_counts[x] += count
        # do not include here y since otherwise we're double-counting
        # (since y is the x of another pair)
    sorted_counts = list(sorted(letter_counts.values(), key=lambda x: x))
    return sorted_counts[-1] - sorted_counts[0] + 1  # +1 for final y, which doesn't have an x


# Part 1
print(simulate(template, rules, 10))

# Part 2
print(simulate(template, rules, 40))

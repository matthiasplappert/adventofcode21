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

    letter_counts_x = defaultdict(int)
    letter_counts_y = defaultdict(int)
    letters = set()
    for (x, y), count in counts.items():
        letter_counts_x[x] += count
        letter_counts_y[y] += count
        letters.add(x)
        letters.add(y)
    combined_counts = {k: max(letter_counts_y[k], letter_counts_x[k]) for k in letters}
    sorted_counts = list(sorted(combined_counts.values()))
    return sorted_counts[-1] - sorted_counts[0]


# Part 1
print(simulate(template, rules, 10))

# Part 2
print(simulate(template, rules, 40))

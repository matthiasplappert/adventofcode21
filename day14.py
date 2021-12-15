from collections import Counter
from tqdm import tqdm


def parse_rule(rule):
    lhs, rhs = rule.strip().split(" -> ")
    return lhs, rhs


with open("day14.txt", "r") as f:
    template, rules = f.read().split("\n\n")
    template = template.strip()
    rules = dict(map(parse_rule, rules.split("\n")))

output = template
for _ in tqdm(range(40)):
    insertions = []
    for idx in range(len(output) - 1):
        pattern = output[idx] + output[idx + 1]
        insertions.append(rules.get(pattern, ""))

    new_output = ""
    for idx in range(len(output)):
        new_output += output[idx]
        if idx < len(insertions):
            new_output += insertions[idx]
    output = new_output

# Part 1
c = Counter(output)
sorted_c = list(sorted(c.values(), key=lambda x: x))
print(sorted_c[-1] - sorted_c[0])

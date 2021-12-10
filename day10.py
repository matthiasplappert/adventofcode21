import numpy as np


with open("day10.txt") as f:
    lines = [x.strip() for x in f.readlines()]
print(len(lines))

PARANTHESE = {'(': ')', '[': ']', '{': '}', "<": ">"}
ALL_PARANTHESE = list(PARANTHESE.keys()) + list(PARANTHESE.values())
SYNTAX_POINTS = {
    ")": 3,
    "]": 57,
    "}": 1197,
    ">": 25137,
}
AUTOCOMPLETE_POINTS = {
    ")": 1,
    "]": 2,
    "}": 3,
    ">": 4,
}

syntax_scores = []
autocomplete_scores = []
for line in lines:
    stack = []
    has_syntax_error = False
    for c in line:
        if c not in ALL_PARANTHESE:
            raise ValueError(f"Invalid character: {c}")
        if c in PARANTHESE.keys():
            # Push opening paranthese onto stack
            stack.append(c)
            continue

        # Check if the last paranthese on the stack matches
        # the closing one from the stack.
        c_ = stack.pop()
        if PARANTHESE[c_] != c:
            has_syntax_error = True
            syntax_scores.append(SYNTAX_POINTS[c])
            break

    if has_syntax_error:
        continue

    autocomplete_score = 0
    for c_ in reversed(stack):
        autocomplete_score *= 5
        c = PARANTHESE[c_]
        autocomplete_score += AUTOCOMPLETE_POINTS[c]
    autocomplete_scores.append(autocomplete_score)

# Part 1
print(sum(syntax_scores))

# Part 2
print(int(np.median(autocomplete_scores)))
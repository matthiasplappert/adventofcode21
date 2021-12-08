from collections import defaultdict, Counter
from tqdm import tqdm


with open("day6.txt") as f:
    state = [int(x) for x in f.read().strip().split(",")]

counts = defaultdict(int)
counts.update(Counter(state))
for _ in tqdm(range(256)):
    new_counts = defaultdict(int)
    num_new_fish = counts[0]
    for i in range(8):
        new_counts[i] = counts[i + 1]
    new_counts[6] += counts[0]
    new_counts[8] = num_new_fish
    counts = new_counts
print(sum([v for v in counts.values()]))

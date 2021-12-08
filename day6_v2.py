import numpy as np
from tqdm import tqdm

with open("day6.txt") as f:
    state = np.array(
        [int(x) for x in f.read().strip().split(",")],
        dtype=np.uint8,
    )
for _ in tqdm(range(256)):
    reproduction_mask = (state == 0)
    state -= 1
    num_new_fish = np.sum(reproduction_mask)
    state[reproduction_mask] = 6
    state = np.concatenate(
        [state, 8 * np.ones(num_new_fish, dtype=np.uint8)]
    )
print(len(state))

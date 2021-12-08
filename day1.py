import numpy as np


with open("day1.txt", "r") as f:
    data = [int(l.strip()) for l in f.readlines()]

# Part 1
print(np.sum(np.diff(data) > 0))

# Part 2
smoothed_data = np.convolve(data, np.ones(3) / 3, "valid")
print(np.sum(np.diff(smoothed_data) > 0))

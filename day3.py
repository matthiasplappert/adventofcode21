import numpy as np

def data_to_numpy(data):
    out = []
    for line in data:
        out.append([int(b) for b in line])
    return np.array(out)


def bin2str(l):
    s = "".join([str(x) for x in l])
    return s


def bin2dec(l):
    s = bin2str(l)
    return int(s, 2)


def compute_gamma(arr):
    num_ones = np.sum(arr == 1, axis=0)
    num_zeros = np.sum(arr == 0, axis=0)
    num_ones += (num_ones == num_zeros)  # tie break towards one
    gamma = np.argmax([num_ones, num_zeros], axis=0)
    return gamma


def compute_epsilon(arr):
    num_ones = np.sum(arr == 1, axis=0)
    num_zeros = np.sum(arr == 0, axis=0)
    num_zeros -= (num_ones == num_zeros)  # tie break towards zero
    gamma = np.argmin([num_ones, num_zeros], axis=0)
    return gamma


with open("day3.txt", "r") as f:
    data = data_to_numpy([x.strip() for x in f.readlines()])

# Part 1
gamma = compute_gamma(data)
epsilon = compute_epsilon(data)
print(bin2dec(gamma) * bin2dec(epsilon))

# Part 2
oxygen_data = data.copy()
co2_data = data.copy()
for i in range(data.shape[1]):
    if len(oxygen_data) > 1:
        oxygen_bit = compute_gamma(oxygen_data[:, i])
        oxygen_data = oxygen_data[oxygen_data[:, i] == oxygen_bit]
    if len(co2_data) > 1:
        co2_bit = compute_epsilon(co2_data[:, i])
        co2_data = co2_data[co2_data[:, i] == co2_bit]
assert len(co2_data) == len(oxygen_data) == 1
print(oxygen_data, co2_data)
print(bin2dec(oxygen_data[0]) * bin2dec(co2_data[0]))

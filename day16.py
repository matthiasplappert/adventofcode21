from bitstring import BitArray
import numpy as np


def take_bits(data, n):
    out = data[:n]
    del data[:n]
    return out


def parse_header(data):
    version = take_bits(data, 3)
    type_id = take_bits(data, 3)
    return int(str(version), 2), int(str(type_id), 2)


def parse_literal(data):
    chunk = take_bits(data, 5)
    value = ""
    while chunk[0]:
        value += chunk[1:].bin
        chunk = take_bits(data, 5)
    value += chunk[1:].bin
    return int(str(value), 2)


def parse_operator(data):
    length_type_id = take_bits(data, 1)[0]
    if length_type_id:
        length = int(take_bits(data, 11).bin, 2)
    else:
        length = int(take_bits(data, 15).bin, 2)
    return length_type_id, length


def parse(data):
    version_sum = 0
    version, type_id = parse_header(data)
    version_sum += version
    if type_id == 4:
        return version_sum, (type_id, parse_literal(data))
    else:
        length_type_id, length = parse_operator(data)
        if length_type_id:
            # Length in number of packages
            values = []
            for _ in range(length):
                subversion_sum, subvalues = parse(data)
                version_sum += subversion_sum
                values.append(subvalues)
            return version_sum, (type_id, values)
        else:
            # Length in number of bits
            start_len = len(data)
            values = []
            while len(data) > start_len - length:
                subversion_sum, subvalues = parse(data)
                version_sum += subversion_sum
                values.append(subvalues)
            return version_sum, (type_id, values)


def evaluate(parsed_data):
    if isinstance(parsed_data, tuple):
        op, sub_data = parsed_data
        if op == 4:
            assert isinstance(sub_data, int)
            return sub_data

        values = evaluate(sub_data)
        if op == 0:
            return np.sum(values)
        elif op == 1:
            return np.prod(values)
        elif op == 2:
            return np.min(values)
        elif op == 3:
            return np.max(values)
        elif op == 5:
            assert len(values) == 2
            return int(values[0] > values[1])
        elif op == 6:
            assert len(values) == 2
            return int(values[0] < values[1])
        elif op == 7:
            assert len(values) == 2
            return int(values[0] == values[1])
        else:
            raise ValueError(f"unknown operator {op}")
    elif isinstance(parsed_data, list):
        return [evaluate(x) for x in parsed_data]
    else:
        raise ValueError(f"unknown type {type(parsed_data)}")


with open("day16.txt", "r") as f:
    input = BitArray(hex=f.read().strip())

version_sum, parsed_data = parse(input)

# Part 1
print(version_sum)

# Part 2
print(evaluate(parsed_data))

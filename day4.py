import numpy as np


def generate_winning_masks():
    winning_masks = []
    for i in range(5):
        mask1 = np.zeros((5, 5), dtype=bool)
        mask1[i, :] = True
        mask2 = np.zeros((5, 5), dtype=bool)
        mask2[:, i] = True
        winning_masks += [mask1, mask2]
    return winning_masks


WINNING_MASKS = generate_winning_masks()


def get_winners(masks, previous_winners):
    winners = []
    for idx, mask in enumerate(masks):
        if idx in previous_winners:
            # This guy already won, cannot win again.
            continue
        for winning_mask in WINNING_MASKS:
            if np.all((winning_mask & mask) == winning_mask):
                winners.append(idx)
    return winners


def compute_score(board, number, mask):
    unmarked_sum = np.sum(board[np.invert(mask)])
    return unmarked_sum * number


with open("day4.txt", "r") as f:
    lines = [l.strip() for l in f.readlines()]

# Parse out the draw numbers.
draw_numbers = [int(x.strip()) for x in lines[0].split(",")]
lines = lines[2:]

# Now get the boards from the remaining lines.
boards = []
while len(lines) > 0:
    board_lines = lines[:5]
    assert len(board_lines) == 5
    board = [[int(x.strip()) for x in l.split()] for l in board_lines]
    boards.append(board)
    lines = lines[6:]  # skip empty line
boards = np.array(boards)
assert boards.shape[1:] == (5, 5)
print(boards.shape)

# Figure out who won.
masks = np.zeros(boards.shape, dtype=bool)
winners, winner_numbers, winner_masks = [], [], []
for number in draw_numbers:
    masks += (boards == number)
    current_winners = get_winners(
        masks,
        previous_winners=winners,
    )
    winners += current_winners
    for winner in current_winners:
        winner_numbers.append(number)
        winner_masks.append(masks[winner].copy())

# Compute score for part 1.
print(compute_score(
    board=boards[winners[0]],
    number=winner_numbers[0],
    mask=winner_masks[0],
))

# Compute score for part 2.
print(compute_score(
    board=boards[winners[-1]],
    number=winner_numbers[-1],
    mask=winner_masks[-1],
))
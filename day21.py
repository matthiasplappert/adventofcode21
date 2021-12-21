import itertools
from collections import defaultdict
import numpy as np
from tqdm import tqdm


class DeterminsticDie:
    def __init__(self):
        self.state = 0

    def roll(self):
        r = (self.state % 100) + 1
        self.state += 1
        return r

    def roll_n(self, n):
        return [self.roll() for _ in range(n)]


def parse_player_pos(s: str) -> int:
    return int(s.strip().split(": ")[-1])


with open("day21.txt", "r") as f:
    player1_init, player2_init = map(parse_player_pos, f.readlines())

# Part 1: simulate a simple game
die = DeterminsticDie()
num_turns = 0
turn_idx = 0
players = [player1_init, player2_init]
scores = [0, 0]
while scores[0] < 1000 and scores[0] < 1000:
    num_moves = sum(die.roll_n(3))
    players[turn_idx] = ((players[turn_idx] - 1 + num_moves) % 10) + 1
    assert 1 <= players[turn_idx] <= 10
    scores[turn_idx] += players[turn_idx]
    turn_idx = (turn_idx + 1) % 2
print(min(scores) * die.state)

# Part 2
WINNING_SCORE = 21

# First, count all possible outcomes of 3 die rolls.
outcome_counts = defaultdict(int)
for outcome in itertools.product(*[[1, 2, 3]] * 3):
    outcome_counts[np.sum(outcome)] += 1

# Next, use a dict to keep track of game state counts. There's relatively
# little distinct states, just lots of them. The state looks like this:
# (((player1_pos, player1_score), (player2_pos, player2_score)), turn_idx)
game_states = defaultdict(int)
game_states[(((player1_init, 0), (player2_init, 0)), 0)] = 1

# This holds the count of states of games that have finished because one of the
# players one.
final_states = defaultdict(int)

# The basic idea of this algorithm is: keep track of unique game states with their
# counts. Pop from the dict. Go through all outcomes, create new state. Count them.
# Repeat until all game states are final.
with tqdm() as pbar:
    while len(game_states):
        (player_states, turn_idx), state_count = game_states.popitem()
        for outcome, outcome_count in outcome_counts.items():
            # Create new state for the given player.
            curr_player_state = player_states[turn_idx]
            new_pos = (curr_player_state[0] - 1 + outcome) % 10 + 1
            new_score = curr_player_state[1] + new_pos
            new_player_state = (new_pos, new_score)

            # Update game state.
            if turn_idx == 0:
                new_state = ((new_player_state, player_states[1]), (turn_idx + 1) % 2)
            else:
                new_state = ((player_states[0], new_player_state), (turn_idx + 1) % 2)

            # If won, add to final states. Otherwise re-add to game states for next round.
            if new_score >= WINNING_SCORE:
                final_states[new_state] += state_count * outcome_count
            else:
                game_states[new_state] += state_count * outcome_count
        pbar.update(1)

# Compute the number of universes that each player won.
player1_wins = 0
player2_wins = 0
for state, count in final_states.items():
    if state[0][0][1] >= WINNING_SCORE:
        player1_wins += count
    else:
        player2_wins += count
print(max(player1_wins, player2_wins))

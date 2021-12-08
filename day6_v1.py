from dataclasses import dataclass
from typing import List

from tqdm import tqdm


@dataclass
class Fish:
    state: int

    def step(self) -> List:
        new_fish = []
        if self.state == 0:
            new_fish.append(Fish(8))
            self.state = 7
        self.state -= 1
        return [self] + new_fish


@dataclass
class Swarm:
    fish: List[Fish]

    def __init__(self, initial_state: List[int]):
        self.fish = [Fish(state) for state in initial_state]

    def step(self):
        self.fish = sum(map(lambda f: f.step(), self.fish), [])

    def __str__(self) -> str:
        return ",".join(map(lambda f: str(f.state), self.fish))


with open("day6.txt") as f:
    initial_state = [int(x) for x in f.read().strip().split(",")]

swarm = Swarm(initial_state)
for _ in tqdm(range(80)):
    swarm.step()
print(len(swarm.fish))

from __future__ import annotations
from typing import List


def read_octopi() -> OctopiGrid:
    return OctopiGrid([[Octopus(int(energy)) for energy in line.strip()] for line in open('input.txt', 'r').readlines()])


def main():
    octopi_grid = read_octopi()
    print(octopi_grid)
    flashes = 0
    for i in range(0, 100):
        octopi_grid.increment_all()
        flashes += octopi_grid.count_flashes()
        octopi_grid.reset_grid()
        print()
        print(octopi_grid)
    print(flashes)

    ## Part 2
    fresh_grid = read_octopi()

    i = 0
    while not fresh_grid.all_flashed():
        fresh_grid.reset_grid()
        fresh_grid.increment_all()
        i += 1

    print(i)





class OctopiGrid:
    def __init__(self, octopi_grid: List[List[Octopus]]):
        self.octopi_grid = octopi_grid

    def __repr__(self):
        return "\n".join(["".join([octopus.energy_repr() for octopus in octopi_line]) for octopi_line in self.octopi_grid])

    def reset_grid(self):
        for octopi_line in self.octopi_grid:
            for octopus in octopi_line:
                octopus.reset_flash()

    def count_flashes(self):
        flashed_octopi = [octopus for octopi_line in self.octopi_grid for octopus in octopi_line if octopus.flashed]
        return len(flashed_octopi)

    def increment_all(self):
        for y, octopi_line in enumerate(self.octopi_grid):
            for x, _ in enumerate(octopi_line):
                self.increment_octopus(x, y)

    def all_flashed(self) -> bool:
        for octopi_line in self.octopi_grid:
            for octopus in octopi_line:
                if not octopus.flashed:
                    return False
        return True


    def increment_octopus(self, x: int, y: int):
        octopus = self.octopi_grid[y][x]
        flashed = octopus.increment()

        if flashed:
            for adjacent_x in range(max(0, x-1), min(x+2, len(self.octopi_grid[0]))):
                for adjacent_y in range (max(0, y-1), min(y+2, len(self.octopi_grid))):
                    self.increment_octopus(adjacent_x, adjacent_y)




class Octopus:

    def __init__(self, init_energy: int):
        self.flashed = False
        self.energy = init_energy

    def reset_flash(self):
        self.flashed = False

    def increment(self) -> bool:
        if not self.flashed:
            if self.energy == 9:
                self.energy = 0
                self.flashed = True
                return True
            else:
                self.energy += 1
        return False

    def energy_repr(self) -> str:
        return '*' if self.energy == 0 else str(self.energy)

    def __repr__(self):
        return f"Octopus({self.energy})"

main()

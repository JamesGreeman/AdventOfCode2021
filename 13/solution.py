from __future__ import annotations

import re
from typing import List, Tuple

point_regex = re.compile("^(\\d+),(\\d+)$")
fold_regex = re.compile("^fold along ([xy])=(\\d+)$")


def read_input() -> Tuple[List[List[str]], List[Tuple[str,int]]]:
    grid = [['.' for _ in range(0, 1350)] for _ in range(0, 900)]
    folds = []
    for line in open('input.txt', 'r').readlines():
        if point_regex.match(line):
            match = point_regex.match(line)
            x = int(match[1])
            y = int(match[2])
            grid[y][x] = '#'
        if fold_regex.match(line):
            match = fold_regex.match(line)
            folds.append((match[1], int(match[2])))
    return grid, folds


def fold(grid: List[List[str]], axis: str, line_num: int):
    if axis == 'x':
        for line in grid:
            for x in range(1, line_num + 1):
                if line[line_num + x] == '#':
                    line[line_num - x] = '#'
            while len(line) > line_num:
                line.pop(line_num)
    if axis == 'y':
        for y in range(1, line_num + 1):
            for x, value in enumerate(grid[y + line_num]):
                if value == '#':
                    grid[line_num - y][x] = '#'
        while len(grid) > line_num:
            grid.pop(line_num)


def print_grid(grid):
    print()
    print()
    print()
    for line in grid:
        print("".join(line))


def main():
    grid, folds = read_input()

    axis, line_num = folds[0]
    fold(grid, axis, line_num)
    print(len([val for line in grid for val in line if val == '#']))

    grid, folds = read_input()
    for axis, line_num in folds:
        fold(grid, axis, line_num)
        print_grid(grid)


main()
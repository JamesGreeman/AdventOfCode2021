from __future__ import annotations

import re
from typing import Tuple, Dict, List

regex = re.compile("target area: x=(\\d+)..(\\d+), y=(-?\\d+)..(-?\\d+)")


def read_input() -> Tuple[int, int, int, int]:
    line = open('input.txt', 'r').readlines()[0]
    match = regex.match(line)

    x_start = int(match[1])
    x_end = int(match[2])
    y_start = int(match[3])
    y_end = int(match[4])

    return x_start, x_end, y_start, y_end


def get_valid_x_velocities(x_start: int, x_end: int) -> Dict[int, List[int]]:
    valid_velocities = {}
    for start_vel_x in range(0, x_end + 1):
        pos_x = 0
        vel_x = start_vel_x
        for step in range(1, 1000):
            pos_x += vel_x
            if x_start <= pos_x <= x_end:
                valid_velocities.setdefault(start_vel_x, [])
                valid_velocities[start_vel_x].append(step)
            if vel_x > 0:
                vel_x -= 1
    return valid_velocities


def get_valid_y_velocities(y_start: int, y_end: int) -> Dict[int, List[int]]:
    valid_velocities = {}
    for start_vel_y in range(min(y_start, y_end), 1000):
        pos_y = 0
        vel_y = start_vel_y
        for step in range(1, 1000):
            pos_y += vel_y
            if pos_y < min(y_start, y_end):
                break
            if y_start <= pos_y <= y_end:
                valid_velocities.setdefault(start_vel_y, [])
                valid_velocities[start_vel_y].append(step)
            vel_y -= 1
    return valid_velocities


def get_intersecting_velocities(y_velocities: Dict[int, List[int]], x_velocities: Dict[int, List[int]]) -> List[Tuple[int, int]]:
    velocities = []
    for y_vel, y_steps in y_velocities.items():
        for x_vel, x_steps in x_velocities.items():
            if any([y_step in x_steps for y_step in y_steps]):
                velocities.append((x_vel, y_vel))
    return velocities


def get_max_y_for_velocity(vel_start: int) -> int:
    pos_y = 0
    while vel_start > 0:
        pos_y += vel_start
        vel_start -= 1
    return pos_y


def main():
    start_x, end_x, start_y, end_y = read_input()
    y_intersecting_steps = get_valid_y_velocities(start_y, end_y)
    print(get_max_y_for_velocity(max(y_intersecting_steps.keys())))

    x_intersecting_steps = get_valid_x_velocities(start_x, end_x)
    intersecting_velocities = get_intersecting_velocities(x_intersecting_steps, y_intersecting_steps)
    print(len(intersecting_velocities))

main()

from __future__ import annotations

import re
from typing import List

INSTRUCTION_REGEX = re.compile("(on|off) x=(-?\\d+)..(-?\\d+),y=(-?\\d+)..(-?\\d+),z=(-?\\d+)..(-?\\d+)")


def read_raw_input() -> List[Instruction]:
    return [parse_instruction(line.strip()) for line in open("input.txt") if line]


def parse_instruction(input_string: str) -> Instruction:
    groups = INSTRUCTION_REGEX.match(input_string).groups()
    
    turn_on = groups[0] == "on"
    x_1 = int(groups[1])
    x_2 = int(groups[2])
    y_1 = int(groups[3])
    y_2 = int(groups[4])
    z_1 = int(groups[5])
    z_2 = int(groups[6])

    x_range = range(min(x_1, x_2), max(x_1, x_2) + 1)
    y_range = range(min(y_1, y_2), max(y_1, y_2) + 1)
    z_range = range(min(z_1, z_2), max(z_1, z_2) + 1)

    return Instruction(turn_on, Volume(x_range, y_range, z_range))


class Instruction:

    def __init__(self, turn_on: bool, volume: Volume):
        self.turn_on = turn_on
        self.volume = volume

    def run_instruction(self, core_grid: List[List[List[bool]]]):
        normal_x = self._normalise_range(self.volume.x_range)
        normal_y = self._normalise_range(self.volume.y_range)
        normal_z = self._normalise_range(self.volume.z_range)

        print(f"{normal_x} - {normal_y} - {normal_z}")

        for x in normal_x:
            for y in normal_y:
                for z in normal_z:
                    core_grid[x][y][z] = self.turn_on

    @staticmethod
    def _normalise_range(range_to_normalise: range):
        start = max(range_to_normalise.start + 50, 0)
        end = min(range_to_normalise.stop + 50, 101)
        return range(start, end)

    def __repr__(self):
        return f"{'on' if self.turn_on else  'off'} - {self.volume}"


class Volume:

    def __init__(self, x_range: range, y_range: range, z_range: range):
        self.x_range = x_range
        self.y_range = y_range
        self.z_range = z_range

    def get_volume(self, excluded_volumes: List[Volume]) -> int:
        initial_volume = (self.x_range.stop - self.x_range.start) * \
                         (self.y_range.stop - self.y_range.start) * \
                         (self.z_range.stop - self.z_range.start)

        intersecting_volumes = [volume.get_intersection(self) for volume in excluded_volumes if volume.intersects(self)]

        processed_volumes = []
        for volume in intersecting_volumes:
            initial_volume -= volume.get_volume(processed_volumes)
            processed_volumes.append(volume)
        return initial_volume

    def intersects(self, other: Volume) -> bool:
        return self.x_range.start < other.x_range.stop and self.x_range.stop > other.x_range.start and \
               self.y_range.start < other.y_range.stop and self.y_range.stop > other.y_range.start and \
               self.z_range.start < other.z_range.stop and self.z_range.stop > other.z_range.start

    def get_intersection(self, other: Volume) -> Volume:
        return Volume(range(max(self.x_range.start, other.x_range.start), min(self.x_range.stop, other.x_range.stop)),
                      range(max(self.y_range.start, other.y_range.start), min(self.y_range.stop, other.y_range.stop)),
                      range(max(self.z_range.start, other.z_range.start), min(self.z_range.stop, other.z_range.stop)))

    def __repr__(self):
        return f"Volume({self.x_range} - {self.y_range} - {self.z_range})"


def main():
    instructions = read_raw_input()

    core_grid = [[[False for _ in range(0, 101)] for _ in range(0, 101)] for _ in range(0, 101)]
    [print(instruction) for instruction in instructions]

    for instruction in instructions:
        instruction.run_instruction(core_grid)

    number_on = sum([1 if on else 0 for x_iter in core_grid for y_iter in x_iter for on in y_iter])
    print(number_on)

    volumes_counted = []
    count_lit = 0

    instructions.reverse()
    for instruction in instructions:
        if instruction.turn_on:
            count_lit += instruction.volume.get_volume(volumes_counted)
        volumes_counted.append(instruction.volume)

    print(count_lit)


main()

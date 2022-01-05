from __future__ import annotations

import json
import re
from typing import Tuple, Dict, List, Optional

snail_number_regex = re.compile("\\[(\\d|\\[.*\\]),(\\d|\\[.*\\])\\]")


def read_raw_input() -> List[List[str]]:

    lists = []
    numbers = []

    for line in open('input.txt', 'r').readlines():
        line = line.strip()
        if not line:
            lists.append(numbers)
            numbers = []
        else:
            numbers.append(line)

    if numbers:
        lists.append(numbers)
    return lists


def read_input() -> List[List[SnailNumber]]:
    lists = []
    numbers = []

    for line in open('input.txt', 'r').readlines():
        line = line.strip()
        if not line:
            lists.append(numbers)
            numbers = []
        else:
            numbers.append(parse_input(json.loads(line)))

    if numbers:
        lists.append(numbers)
    return lists


def parse_input(input):
    if isinstance(input, list):
        left = parse_input(input[0])
        right = parse_input(input[1])

        return SnailNumber(left, right)
    return int(input)


class SnailNumber:

    def __init__(self, left, right):
        self.left = left
        self.right = right

    def add(self, another: SnailNumber):
        self.left = SnailNumber(self.left, self.right)
        self.right = another
        self._normalise()

    def _normalise(self):
        if self.try_explode():
            self._normalise()
            return
        if self.try_split():
            self._normalise()
            return

    def get_magnitude(self):
        left_mag = self.left if isinstance(self.left, int) else self.left.get_magnitude()
        right_mag = self.right if isinstance(self.right, int) else self.right.get_magnitude()

        return 3 * left_mag + 2 * right_mag

    def add_exploded_value(self, value: int, left: bool):
        next_node = self.left if left else self.right

        if isinstance(next_node, int):
            if left:
                self.left += value
            else:
                self.right += value
        else:
            next_node.add_exploded_value(value, left)

    def try_explode(self, depth: int = 0) -> Optional[Tuple[Optional[int], Optional[int]]]:
        # If any pair is nested inside four pairs, the leftmost such pair explodes.

        if depth == 4:
            return self.left, self.right

        if isinstance(self.left, SnailNumber):
            left_result = self.left.try_explode(depth + 1)
            if left_result:
                if left_result[0] is not None and left_result[1] is not None:
                    self.left = 0
                if left_result[1] is not None:
                    if isinstance(self.right, int):
                        self.right += left_result[1]
                    else:
                        self.right.add_exploded_value(left_result[1], True)
                return left_result[0], None

        if isinstance(self.right, SnailNumber):
            right_result = self.right.try_explode(depth + 1)
            if right_result:
                if right_result[0] is not None and right_result[1] is not None:
                    self.right = 0
                if right_result[0] is not None:
                    if isinstance(self.left, int):
                        self.left += right_result[0]
                    else:
                        self.left.add_exploded_value(right_result[0], False)
                return None, right_result[1]
        return None

    def try_split(self) -> bool:
        # If any regular number is 10 or greater, the leftmost such regular number splits.

        if isinstance(self.left, int):
            if self.left >= 10:
                self.left = SnailNumber(self.left // 2, (self.left + 1) // 2)
                return True
        else:
            split = self.left.try_split()
            if split:
                return True

        if isinstance(self.right, int):
            if self.right >= 10:
                self.right = SnailNumber(self.right // 2, (self.right + 1) // 2)
                return True
        else:
            split = self.right.try_split()
            if split:
                return True

        # To split a regular number, replace it with a pair; the left element of the pair should be the regular number
        # divided by two and rounded down, while the right element of the pair should be the regular number divided by
        # two and rounded up. For example, 10 becomes [5,5], 11 becomes [5,6], 12 becomes [6,6], and so on.
        return False

    def __repr__(self):
        return f"[{self.left},{self.right}]"

def find_largest_score():
    raw_numbers = read_raw_input()

    for list in raw_numbers:
        max_score = 0
        for num_a in list:
            for num_b in list:
                if num_a != num_b:
                    a = parse_input(json.loads(num_a))
                    a.add(parse_input(json.loads(num_b)))
                    mag = a.get_magnitude()
                    max_score = max(max_score, mag)
        print(list)
        print(max_score)
        print()




def main():
    snail_numbers = read_input()
    for number_list in snail_numbers:
        print()
        print(number_list)
        start = number_list[0]

        for number in number_list[1:]:
            start.add(number)

        print(start)
        print(start.get_magnitude())

    find_largest_score()


main()

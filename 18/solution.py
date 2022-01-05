from __future__ import annotations

import json
from abc import ABC, abstractmethod
from typing import Tuple, List, Optional


def read_raw_input() -> List[List[str]]:

    lists = []
    numbers = []

    for line in open('sample.txt', 'r').readlines():
        line = line.strip()
        if not line:
            lists.append(numbers)
            numbers = []
        else:
            numbers.append(line)

    if numbers:
        lists.append(numbers)
    return lists


def read_input() -> List[List[Node]]:
    return [[parse_input(json.loads(line)) for line in lines] for lines in read_raw_input()]


def parse_input(input_str) -> Node:
    if isinstance(input_str, list):
        left = parse_input(input_str[0])
        right = parse_input(input_str[1])

        return PairNode(left, right)
    return ValueNode(int(input_str))


class Node(ABC):

    @abstractmethod
    def add(self, node: Node):
        pass

    @abstractmethod
    def get_magnitude(self) -> int:
        pass

    @abstractmethod
    def get_split(self) -> Optional[PairNode] | bool:
        pass

    @abstractmethod
    def get_exploded(self, depth: int) -> Optional[Tuple[Optional[int], Optional[int]]]:
        pass

    @abstractmethod
    def add_exploded_value(self, value: int, left: bool) -> bool:
        pass


class ValueNode(Node):

    def __init__(self, value: int):
        self.value = value

    def get_magnitude(self) -> int:
        return self.value

    def add(self, node: Node):
        raise NotImplementedError("Cannot add a node to a value node")

    def get_split(self) -> Optional[PairNode] | bool:
        if self.value >= 10:
            left_value = self.value // 2
            right_value = (self.value + 1) // 2
            return PairNode(ValueNode(left_value), ValueNode(right_value))
        return None

    def get_exploded(self, depth: int) -> Optional[Tuple[Optional[int], Optional[int]]]:
        return None

    def add_exploded_value(self, value: int, left: bool) -> bool:
        self.value += value
        return True

    def __repr__(self) -> str:
        return str(self.value)


class PairNode(Node):

    def __init__(self, left: Node, right: Node):
        self.left = left
        self.right = right

    def add(self, another: Node):
        self.left = PairNode(self.left, self.right)
        self.right = another
        self._normalise()

    def _normalise(self):
        if self.get_exploded():
            self._normalise()
            return
        if self.get_split():
            self._normalise()
            return

    def get_magnitude(self):
        return 3 * self.left.get_magnitude() + 2 * self.right.get_magnitude()

    def add_exploded_value(self, value: int, left: bool) -> bool:
        node_to_add = self.left if left else self.right
        if node_to_add.add_exploded_value(value, left):
            return True
        return False

    def get_exploded(self, depth: int = 0) -> Optional[Tuple[Optional[int], Optional[int]]]:
        if depth == 4:
            # Nodes at depth 4 are always two values - so we can use the magnitude
            return self.left.get_magnitude(), self.right.get_magnitude()

        left_exploded = self.left.get_exploded(depth + 1)
        if left_exploded:
            if left_exploded[1] is not None:
                if left_exploded[0] is not None:
                    self.left = ValueNode(0)
                self.right.add_exploded_value(left_exploded[1], True)
            return left_exploded[0], None

        right_exploded = self.right.get_exploded(depth + 1)
        if right_exploded:
            if right_exploded[0] is not None:
                if right_exploded[1] is not None:
                    self.right = ValueNode(0)
                self.left.add_exploded_value(right_exploded[0], False)
            return None, right_exploded[1]
        return None

    def get_split(self) -> Optional[Node] | bool:
        left_split = self.left.get_split()
        if left_split:
            if isinstance(left_split, Node):
                self.left = left_split
            return True
        right_split = self.right.get_split()
        if right_split:
            if isinstance(right_split, Node):
                self.right = right_split
            return True
        return None

    def __repr__(self):
        return f"[{self.left},{self.right}]"


def find_largest_score():
    raw_numbers = read_raw_input()

    for num_list in raw_numbers:
        max_score = 0
        for num_a in num_list:
            for num_b in num_list:
                if num_a != num_b:
                    a = parse_input(json.loads(num_a))
                    a.add(parse_input(json.loads(num_b)))
                    mag = a.get_magnitude()
                    max_score = max(max_score, mag)
        print(num_list)
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

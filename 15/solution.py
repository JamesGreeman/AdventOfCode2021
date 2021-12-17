from __future__ import annotations

from typing import List


def read_input() -> List[List[Node]]:
    nodes = [[Node(int(value), x, y) for x, value in enumerate(line.strip())]
             for y, line in enumerate(open('input.txt', 'r').readlines())]
    start_node = nodes[0][0]
    start_node.distance_from_start = 0
    start_node.nearest_node = start_node
    return nodes


def create_repeating_grid(initial_grid: List[List[Node]]) -> List[List[Node]]:
    new_grid = []

    for grid_y in range(0, 5):
        for y, line in enumerate(initial_grid):
            row = []
            new_grid.append(row)
            y_value = grid_y * len(initial_grid) + y

            for grid_x in range(0, 5):
                for x, node in enumerate(line):
                    additional_value = grid_x + grid_y
                    x_value = grid_x * len(initial_grid[0]) + x
                    new_value = node.value + additional_value
                    if new_value > 9:
                        new_value = new_value % 10 + 1
                    row.append(Node(new_value, x_value, y_value))

    start_node = new_grid[0][0]
    start_node.distance_from_start = 0
    start_node.nearest_node = start_node

    print(len(new_grid))
    print(len(new_grid[0]))
    return new_grid


def calculate_distances(grid: List[List[Node]]):
    for i in range(1, len(grid)):
        for j in range(0, i):
            process_node(grid, grid[i][j])
            process_node(grid, grid[j][i])
        process_node(grid, grid[i][i])


def process_node(grid: List[List[Node]], node: Node):
    surrounding_nodes = node.find_processed_adjacent_nodes(grid)

    updated = False
    for surrounding_node in surrounding_nodes:
        if node.check_if_closer(surrounding_node):
            updated = True

    if updated:
        for surrounding_node in surrounding_nodes:
            process_node(grid, surrounding_node)


def main():
    nodes = read_input()

    calculate_distances(nodes)


    [print(line) for line in nodes]

    bigger_grid = create_repeating_grid(read_input())

    [print("".join([str(node.value) for node in line])) for line in bigger_grid]

    calculate_distances(bigger_grid)

    [print(line) for line in bigger_grid]

    print(bigger_grid[len(bigger_grid) - 1][len(bigger_grid[0]) -1].distance_from_start)


class Node:

    def __init__(self, value: int, x: int, y: int):
        self.value = value
        self.nearest_node = None
        self.distance_from_start = 1_000_000_000
        self.x = x
        self.y = y

    def check_if_closer(self, node) -> bool:
        if node.distance_from_start + self.value < self.distance_from_start:
            self.nearest_node = node
            self.distance_from_start = node.distance_from_start + self.value
            return True
        return False

    def find_processed_adjacent_nodes(self, grid: List[List[Node]]) -> List[Node]:
        surrounding_nodes = []
        if self.y > 0:
            surrounding_nodes.append(grid[self.y - 1][self.x])
        if self.y < len(grid) - 1:
            surrounding_nodes.append(grid[self.y + 1][self.x])
        if self.x > 0:
            surrounding_nodes.append(grid[self.y][self.x - 1])
        if self.x < len(grid[0]) - 1:
            surrounding_nodes.append(grid[self.y][self.x + 1])
        # filter out nodes that haven't been processed yet
        surrounding_nodes = list(filter(lambda node: node.nearest_node, surrounding_nodes))
        return surrounding_nodes

    def __repr__(self):
        return f"{self.value}:{self.distance_from_start if self.nearest_node else '_'}"


main()

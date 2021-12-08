
def read_positions():
    crabs = [int(value) for value in open('input.txt', 'r').readline().strip().split(",")]
    return crabs


def main():
    initial_positions = read_positions()

    # Part 1 - the median value is the cheapest to travel to
    median = sorted(initial_positions)[len(initial_positions) // 2]
    cost = simple_cost_to_position(initial_positions, median)

    print(f"Position: {median}, Cost: {cost}")

    # Part 2 - the cost is now the triangle value of the position. Trying to binary search:
    positions = sorted(initial_positions)
    lower = 0
    upper = max(positions)

    while lower < upper:
        middle_pos = lower + ((upper - lower) // 2)
        cost_a = triangle_cost_to_position(positions, middle_pos)
        cost_b = triangle_cost_to_position(positions, middle_pos + 1)
        cost_c = triangle_cost_to_position(positions, middle_pos - 1)

        if cost_a > cost_b:
            lower = middle_pos
        elif cost_a > cost_c:
            upper = middle_pos
        else:
            lower = middle_pos
            upper = middle_pos
    new_cost = triangle_cost_to_position(initial_positions, lower)

    print(f"Position: {lower}, Cost: {new_cost}")


def simple_cost_to_position(positions, target_pos):
    return sum([abs(target_pos - pos) for pos in positions])


def triangle_cost_to_position(positions, target_pos):
    return sum([get_triangle_number(abs(target_pos - pos)) for pos in positions])


def get_triangle_number(n):
    number = 0
    for i in range(0, n + 1):
        number += i
    return number


main()

from typing import List


def read_map() -> List[List[int]]:
    return [[int(num) for num in line.strip()] for line in open('input.txt', 'r').readlines()]


def get_hotspots_scores(heat_map: List[List[int]]) -> List[int]:
    hotspot_scores = []
    for y, values in enumerate(heat_map):
        for x, value in enumerate(values):
            left = heat_map[y][x - 1] if 0 <= x - 1 else 10
            right = heat_map[y][x + 1] if x + 1 < len(heat_map[y]) else 10
            up = heat_map[y - 1][x] if 0 <= y - 1else 10
            down = heat_map[y + 1][x] if y + 1 < len(heat_map) else 10
            if value < right and value < left and value < up and value < down:
                hotspot_scores.append(value + 1)
    return hotspot_scores


def find_basin_sizes(depth_map: List[List[int]]) -> List[int]:
    sizes = []
    for y, values in enumerate(depth_map):
        for x, value in enumerate(values):
            basin_size = find_connected_values(x, y, depth_map)
            if basin_size > 0:
                sizes.append(basin_size)

    return sizes

def find_connected_values(x, y, depth_map: List[List[int]]):
    if y < 0 or y >= len(depth_map):
        return 0
    if (x < 0 or x >= len(depth_map[y])):
        return 0
    if depth_map[y][x] == 9 or depth_map[y][x] == '_':
        return 0
    depth_map[y][x] = '_'
    left = find_connected_values(x-1, y, depth_map)
    right = find_connected_values(x + 1, y, depth_map)
    up = find_connected_values(x, y - 1, depth_map)
    down = find_connected_values(x, y + 1, depth_map)
    return left + right + up + down + 1

def main():
    heat_map = read_map()

    hotspot_scores = get_hotspots_scores(heat_map)

    print(sum(hotspot_scores))

    basin_sizes = sorted(find_basin_sizes(read_map()))
    length = len(basin_sizes)

    print(basin_sizes[length -1] * basin_sizes[length -2] * basin_sizes[length -3])


main()

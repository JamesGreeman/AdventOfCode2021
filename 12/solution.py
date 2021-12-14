from __future__ import annotations
from typing import List, Dict


def read_paths() -> Dict[str, List[str]]:
    paths = {}
    for line in open('input.txt', 'r').readlines():
        a,b = line.strip().split("-")
        paths.setdefault(a, [])
        paths.setdefault(b, [])
        paths[a].append(b)
        paths[b].append(a)
    return paths


def get_possible_paths(current_path: List[str],
                       paths: Dict[str, List[str]],
                       can_visit_twice: bool,
                       final_cave: str = "end") -> List[List[str]]:
    current_cave = current_path[len(current_path) - 1]
    if current_cave == final_cave:
        return [current_path]
    all_paths = []
    for cave in paths[current_cave]:
        new_path = [path for path in current_path]
        new_path.append(cave)
        if should_visit_cave(cave, current_path, can_visit_twice):
            [all_paths.append(path) for path in get_possible_paths(new_path, paths, can_visit_twice, final_cave)]
    return all_paths


def should_visit_cave(cave: str, visited_caves: List[str], can_visit_twice: bool) -> bool:
    if cave == "start":
        return False
    if cave.isupper():
        return True
    if cave not in visited_caves:
        return True
    if not can_visit_twice:
        return False
    duplicate_list = []
    for vc in visited_caves:
        if vc.islower() and vc in duplicate_list:
            return False
        duplicate_list.append(vc)
    return True


def has_visited_small_cave_twice(path: [List[str]]) -> bool:
    visited = []
    for cave in path:
        if cave.islower:
            if cave in visited:
                return True
            visited.append(cave)
    return False


def main():
    possible_paths = read_paths()

    paths = get_possible_paths(["start"], possible_paths, can_visit_twice=False)

    paths2 = get_possible_paths(["start"], possible_paths, can_visit_twice=True)

    print(len(paths))
    print(len(paths2))


main()
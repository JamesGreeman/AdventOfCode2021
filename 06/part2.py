from typing import List

def read_data():
    fish_counts = [0] * 9
    for value in open('input.txt', 'r').readline().strip().split(","):
        fish_counts[int(value)] += 1

    return fish_counts


def simulate_for_days(fish: List[int], days: int) -> List[int]:
    for _ in range(0, days):
        temp_count = fish[0]
        for i in range(0, 8):
            fish[i] = fish[i+1]
        fish[6] += temp_count
        fish[8] = temp_count
        print(fish)
    return fish


def main():
    print(sum(simulate_for_days(read_data(), 80)))
    print(sum(simulate_for_days(read_data(), 256)))


main()

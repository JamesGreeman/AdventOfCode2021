from typing import List

def read_data():
    days = [int(value) for value in open('input.txt', 'r').readline().strip().split(",")]
    fish = [LanternFish(day) for day in days]
    return fish


class LanternFish:

    def __init__(self, days_to_spawn: int):
        self.days_to_spawn = days_to_spawn

    def another_day(self):
        fish = [self]
        if self.days_to_spawn > 0:
            self.days_to_spawn -= 1
        else:
            self.days_to_spawn = 6
            new_fish = LanternFish(8)
            fish.append(new_fish)
        return fish

    def __repr__(self):
        return f"Fish({self.days_to_spawn})"


def simulate_for_days(fish: List[LanternFish], days: int) -> List[LanternFish]:
    for _ in range(0, days):
        fish = [nf for of in fish for nf in of.another_day()]
    return fish


def main():
    print(len(simulate_for_days(read_data(), 80)))


main()

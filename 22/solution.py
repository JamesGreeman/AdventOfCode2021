from __future__ import annotations

from abc import ABC, abstractmethod
from typing import List, Dict, Tuple


def read_raw_input() -> List[Player, Player]:
    lines = [line.strip() for line in open("input.txt")]
    return [Player(parse_start_pos(line)) for line in lines]


def read_starting_key() -> str:
    lines = [line.strip() for line in open("input.txt")]
    start_pos_1 = lines[0][len(lines[0]) - 1]
    start_pos_2 = lines[1][len(lines[1]) - 1]
    return f"{start_pos_1}_0_{start_pos_2}_0"


def parse_start_pos(line: str) -> int:
    return int(line[len(line) - 1])


class Player:

    def __init__(self, position: int):
        self.position = position
        self.score = 0

    def play(self, dice: Dice):
        moves = dice.roll() + dice.roll() + dice.roll()
        self.position = ((self.position + moves - 1) % 10) + 1
        self.score += self.position

    def __repr__(self) -> str:
        return f"Player(pos={self.position}, score={self.score})"


class Dice(ABC):

    @abstractmethod
    def roll(self) -> int:
        pass


class DeterministicDice(Dice):

    def __init__(self):
        self.value = 0
        self.roll_count = 0

    def roll(self) -> int:
        if self.value == 100:
            self.value = 0
        self.value += 1
        self.roll_count += 1
        return self.value


def main():
    players = read_raw_input()
    dice = DeterministicDice()
    current_player = 0
    while all([player.score < 1000 for player in players]):
        players[current_player].play(dice)
        current_player = 0 if current_player == len(players) - 1 else current_player + 1

    [print(player) for player in players]
    print(dice.roll_count)

    loser = [player for player in players if player.score < 1000][0]

    print(loser.score * dice.roll_count)

    wins = get_winning_universe_counts()
    print(wins)


def get_winning_universe_counts():
    universes_per_roll = get_universes_per_roll()
    print(universes_per_roll)
    wins = [0, 0]
    incomplete_games = {
        read_starting_key(): 1
    }
    while len(incomplete_games) > 0:
        new_games = {}
        for key, universes in incomplete_games.items():
            (p1_pos, p1_score), (p2_pos, p2_score) = parse_key(key)
            for roll, uni_count_1 in universes_per_roll.items():
                p1_end_pos = get_new_pos(p1_pos, roll)
                p1_end_score = p1_end_pos + p1_score
                if p1_end_score >= 21:
                    wins[0] += universes * uni_count_1
                else:
                    for roll_2, uni_count_2 in universes_per_roll.items():
                        p2_end_pos = get_new_pos(p2_pos, roll_2)
                        p2_end_score = p2_end_pos + p2_score
                        if p2_end_score >= 21:
                            wins[1] += universes * uni_count_1 * uni_count_2
                        else:
                            new_key = f"{p1_end_pos}_{p1_end_score}_{p2_end_pos}_{p2_end_score}"
                            new_games.setdefault(new_key, 0)
                            new_games[new_key] += universes * uni_count_1 * uni_count_2
        incomplete_games = new_games
    return wins


def get_new_pos(old_pos: int, roll: int) -> int:
    return (old_pos + roll - 1) % 10 + 1


def parse_key(key: str) -> Tuple[Tuple[int, int], Tuple[int, int]]:
    p1_pos, p1_score, p2_pos, p2_score = key.split("_")
    return (int(p1_pos), int(p1_score)), (int(p2_pos), int(p2_score))


def get_universes_per_roll() -> Dict[int, int]:

    universes = {n: 0 for n in range(1, 11)}
    for roll1 in range(1, 4):
        for roll2 in range(1, 4):
            for roll3 in range(1, 4):
                roll_val = (roll1 + roll2 + roll3)
                universes[roll_val] += 1

    return {k: v for k, v in universes.items() if v > 0}


main()

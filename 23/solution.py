from __future__ import annotations

import enum
from typing import List

LEGAL_CORRIDOR_POSITIONS = [0, 1, 3, 5, 7, 9, 10]


def read_initial_state() -> GameState:
    lines = open("input_p2.txt").readlines()
    corridor = [get_amphipod(char) for char in lines[1][1:12]]
    rooms = [[], [], [], []]
    for line in lines[2:]:
        if 'A' in line or 'B' in line or 'C' in line or 'D' in line:
            rooms[0].append(get_amphipod(line[3]))
            rooms[1].append(get_amphipod(line[5]))
            rooms[2].append(get_amphipod(line[7]))
            rooms[3].append(get_amphipod(line[9]))
    return GameState(corridor, rooms)


def get_amphipod(string: str) -> Amphipod:
    if string == 'A':
        return Amphipod.AMBER
    if string == 'B':
        return Amphipod.BRONZE
    if string == 'C':
        return Amphipod.COPPER
    if string == 'D':
        return Amphipod.DESERT
    return Amphipod.NONE


class GameState:

    def __init__(self,
                 corridor: List[Amphipod],
                 rooms: List[List[Amphipod]],
                 cost: int = 0):
        self.corridor = corridor
        self.rooms = rooms
        self.cost = cost

    def get_next_states(self) -> List[GameState]:
        states = []
        for pos, pod in enumerate(self.corridor):
            if pod is not Amphipod.NONE:
                if self.is_corridor_clear(pos, pod.target_room, True):
                    room = self.rooms[pod.target_room]
                    for room_pos, room_pod in enumerate(room):
                        if all([p is Amphipod.NONE for p in room[0:room_pos + 1]]) and \
                                (room_pos == len(room) - 1 or
                                 all([p.target_room == pod.target_room for p in room[room_pos + 1:]])):
                            states.append(self.get_new_state(pod, pos, pod.target_room, room_pos, True))
                            break

        for room_num, room in enumerate(self.rooms):
            for room_pos, pod in enumerate(room):
                if pod is not Amphipod.NONE:
                    if not all([p.target_room == room_num for p in room[room_pos:]]):
                        for corridor_pos in self.get_reachable_corridor_positions(room_num):
                            states.append(self.get_new_state(pod, corridor_pos, room_num, room_pos, False))
                    break
        return states

    def get_new_state(self,
                      pod: Amphipod,
                      corr_pos: int,
                      room_num: int,
                      room_pos: int,
                      into_room: bool) -> GameState:
        new_corr_pod = Amphipod.NONE if into_room else pod
        new_room_pod = pod if into_room else Amphipod.NONE
        new_corridor = self.new_corridor(new_corr_pod, corr_pos)
        new_rooms = self.new_rooms(new_room_pod, room_num, room_pos)
        cost = self.get_steps(corr_pos, room_num, room_pos) * pod.cost_to_move
        return GameState(new_corridor, new_rooms, self.cost + cost)

    def get_reachable_corridor_positions(self, start_room: int) -> List[int]:
        return [pos for pos in LEGAL_CORRIDOR_POSITIONS
                if self.corridor[pos] is Amphipod.NONE
                and self.is_corridor_clear(pos, start_room, False)]

    def is_corridor_clear(self, corridor_pos: int, room_num: int, into_room: bool) -> bool:
        room_corridor_pos = self.room_to_corridor_pos(room_num)
        start_pos = room_corridor_pos if room_corridor_pos < corridor_pos else \
            corridor_pos + 1 if into_room else corridor_pos
        end_pos = room_corridor_pos if room_corridor_pos > corridor_pos else \
            corridor_pos if into_room else corridor_pos + 1
        corridor_range = range(start_pos, end_pos)
        return all([self.corridor[pos] is Amphipod.NONE for pos in corridor_range])

    def new_corridor(self, new_pod: Amphipod, pos: int) -> List[Amphipod]:
        new_corridor = [pod for pod in self.corridor]
        new_corridor[pos] = new_pod
        return new_corridor

    def new_rooms(self, new_pod: Amphipod, room_num: int, pos: int) -> List[List[Amphipod]]:
        new_rooms = [[pod for pod in room] for room in self.rooms]
        new_rooms[room_num][pos] = new_pod
        return new_rooms

    def is_winning_state(self):
        return self.rooms[0][0] is Amphipod.AMBER and self.rooms[0][1] is Amphipod.AMBER \
               and self.rooms[1][0] is Amphipod.BRONZE and self.rooms[1][1] is Amphipod.BRONZE \
               and self.rooms[2][0] is Amphipod.COPPER and self.rooms[2][1] is Amphipod.COPPER \
               and self.rooms[3][0] is Amphipod.DESERT and self.rooms[3][1] is Amphipod.DESERT

    @staticmethod
    def room_to_corridor_pos(room_num: int) -> int:
        return room_num * 2 + 2

    @staticmethod
    def get_steps(corridor_pos: int, room_num: int, room_pos: int) -> int:
        return abs(corridor_pos - GameState.room_to_corridor_pos(room_num)) + room_pos + 1

    def get_layout_key(self):
        room_string = "_".join(["".join([str(pod) for pod in room]) for room in self.rooms])
        return f"{''.join([str(place) for place in self.corridor])}_{room_string}"

    def __repr__(self):
        representation = "#############\n#"
        representation += "".join([str(place) for place in self.corridor])
        representation += "#\n###"
        representation += f"{self.rooms[0][0]}#{self.rooms[1][0]}#{self.rooms[2][0]}#{self.rooms[3][0]}"
        representation += "###\n"
        for row in range(1, len(self.rooms[0])):
            representation += f"  #{self.rooms[0][row]}#" \
                              f"{self.rooms[1][row]}#" \
                              f"{self.rooms[2][row]}#" \
                              f"{self.rooms[3][row]}#\n"
        representation += "  #########"
        representation += f"\nCost: {self.cost}"
        return representation


class Amphipod(enum.Enum):

    AMBER = 0, 1, 'A'
    BRONZE = 1, 10, 'B'
    COPPER = 2, 100, 'C'
    DESERT = 3, 1000, 'D'
    NONE = -1, -1, '.'

    def __init__(self, target_room, cost_to_move, character):
        self.target_room = target_room
        self.cost_to_move = cost_to_move
        self.character = character

    def __str__(self):
        return self.character


def main():
    game_state = read_initial_state()

    print(game_state)

    # [print(state) for state in game_state.get_next_states()]
    #
    # exit()

    states = [game_state]
    costs = {}
    winning_cost = 10000000000000

    while len(states) > 0:
        state = states.pop()
        for next_state in state.get_next_states():
            if next_state.is_winning_state():
                winning_cost = min(winning_cost, next_state.cost)
            else:
                key = next_state.get_layout_key()
                if next_state.cost < costs.get(key, 100000000):
                    costs[key] = next_state.cost
                    states = [state for state in states if state.get_layout_key() != key]
                    states.append(next_state)
        states = [state for state in states if state.cost < winning_cost]

    print(winning_cost)


main()

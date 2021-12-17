from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Tuple, List


def read_input() -> List[str]:
    return [line.strip() for line in open('input.txt', 'r').readlines()]


def hex_to_binary(hex_string: str) -> str:
    prefix = ""
    for character in hex_string:
        if character == '0':
            prefix += "0000"
        else:
            break
    bit_string = bin(int(hex_string, base=16)).lstrip('0b')
    while len(bit_string) % 4 != 0:
        bit_string = "0" + bit_string
    return prefix + bit_string


def decode_packets(bit_string: str, max_packets: int = 9999) -> Tuple[List[Packet], str]:
    packets = []

    while len(bit_string) > 0 and len(packets) < max_packets:
        version = int(bit_string[:3], 2)
        p_type = int(bit_string[3:6], 2)

        if p_type == 4:
            bit_string, packet = parse_literal_packet(bit_string, version)
            packets.append(packet)
        else:
            len_type = bit_string[6]
            if len_type == '0':
                total_len = int(bit_string[7:22], 2)
                sub_packets, _ = decode_packets(bit_string[22:22+total_len])
                packets.append(OperatorPacket(version, p_type, sub_packets))
                bit_string = bit_string[22 + total_len:]
            else:
                total_packets = int(bit_string[7:18], 2)
                sub_packets, bit_string = decode_packets(bit_string[18:], total_packets)
                packets.append(OperatorPacket(version, p_type, sub_packets))

    return packets, bit_string


def parse_literal_packet(bit_string, version):
    literal_string = get_literal_string(bit_string)
    literal = int(literal_string, 2)
    packet = LiteralPacket(version, literal)
    packet_len = get_type_4_length(literal_string)
    bit_string = bit_string[packet_len:]
    return bit_string, packet


def get_literal_string(bit_string):
    index = 6
    chunks = [bit_string[index: index + 5]]
    while not chunks[len(chunks) - 1][0] == '0':
        index += 5
        chunks.append(bit_string[index:index + 5])
    literal_string = "".join(chunk[1:6] for chunk in chunks)
    return literal_string


def get_type_4_length(literal_string) -> int:
    packet_len = 6 + ((len(literal_string) // 4) * 5)
    return packet_len


def main():
    lines = read_input()
    for line in lines:
        bit_string = hex_to_binary(line)
        decoded_packet = decode_packets(bit_string, 1)[0][0]
        print(f"{line} -> {hex_to_binary(line)}")
        print(decoded_packet)
        sum_versions = sum(decoded_packet.get_all_versions())
        value = decoded_packet.get_value()
        print(f"Versions summed: {sum_versions}, Value: {value}")


class Packet(ABC):

    def __init__(self, version: int, p_type: int):
        self.version = version
        self.p_type = p_type

    @abstractmethod
    def get_all_versions(self) -> List[int]:
        pass

    @abstractmethod
    def get_value(self) -> int:
        pass


class LiteralPacket(Packet):

    def __init__(self, version: int, literal: int):
        super().__init__(version, 4)
        self.literal = literal

    def get_all_versions(self) -> List[int]:
        return [self.version]

    def get_value(self) -> int:
        return self.literal

    def __repr__(self):
        return f"LiteralPacket({self.version}:{self.literal})"


class OperatorPacket(Packet):

    def __init__(self, version: int, p_type: int, sub_packets: List[Packet]):
        super().__init__(version, p_type)
        self.sub_packets = sub_packets

    def get_all_versions(self) -> List[int]:
        sub_versions = [version for sub_packet in self.sub_packets for version in sub_packet.get_all_versions()]
        sub_versions.append(self.version)
        return sub_versions

    def get_value(self) -> int:
        if self.p_type == 0:
            return sum([packet.get_value() for packet in self.sub_packets])
        if self.p_type == 1:
            value = self.sub_packets[0].get_value()
            for packet in self.sub_packets[1:]:
                value *= packet.get_value()
            return value
        if self.p_type == 2:
            return min([packet.get_value() for packet in self.sub_packets])
        if self.p_type == 3:
            return max([packet.get_value() for packet in self.sub_packets])
        if self.p_type == 5:
            return 1 if self.sub_packets[0].get_value() > self.sub_packets[1].get_value() else 0
        if self.p_type == 6:
            return 1 if self.sub_packets[0].get_value() < self.sub_packets[1].get_value() else 0
        if self.p_type == 7:
            return 1 if self.sub_packets[0].get_value() == self.sub_packets[1].get_value() else 0
        raise NotImplementedError(f"Have not implement type: {self.p_type}")

    def __repr__(self):
        return f"OperatorPacket({self.version}:{self.p_type}:{self.sub_packets})"


main()

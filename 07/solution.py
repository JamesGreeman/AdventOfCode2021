from typing import List, Tuple


def signal_contains(signal_a, signal_b):
    return all([(letter in signal_a) for letter in signal_b])


def solve_entry(entry: Tuple[List[str], List[str]]) -> int:
    input = entry[0]
    signal_patterns = [''] * 10

    signal_patterns[1] = [signal for signal in input if len(signal) == 2][0]

    signal_patterns[4] = [signal for signal in input if len(signal) == 4][0]

    signal_patterns[7] = [signal for signal in input if len(signal) == 3][0]

    signal_patterns[8] = [signal for signal in input if len(signal) == 7][0]

    signal_patterns[9] = \
    [signal for signal in input if len(signal) == 6 and signal_contains(signal, signal_patterns[4])][0]

    signal_patterns[3] = \
    [signal for signal in input if len(signal) == 5 and signal_contains(signal, signal_patterns[7])][0]
    input = [i for i in input if i not in signal_patterns]

    signal_patterns[0] = \
    [signal for signal in input if len(signal) == 6 and signal_contains(signal, signal_patterns[7])][0]
    input = [i for i in input if i not in signal_patterns]

    signal_patterns[6] = [signal for signal in input if len(signal) == 6][0]

    signal_patterns[5] = \
    [signal for signal in input if len(signal) == 5 and signal_contains(signal_patterns[6], signal)][0]
    signal_patterns[2] = [i for i in input if i not in signal_patterns][0]

    output = resolve_out_with_signal_patterns(entry[1], signal_patterns)
    return output


def resolve_out_with_signal_patterns(output_patterns, signal_patterns):
    output = 0
    first = True
    for pattern in output_patterns:
        if not first:
            output *= 10
        match = \
            [value for value, p in enumerate(signal_patterns) if
             len(p) == len(pattern) and signal_contains(p, pattern)][0]
        output += match
        first = False
    return output


def count_all_with_sizes(input: List[Tuple[List[str], List[str]]], sizes: List[int]) -> List[Tuple[int, int]]:
    def count_with_sizes(input: List[str], sizes: List[int]) -> int:
        return len([item for item in input if len(item) in sizes])

    counts_per_line = [(count_with_sizes(i, sizes), count_with_sizes(o, sizes)) for i, o in input]

    return counts_per_line


def read_signal() -> List[Tuple[List[str], List[str]]]:
    def split_values(raw_values: str) -> List[str]:
        return raw_values.strip().split(" ")

    lines = [line.strip() for line in open('input.txt', 'r').readlines()]
    input_output_pairs = [(line.split("|")) for line in lines]
    return [(split_values(i), split_values(o)) for i, o in input_output_pairs]


def main():
    signals = read_signal()

    counts = count_all_with_sizes(signals, [2, 3, 4, 7])
    output_counts = sum([oc for _, oc in counts])
    print(output_counts)

    solved_signals = [solve_entry(entry) for entry in signals]

    print(sum(solved_signals))


main()

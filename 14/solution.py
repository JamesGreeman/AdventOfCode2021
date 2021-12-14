from __future__ import annotations

from typing import Tuple, Dict


def read_input() -> Tuple[str, Dict[str, Dict[str, str]]]:
    def parse_rule(line: str) -> Tuple[str,str,str]:
        input, output = line.split(" -> ")
        return input[0], input[1], output
    lines = [line.strip() for line in open('input.txt', 'r').readlines()]
    chain = lines[0]

    insertion_rules = {}
    for line in lines[1:]:
        if line != "":
            a, b, out = parse_rule(line)
            insertion_rules.setdefault(a, {})
            insertion_rules[a][b] = out

    return chain, insertion_rules


def get_pairs(chain: str) -> Dict[str, int]:
    pairs = {}
    for i in range(0, len(chain) - 1):
        pair = f"{chain[i]}{chain[i+1]}"
        pairs.setdefault(pair, 0)
        pairs[pair] += 1
    return pairs


def execute_rules(pairs: Dict[str, int], insertion_rules: Dict[str,Dict[str, str]]) -> Dict[str, int]:
    new_pairs = {}
    for pair, count in pairs.items():
        letter_a = pair[0]
        letter_b = pair[1]
        letter_c = insertion_rules[letter_a][letter_b]
        new_pair_a = f"{letter_a}{letter_c}"
        new_pair_b = f"{letter_c}{letter_b}"
        new_pairs.setdefault(new_pair_a, 0)
        new_pairs.setdefault(new_pair_b, 0)
        new_pairs[new_pair_a] += count
        new_pairs[new_pair_b] += count
    return new_pairs


def count_elements(initial_chain: str, pairs: Dict[str, int]) -> Dict[str, int]:
    counts = {
        initial_chain[0]: 1,
        initial_chain[len(initial_chain) - 1]: 1
    }
    for pair, count in pairs.items():
        element_a = pair[0]
        element_b = pair[1]
        counts.setdefault(element_a, 0)
        counts.setdefault(element_b, 0)
        counts[element_a] += count
        counts[element_b] += count

    return {element:count//2 for element, count in counts.items()}


def main():
    chain, insertion_rules = read_input()
    print(chain)
    print(insertion_rules)
    element_counts = run_x_times(chain, insertion_rules, 10)
    print(max(element_counts.values()) - min(element_counts.values()))
    element_counts = run_x_times(chain, insertion_rules, 40)
    print(max(element_counts.values()) - min(element_counts.values()))


def run_x_times(chain, insertion_rules, x):
    pairs = get_pairs(chain)
    for i in range(0, x):
        pairs = execute_rules(pairs, insertion_rules)
    element_counts = count_elements(chain, pairs)
    return element_counts


main()
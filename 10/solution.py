from typing import List, Optional

scores = {
    ')': 3,
    ']': 57,
    '}': 1197,
    '>': 25137
}


scores_for_unclosed = {
    '(': 1,
    '[': 2,
    '{': 3,
    '<': 4
}

opening_pair = {
    ')': '(',
    ']': '[',
    '}': '{',
    '>': '<'
}


closing_pari = {
    '(': ')',
    '[': ']',
    '{': '}',
    '<': '>'
}


def read_lines() -> List[str]:
    return [line.strip() for line in open('input.txt', 'r').readlines()]


def find_first_illegal_close(line: str) -> Optional[str]:
    stack = []
    for character in line:
        is_closing = character in scores.keys()
        if is_closing:
            most_recent_char = stack.pop()
            if not most_recent_char == opening_pair[character]:
                return character
        else:
            stack.append(character)
    return None


def get_unclosed_braces(line: str) -> Optional[List[str]]:
    stack = []
    for character in line:
        is_closing = character in scores.keys()
        if is_closing:
            most_recent_char = stack.pop()
            if not most_recent_char == opening_pair[character]:
                return None
        else:
            stack.append(character)
    return stack


def get_score_for_unclosed(unclosed_braces: List[str]) -> int:
    score = 0
    print(unclosed_braces)
    for brace in reversed(unclosed_braces):
        score *= 5
        score += scores_for_unclosed[brace]
    return score


def main():
    lines = read_lines()

    #### Part 1

    first_illegal_closes = [find_first_illegal_close(line) for line in lines]

    print(first_illegal_closes)

    all_scores = [scores[character] for character in first_illegal_closes if character]

    print(all_scores)

    print(sum(all_scores))

    ##### Part 2

    unclosed_braces = [line for line in [get_unclosed_braces(line) for line in lines] if line]

    print(unclosed_braces)

    unclosed_scores = [get_score_for_unclosed(braces) for braces in unclosed_braces]

    print(unclosed_scores)

    middle_score = sorted(unclosed_scores)[len(unclosed_scores) // 2]

    print(middle_score)


main()

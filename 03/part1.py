def total_binary_elements(input_lines):
    element_counts = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    for line in input_lines:
        line = line.strip()
        i = 0
        for char in line:
            if char == '1':
                element_counts[i] += 1
            i += 1
    return element_counts


lines = open('input.txt', 'r').readlines()

total = len(lines)

counts = total_binary_elements(lines)

delta = int(''.join(["1" if count > total / 2 else "0" for count in counts]), 2)
epsilon = 0b111111111111 ^ delta

print(f"delta: {delta},  epsilon: {epsilon}, total: {delta * epsilon}")

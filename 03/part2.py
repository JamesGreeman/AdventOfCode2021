def count_binary_elements(input_lines):
    element_counts = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    for line in input_lines:
        for (i, char) in enumerate(line):
            if char == '1':
                element_counts[i] += 1
    return element_counts


def find_value(input_lines, criteria):
    index = 0
    while index < 12 and len(input_lines) > 1:
        counts = count_binary_elements(input_lines)
        bit_filter = criteria(counts[index], len(input_lines))
        input_lines = [line for line in input_lines if line[index] == bit_filter]
        index += 1

    return int(input_lines[0], 2)


lines = [line.strip() for line in open('input.txt', 'r').readlines()]

o2 = find_value(lines, lambda count, num_lines: "1" if count >= num_lines / 2 else "0")
co2 = find_value(lines, lambda count, num_lines: "1" if count < num_lines / 2 else "0")

print(f"O2: {o2}, CO2: {co2}, rating: {o2 * co2}")

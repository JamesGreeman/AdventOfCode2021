lines = open('input.txt', 'r').readlines()

previous_depth = None
increases = 0
for line in lines:
    line = line.strip()
    current_depth = int(line)
    if previous_depth and current_depth > previous_depth:
        increases += 1
    previous_depth = current_depth
print(increases)
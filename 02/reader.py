lines = open('input.txt', 'r').readlines()

queue = []
horizontal = 0
vertical = 0
aim = 0
for line in lines:
    line = line.strip()
    (direction, size) = line.split(' ')
    size = int(size)
    if direction == 'forward':
        horizontal += size
        vertical += aim * size
    if direction == 'up':
        aim -= size
    if direction == 'down':
        aim += size
    print(f"line: {line}, h: {horizontal}, v: {vertical}, a: {aim}")
print(horizontal * vertical)

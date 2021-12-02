lines = open('input.txt', 'r').readlines()

queue = []
horizontal = 0
vertical = 0
for line in lines:
    line = line.strip()
    (direction, size) = line.split(' ')
    size = int(size)
    if direction == 'forward':
        horizontal += size
    if direction == 'up':
        vertical -= size
    if direction == 'down':
        vertical += size
print(horizontal * vertical)

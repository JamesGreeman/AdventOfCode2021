lines = open('input.txt', 'r').readlines()

queue = []
increases = 0
for line in lines:
    line = line.strip()
    if not line == '':
        print(queue)
        current_depth = int(line)
        if len(queue) == 3:
            current_size = sum(queue)
            queue.pop(0)
            queue.append(current_depth)
            new_size = sum(queue)
            if new_size > current_size:
                increases += 1
        else:
            queue.append(int(line))
print(len(lines))
print(increases)
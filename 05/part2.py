def read_data():
    lines = [line.strip() for line in open('input.txt', 'r').readlines()]

    lines = [process_line(line) for line in lines]
    return lines


def process_line(line):
    point1, point2 = line.split("->")
    return Line(process_point(point1), process_point(point2))


def process_point(point):
    x, y = point.strip().split(",")
    return Point(int(x), int(y))


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return f"Point(x: {self.x}, y: {self.y})"

class Line:
    def __init__(self, start: Point, end: Point):
        self.start = start
        self.end = end

    def is_horizontal(self):
        return self.start.y == self.end.y

    def is_vertical(self):
        return self.start.x == self.end.x

    def get_all_points_in_line(self):

        x_increment = 1 if self.start.x < self.end.x else -1 if self.start.x > self.end.x else 0
        y_increment = 1 if self.start.y < self.end.y else -1 if self.start.y > self.end.y else 0

        points = []

        x = self.start.x
        y = self.start.y

        line_length = max(abs(self.start.x - self.end.x), abs(self.start.y - self.end.y)) + 1
        for i in range(0, line_length):
            points.append(Point(x, y))
            x += x_increment
            y += y_increment

        return points

    def __repr__(self):
        return f"Line({self.start}, {self.end})"


def createMap():
    vent_map = []
    for i in range(0, 1000):
        line = []
        for i in range(0, 1000):
            line.append(0)
        vent_map.append(line)
    return vent_map


def count_intersections(vent_map):
    return len([point for line in vent_map for point in line if point > 1])


def main():
    lines = read_data()

    vent_map = createMap()

    for line in lines:
        for point in line.get_all_points_in_line():
            vent_map[point.x][point.y] += 1

    print(count_intersections(vent_map))


main()

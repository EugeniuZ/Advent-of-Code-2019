from collections import namedtuple

Point = namedtuple('Point', 'x, y')


class Segment:
    def __init__(self, p1, p2):
        self.p1 = p1
        self.p2 = p2
        if p1.x == p2.x:
            self.d = '-'
            self.c = p1.x
            self.start = min(p1.y, p2.y)
            self.end = max(p1.y, p2.y)
        elif p1.y == p2.y:
            self.d = '|'
            self.c = p1.y
            self.start = min(p1.x, p2.x)
            self.end = max(p1.x, p2.x)
        else:
            raise Exception(f'Invalid segment ({p1}, {p2}): must be vertical or horizontal')

    def intersect(self, other):
        # parallel lines
        if self.d == other.d:
            if self.c == other.c:
                if self.start >= other.start:
                    other, self = self, other
                # maybe common segment if range is not empty
                if self.start <= other.start <= self.end:
                    end = 1 + min(self.end, other.end)
                    if self.d == '-':
                        return {Point(self.c, y) for y in range(other.start, end)}
                    if self.d == '|':
                        return {Point(x, self.c) for x in range(other.start, end)}
        # perpendicular lines
        else:
            if self.start <= other.c <= self.end and other.start <= self.c <= other.end:
                # point intersection
                return {Point(self.c, other.c)} if self.d == '-' else {Point(other.c, self.c)}
        return set()

    def __contains__(self, point):
        return \
            (self.c == point.x and self.d == '-' and self.start <= point.y <= self.end) \
            or \
            (self.c == point.y and self.d == '|' and self.start <= point.x <= self.end)

    def __eq__(self, other):
        return self.p1 == other.p1 and self.p2 == other.p2

    def __repr__(self):
        return f'Segment({self.p1}, {self.p2})'


def read_input(filename):
    with open(filename) as f:
        line1, line2 = f.readlines()
        return _wire_to_coordinates(line1.split(',')), _wire_to_coordinates(line2.split(','))


def test_solution1():
    # s2 included in s1
    s1 = Segment(Point(0, 0), Point(3, 0))
    s2 = Segment(Point(1, 0), Point(2, 0))
    assert {Point(x, 0) for x in range(s1.start, s1.end + 1)} == s1.intersect(s1)
    assert {Point(1, 0), Point(2, 0)} == s1.intersect(s2)
    assert {Point(1, 0), Point(2, 0)} == s2.intersect(s1)

    s1 = Segment(Point(0, 0), Point(0, 3))
    s2 = Segment(Point(0, 1), Point(0, 2))
    assert {Point(0, 1), Point(0, 2)} == s1.intersect(s2)
    assert {Point(0, 1), Point(0, 2)} == s2.intersect(s1)

    # s2 partial overlap with s1
    s1 = Segment(Point(0, 0), Point(3, 0))
    s2 = Segment(Point(1, 0), Point(5, 0))
    assert {Point(1, 0), Point(2, 0), Point(3, 0)} == s1.intersect(s2)

    # point intersection
    s1 = Segment(Point(0, 0), Point(3, 0))
    s2 = Segment(Point(0, 0), Point(0, 3))
    assert {Point(0, 0)} == s1.intersect(s2)

    s1 = Segment(Point(0, 0), Point(3, 0))
    s2 = Segment(Point(1, 0), Point(1, 5))
    assert {Point(1, 0)} == s1.intersect(s2)

    s1 = Segment(Point(3, 2), Point(7, 2))
    s2 = Segment(Point(5, 0), Point(5, 10))
    assert {Point(5, 2)} == s1.intersect(s2)

    # no intersections

    s1 = Segment(Point(0, 0), Point(3, 0))
    s2 = Segment(Point(6, 0), Point(15, 0))
    assert not s1.intersect(s2)

    s1 = Segment(Point(0, 0), Point(3, 0))
    s2 = Segment(Point(1, 1), Point(2, 1))
    assert not s1.intersect(s2)

    w1 = _wire_to_coordinates('R8,U5,L5,D3'.split(','))
    w2 = _wire_to_coordinates('U7,R6,D4,L4'.split(','))
    expected = [
        Segment(Point(1, 0), Point(8, 0)),
        Segment(Point(8, 1), Point(8, 5)),
        Segment(Point(7, 5), Point(3, 5)),
        Segment(Point(3, 4), Point(3, 2))
    ]
    assert expected == w1
    assert 6 == solution1((w1, w2))

    w1 = _wire_to_coordinates('R75,D30,R83,U83,L12,D49,R71,U7,L72'.split(','))
    w2 = _wire_to_coordinates('U62,R66,U55,R34,D71,R55,D58,R83'.split(','))
    assert 159 == solution1((w1, w2))

    w1 = _wire_to_coordinates('R98,U47,R26,D63,R33,U87,L62,D20,R33,U53,R51'.split(','))
    w2 = _wire_to_coordinates('U98,R91,D20,R16,D67,R40,U7,R15,U6,R7'.split(','))
    assert 135 == solution1((w1, w2))


def _wire_to_coordinates(wire):
    x = 0
    y = 0
    result = []
    for spec in wire:
        direction, length = spec[0], int(spec[1:])
        if direction == 'R':
            result.append(Segment(Point(x + 1, y), Point(x + length, y)))
            x += length
        elif direction == 'L':
            result.append(Segment(Point(x - 1, y), Point(x - length, y)))
            x -= length
        elif direction == 'U':
            result.append(Segment(Point(x, y + 1), Point(x, y + length)))
            y += length
        elif direction == 'D':
            result.append(Segment(Point(x, y - 1), Point(x, y - length)))
            y -= length
        else:
            raise Exception(f'Unknown direction: {direction}')
    return result


def _intersect_wires(wire1, wire2):
    result = set()
    for s1 in wire1:
        for s2 in wire2:
            p = s1.intersect(s2)
            result = result.union(p)
    return result


def solution1(wires):
    crossings = _intersect_wires(*wires)
    point = min(crossings, key=lambda p1: abs(p1[0]) + abs(p1[1]))
    return abs(point[0]) + abs(point[1])


def _path_len(point, wire):
    path_len = 0
    for segment in wire:
        if point in segment:
            return path_len + 1 + (abs(segment.p1.y - point.y) if segment.d == '-' else abs(segment.p1.x - point.x))
        path_len += segment.end - segment.start + 1
    raise Exception(f'Point {point} does not belong to wire {wire}')


def test_solution2():
    w1 = _wire_to_coordinates('R8,U5,L5,D3'.split(','))
    w2 = _wire_to_coordinates('U7,R6,D4,L4'.split(','))
    assert 30 == solution2((w1, w2))

    w1 = _wire_to_coordinates('R75,D30,R83,U83,L12,D49,R71,U7,L72'.split(','))
    w2 = _wire_to_coordinates('U62,R66,U55,R34,D71,R55,D58,R83'.split(','))
    assert 610 == solution2((w1, w2))

    w1 = _wire_to_coordinates('R98,U47,R26,D63,R33,U87,L62,D20,R33,U53,R51'.split(','))
    w2 = _wire_to_coordinates('U98,R91,D20,R16,D67,R40,U7,R15,U6,R7'.split(','))
    assert 410 == solution2((w1, w2))


def solution2(wires):
    wire1, wire2 = wires
    crossings = _intersect_wires(wire1, wire2)
    point = min(crossings, key=lambda p: _path_len(p, wire1) + _path_len(p, wire2))
    return _path_len(point, wire1) + _path_len(point, wire2)

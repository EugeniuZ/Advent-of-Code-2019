from collections import namedtuple

Point = namedtuple('Point', 'x, y')


class Segment:
    def __init__(self, p1, p2):
        self.p1 = p1
        self.p2 = p2
        if p1.x == p2.x:
            self.t = 'x'
            self.c = p1.x
            self.start = min(p1.y, p2.y)
            self.end = max(p1.y, p2.y)
        elif p1.y == p2.y:
            self.t = 'y'
            self.c = p1.y
            self.start = min(p1.x, p2.x)
            self.end = max(p1.x, p2.x)
        else:
            raise Exception(f'Invalid segment ({p1}, {p2}): must be vertical or horizontal')

    def __eq__(self, other):
        return self.p1 == other.p1 and self.p2 == other.p2

    def __repr__(self):
        return f'Segment({self.p1}, {self.p2})'


def read_input(filename):
    with open(filename) as f:
        line1, line2 = f.readlines()
        return line1.split(','), line2.split(',')


def test_solution1():

    # s2 included in s1
    s1 = Segment(Point(0, 0), Point(3, 0))
    s2 = Segment(Point(1, 0), Point(2, 0))
    assert {Point(1, 0), Point(2, 0)} == _intersect_segments(s1, s2)
    assert {Point(1, 0), Point(2, 0)} == _intersect_segments(s2, s1)

    s1 = Segment(Point(0, 0), Point(0, 3))
    s2 = Segment(Point(0, 1), Point(0, 2))
    assert {Point(0, 1), Point(0, 2)} == _intersect_segments(s1, s2)
    assert {Point(0, 1), Point(0, 2)} == _intersect_segments(s2, s1)

    # s2 partial overlap with s1
    s1 = Segment(Point(0, 0), Point(3, 0))
    s2 = Segment(Point(1, 0), Point(5, 0))
    assert {Point(1, 0), Point(2, 0), Point(3, 0)} == _intersect_segments(s1, s2)

    # point intersection
    s1 = Segment(Point(0, 0), Point(3, 0))
    s2 = Segment(Point(0, 0), Point(0, 3))
    assert {Point(0, 0)} == _intersect_segments(s1, s2)

    s1 = Segment(Point(0, 0), Point(3, 0))
    s2 = Segment(Point(1, 0), Point(1, 5))
    assert {Point(1, 0)} == _intersect_segments(s1, s2)

    s1 = Segment(Point(3, 2), Point(7, 2))
    s2 = Segment(Point(5, 0), Point(5, 10))
    assert {Point(5, 2)} == _intersect_segments(s1, s2)

    # no intersections

    s1 = Segment(Point(0, 0), Point(3, 0))
    s2 = Segment(Point(6, 0), Point(15, 0))
    assert not _intersect_segments(s1, s2)

    s1 = Segment(Point(0, 0), Point(3, 0))
    s2 = Segment(Point(1, 1), Point(2, 1))
    assert not _intersect_segments(s1, s2)


    w1 = 'R8,U5,L5,D3'.split(',')
    w2 = 'U7,R6,D4,L4'.split(',')
    assert [
               Segment(Point(1, 0), Point(8, 0)),
               Segment(Point(8, 1), Point(8, 5)),
               Segment(Point(7, 5), Point(3, 5)),
               Segment(Point(3, 4), Point(3, 2))
    ] == _wire_to_coordinates(w1)
    assert 6 == solution1((w1, w2))

    w1 = 'R75,D30,R83,U83,L12,D49,R71,U7,L72'.split(',')
    w2 = 'U62,R66,U55,R34,D71,R55,D58,R83'.split(',')
    assert 159 == solution1((w1, w2))

    w1 = 'R98,U47,R26,D63,R33,U87,L62,D20,R33,U53,R51'.split(',')
    w2 = 'U98,R91,D20,R16,D67,R40,U7,R15,U6,R7'.split(',')
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
            raise Exception(f'Unknown direction: {d}')
    return result


def _intersect_segments(segment1, segment2):
    # parallel lines
    if segment1.t == segment2.t:
        if segment1.c == segment2.c:
            if segment1.start >= segment2.start:
                segment2, segment1 = segment1, segment2
            # maybe common segment if range is not empty
            if segment1.start <= segment2.start <= segment1.end:
                end = 1 + min(segment1.end, segment2.end)
                if segment1.t == 'x':
                    return {Point(segment1.c, y) for y in range(segment2.start, end)}
                if segment1.t == 'y':
                    return {Point(x, segment1.c) for x in range(segment2.start, end)}
    # perpendicular lines
    else:
        if segment1.start <= segment2.c <= segment1.end and segment2.start <= segment1.c <= segment2.end:
            # point intersection
            return {Point(segment1.c, segment2.c)} if segment1.t == 'x' else {Point(segment2.c, segment1.c)}
    return set()


def _intersect_wires(wc1, wc2):
    result = set()
    for s1 in wc1:
        for s2 in wc2:
            p = _intersect_segments(s1, s2)
            result = result.union(p)
    return result


def solution1(wires):
    wire1, wire2 = wires
    wc1 = _wire_to_coordinates(wire1)
    wc2 = _wire_to_coordinates(wire2)
    crossings = _intersect_wires(wc1, wc2)
    pt = min(crossings, key=lambda p1: abs(p1[0]) + abs(p1[1]))
    return abs(pt[0]) + abs(pt[1])


def _path_len(point, wc):
    path_len = 0
    for s in wc:
        if s.c == point.x and s.t == 'x' and s.start <= point.y <= s.end:
            return path_len + abs(s.p1.y - point.y) + 1
        elif s.c == point.y and s.t == 'y' and s.start <= point.x <= s.end:
            return path_len + abs(s.p1.x - point.x) + 1
        else:
            path_len += s.end - s.start + 1
    raise Exception(f'Point {point} does not belong to wire {wire}')


def test_solution2():
    w1 = 'R8,U5,L5,D3'.split(',')
    w2 = 'U7,R6,D4,L4'.split(',')
    assert 30 == solution2((w1, w2))

    w1 = 'R75,D30,R83,U83,L12,D49,R71,U7,L72'.split(',')
    w2 = 'U62,R66,U55,R34,D71,R55,D58,R83'.split(',')
    assert 610 == solution2((w1, w2))

    w1 = 'R98,U47,R26,D63,R33,U87,L62,D20,R33,U53,R51'.split(',')
    w2 = 'U98,R91,D20,R16,D67,R40,U7,R15,U6,R7'.split(',')
    assert 410 == solution2((w1, w2))


def solution2(wires):
    wire1, wire2 = wires
    wc1 = _wire_to_coordinates(wire1)
    wc2 = _wire_to_coordinates(wire2)
    crossings = _intersect_wires(wc1, wc2)
    pt = min(crossings, key=lambda p: _path_len(p, wc1) + _path_len(p, wc2))
    return _path_len(pt, wc1) + _path_len(pt, wc2)

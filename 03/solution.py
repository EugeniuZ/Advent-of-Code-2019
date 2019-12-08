def read_input(filename):
    with open(filename) as f:
        line1, line2 = f.readlines()
        return line1.split(','), line2.split(',')


def test_solution1():
    w1 = 'R8,U5,L5,D3'.split(',')
    w2 = 'U7,R6,D4,L4'.split(',')
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
    result = set()
    for spec in wire:
        d, l = spec[0], int(spec[1:])
        if d in 'RL':
            delta = 1 if d == 'R' else -1
            for _ in range(l):
                x += delta
                result.add((x, y))
        elif d in 'UD':
            delta = 1 if d == 'U' else -1
            for _ in range(l):
                y += delta
                result.add((x, y))
    return result


def solution1(wires):
    wire1, wire2 = wires
    wc1 = _wire_to_coordinates(wire1)
    wc2 = _wire_to_coordinates(wire2)
    crossings = wc1.intersection(wc2)
    pt = min(crossings, key=lambda p1: abs(p1[0]) + abs(p1[1]))
    return abs(pt[0]) + abs(pt[1])


def _path_len(point, wire):
    if point == (0, 0):
        return 0

    x = 0
    y = 0
    result = 0
    for spec in wire:
        d, l = spec[0], int(spec[1:])
        if d in 'RL':
            delta = 1 if d == 'R' else -1
            for _ in range(l):
                x += delta
                result += 1
                if (x, y) == point:
                    return result
        elif d in 'UD':
            delta = 1 if d == 'U' else -1
            for _ in range(l):
                y += delta
                result += 1
                if (x, y) == point:
                    return result
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
    crossings = wc1.intersection(wc2)
    pt = min(crossings, key=lambda p: _path_len(p, wire1) + _path_len(p, wire2))
    return _path_len(pt, wire1) + _path_len(pt, wire2)

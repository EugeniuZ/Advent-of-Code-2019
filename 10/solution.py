from collections import defaultdict, namedtuple
from sys import float_info

Asteroid = namedtuple('Asteroid', 'x,y')
Station = namedtuple('Station', 'asteroids,station')

ASTEROID = '#'
EMPTY = '.'

HORIZONTAL_POS_SLOPE = float_info.min
HORIZONTAL_NEG_SLOPE = -HORIZONTAL_POS_SLOPE
VERTICAL_NEG_SLOPE = float('-inf')


def _read_map(data):
    asteroids = set()
    data = data.strip()
    for y, line in enumerate(data.splitlines()):
        for x, c in enumerate(line):
            if c == ASTEROID:
                asteroids.add(Asteroid(x=x, y=y))
    return asteroids


def read_input(filename):
    with open(filename) as f:
        return _read_map(f.read())


def _quadrant(destination, source):
    # clockwise numeration
    if destination.x == source.x:
        return 1 if destination.y < source.y else 3
    if destination.y == source.y:
        return 2 if destination.x > source.x else 4
    if destination.x > source.x:
        return 1 if destination.y < source.y else 2
    return 3 if destination.y >= source.y else 4  # a.x < s.x


def _make_line_slopes(asteroids):
    result = {a: defaultdict(set) for a in asteroids}
    l_asteroids = list(asteroids)
    for i, station in enumerate(l_asteroids):
        for asteroid in l_asteroids[i+1:]:  # sorting by distance makes the solution slower
            if asteroid.x == station.x:
                # tricky logic, no VERTICAL_POS_SLOPE because clockwise quadrant 3 traversal goes
                # from +inf to -inf instantly
                slope = VERTICAL_NEG_SLOPE
                result[station][slope, _quadrant(asteroid, station)].add(asteroid)
                result[asteroid][slope, _quadrant(station, asteroid)].add(station)
            elif asteroid.y == station.y:
                slope = HORIZONTAL_POS_SLOPE if asteroid.x > station.x else HORIZONTAL_NEG_SLOPE
                result[station][slope, _quadrant(asteroid, station)].add(asteroid)
                result[asteroid][-slope, _quadrant(station, asteroid)].add(station)
            else:
                # slope calculation can be made with Fraction but is 20x times slower, esp. due to __hash__
                slope = (asteroid.y - station.y) / (asteroid.x - station.x)
                result[station][slope, _quadrant(asteroid, station)].add(asteroid)
                result[asteroid][slope, _quadrant(station, asteroid)].add(station)
    return result


def _test_quadrant():
    station = Asteroid(x=2, y=2)
    for asteroid, quadrant in [
        (Asteroid(x=2, y=1), 1),
        (Asteroid(x=3, y=1), 1),
        (Asteroid(x=3, y=2), 2),
        (Asteroid(x=3, y=3), 2),
        (Asteroid(x=2, y=3), 3),
        (Asteroid(x=1, y=3), 3),
        (Asteroid(x=1, y=2), 4),
        (Asteroid(x=1, y=1), 4),
    ]:
        assert quadrant == _quadrant(asteroid, station)


def test_solution1():
    _test_quadrant()
    asteroid_map = """
.#..#
.....
#####
....#
...##
"""
    assert Station(asteroids=8, station=Asteroid(3, 4)) == solution1(_read_map(asteroid_map))

    asteroid_map = """
......#.#.
#..#.#....
..#######.
.#.#.###..
.#..#.....
..#....#.#
#..#....#.
.##.#..###
##...#..#.
.#....####
"""
    assert Station(asteroids=33, station=Asteroid(5, 8)) == solution1(_read_map(asteroid_map))

    asteroid_map = """
#.#...#.#.
.###....#.
.#....#...
##.#.#.#.#
....#.#.#.
.##..###.#
..#...##..
..##....##
......#...
.####.###.
"""
    assert Station(asteroids=35, station=Asteroid(1, 2)) == solution1(_read_map(asteroid_map))

    asteroid_map = """
.#..#..###
####.###.#
....###.#.
..###.##.#
##.##.#.#.
....###..#
..#.#..#.#
#..#.#.###
.##...##.#
.....#.#..
"""
    assert Station(asteroids=41, station=Asteroid(6, 3)) == solution1(_read_map(asteroid_map))

    asteroid_map = """
.#..##.###...#######
##.############..##.
.#.######.########.#
.###.#######.####.#.
#####.##.#.##.###.##
..#####..#.#########
####################
#.####....###.#.#.##
##.#################
#####.##.###..####..
..######..##.#######
####.##.####...##..#
.#####..#.######.###
##...#.##########...
#.##########.#######
.####.#.###.###.#.##
....##.##.###..#####
.#.#.###########.###
#.#.#.#####.####.###
###.##.####.##.#..##
"""
    assert Station(asteroids=210, station=Asteroid(x=11, y=13)) == solution1(_read_map(asteroid_map))


def solution1(asteroids):
    slope_data = _make_line_slopes(asteroids)
    monitoring_station = max(slope_data, key=lambda a: len(slope_data[a]))
    # for each (slope, quandrant) combination there is a visible asteroid by definition
    return Station(asteroids=len(slope_data[monitoring_station]), station=monitoring_station)


def test_solution2():
    small_map = '''
.#....#####...#..
##...##.#####..##
##...#...#.#####.
..#.....#...###..
..#.#.....#....##
'''
    asteroids = _read_map(small_map)
    station = Asteroid(x=8, y=3)
    asteroid_iter = _solution2_iter(asteroids, station)
    for asteroid, n_asteroid in [
        (Asteroid(x=8, y=1), 1),
        (Asteroid(x=9, y=0), 2),
        (Asteroid(x=9, y=1), 3),
        (Asteroid(x=10, y=0), 4),
        (Asteroid(x=9, y=2), 5),
        (Asteroid(x=11, y=1), 6),
        (Asteroid(x=12, y=1), 7),
        (Asteroid(x=11, y=2), 8),
        (Asteroid(x=15, y=1), 9),
        (Asteroid(x=12, y=2), 10),
        (Asteroid(x=13, y=2), 11),
        (Asteroid(x=14, y=2), 12),
        (Asteroid(x=15, y=2), 13),
        (Asteroid(x=12, y=3), 14),
        (Asteroid(x=16, y=4), 15),
        (Asteroid(x=15, y=4), 16),
        (Asteroid(x=10, y=4), 17),
        (Asteroid(x=4, y=4), 18),
        (Asteroid(x=2, y=4), 19),
        (Asteroid(x=2, y=3), 20),
        (Asteroid(x=0, y=2), 21),
        (Asteroid(x=1, y=2), 22),
        (Asteroid(x=0, y=1), 23),
        (Asteroid(x=1, y=1), 24),
        (Asteroid(x=5, y=2), 25),
        (Asteroid(x=1, y=0), 26),
        (Asteroid(x=5, y=1), 27),
        (Asteroid(x=6, y=1), 28),
        (Asteroid(x=6, y=0), 29),
        (Asteroid(x=7, y=0), 30),
        (Asteroid(x=8, y=0), 31),
        (Asteroid(x=10, y=1), 32),
        (Asteroid(x=14, y=0), 33),
        (Asteroid(x=16, y=1), 34),
        (Asteroid(x=13, y=3), 35),
        (Asteroid(x=14, y=3), 36),
    ]:
        assert asteroid.x * 100 + asteroid.y == next(asteroid_iter)

    big_map = '''
.#..##.###...#######
##.############..##.
.#.######.########.#
.###.#######.####.#.
#####.##.#.##.###.##
..#####..#.#########
####################
#.####....###.#.#.##
##.#################
#####.##.###..####..
..######..##.#######
####.##.####...##..#
.#####..#.######.###
##...#.##########...
#.##########.#######
.####.#.###.###.#.##
....##.##.###..#####
.#.#.###########.###
#.#.#.#####.####.###
###.##.####.##.#..##
'''
    asteroids = _read_map(big_map)
    station = Asteroid(x=11, y=13)
    asteroid_iter = _solution2_iter(asteroids, station)
    i_n = 0
    for asteroid, n_asteroid in [
        (Asteroid(x=11, y=12), 1),
        (Asteroid(x=12, y=1), 2),
        (Asteroid(x=12, y=2), 3),
        (Asteroid(x=12, y=8), 10),
        (Asteroid(x=16, y=0), 20),
        (Asteroid(x=16, y=9), 50),
        (Asteroid(x=10, y=16), 100),
        (Asteroid(x=9, y=6), 199),
        (Asteroid(x=8, y=2), 200),
        (Asteroid(x=10, y=9), 201),
        (Asteroid(x=11, y=1), 299),
    ]:
        while True:
            i_n += 1
            if i_n == n_asteroid:
                assert asteroid.x * 100 + asteroid.y == next(asteroid_iter)
                break
            next(asteroid_iter)


def _solution2_iter(asteroids, station):
    slope_data_station = _make_line_slopes(asteroids)[station]
    for (slope, quadrant), asteroids_in_direction in slope_data_station.items():
        slope_data_station[slope, quadrant] = sorted(
            asteroids_in_direction,
            # visible items are put at the end of the list for faster removal from end
            key=lambda a: - (abs(a.x - station.x) + abs(a.y - station.y))
        )
    asteroid_iterator = sorted(slope_data_station, key=lambda t: (t[1], t[0]))
    vaporized_asteroid = True
    while vaporized_asteroid:
        vaporized_asteroid = None
        for key in asteroid_iterator:
            if slope_data_station[key]:
                vaporized_asteroid = slope_data_station[key].pop()
                yield vaporized_asteroid.x * 100 + vaporized_asteroid.y


def solution2(asteroids, station=Asteroid(x=19, y=11), n_asteroid=200):
    if n_asteroid is None:
        n_asteroid = len(asteroids) - 1  # exclude the station itself
    for i, coordinate in enumerate(_solution2_iter(asteroids, station), start=1):
        if i == n_asteroid:
            return coordinate
    raise ValueError(f'No asteroid with number {n_asteroid} found in {asteroids}')

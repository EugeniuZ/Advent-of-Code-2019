from collections import defaultdict, deque

def read_input(filename):
    with open(filename) as f:
        return _read_orbits(f.read())

def _read_orbits(input_data):
    orbits = {}
    for line in input_data.splitlines():
        obj, satellite = line.split(')')
        orbits[satellite] = obj
    return orbits


def test_solution1():
    test_case = """COM)B
B)C
C)D
D)E
E)F
B)G
G)H
D)I
E)J
J)K
K)L"""
    assert 42 == solution1(_read_orbits(test_case))


def solution1(orbits):
    children = defaultdict(list)
    for satellite, parent in orbits.items():
        children[parent].append(satellite)
    queue = deque([('COM', 0)])
    n_orbits = 0
    while queue:
        obj, depth = queue.pop()
        n_orbits += depth
        if children[obj]:
            for satellite in children[obj]:
                queue.append((satellite, depth + 1))
    return n_orbits


def test_solution2():
    test_case = """COM)B
B)C
C)D
D)E
E)F
B)G
G)H
D)I
E)J
J)K
K)L
K)YOU
I)SAN"""

    assert 4 == solution2(_read_orbits(test_case))


def solution2(orbits):
    orbital_transfers_you = {}
    ancestor_you = orbits['YOU']
    n_transfers_you = 0
    orbital_transfers_santa = {}
    ancestor_santa = orbits['SAN']
    n_transfers_santa = 0

    while ancestor_you != 'COM' or ancestor_santa != 'COM':
        if ancestor_you != 'COM':
            ancestor_you = orbits[ancestor_you]
            n_transfers_you += 1
            orbital_transfers_you[ancestor_you] = n_transfers_you
            if ancestor_you in orbital_transfers_santa:
                return n_transfers_you + orbital_transfers_santa[ancestor_you]

        if ancestor_santa != 'COM':
            ancestor_santa = orbits[ancestor_santa]
            n_transfers_santa += 1
            orbital_transfers_santa[ancestor_santa] = n_transfers_santa
            if ancestor_santa in orbital_transfers_you:
                return n_transfers_santa + orbital_transfers_you[ancestor_santa]

    return orbital_transfers_you['COM'] + orbital_transfers_santa['COM']

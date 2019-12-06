from functools import lru_cache
from math import log


def read_input(filename):
    with open(filename) as f:
        return [int(line) for line in f]


def test_solution1():
    assert 2 == solution1([12])
    assert 2 == solution1([14])
    assert 654 == solution1([1969])
    assert 33583 == solution1([100756])


@lru_cache(maxsize=1000)
def fuel(module_mass):
    return int(module_mass / 3) - 2


@lru_cache(maxsize=1000)
def fuel_full(module_mass):
    result = 0
    while True:
        module_mass = fuel(module_mass)
        if module_mass <= 0:
            break
        result += module_mass
    return result


def solution1(module_masses):
    return sum(fuel(mass) for mass in module_masses)


def test_solution2():
    assert 2 == solution2([14])
    assert 966 == solution2([1969])
    assert 50346 == solution2([100756])
    assert 968 == solution2([14, 1969])


def solution2(module_masses):
    return sum(fuel_full(mass) for mass in module_masses)

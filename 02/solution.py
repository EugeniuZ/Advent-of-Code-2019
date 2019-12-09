import bisect

OPCODE_ADD = 1
OPCODE_MULTIPLY = 2
OPCODE_HALT = 99
OUTPUT = 19690720


def read_input(filename):
    with open(filename) as f:
        return [int(num) for num in f.read().split(',')]


def _execute(ip, program):
    if program[ip] == OPCODE_ADD:
        program[program[ip + 3]] = program[program[ip + 1]] + program[program[ip + 2]]
        return ip + 4
    if program[ip] == OPCODE_MULTIPLY:
        program[program[ip + 3]] = program[program[ip + 1]] * program[program[ip + 2]]
        return ip + 4
    if program[ip] == OPCODE_HALT:
        return ip
    raise Exception(f'Unknown opcode {program[ip]} at position {ip}')


def test_solution1():
    # Single step tests
    step_0 = [1, 9, 10, 3, 2, 3, 11, 0, 99, 30, 40, 50]
    step_1 = [1, 9, 10, 70, 2, 3, 11, 0, 99, 30, 40, 50]
    step_2 = [3500, 9, 10, 70, 2, 3, 11, 0, 99, 30, 40, 50]
    assert (4, step_1) == (_execute(0, step_0), step_0)
    assert (8, step_2) == (_execute(4, step_1), step_1)

    # Complete program tests
    step_0 = [1, 9, 10, 3, 2, 3, 11, 0, 99, 30, 40, 50]
    assert (3500, step_2) == (_solution1(step_0), step_0)

    program = [1, 0, 0, 0, 99]
    assert (2, [2, 0, 0, 0, 99]) == (_solution1(program), program)

    program = [2, 3, 0, 3, 99]
    assert (2, [2, 3, 0, 6, 99]) == (_solution1(program), program)

    program = [2, 4, 4, 5, 99, 0]
    assert (2, [2, 4, 4, 5, 99, 9801]) == (_solution1(program), program)

    program = [1, 1, 1, 4, 99, 5, 6, 0, 99]
    assert (30, [30, 1, 1, 4, 2, 5, 6, 0, 99]) == (_solution1(program), program)


def solution1(intcode, noun=12, verb=2):
    program = list(intcode)
    program[1], program[2] = (noun, verb)
    return _solution1(program)


def _solution1(intcode):
    instruction_pointer = 0
    while intcode[instruction_pointer] != OPCODE_HALT:
        instruction_pointer = _execute(instruction_pointer, intcode)
    return intcode[0]


def test_solution2():
    # quick check that program result is an increasing function of its inputs
    # consists of additions and multiplications of inputs
    intcode = read_input('02/input.txt')
    prev = solution1(intcode, noun=0, verb=0)
    for verb in range(1, 100):
        current_verb = solution1(intcode, noun=0, verb=verb)
        assert current_verb >= prev
        prev = current_verb

    prev = solution1(intcode, noun=0, verb=0)
    for noun in range(1, 100):
        current_noun = solution1(intcode, noun=noun, verb=0)
        assert current_noun >= prev

    assert current_noun > current_verb  # explains the indexation logic in ProgramSearchSpace


class ProgramSearchSpace:
    def __init__(self, intcode):
        self.intcode = intcode

    def __len__(self):
        return 10000  # 100 x 100

    def __getitem__(self, ind):
        noun = ind // 100
        verb = ind % 100
        return solution1(self.intcode, noun, verb)


def solution2(intcode):
    i = bisect.bisect_left(ProgramSearchSpace(intcode), OUTPUT)
    noun = i // 100
    verb = i % 100
    return f'{noun:02d}{verb:02d}'

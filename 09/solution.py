MODE_POSITION = 0
MODE_IMMEDIATE = 1
MODE_RELATIVE = 2

MODES = {MODE_POSITION, MODE_IMMEDIATE, MODE_RELATIVE}

OPCODE_ADD = 1
OPCODE_MULTIPLY = 2
OPCODE_STORE = 3
OPCODE_OUTPUT = 4
OPCODE_JMPIFTRUE = 5
OPCODE_JMPIFFALSE = 6
OPCODE_LESSTHAN = 7
OPCODE_EQUAL = 8
OPCODE_RELMODE = 9
OPCODE_HALT = 99


# pylint: disable=too-few-public-methods
class CPUState:
    def __init__(self):
        self.ip = 0
        self.base = 0

    def __str__(self):
        return f'ip={self.ip}, base={self.base}'


class RAM:
    def __init__(self, program):
        self.program = list(program)
        self.page_fault = {}  # stores the writes to memory locations outside program list

    def __getitem__(self, i):
        try:
            return self.program[i]
        except IndexError:
            if i < 0:
                raise
            return self.page_fault.get(i, 0)

    def __setitem__(self, key, value):
        try:
            self.program[key] = value
        except IndexError:
            if key < 0:
                raise
            self.page_fault[key] = value

    def __str__(self):
        return f'program={self.program}, extras={self.page_fault}'


def read_input(filename):
    with open(filename) as f:
        return [int(num) for num in f.read().split(',')]


def _get_param(program, mode, cpustate, offset):
    ip = cpustate.ip
    assert mode in MODES
    if mode == MODE_IMMEDIATE:
        return program[ip + offset]
    if mode == MODE_POSITION:
        return program[program[ip + offset]]
    return program[cpustate.base + program[ip + offset]]


def _set_param(program, mode, cpustate, offset, value):
    addr = cpustate.ip + offset
    base = cpustate.base if mode == MODE_RELATIVE else 0
    program[base + program[addr]] = value


def _op_add(program, cpustate, modes, **_unused):
    mode_param_1, modes = modes % 10, modes // 10
    mode_param_2, modes = modes % 10, modes // 10
    mode_param_3, modes = modes % 10, modes // 10
    assert MODE_IMMEDIATE != mode_param_3  # testing the constraint for output params
    param_1 = _get_param(program, mode_param_1, cpustate, 1)
    param_2 = _get_param(program, mode_param_2, cpustate, 2)
    _set_param(program, mode_param_3, cpustate, 3, param_1 + param_2)
    cpustate.ip += 4


def _op_multiply(program, cpustate, modes, **_unused):
    mode_param_1, modes = modes % 10, modes // 10
    mode_param_2, modes = modes % 10, modes // 10
    mode_param_3, modes = modes % 10, modes // 10
    assert MODE_IMMEDIATE != mode_param_3  # testing the constraint for output params
    param_1 = _get_param(program, mode_param_1, cpustate, 1)
    param_2 = _get_param(program, mode_param_2, cpustate, 2)
    _set_param(program, mode_param_3, cpustate, 3, param_1 * param_2)
    cpustate.ip += 4


def _op_store(program, cpustate, modes, pinput=None, **_unused):
    mode_param_1, modes = modes % 10, modes // 10
    assert MODE_IMMEDIATE != mode_param_1  # testing the constraint for output params
    _set_param(program, mode_param_1, cpustate, 1, pinput)
    cpustate.ip += 2


def _op_output(program, cpustate, modes, output=None, **_unused):
    mode_param_1, modes = modes % 10, modes // 10
    param_1 = _get_param(program, mode_param_1, cpustate, 1)
    output.append(param_1)
    cpustate.ip += 2


def _op_jmpiftrue(program, cpustate, modes, **_unused):
    mode_param_1, modes = modes % 10, modes // 10
    mode_param_2, modes = modes % 10, modes // 10
    param_1 = _get_param(program, mode_param_1, cpustate, 1)
    param_2 = _get_param(program, mode_param_2, cpustate, 2)
    if param_1 != 0:
        cpustate.ip = param_2
    else:
        cpustate.ip += 3


def _op_jmpiffalse(program, cpustate, modes, **_unused):
    mode_param_1, modes = modes % 10, modes // 10
    mode_param_2, modes = modes % 10, modes // 10
    param_1 = _get_param(program, mode_param_1, cpustate, 1)
    param_2 = _get_param(program, mode_param_2, cpustate, 2)
    if param_1 == 0:
        cpustate.ip = param_2
    else:
        cpustate.ip += 3


def _op_lessthan(program, cpustate, modes, **_unused):
    mode_param_1, modes = modes % 10, modes // 10
    mode_param_2, modes = modes % 10, modes // 10
    mode_param_3, modes = modes % 10, modes // 10
    assert MODE_IMMEDIATE != mode_param_3  # testing the constraint for output params
    param_1 = _get_param(program, mode_param_1, cpustate, 1)
    param_2 = _get_param(program, mode_param_2, cpustate, 2)
    _set_param(program, mode_param_3, cpustate, 3, int(param_1 < param_2))
    cpustate.ip += 4


def _op_equal(program, cpustate, modes, **_unused):
    mode_param_1, modes = modes % 10, modes // 10
    mode_param_2, modes = modes % 10, modes // 10
    mode_param_3, modes = modes % 10, modes // 10
    assert MODE_IMMEDIATE != mode_param_3  # testing the constraint for output params
    param_1 = _get_param(program, mode_param_1, cpustate, 1)
    param_2 = _get_param(program, mode_param_2, cpustate, 2)
    _set_param(program, mode_param_3, cpustate, 3, int(param_1 == param_2))
    cpustate.ip += 4


def _op_relmode(program, cpustate, modes, **_unused):
    mode_param_1, modes = modes % 10, modes // 10
    cpustate.base += _get_param(program, mode_param_1, cpustate, 1)
    cpustate.ip += 2


EXECUTE = {
    OPCODE_ADD: _op_add,
    OPCODE_MULTIPLY: _op_multiply,
    OPCODE_STORE: _op_store,
    OPCODE_OUTPUT: _op_output,
    OPCODE_JMPIFTRUE: _op_jmpiftrue,
    OPCODE_JMPIFFALSE: _op_jmpiffalse,
    OPCODE_LESSTHAN: _op_lessthan,
    OPCODE_EQUAL: _op_equal,
    OPCODE_RELMODE: _op_relmode,
}


def _execute(cpustate, opcode, program, pinput=None, output=None):
    modes, opcode = opcode // 100, opcode % 100
    if opcode not in EXECUTE:
        raise Exception(f'Unknown instruction {opcode} encountered at position {cpustate.ip}')
    return EXECUTE[opcode](program, cpustate, modes, pinput=pinput, output=output)


def test_solution1():
    program = [109, 1, 204, -1, 1001, 100, 1, 100, 1008, 100, 16, 101, 1006, 101, 0, 99]
    assert program == solution1(program)

    program = [1102, 34915192, 34915192, 7, 4, 7, 99, 0]
    output = solution1(program)
    assert 10 ** 15 <= output[0] < 10 ** 16

    program = [104, 1125899906842624, 99]
    assert [program[1]] == solution1(program)


def solution1(boost_program, pinput=1):
    cpustate = CPUState()
    output = []
    program = RAM(boost_program)
    opcode = program[cpustate.ip]
    while opcode != OPCODE_HALT:
        _execute(cpustate, opcode, program, pinput=pinput, output=output)
        opcode = program[cpustate.ip]
    return output


def solution2(boost_program, pinput=2):
    return solution1(boost_program, pinput=pinput)

MODE_POSITION = 0
MODE_IMMEDIATE = 1

OPCODE_ADD = 1
OPCODE_MULTIPLY = 2
OPCODE_STORE = 3
OPCODE_OUTPUT = 4
OPCODE_JMPIFTRUE = 5
OPCODE_JMPIFFALSE = 6
OPCODE_LESSTHAN = 7
OPCODE_EQUAL = 8
OPCODE_HALT = 99


def read_input(filename):
    with open(filename) as f:
        return [int(num) for num in f.read().split(',')]


def _op_add(program, ip, modes, **_unused):
    mode_param_1, modes = modes % 10, modes // 10
    mode_param_2, modes = modes % 10, modes // 10
    mode_param_3, modes = modes % 10, modes // 10
    assert MODE_POSITION == mode_param_3  # testing the constraint for output params
    param_1 = program[ip + 1] if mode_param_1 == MODE_IMMEDIATE else program[program[ip + 1]]
    param_2 = program[ip + 2] if mode_param_2 == MODE_IMMEDIATE else program[program[ip + 2]]
    program[program[ip + 3]] = param_1 + param_2
    return ip + 4


def _op_multiply(program, ip, modes, **_unused):
    mode_param_1, modes = modes % 10, modes // 10
    mode_param_2, modes = modes % 10, modes // 10
    mode_param_3, modes = modes % 10, modes // 10
    assert MODE_POSITION == mode_param_3  # testing the constraint for output params
    param_1 = program[ip + 1] if mode_param_1 == MODE_IMMEDIATE else program[program[ip + 1]]
    param_2 = program[ip + 2] if mode_param_2 == MODE_IMMEDIATE else program[program[ip + 2]]
    program[program[ip + 3]] = param_1 * param_2
    return ip + 4


def _op_store(program, ip, modes, pinput=None, **_unused):
    assert MODE_POSITION == modes  # testing the constraint for output params
    program[program[ip + 1]] = pinput
    return ip + 2


def _op_output(program, ip, modes, output=None, **_unused):
    mode_param_1, modes = modes % 10, modes // 10
    param_1 = program[ip + 1] if mode_param_1 == MODE_IMMEDIATE else program[program[ip + 1]]
    output[0] = param_1
    return ip + 2


def _op_jmpiftrue(program, ip, modes, **_unused):
    mode_param_1, modes = modes % 10, modes // 10
    mode_param_2, modes = modes % 10, modes // 10
    param_1 = program[ip + 1] if mode_param_1 == MODE_IMMEDIATE else program[program[ip + 1]]
    param_2 = program[ip + 2] if mode_param_2 == MODE_IMMEDIATE else program[program[ip + 2]]
    if param_1 != 0:
        return param_2
    return ip + 3


def _op_jmpiffalse(program, ip, modes, **_unused):
    mode_param_1, modes = modes % 10, modes // 10
    mode_param_2, modes = modes % 10, modes // 10
    param_1 = program[ip + 1] if mode_param_1 == MODE_IMMEDIATE else program[program[ip + 1]]
    param_2 = program[ip + 2] if mode_param_2 == MODE_IMMEDIATE else program[program[ip + 2]]
    if param_1 == 0:
        return param_2
    return ip + 3


def _op_lessthan(program, ip, modes, **_unused):
    mode_param_1, modes = modes % 10, modes // 10
    mode_param_2, modes = modes % 10, modes // 10
    mode_param_3, modes = modes % 10, modes // 10
    assert MODE_POSITION == mode_param_3  # testing the constraint for output params
    param_1 = program[ip + 1] if mode_param_1 == MODE_IMMEDIATE else program[program[ip + 1]]
    param_2 = program[ip + 2] if mode_param_2 == MODE_IMMEDIATE else program[program[ip + 2]]
    program[program[ip + 3]] = int(param_1 < param_2)
    return ip + 4


def _op_equal(program, ip, modes, **_unused):
    mode_param_1, modes = modes % 10, modes // 10
    mode_param_2, modes = modes % 10, modes // 10
    mode_param_3, modes = modes % 10, modes // 10
    assert MODE_POSITION == mode_param_3  # testing the constraint for output params
    param_1 = program[ip + 1] if mode_param_1 == MODE_IMMEDIATE else program[program[ip + 1]]
    param_2 = program[ip + 2] if mode_param_2 == MODE_IMMEDIATE else program[program[ip + 2]]
    program[program[ip + 3]] = int(param_1 == param_2)
    return ip + 4


EXECUTE = {
    OPCODE_ADD: _op_add,
    OPCODE_MULTIPLY: _op_multiply,
    OPCODE_STORE: _op_store,
    OPCODE_OUTPUT: _op_output,
    OPCODE_JMPIFTRUE: _op_jmpiftrue,
    OPCODE_JMPIFFALSE: _op_jmpiffalse,
    OPCODE_LESSTHAN: _op_lessthan,
    OPCODE_EQUAL: _op_equal,
}


def _execute(ip, program, pinput=None, output=None):
    opcode = program[ip]
    modes, opcode = opcode // 100, opcode % 100
    if opcode not in EXECUTE:
        raise Exception(f'Unknown instruction {opcode} encountered at position {ip}')
    return EXECUTE[opcode](program, ip, modes, pinput=pinput, output=output)


def test_solution1():
    _test_new_instructions()
    _test_modes()


def _test_new_instructions():
    program = [3, 1, 99]
    pinput = 44
    _solution1(program, pinput=pinput)
    assert [3, pinput, 99] == program

    program = [4, 2, 99]
    assert 99 == _solution1(program)
    assert [4, 2, 99] == program

    program = [3, 0, 4, 0, 99]
    pinput = 777
    assert pinput == _solution1(program, pinput=pinput)
    assert [pinput, 0, 4, 0, 99] == program


def _test_modes():
    program = [1002, 4, 3, 4, 33]
    _solution1(program)
    assert [1002, 4, 3, 4, 99] == program

    program = [1101, 100, -1, 4, 0]
    _solution1(program)
    assert [1101, 100, -1, 4, 99] == program


def _solution1(intcode, pinput=None):
    instruction_pointer = 0
    output = [0]
    while intcode[instruction_pointer] != OPCODE_HALT:
        # intermediate output tests should be successful
        assert 0 == output[0], f'Output test failed at position {instruction_pointer}'
        instruction_pointer = _execute(instruction_pointer, intcode, pinput=pinput, output=output)
    return output[0]


def solution1(intcode, pinput=1):
    return _solution1(list(intcode), pinput=pinput)


def test_solution2():
    _test_comparisons()
    _test_jumps()
    program = [3, 21, 1008, 21, 8, 20, 1005, 20, 22, 107, 8, 21, 20, 1006, 20, 31,
               1106, 0, 36, 98, 0, 0, 1002, 21, 125, 20, 4, 20, 1105, 1, 46, 104,
               999, 1105, 1, 46, 1101, 1000, 1, 20, 4, 20, 1105, 1, 46, 98, 99]
    for pinput, output in [(6, 999), (7, 999), (8, 1000), (9, 1001), (10, 1001)]:
        assert output == solution2(program, pinput=pinput)


def _test_comparisons():
    for program in [
        [3, 9, 8, 9, 10, 9, 4, 9, 99, -1, 8],
        [3, 3, 1108, -1, 8, 3, 4, 3, 99]
    ]:
        for pinput in [8, 7]:
            assert int(pinput == 8) == solution2(program, pinput)

    for program in [
        [3, 9, 7, 9, 10, 9, 4, 9, 99, -1, 8],
        [3, 3, 1107, -1, 8, 3, 4, 3, 99]
    ]:
        for pinput in [8, 7]:
            assert int(pinput < 8) == solution2(program, pinput)


def _test_jumps():
    for program in [
        [3, 12, 6, 12, 15, 1, 13, 14, 13, 4, 13, 99, -1, 0, 1, 9],
        [3, 3, 1105, -1, 9, 1101, 0, 0, 12, 4, 12, 99, 1]
    ]:
        for pinput in [0, 1]:
            assert int(pinput != 0) == solution2(program, pinput=pinput)


def _solution2(intcode, pinput=None):
    instruction_pointer = 0
    output = [0]
    while intcode[instruction_pointer] != OPCODE_HALT:
        instruction_pointer = _execute(instruction_pointer, intcode, pinput=pinput, output=output)
    return output[0]


def solution2(intcode, pinput=5):
    return _solution2(list(intcode), pinput=pinput)

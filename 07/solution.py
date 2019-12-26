from queue import Queue
from threading import Thread

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


def _read_program(input_data):
    return [int(num) for num in input_data.split(',')]


def read_input(filename):
    with open(filename) as f:
        return _read_program(f.read())


class Amplifier:
    def __init__(self, program, amp_in, amp_out):
        self.program = list(program)
        self.amp_in = amp_in
        self.amp_out = amp_out
        self.thread = None

    def start(self):
        self.thread = Thread(target=self._execute)
        self.thread.start()

    def stop(self):
        if not self.thread:
            raise Exception('Amplifier must be started first')
        self.thread.join()

    def _execute(self):
        instruction_pointer = 0
        intcode = self.program
        pinput = self.amp_in
        poutput = self.amp_out
        while intcode[instruction_pointer] != OPCODE_HALT:
            instruction_pointer = _execute(instruction_pointer, intcode, pinput, poutput)


def _op_add(program, ip, modes, *_unused):
    mode_param_1, modes = modes % 10, modes // 10
    mode_param_2, modes = modes % 10, modes // 10
    mode_param_3, modes = modes % 10, modes // 10
    assert MODE_POSITION == mode_param_3  # testing the constraint for output params
    param_1 = program[ip + 1] if mode_param_1 == MODE_IMMEDIATE else program[program[ip + 1]]
    param_2 = program[ip + 2] if mode_param_2 == MODE_IMMEDIATE else program[program[ip + 2]]
    program[program[ip + 3]] = param_1 + param_2
    return ip + 4


def _op_multiply(program, ip, modes, *_unused):
    mode_param_1, modes = modes % 10, modes // 10
    mode_param_2, modes = modes % 10, modes // 10
    mode_param_3, modes = modes % 10, modes // 10
    assert MODE_POSITION == mode_param_3  # testing the constraint for output params
    param_1 = program[ip + 1] if mode_param_1 == MODE_IMMEDIATE else program[program[ip + 1]]
    param_2 = program[ip + 2] if mode_param_2 == MODE_IMMEDIATE else program[program[ip + 2]]
    program[program[ip + 3]] = param_1 * param_2
    return ip + 4


def _op_store(program, ip, modes, pinput, *_unused):
    assert MODE_POSITION == modes  # testing the constraint for output params
    program[program[ip + 1]] = pinput.get()  # blocks until some input is available
    return ip + 2


def _op_output(program, ip, modes, _, poutput, *_unused):
    mode_param_1, modes = modes % 10, modes // 10
    param_1 = program[ip + 1] if mode_param_1 == MODE_IMMEDIATE else program[program[ip + 1]]
    poutput.put(param_1)
    return ip + 2


def _op_jmpiftrue(program, ip, modes, *_unused):
    mode_param_1, modes = modes % 10, modes // 10
    mode_param_2, modes = modes % 10, modes // 10
    param_1 = program[ip + 1] if mode_param_1 == MODE_IMMEDIATE else program[program[ip + 1]]
    param_2 = program[ip + 2] if mode_param_2 == MODE_IMMEDIATE else program[program[ip + 2]]
    if param_1 != 0:
        return param_2
    return ip + 3


def _op_jmpiffalse(program, ip, modes, *_unused):
    mode_param_1, modes = modes % 10, modes // 10
    mode_param_2, modes = modes % 10, modes // 10
    param_1 = program[ip + 1] if mode_param_1 == MODE_IMMEDIATE else program[program[ip + 1]]
    param_2 = program[ip + 2] if mode_param_2 == MODE_IMMEDIATE else program[program[ip + 2]]
    if param_1 == 0:
        return param_2
    return ip + 3


def _op_lessthan(program, ip, modes, *_unused):
    mode_param_1, modes = modes % 10, modes // 10
    mode_param_2, modes = modes % 10, modes // 10
    mode_param_3, modes = modes % 10, modes // 10
    assert MODE_POSITION == mode_param_3  # testing the constraint for output params
    param_1 = program[ip + 1] if mode_param_1 == MODE_IMMEDIATE else program[program[ip + 1]]
    param_2 = program[ip + 2] if mode_param_2 == MODE_IMMEDIATE else program[program[ip + 2]]
    program[program[ip + 3]] = int(param_1 < param_2)
    return ip + 4


def _op_equal(program, ip, modes, *_unused):
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


def _execute(ip, program, pinput, poutput):
    opcode = program[ip]
    modes, opcode = opcode // 100, opcode % 100
    if opcode not in EXECUTE:
        raise Exception(f'Unknown instruction {opcode} encountered at position {ip}')
    return EXECUTE[opcode](program, ip, modes, pinput, poutput)


def _test_permutations():
    assert [[1]] == list(_generate_permutations([1]))
    assert [[1, 2], [2, 1]] == list(_generate_permutations([1, 2]))
    assert [
               [1, 2, 3], [1, 3, 2],
               [2, 1, 3], [2, 3, 1],
               [3, 1, 2], [3, 2, 1]
    ] == list(_generate_permutations([1, 2, 3]))


def test_solution1():
    _test_permutations()
    test_cases = [
        (43210, '3,15,3,16,1002,16,10,16,1,16,15,15,4,15,99,0,0'),
        (54321, '3,23,3,24,1002,24,10,24,1002,23,-1,23,101,5,23,23,1,24,23,23,4,23,99,0,0'),
        (65210, '3,31,3,32,1002,32,10,32,1001,31,-2,31,1007,31,0,33,1002,33,7,33,1,33,31,31,1,32,31,31,4,31,99,0,0,0')
    ]
    for expected_thrust, amplifier_program in test_cases:
        assert expected_thrust == solution1(_read_program(amplifier_program))


def _generate_permutations(settings):
    if len(settings) == 1:
        yield settings
    for i, setting in enumerate(settings):
        fixed_element = [setting]
        for p in _generate_permutations(settings[:i] + settings[i+1:]):
            yield fixed_element + p


def _solution(amplifier_software, phase_settings_permutations, configure_buffers):
    max_thrust = float('-inf')
    for phase_settings in phase_settings_permutations:
        buffers = configure_buffers()
        amps = []
        for i, phase_setting in enumerate(phase_settings):
            buffer = buffers[i]
            buffer.put(phase_setting)
            if i == 0:
                buffer.put(0)
            amp = Amplifier(amplifier_software, buffer, buffers[i+1])
            amps.append(amp)
        for amp in amps:
            amp.start()
        for amp in amps:
            amp.stop()
        max_thrust = max(max_thrust, buffers[-1].get())
    return max_thrust


def solution1(amplifier_software):
    phase_settings = [0, 1, 2, 3, 4]
    def linear_buffers():
        return [Queue() for _ in range(len(phase_settings) + 1)]
    return _solution(amplifier_software, _generate_permutations(phase_settings), linear_buffers)


def test_solution2():
    test_cases = [
        (139629729, '3,26,1001,26,-4,26,3,27,1002,27,2,27,1,27,26,27,4,27,1001,28,-1,28,1005,28,6,99,0,0,5'),
        (18216, '3,52,1001,52,-5,52,3,53,1,52,56,54,1007,54,5,55,1005,55,26,1001,54,-5,54,1105,1,12,1,53,54,'
                '53,1008,54,0,55,1001,55,1,55,2,53,55,53,4,53,1001,56,-1,56,1005,56,6,99,0,0,0,0,10')
    ]
    for expected_thrust, amplifier_program in test_cases:
        assert expected_thrust == solution2(_read_program(amplifier_program))


def solution2(amplifier_software):
    phase_settings = [5, 6, 7, 8, 9]
    def ring_buffers():
        buffers = [Queue() for _ in range(len(phase_settings))]
        return buffers + [buffers[0]]
    return _solution(amplifier_software, _generate_permutations(phase_settings), ring_buffers)

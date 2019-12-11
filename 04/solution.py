from collections import Counter


def read_input(filename):
    with open(filename) as f:
        start, end = f.read().split('-')
        return start, end


def test_solution1():
    assert '188888' == _next_password('183564')
    assert '123466' == _next_password('123456')
    assert '456799' == _next_password('456789')
    assert not solution1(['100000', '111110'])
    assert len([111111]) == solution1(['100000', '111111'])
    expected = [
        111111, 111112, 111113, 111114, 111115, 111116, 111117, 111118, 111119,
        111122, 111123, 111124, 111125, 111126, 111127, 111128, 111129,
        111133, 111134, 111135, 111136, 111137, 111138, 111139,
        111144, 111145, 111146, 111147, 111148, 111149,
        111155, 111156, 111157, 111158, 111159,
        111166, 111167, 111168, 111169,
        111177, 111178, 111179,
        111188, 111189,
        111199
    ]
    assert len(expected) == solution1(['100000', '111200'])


def _next_password(input_string):
    prev_digit = input_string[0]
    password = [prev_digit]
    for position, current_digit in enumerate(input_string[1:], start=1):
        if prev_digit > current_digit:
            password.append(prev_digit * (len(input_string) - position))
            break
        password.append(current_digit)
        prev_digit = current_digit
    password = ''.join(password)
    if max(Counter(password).values()) == 1:  # if there are no repeating digits
        # repeat the last digit in previous position, e.g 123456 -> 123466
        password = ''.join([password[:-2], password[-1], password[-1]])
    return password


def solution1(password_range):
    start, end = password_range
    password_count = 0
    password = start
    while True:
        password = _next_password(password)
        if password > end:
            break
        password_count += 1
        password = str(int(password) + 1)
    return password_count


def test_solution2():
    for ranges in [('100000', '200000'), ('200000', '300000')]:
        assert solution1(ranges) >= solution2(ranges)


def solution2(password_range):
    start, end = password_range
    password_count = 0
    password = start
    while True:
        password = _next_password(password)
        if password > end:
            break
        if 2 in Counter(password).values():
            password_count += 1
        password = str(int(password) + 1)
    return password_count

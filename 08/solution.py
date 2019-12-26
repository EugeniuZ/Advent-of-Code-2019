from collections import Counter

BLACK = '0'
WHITE = '1'
TRANSPARENT = '2'

PRINT_BLACK = ' '
PRINT_WHITE = '*'

FONT_SIZE = 3

def read_input(filename):
    with open(filename) as f:
        return f.read()


def test_solution1():
    stream = '123456789012'
    assert 1 == solution1(stream, width=3, height=2)


def solution1(image_stream, width=25, height=6):
    layer_size = width * height
    layer_stats = []
    while image_stream:
        layer = image_stream[:layer_size]
        assert layer_size == len(layer), 'Incomplete layer received !'
        layer_stats.append(Counter(layer))
        image_stream = image_stream[layer_size:]
    layer_min_zeros = min(layer_stats, key=lambda ls: ls[BLACK])
    return layer_min_zeros[WHITE] * layer_min_zeros[TRANSPARENT]


def test_solution2():
    white = PRINT_WHITE * FONT_SIZE
    black = PRINT_BLACK * FONT_SIZE
    assert f'\n{black}{white}\n{white}{black}' == solution2('0222112222120000', width=2, height=2)


def _combine(final_layer, new_layer):
    for i, (fpixel, npixel) in enumerate(zip(final_layer, new_layer)):
        if fpixel == TRANSPARENT and npixel != TRANSPARENT:
            pixel = PRINT_WHITE if npixel == WHITE else PRINT_BLACK
            final_layer[i] = pixel * FONT_SIZE


def solution2(image_stream, width=25, height=6):
    layer_size = width * height
    final_image = [TRANSPARENT] * layer_size
    while image_stream:
        layer = image_stream[:layer_size]
        _combine(final_image, layer)
        image_stream = image_stream[layer_size:]
    return '\n' + '\n'.join(
        ''.join(final_image[start:start+width])
        for start in range(0, layer_size, width)
    )

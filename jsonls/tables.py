from collections import namedtuple
from functools import partial

import click
from colorclass import Color, Windows
from terminaltables import SingleTable


Colors = namedtuple('Color', ['num', 'text'])

# Windows.enable(auto_colors=True, reset_atexit=True)


def autocolor(text, color):
    fmt = '{{auto{color}}}{text}{{/auto{color}}}'
    return Color(fmt.format(color=color, text=text))


def set_color(color='white'):
    fg_color = color.lstrip('*')
    return partial(click.style, fg=fg_color, bold=color.startswith('*'))


def color_table(rows, colors=None):
    strings = [tuple(str(j) for j in i) for i in rows]
    lengths = tuple(len(max(i, key=len)) for i in zip(*strings))
    table = [[c.ljust(lengths[n]) for n, c in enumerate(i)] for i in strings]
    if colors:
        colors_ = tuple(map(set_color, colors))
        result = (' '.join(colors_[n](c) for n, c in enumerate(i))
                  for i in table)
    else:
        result = (' '.join(i) for i in table)
    return result


def draw3columns(rows, colors=Colors(num='yellow', text=('blue', 'white'))):
    colors = (colors.num, *colors.text)
    row_colors = (zip(row, colors) for row in rows)
    table_data = [[autocolor(*col) for col in row] for row in row_colors]
    return SingleTable(table_data).table


def number_lines(s):
    return ((str(n) + '.', i) for n, i in enumerate(s, 1))


def number_tuples(s):
    return ((str(n) + '.', *t) for n, t in enumerate(s, 1))


'''
def number_lines(d, color=Colors(num='yellow', text='white')):
    padding = len(str(len(d)))
    numbers = (str(i).rjust(padding) for i in range(1, len(d) + 1))
    nums = map(partial(click.style, fg=color.num), numbers)
    data = map(partial(click.style, fg=color.text), d)
    return (n + ' ' + i for n, i in zip(nums, data))
'''

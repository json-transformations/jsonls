from collections import namedtuple
from functools import partial

import click

Colors = namedtuple('Color', ['num', 'text'])


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


def number_lines(s):
    return ((str(n) + '.', i) for n, i in enumerate(s, 1))


def number_tuples(s):
    return ((str(n) + '.', *t) for n, t in enumerate(s, 1))

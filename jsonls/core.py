from toolz import curry

from jsoncrawl.core import Node, node_visitor
from jsoncore import WILDCARD, uniq_nodes, get_value

from .tables import color_table, number_lines, number_tuples

KEY_SEP = '.'
BICOLOR = ('yellow', 'white')
TRICOLOR = ('yellow', 'cyan', 'white')


@curry
def not_element_ch(node, wildcard=WILDCARD):
    return not (
        node.keys[-1:] == (wildcard,) and
        node.dtype != 'array'
    )


@curry
def get_nodes(d, wildcard=WILDCARD):
    """Generates a sequence of sorted, unique key tuples.

    Elements (keys) can names (str), indexes (int) or slices (slice).
    """
    nodes = uniq_nodes(d, wildcard=wildcard)
    not_array_index = not_element_ch(wildcard=wildcard)
    return filter(not_array_index, nodes)


@curry
def add_wildcards_to_arrays(node, wildcard=WILDCARD):
    """Add trailing wildcard to keys pointing to arrays."""
    keys = node.keys
    if node.dtype == 'array' and keys[-1:] != wildcard:
        keys += wildcard,
    return Node(keys, node.val, node.dtype)


@curry
def get_keylists(d, wildcard=WILDCARD):
    nodes = get_nodes(d, wildcard=WILDCARD)
    add_wildcards = add_wildcards_to_arrays(wildcard=WILDCARD)
    result = (i.keys for i in map(add_wildcards, nodes))
    return result


@curry
def join_keys(node, sep=KEY_SEP, wildcard=WILDCARD):
    keystr = sep.join(map(str, node.keys))
    if node.dtype == 'array':
        keystr += sep + wildcard if node.keys else '*'
    if not keystr.startswith(wildcard):
        keystr = sep + keystr
    return keystr


@curry
def get_keystrings(d, sep=KEY_SEP, wildcard=WILDCARD):
    """Generates a sequence of sorted, unique key tuples.

    Elements (keys) can names (str), indexes (int) or slices (slice).
    """
    nodes = get_nodes(d, wildcard=wildcard)
    key_join = join_keys(sep=sep, wildcard=wildcard)
    keystrings = sorted(set(map(key_join, nodes)))
    return keystrings


@curry
def list_keys(d, sep=KEY_SEP, wildcard=WILDCARD, colors=BICOLOR):
    keystrings = get_keystrings(d, sep=sep, wildcard=wildcard)
    lines = number_lines(keystrings)
    return color_table(lines, colors=colors)


@curry
def list_types(d, sep=KEY_SEP, wildcard=WILDCARD, colors=TRICOLOR):
    nodes = get_nodes(d, wildcard=wildcard)
    ordered = sorted(nodes, key=lambda x: x.keys)
    key_join = join_keys(sep=sep, wildcard=wildcard)
    types = ((i.dtype[:3], key_join(i)) for i in ordered)
    lines = number_tuples(types)
    return color_table(lines, colors=colors)


def single_array(node):
    return node.dtype == 'array' and WILDCARD not in node.keys


def list_counts(d, sep=KEY_SEP, wildcard=WILDCARD, colors=TRICOLOR):
    nodes = get_nodes(d, wildcard=wildcard)
    ordered = sorted(nodes, key=lambda x: x.keys)
    lines = number_lines(ordered)
    arrays = ((n, i) for n, i in lines if i.dtype == 'array')
    key_join = join_keys(sep=sep, wildcard=wildcard)
    counts = ((n, key_join(i), len(i.val)) for n, i in arrays)
    return color_table(counts, colors=colors)

    '''
    nodes = node_visitor(d, element_ch=wildcard)
    keys = number_lines(i for i in nodes if i.keys is not None)
    arrays = ((n, i.keys) for n, i in keys if single_array(i))
    counts = ((n, len(get_value(i, d)), i) for n, i in arrays)
    result = ((n, c, '.'.join(k + [wildcard])) for n, c, k in counts)
    return color_table(result, colors=colors)
    '''

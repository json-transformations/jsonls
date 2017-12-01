from click import command, option, version_option, pass_context
import click._termui_impl

from jsoncore import jsonfile, rootkey

from .core import BICOLOR, TRICOLOR, list_counts, list_keys, list_types


@command()
@jsonfile
@rootkey
@option('-t', '--types', is_flag=True, help='Show JSON node data types')
@option('-c', '--count', is_flag=True, help='Show array counts')
@option('-m', '--nocolor', is_flag=True, help='Monochrome (no color)')
@version_option()
@pass_context
def main(ctx, jsonfile, root, types, count, nocolor):
    if types:
        color = TRICOLOR
        fn = list_types
    elif count:
        color = TRICOLOR
        fn = list_counts
    else:
        color = BICOLOR
        fn = list_keys
    if jsonfile is not None:
        if nocolor:
            color = None
        for i in fn(root, colors=color):
            click.echo(i)


if __name__ == '__main__':
    main()

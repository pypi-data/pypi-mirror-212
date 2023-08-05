#!/usr/bin/env python3

import sys

import click
import confuse

from puup.render import render
from puup.dump import dump
import puup.entropy


@click.command()
@click.option('--template', '-t', default='rran', metavar='TEMPLATE', show_default=True)
@click.option('--prefix', '-P', default='', metavar='TEMPLATE', show_default=True)
@click.option('--suffix', '-S', default='', metavar='TEMPLATE', show_default=True)
@click.option('--separator', '-s', 'separator', default=' ', metavar='STRING', show_default=True)
@click.option('--output', '-o', 'fp', type=click.File('w'), default=sys.stdout)
@click.option('--output-type', '-O', type=click.Choice(['text', 'json']), default='text', show_default=True)
@click.option('--n', '-n', type=int, default=1, show_default=True)
@click.option('--entropy', '-e', is_flag=True)
def cmd(template, prefix, suffix, n, **kwargs):

    '''Generate a Potentially Universally Unique Phrase.'''

    t = prefix + template + suffix

    if kwargs.get('entropy') is True:
        dump(puup.entropy.estimate(t), **kwargs)
    else:
        for _ in range(n):
            dump(render(t), **kwargs)


def main():
    cmd(auto_envvar_prefix='PUUP',
        default_map=confuse.Configuration('puup').flatten())


if __name__ == '__main__':
    main()

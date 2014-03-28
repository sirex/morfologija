"""Morphology database tool.

Usage:
  morfologija <lexeme> [-d <path>]

Options:
  <lexeme>              A lexeme from morphology database.
  -h --help             Show this screen.
  -d --data-dir=<path>  Data directory [default: data].

"""

import yaml
import docopt
import os.path
import textwrap

from ..grammar import Node
from ..lexemes import Lexeme
from ..paradigms import ParadigmCollection
from ..utils import first

wrapper = textwrap.TextWrapper(subsequent_indent='       ')


def print_field(field_code, field_label, value_code, value_label):
    if value_label:
        value_label = '\n'.join(wrapper.wrap(value_label))

    print('{:2}: {}'.format(field_code, field_label))

    if value_code is None:
        print('    {}'.format(value_code, value_label))
    else:
        print('    {}: {}'.format(value_code, value_label))

    print()


def main():
    args = docopt.docopt(__doc__)
    data_dir = args['--data-dir']
    data = lambda name: os.path.join(data_dir, name)

    with open(data('grammar.yaml'), encoding='utf-8') as f:
        grammar = yaml.load(f)
    grammar = Node(dict(nodes=grammar))

    with open(data('sources.yaml'), encoding='utf-8') as f:
        sources = yaml.load(f)
    sources = Node(dict(nodes=sources))

    with open(data('paradigms.yaml'), encoding='utf-8') as f:
        paradigms = yaml.load(f)
    paradigms = ParadigmCollection(paradigms)

    with open(data('lexemes.txt'), encoding='utf-8') as f:
        for i, line in enumerate(f, 1):
            if line.startswith(args['<lexeme>'] + ' ') or line.startswith(args['<lexeme>'] + '('):
                try:
                    lexeme = Lexeme(grammar, sources, line)
                except:
                    print('Error in line: {}'.format(line.strip()))
                    print('      in {}:{}'.format(data('lexemes.txt'), i))
                    raise

                print('Leksema: {}'.format(lexeme.lexeme))
                print('Vieta: {}:{}'.format(data('lexemes.txt'), i))
                print('Eilutė: {}'.format(line.strip()))
                print('Parametrai: {}'.format(', '.join([
                    '{}={}'.format(k, v) for k, v in lexeme.names.items()
                ])))
                print()

                print_field(1, 'Šaltinis', lexeme.source.code, lexeme.source.label)
                print_field(2, 'Lemma', None, lexeme.lemma)
                print_field(3, 'Kalbos dalis', lexeme.pos.code, lexeme.pos.label)

                for node in lexeme.properties:
                    parent = first(node.parents(code__isnull=False))
                    print_field(parent.code, parent.label, node.code, node.label)

                    for pardef in lexeme.get_pardefs(node):
                        paradigm = paradigms.get(pardef)
                        stem = None
                        for suffix, symbols in paradigm.suffixes():
                            if stem is None:
                                sfx = ''.join(suffix)
                                stem = lexeme.lexeme[:-len(sfx)]

                            symbols = ', '.join(symbols)
                            suffix = '-'.join(suffix)

                            print('    {}: {}/{}'.format(
                                symbols, stem, suffix,
                            ))

                    print()


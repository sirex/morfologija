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

from ..grammar import Node
from ..lexemes import Lexeme


def main():
    args = docopt.docopt(__doc__)
    data_dir = args['--data-dir']
    data = lambda name: os.path.join(data_dir, name)

    with open(data('grammar.yaml'), encoding='utf-8') as f:
        grammar = yaml.load(f)
    grammar = Node(dict(nodes=grammar))

    #with open(data('paradigms.yaml'), encoding='utf-8') as f:
    #    paradigms = yaml.load(f)

    with open(data('lexemes.txt'), encoding='utf-8') as f:
        for line in f:
            lexeme = Lexeme(grammar, line)
            if args['<lexeme>'] == lexeme.lexeme:
                print(line)

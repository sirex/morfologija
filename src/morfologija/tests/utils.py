import yaml
import os.path

from ..grammar import Node
from ..paradigms import ParadigmCollection


test_dir = os.path.dirname(__file__)
data_dir = os.path.join(test_dir, '..', '..', '..', 'data')
data_dir = os.path.abspath(data_dir)
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



def genlexemes(word, **kwargs):
    pass


def lexeme(self, word, **kwargs):
    numbers = [
        prop.values[kwargs.get(name, prop.default)]
        for name, prop in PROPERTIES
    ]
    numbers = ' '.join(map(str, numbers))
    line = ('{word} 1 - {numbers}').format(word=word, numbers=numbers)
    lexeme = Lexeme(self.grammar, self.paradigms, self.source, line)
    return lexeme

def pardefs(self, word, **kwargs):
    lexeme = self.lexeme(word, **kwargs)
    prop = lexeme.properties[0]
    return list(lexeme.get_pardefs(prop))

def lexemes(self, word, **kwargs):
    lexemes = []
    lexeme = self.lexeme(word, **kwargs)
    symorder = ('number', 'gender', 'case')
    for node in lexeme.properties:
        for pardef in lexeme.get_pardefs(node):
            paradigm = self.paradigms.get(pardef)
            for forms, symbols in lexeme.affixes(paradigm, 'suffixes'):
                symbols = [symbols[key] for key in symorder]
                _lexeme = [
                    '%s/%s' % (stem, '/'.join(suffix))
                    for stem, suffix in forms
                ]
                lexemes.append((_lexeme, symbols))
    return lexemes

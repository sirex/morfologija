import yaml
import unittest

from ..grammar import Node
from ..lexemes import Lexeme
from ..paradigms import ParadigmCollection

RES = dict(
    paradigms = """\
- key: case
  symbols:
  - nom
  - gen
  - dat
  - acc
  - ins
  - loc
  - voc

- key: gerv/ės
  symbols:
    gender: f
    number: pl
  define:
    suffixes:
      case:
      - ės
      - ių
      - ėms
      - es
      - ėmis
      - ėse

- key: dėd/ės
  symbols:
    gender: f
    number: pl
  extends:
  - keys: gerv/ės
    replace:
      suffixes:
        case:
          gen: žių
""",

    grammar = """\
nodes:
- code: 1
  nodes:
  - code: 4
    name: declension
    nodes:
    - code: 1
      pardefs:
      - - key: Jon/as
          properties:
            properness: name
        - key: vyr/as
      - vyr/ai
    - code: 2
      pardefs:
      - - key: eln/ias
          endswith: ias
        - key: vėj/as
      - vyr/ai
    - code: 3
      pardefs:
      - dėd/ės
  - code: 5
    name: properness
    nodes:
    - code: 1
    - code: 2
      name: name
  - code: 6
    name: gender
    nodes:
    - code: 1
      symbol: m
    - code: 2
      symbol: f
""",
)


class NodeTests(unittest.TestCase):
    def setUp(self):
        grammar = yaml.load(RES['grammar'])
        self.grammar = Node(grammar)
        self.source = Node(dict(nodes=[dict(code=1, label='')]))
        paradigms = yaml.load(RES['paradigms'])
        self.paradigms = ParadigmCollection(paradigms)

    def lexeme(self, word, declension, properness, gender):
        line = '{word} 1 - 1 {declension} {properness} {gender}'.format(
            word=word, declension=declension, properness=properness,
            gender=gender,
        )
        lexeme = Lexeme(self.grammar, self.source, line)
        return lexeme

    def pardefs(self, *args):
        lexeme = self.lexeme(*args)
        prop = lexeme.properties[0]
        return list(lexeme.get_pardefs(prop))

    def test_pardefs_properties(self):
        self.assertEqual(self.pardefs('vyras',  1, 1, 1), ['vyr/as',  'vyr/ai'])
        self.assertEqual(self.pardefs('Jonas',  1, 2, 1), ['Jon/as',  'vyr/ai'])

    def test_pardefs_endswith(self):
        self.assertEqual(self.pardefs('vėjas',  2, 1, 1), ['vėj/as',  'vyr/ai'])
        self.assertEqual(self.pardefs('elnias', 2, 1, 1), ['eln/ias', 'vyr/ai'])

    def test_symbols(self):
        paradigm = self.paradigms.get('dėd/ės')
        lexeme = self.lexeme('dėdė', 1, 1, 2)
        suffixes = [
            (forms, dict(symbols, **lexeme.symbols))
            for forms, symbols in paradigm.affixes('suffixes')
        ]
        self.assertEqual(suffixes, [
            ([['ės'  ]], {'case': 'nom', 'gender': 'f', 'number': 'pl'}),
            ([['žių' ]], {'case': 'gen', 'gender': 'f', 'number': 'pl'}),
            ([['ėms' ]], {'case': 'dat', 'gender': 'f', 'number': 'pl'}),
            ([['es'  ]], {'case': 'acc', 'gender': 'f', 'number': 'pl'}),
            ([['ėmis']], {'case': 'ins', 'gender': 'f', 'number': 'pl'}),
            ([['ėse' ]], {'case': 'loc', 'gender': 'f', 'number': 'pl'}),
        ])

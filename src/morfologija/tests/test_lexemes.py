import yaml
import unittest

from ..grammar import Node
from ..lexemes import Lexeme

RES = dict(
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
  - code: 5
    name: properness
    nodes:
    - code: 1
    - code: 2
      name: name
""",
)


class NodeTests(unittest.TestCase):
    def setUp(self):
        grammar = yaml.load(RES['grammar'])
        self.grammar = Node(grammar)
        self.source = Node(dict(nodes=[dict(code=1, label='')]))

    def pardefs(self, word, declension, properness):
        line = '{word} 1 - 1 {declension} {properness}'.format(
            word=word, declension=declension, properness=properness
        )
        lexeme = Lexeme(self.grammar, self.source, line)
        prop = lexeme.properties[0]
        return list(lexeme.get_pardefs(prop))

    def test_pardefs_properties(self):
        self.assertEqual(self.pardefs('vyras',  1, 1), ['vyr/as',  'vyr/ai'])
        self.assertEqual(self.pardefs('Jonas',  1, 2), ['Jon/as',  'vyr/ai'])

    def test_pardefs_endswith(self):
        self.assertEqual(self.pardefs('vėjas',  2, 1), ['vėj/as',  'vyr/ai'])
        self.assertEqual(self.pardefs('elnias', 2, 1), ['eln/ias', 'vyr/ai'])

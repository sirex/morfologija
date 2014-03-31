import yaml
import unittest

from ..nodes import Node

from .utils import genlexemes

grammar = """\
- code: 1
  symbol: a
  nodes:
  - code: 1
    symbol: aa
  - code: 2
    symbol: ab
- label: Category
  nodes:
  - label: Subcategory
    nodes:
    - code: 2
      symbol: b
      nodes:
      - code: 1
        symbol: ba
"""


class NodeTests(unittest.TestCase):
    def setUp(self):
        data = yaml.load(grammar)
        self.grammar = Node(dict(nodes=data))

    def test_query(self):
        nodes = self.grammar.query(code__isnull=False)
        symbols = list([n.symbol for n in nodes])
        self.assertEqual(symbols, ['a', 'b'])

    def test_chained_query(self):
        symbol = self.grammar.query(code__isnull=False).get(code=2).symbol
        self.assertEqual(symbol, 'b')


class GrammarTests(unittest.TestCase):
    def test_restrict(self):
        props = dict(declension=1, number='plural')
        self.assertEqual(genlexemes('miltai', 'noun', **props), [
            (['milt/as'  ], ['sg', 'm', 'nom']),
            (['milt/o'   ], ['sg', 'm', 'gen']),
            (['milt/ui'  ], ['sg', 'm', 'dat']),
            (['milt/ą'   ], ['sg', 'm', 'acc']),
            (['milt/u'   ], ['sg', 'm', 'ins']),
            (['milt/e'   ], ['sg', 'm', 'loc']),
            (['milt/e',
              'milt/ai'  ], ['sg', 'm', 'voc']),

            (['milt/ai'  ], ['pl', 'm', 'nom']),
            (['milt/ų'   ], ['pl', 'm', 'gen']),
            (['milt/ams' ], ['pl', 'm', 'dat']),
            (['milt/us'  ], ['pl', 'm', 'acc']),
            (['milt/ais' ], ['pl', 'm', 'ins']),
            (['milt/uose'], ['pl', 'm', 'loc'])
        ])

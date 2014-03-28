import yaml
import unittest

from ..grammar import Node

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

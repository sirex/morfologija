"""
Run tests with:

    env/bin/python -m unittest tests

"""

import yaml
import unittest

from ..grammar import Node

grammar = """\
- code: 1
  symbol: a
  nodes:
  - code: 10
    symbol: a.a
- label: Category
  nodes:
  - label: Subcategory
    nodes:
    - code: 2
      symbol: b
      nodes:
      - code: 20
        symbol: b.a
"""


class NodeTests(unittest.TestCase):
    def test_(self):
        data = yaml.load(grammar)
        node = Node(dict(nodes=data))

        nodes = node.query(code__isnull=False)
        codes = list([n.code for n in nodes])
        self.assertEqual(codes, [1, 2])

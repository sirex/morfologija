"""
Run tests with:

    env/bin/python -m unittest tests

"""

import parse2
import unittest


class NodeTests(unittest.TestCase):
    def test_(self):
        node = parse2.Node(dict(
            fields=[
                dict(code=1, symbol='a', fields=[
                    dict(code=10, symbol='a.a', fields=[
                    ])
                ]),
                dict(label='Category', fields=[
                    dict(label='Subcategory', fields=[
                        dict(code=2, symbol='b', fields=[
                            dict(code=20, symbol='b.a')
                        ])
                    ])
                ]),
            ]
        ))

        nodes = node.query(code__isnull=False)
        codes = list([n.code for n in nodes])
        self.assertEqual(codes, [1, 2])

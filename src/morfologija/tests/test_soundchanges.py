import unittest

from ..soundchanges import affrication


class AffricationTests(unittest.TestCase):
    def assertAffrication(self, sample, expected):
        stem, suffix = sample.split('/')
        stem = affrication(stem, suffix)
        self.assertEqual(expected, '%s/%s' % (stem, suffix))

    def test_affrication(self):
        self.assertAffrication('mart/i',   'mart/i')
        self.assertAffrication('mart/ios', 'marč/ios')

        self.assertAffrication('sodž/ius', 'sodž/ius')

        self.assertAffrication('aikšt/ė',  'aikšt/ė')
        self.assertAffrication('aikšt/ių', 'aikšč/ių')

        self.assertAffrication('šird/is',  'šird/is')
        self.assertAffrication('šird/ies', 'šird/ies')
        self.assertAffrication('šird/iai', 'širdž/iai')
        self.assertAffrication('šird/ių',  'širdž/ių')

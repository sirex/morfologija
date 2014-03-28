import yaml
import unittest

from ..paradigms import ParadigmCollection

RES = dict(
    paradigms = """\
- type: symbols
  key: declension
  label: Linksniai
  symbols:
  - nom
  - gen
  - dat
  - acc
  - ins
  - loc
  - voc

- type: suffixes
  key: vyr/as
  symbols:
  - m
  - sg
  define:
    suffixes:
      declension:
      - as
      - o
      - ui
      - ą
      - u
      - e
      - e

- type: suffixes
  key: Jon/as
  extends:
  - keys: vyr/as
    replace:
      suffixes:
        declension:
          voc: ai

- key: brol/is
  symbols:
  - m
  - sg
  define:
    suffixes:
      declension:
      - is
      - io
      - iui
      - į
      - iu
      - yje
      - i

- key: brol/el/is
  extends:
  - keys:
    - brol/is
    prefix:
      suffixes: el

- key: vėj/as
  symbols:
  - m
  - sg
  define:
    suffixes:
      declension:
      - as
      - o
      - ui
      - ą
      - u
      - [uje, yje]
      - i

""",
)


class NodeTests(unittest.TestCase):
    def setUp(self):
        paradigms = yaml.load(RES['paradigms'])
        self.paradigms = ParadigmCollection(paradigms)

    def test_define(self):
        paradigm = self.paradigms.get('vyr/as')
        suffixes = list(paradigm.affixes('suffixes'))
        self.assertEqual(suffixes, [
            ([['as']], ['nom', 'm', 'sg']),
            ([['o' ]], ['gen', 'm', 'sg']),
            ([['ui']], ['dat', 'm', 'sg']),
            ([['ą' ]], ['acc', 'm', 'sg']),
            ([['u' ]], ['ins', 'm', 'sg']),
            ([['e' ]], ['loc', 'm', 'sg']),
            ([['e' ]], ['voc', 'm', 'sg']),
        ])

    def test_replace(self):
        paradigm = self.paradigms.get('Jon/as')
        suffixes = list(paradigm.affixes('suffixes'))
        self.assertEqual(suffixes, [
            ([['as']], ['nom', 'm', 'sg']),
            ([['o' ]], ['gen', 'm', 'sg']),
            ([['ui']], ['dat', 'm', 'sg']),
            ([['ą' ]], ['acc', 'm', 'sg']),
            ([['u' ]], ['ins', 'm', 'sg']),
            ([['e' ]], ['loc', 'm', 'sg']),
            ([['ai']], ['voc', 'm', 'sg']),
        ])

    def test_prefix(self):
        paradigm = self.paradigms.get('brol/el/is')
        suffixes = list(paradigm.affixes('suffixes'))
        self.assertEqual(suffixes, [
            ([['el', 'is' ]], ['nom', 'm', 'sg']),
            ([['el', 'io' ]], ['gen', 'm', 'sg']),
            ([['el', 'iui']], ['dat', 'm', 'sg']),
            ([['el', 'į'  ]], ['acc', 'm', 'sg']),
            ([['el', 'iu' ]], ['ins', 'm', 'sg']),
            ([['el', 'yje']], ['loc', 'm', 'sg']),
            ([['el', 'i'  ]], ['voc', 'm', 'sg']),
        ])


    def test_multiple_forms(self):
        paradigm = self.paradigms.get('vėj/as')
        suffixes = list(paradigm.affixes('suffixes'))
        self.assertEqual(suffixes, [
            ([['as' ]], ['nom', 'm', 'sg']),
            ([['o'  ]], ['gen', 'm', 'sg']),
            ([['ui' ]], ['dat', 'm', 'sg']),
            ([['ą'  ]], ['acc', 'm', 'sg']),
            ([['u'  ]], ['ins', 'm', 'sg']),
            ([['uje'],
              ['yje']], ['loc', 'm', 'sg']),
            ([['i'  ]], ['voc', 'm', 'sg']),
        ])

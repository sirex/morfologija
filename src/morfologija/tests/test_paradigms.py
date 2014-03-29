import yaml
import unittest

from ..paradigms import ParadigmCollection

RES = dict(
    paradigms = """\
- type: symbols
  key: case
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
   gender: m
   number: sg
  define:
    suffixes:
      case:
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
        case:
          voc: ai

- key: brol/is
  symbols:
    gender: m
    number: sg
  define:
    suffixes:
      case:
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
    gender: m
    number: sg
  define:
    suffixes:
      case:
      - as
      - o
      - ui
      - ą
      - u
      - [uje, yje]
      - i

- key: jūr/a
  symbols:
    gender: f
    number: sg
  define:
    suffixes:
      case:
      - a
      - os
      - ai
      - ą
      - a
      - oje
      - a
    optional-prefixes:
      suffixes: i

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
            ([['as']], {'case': 'nom', 'gender': 'm', 'number': 'sg'}),
            ([['o' ]], {'case': 'gen', 'gender': 'm', 'number': 'sg'}),
            ([['ui']], {'case': 'dat', 'gender': 'm', 'number': 'sg'}),
            ([['ą' ]], {'case': 'acc', 'gender': 'm', 'number': 'sg'}),
            ([['u' ]], {'case': 'ins', 'gender': 'm', 'number': 'sg'}),
            ([['e' ]], {'case': 'loc', 'gender': 'm', 'number': 'sg'}),
            ([['e' ]], {'case': 'voc', 'gender': 'm', 'number': 'sg'}),
        ])

    def test_define_prefix(self):
        paradigm = self.paradigms.get('jūr/a')
        suffixes = list(paradigm.affixes('suffixes'))
        suffixes = [sfx[0][0] for sfx, symbols in suffixes]
        self.assertEqual(suffixes, [
            'a', 'os', 'ai', 'ą', 'a', 'oje', 'a',
        ])

    def test_replace(self):
        paradigm = self.paradigms.get('Jon/as')
        suffixes = list(paradigm.affixes('suffixes'))
        self.assertEqual(suffixes, [
            ([['as']], {'case': 'nom', 'gender': 'm', 'number': 'sg'}),
            ([['o' ]], {'case': 'gen', 'gender': 'm', 'number': 'sg'}),
            ([['ui']], {'case': 'dat', 'gender': 'm', 'number': 'sg'}),
            ([['ą' ]], {'case': 'acc', 'gender': 'm', 'number': 'sg'}),
            ([['u' ]], {'case': 'ins', 'gender': 'm', 'number': 'sg'}),
            ([['e' ]], {'case': 'loc', 'gender': 'm', 'number': 'sg'}),
            ([['ai']], {'case': 'voc', 'gender': 'm', 'number': 'sg'}),
        ])

    def test_prefix(self):
        paradigm = self.paradigms.get('brol/el/is')
        suffixes = list(paradigm.affixes('suffixes'))
        self.assertEqual(suffixes, [
            ([['el', 'is' ]], {'case': 'nom', 'gender': 'm', 'number': 'sg'}),
            ([['el', 'io' ]], {'case': 'gen', 'gender': 'm', 'number': 'sg'}),
            ([['el', 'iui']], {'case': 'dat', 'gender': 'm', 'number': 'sg'}),
            ([['el', 'į'  ]], {'case': 'acc', 'gender': 'm', 'number': 'sg'}),
            ([['el', 'iu' ]], {'case': 'ins', 'gender': 'm', 'number': 'sg'}),
            ([['el', 'yje']], {'case': 'loc', 'gender': 'm', 'number': 'sg'}),
            ([['el', 'i'  ]], {'case': 'voc', 'gender': 'm', 'number': 'sg'}),
        ])

    def test_multiple_forms(self):
        paradigm = self.paradigms.get('vėj/as')
        suffixes = list(paradigm.affixes('suffixes'))
        self.assertEqual(suffixes, [
            ([['as' ]], {'case': 'nom', 'gender': 'm', 'number': 'sg'}),
            ([['o'  ]], {'case': 'gen', 'gender': 'm', 'number': 'sg'}),
            ([['ui' ]], {'case': 'dat', 'gender': 'm', 'number': 'sg'}),
            ([['ą'  ]], {'case': 'acc', 'gender': 'm', 'number': 'sg'}),
            ([['u'  ]], {'case': 'ins', 'gender': 'm', 'number': 'sg'}),
            ([['uje'],
              ['yje']], {'case': 'loc', 'gender': 'm', 'number': 'sg'}),
            ([['i'  ]], {'case': 'voc', 'gender': 'm', 'number': 'sg'}),
        ])

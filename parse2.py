#!/usr/bin/env python3

import sys

import yaml

#   3  1  daiktavardis
#   4  1  tikriniškumas
#   5  1  neigiamumas
#   6  1  pobūdis
#   7  3  linksniuotė
#   8  1  giminė
#   9  1  skaičius
#  10  0  sangrąžiškumas
#  11  0  daryba
#  12  2  mažybiniuotė
#  13  0  -ininkas
#  14  0  -ybė
#  15  0  -ystė
#  16  0  -ingas
#  17  1  -iškas
#  18  1  -inis
#  19  0  -in(i)ai
#  20  0  -ėtas
#  21  0  -(u)otas
#  22  0  prefiksuotė
#
# [5199]
#
# ainis 1 - 1 1 1 1 3 1 1 0 0 2 0 0 0 0 1 1 0 0 0 0


POS = {
     1: ('n',      'daiktavardis'),
     2: ('adj',    'būdvardis'),
     3: ('num',    'skaitvardis'),
     4: ('prn',    'įvardis'),
     5: ('vblex',  'veiksmažodis'),
     6: ('adv',    'prieveiksmis'),
     #7: ('',       'dalelytė'),
     8: ('pr',     'prielinksnis'),
     9: ('cnjcoo', 'jungtukas'),
    10: ('ij',     'jaustukas'),
    #11: ('',       'ištiktukas'),
}


CASES = ('nom', 'gen', 'dat', 'acc', 'ins', 'loc', 'voc')


class DPref(object):
    """Declension prefixes."""
    def __init__(self, name, affixes, sumbols=()):
        pass


class Declension(object):
    def __init__(self, name, affixes, sumbols=()):
        pass


class Derivation(object):
    def __init__(self, name, affixes, sumbols=()):
        pass


class Diminutive(Derivation):
    def __init__(self, name, affixes, sumbols=()):
        pass


PARADIGMS = [
    # Declension prefixes
    DPref('ain/is',        'is  io  iui  į   iu   yje   i',   ('m', 'sg')),
    DPref('ain/iai',       'iai ių  iams ius iais iuose iai', ('m', 'pl')),
    DPref('ain/ė',         'ė   ės  ei   ę   e    ėje   e',   ('f', 'sg')),
    DPref('ain/ės',        'ės  ių  ėms  es  ėmis ėse   ės',  ('f', 'pl')),

    DPref('nam/as',        'as  o   ui   ą   u    e     e',   ('m', 'sg')),
    DPref('nam/ai',        'ai  ų   ams  us  ais  uose  ai',  ('m', 'pl')),

    DPref('aini/išk/as',   'as  ko  kam  ką  ku   kame  as',  ('m', 'sg')),
    DPref('aini/išk/i',    'i   ų   iems us  ais  uose  i',   ('m', 'pl')),
    DPref('aini/išk/a',    'a   os  ai   ą   a    oje   a',   ('f', 'sg')),
    DPref('aini/išk/os',   'os  ų   oms  as  omis ose   os',  ('f', 'pl')),

    # Mažybinės formos (deminutyvai)
    Diminutive('nam/el/is',     'el',    ('ain/is', 'ain/iai', 'ain/ė', 'ain/ės')),
    Diminutive('nam/eliuk/as',  'eliuk', ('nam/as', 'nam/ai',  'ain/ė', 'ain/ės')),
    Diminutive('nam/užėl/is',   'užėl',  ('ain/is', 'ain/iai', 'ain/ė', 'ain/ės')),

    # Kitos derivacijos
    Derivation('bank/inink/as', 'inink', ('nam/as', 'nam/ai',  'ain/ė', 'ain/ės')),
    Derivation('auks/išk/as',   'išk',   ('nam/as', 'nam/ai',  'ain/ė', 'ain/ės')),

    # Paradigmos
    Declension('ain/is', ('ain/is', 'ain/iai',)),

    #Declension('ain/is', (
    #    'BASE__ain/is',       'BASE__ain/iai',
    #    'BASE__nam/el/is',    'BASE__nam/el/iai',
    #    'BASE__nam/eliuk/as', 'BASE__nam/eliuk/ai',
    #    'BASE__auks/išk/as',  'BASE__auks/išk/i',
    #)),
]


def read_data(lmdb):
    with open(lmdb, encoding='cp1257') as f:
        for line in f:
            yield line


def gen_paradigms(lmdb):
    data = read_data(lmdb)
    for i, line in enumerate(data):
        line = line.strip()
        if line.endswith('1 1 1 1 3 1 1 0 0 2 0 0 0 0 1 1 0 0 0 0'):
            print(line)
            break


def gen_symbols(mdb, paradigms):
    for node in mdb:
        symbol = node.get('symbol')
        if symbol is not None:
            yield '<sdef n=%-10s c="%s"/>' % (
                '"%s"' % node['symbol'], node['label']
            )
        else:
            yield '<!-- sdef n=%-10s c="%s"/ -->' % (
                '"%s"' % '', node['label']
            )

    for paradigm in paradigms:
        if paradigm['type'] == 'symbol':
            yield '<sdef n=%-10s c="%s"/>' % (
                '"%s"' % paradigm['key'], paradigm['label']
            )

    #for node in mdb.items():
    #    for category, rules in posrules:
    #        yield ''
    #        yield '%s<!-- %s -->' % (indent, category)
    #        for name, options in rules.values():
    #            yield ''
    #            if name:
    #                yield '%s<!-- %s -->' % (indent, name)
    #            for option in options.values():
    #                if isinstance(option, tuple):
    #                    n, c = option
    #                    yield '%s<sdef n=%-10s c="%s"/>' % (
    #                        indent, '"%s"' % n, c
    #                    )


def build(mdb, paradigms):
    yield '<?xml version="1.0" encoding="UTF-8"?>'
    yield '<dictionary>'
    yield '  <alphabet>AĄBCČDEĘĖFGHIĮYJKLMNOPRSŠTUŲŪVZŽaąbcčdeęėfghiįyjklmnoprsštuųūvzž</alphabet>'
    yield '  <sdefs>'
    for line in gen_symbols(mdb, paradigms):
        yield '    ' + line
    yield '  </sdefs>'
    yield '  <pardefs>'

    #for name, forms in LMDB.items():
    #    for line in gen_paradigm('    ', name, forms, []):
    #        yield line

    #for line in gen_paradigms(lmdb, '    '):
    #    yield line

    yield '  </pardefs>'
    yield '  <section id="main" type="standard">'

    #for line in gen_entries(lmdb, '    '):
    #    yield line

    yield '  </section>'
    yield '</dictionary>'



def main(lmdb):
    with open('lmdb.yaml', encoding='utf-8') as f:
        mdb = yaml.load(f)

    with open('paradigms.yaml', encoding='utf-8') as f:
        paradigms = yaml.load(f)

    #gen_paradigms(lmdb)
    with open('build.dix', 'w', encoding='utf-8') as f:
        for line in build(mdb, paradigms):
            f.write(line + '\n')

    with open('build.dix') as f:
        print(f.read())



if __name__ == '__main__':
    lmdb = sys.argv[1]
    main(lmdb)

#!/usr/bin/env python
# coding: utf-8

import sys

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

CASES = ('nom', 'gen', 'dat', 'acc', 'ins', 'loc', 'voc')

class Base(object):
    pass

class Par(object):
    pass

PARADIGMS = [
    Base(u'ain/is',        u'is  io  iui  į   iu   yje   i',   ('m', 'sg')),
    Base(u'ain/iai',       u'iai ių  iams ius iais iuose iai', ('m', 'pl')),
    Base(u'ain/ė',         u'ė   ės  ei   ę   e    ėje   e',   ('f', 'sg')),
    Base(u'ain/ės',        u'ės  ių  ėms  es  ėmis ėse   ės',  ('f', 'pl')),

    Base(u'nam/as',        u'as  o   ui   ą   u    e     e',   ('m', 'sg')),
    Base(u'nam/ai',        u'ai  ų   ams  us  ais  uose  ai',  ('m', 'pl')),

    Base(u'aini/išk/as',   u'as  ko  kam  ką  ku   kame  as',  ('m', 'sg')),
    Base(u'aini/išk/i',    u'i   ų   iems us  ais  uose  i',   ('m', 'pl')),
    Base(u'aini/išk/a',    u'a   os  ai   ą   a    oje   a',   ('f', 'sg')),
    Base(u'aini/išk/os',   u'os  ų   oms  as  omis ose   os',  ('f', 'pl')),




    # Mažybinės formos (deminutyvai)
    Base(u'nam/el/is',     prefix=u'el',    extends=u'ain/is'),
    Base(u'nam/el/iai',    prefix=u'el',    extends=u'ain/iai'),
    Base(u'merg/el/ė',     prefix=u'el',    extends=u'ain/ė'),
    Base(u'merg/el/ės',    prefix=u'el',    extends=u'ain/ės'),

    Base(u'nam/eliuk/as',  prefix=u'eliuk', extends=u'nam/as'),
    Base(u'nam/eliuk/ai',  prefix=u'eluik', extends=u'nam/ai'),
    Base(u'merg/eliuk/ė',  prefix=u'eliuk', extends=u'ain/ė'),
    Base(u'merg/eliuk/ės', prefix=u'eliuk', extends=u'ain/ės'),

    Base(u'nam/užėl/is',   prefix=u'užėl',  extends=u'ain/is'),
    Base(u'nam/užėl/iai',  prefix=u'užėl',  extends=u'ain/iai'),
    Base(u'merg/užėl/ė',   prefix=u'užėl',  extends=u'ain/ė'),
    Base(u'merg/užėl/ės',  prefix=u'užėl',  extends=u'ain/ės'),


    # Derivacijos
    Base(u'bank/inink/as', prefix=u'inink', extends=u'nam/as'),
    Base(u'bank/inink/ai', prefix=u'inink', extends=u'nam/ai'),
    Base(u'bank/inink/ė',  prefix=u'inink', extends=u'ain/ė'),
    Base(u'bank/inink/ės', prefix=u'inink', extends=u'ain/ės'),

    Base(u'auks/išk/as',   prefix=u'išk',   extends=u'ain/išk/as'),
    Base(u'auks/išk/i',    prefix=u'išk',   extends=u'ain/išk/i'),


    # Paradigmos
    Par(u'ain/is', '1 1 1 1 3 1 1 0 0 2 0 0 0 0 1 1 0 0 0 0', (
        u'BASE__ain/is',       u'BASE__ain/iai',
        u'BASE__nam/el/is',    u'BASE__nam/el/iai',
        u'BASE__nam/eliuk/as', u'BASE__nam/eliuk/ai',
        u'BASE__auks/išk/as',  u'BASE__auks/išk/i',
    )),
]


def read_data(lmdb):
    with open(lmdb) as f:
        for line in f:
            yield line.decode('cp1257')


def gen_paradigms(lmdb):
    data = read_data(lmdb)
    for i, line in enumerate(data):
        line = line.strip()
        if line.endswith('1 1 1 1 3 1 1 0 0 2 0 0 0 0 1 1 0 0 0 0'):
            print line
            break



def main(lmdb):
    gen_paradigms(lmdb)



if __name__ == '__main__':
    lmdb = sys.argv[1]
    main(lmdb)

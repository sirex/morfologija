#!/usr/bin/env python
# coding: utf-8

import sys
import subprocess


class Paradigm(object):
    def __init__(self, name, forms, overrides=None):
        self.name = name
        self.forms = forms
        self.overrides = overrides or {}


POS = {
     1: (u'n',      u'daiktavardis'),
     2: (u'adj',    u'būdvardis'),
     3: (u'num',    u'skaitvardis'),
     4: (u'prn',    u'įvardis'),
     5: (u'vblex',  u'veiksmažodis'),
     6: (u'adv',    u'prieveiksmis'),
     #7: (u'',       u'dalelytė'),
     8: (u'pr',     u'prielinksnis'),
     9: (u'cnjcoo', u'jungtukas'),
    10: (u'ij',     u'jaustukas'),
    #11: (u'',       u'ištiktukas'),
}

SOURCES = {
     1: u'DLKŽ72',
     2: u'DLKŽ72 papild',
     3: u'TŽŽ85',
     4: u'TŽŽ85 papild',
     5: u'Kt., pvz., necenzūr. žodžiai ir pan.',
}


PREFIXES = {
    '+':  (u'',   u' leksemos dalis be prefikso'),
    'N':  (u'ne', u'ne-'),
    'N_': (u'n',  u'n(e)-'),
    'B':  (u'be', u'be-'),
    'B_': (u'b',  u'b(e)-'),
    'S':  (u'si', u'si-'),
    'S_': (u's',  u's(i)-'),
    'E':  (u'ap,su', u'elementarus į daiktavadžio prefiksinę dalį įeinantis priešdėlis (ap-, su- ir t.t., išskyrus N, S, B)'),
    'F':  (u'', u'visi elementarūs priešdėliai, išskyrus ap(i)-, at(i)-, par-'),
    'R':  (u'', u'visi elementarūs priešdėliai, išskyrus ap-, at(i)-, par-, tame tarpe ir api- !'),
    'H':  (u'', u'visi elementarūs priešdėliai, išskyrus at(i)-, par-, tame tarpe ir ap-, api- !'),
    'G':  (u'', u'visi elementarūs priešdėliai, išskyrus at(i)-, par-, api-, tame tarpe ir ap- (bet ne api- !)'),
    'K':  (u'', u'visi elementarūs priešdėliai, išskyrus ap(i)-, ati-, tame tarpe ir at- (be įterptinio i !), ir par-.'),
    'ap': (u'ap', u'elementarusis priešdėlis ap- (be i !)'),
    'at': (u'ap', u'elementarusis priešdėlis at- (be i !)'),
}


VERB_PREFIXES = {
    '+':   (u'', u'be prefikso'),
    'N':   (u'', u'ne-, '),
    'N_':  (u'', u'n(e)-,'),
    'S':   (u'', u'si-,'),
    'S_':  (u'', u's(i)-,'),
    'T':   (u'', u'te-, '),
    'T_':  (u'', u't(e)-, '),
    'B':   (u'', u'be-, '),
    'B_':  (u'', u'b(e)-, '),
    'p':   (u'', u'elementarus į leksemos prefiksinę dalį įeinantis priešdėlis'),
    'f':   (u'', u'visi elementarūs priešdėliai, išskyrus ap(i)-, at(i)-, par-'),
    'g':   (u'', u'visi elementarūs priešdėliai, išskyrus api-,   at(i)-, par-, tame tarpe ir ap- (bet ne api- !)'),
    'r':   (u'', u'visi elementarūs priešdėliai, išskyrus ap-,    at(i)-, par-, tame tarpe ir api- !'),
    'h':   (u'', u'visi elementarūs priešdėliai, išskyrus         at(i)-, par-, tame tarpe ir ap-, api- !'),
    'x':   (u'', u'visi elementarūs priešdėliai, išskyrus ap-,    ati-,   par-, tame tarpe ir at-, ir api- (su įterptiniu i !)'),
    'u':   (u'', u'visi elementarūs priešdėliai, išskyrus api-,   ati-,   par-, tame tarpe ir at-, ir ap- (be įterptinio i !)'),
    'v':   (u'', u'visi elementarūs priešdėliai, išskyrus ap(i)-, at(i)-,       tame tarpe ir par-'),
    'k':   (u'', u'visi elementarūs priešdėliai, išskyrus api,    ati   , par-, tame tarpe ir at-, ap-'),
    'm':   (u'', u'visi elementarūs priešdėliai, išskyrus ap(i)-,         par-, tame tarpe ir at(i)'),
    'n':   (u'', u'visi elementarūs priešdėliai, išskyrus ap(i)-, ati-,   par-, tame tarpe ir at-'),
    'c':   (u'', u'visi elementarūs priešdėliai, išskyrus ap(i)-, ati-,         tame tarpe ir par-, at-'),
    'w':   (u'', u'visi elementarūs priešdėliai, išskyrus         ati-,   par-, tame tarpe ir at-, ir ap(i) -'),
    'd':   (u'', u'visi elementarūs priešdėliai, išskyrus ap(i)-, at-,          tame tarpe ir par-, ati-'),
    'z':   (u'', u'visi elementarūs priešdėliai, išskyrus                 par-, tame tarpe ir at(i)-, ap(i)-'),
    'ap':  (u'', u'elementarusis priešdėlis ap-  (be i)'),
    'api': (u'', u'elementarusis priešdėlis api- (su i)'),
    'at':  (u'', u'elementarusis priešdėlis at-  (be i)'),
    'ati': (u'', u'elementarusis priešdėlis ati- (su i)'),
}


PARADIGMS = {
    u'BASE__nam/elis': [
        (u'elis',    u'', ('m', 'sg', 'nom',), ()),
        (u'elio',    u'', ('m', 'sg', 'gen',), ()),
        (u'eliui',   u'', ('m', 'sg', 'dat',), ()),
        (u'elį',     u'', ('m', 'sg', 'acc',), ()),
        (u'eliu',    u'', ('m', 'sg', 'ins',), ()),
        (u'elyje',   u'', ('m', 'sg', 'loc',), ()),
        (u'eli',     u'', ('m', 'sg', 'voc',), ()),
        (u'eliai',   u'', ('m', 'pl', 'nom',), ()),
        (u'elių',    u'', ('m', 'pl', 'gen',), ()),
        (u'eliams',  u'', ('m', 'pl', 'dat',), ()),
        (u'elius',   u'', ('m', 'pl', 'acc',), ()),
        (u'eliais',  u'', ('m', 'pl', 'ins',), ()),
        (u'eliuose', u'', ('m', 'pl', 'loc',), ()),
        (u'eliai',   u'', ('m', 'pl', 'voc',), ()),

        (u'elė',     u'', ('f', 'sg', 'nom',), ()),
        (u'elės',    u'', ('f', 'sg', 'gen',), ()),
        (u'elei',    u'', ('f', 'sg', 'dat',), ()),
        (u'elę',     u'', ('f', 'sg', 'acc',), ()),
        (u'ele',     u'', ('f', 'sg', 'ins',), ()),
        (u'elėje',   u'', ('f', 'sg', 'loc',), ()),
        (u'ele',     u'', ('f', 'sg', 'voc',), ()),
        (u'elės',    u'', ('f', 'pl', 'nom',), ()),
        (u'elių',    u'', ('f', 'pl', 'gen',), ()),
        (u'elėms',   u'', ('f', 'pl', 'dat',), ()),
        (u'eles',    u'', ('f', 'pl', 'acc',), ()),
        (u'elėmis',  u'', ('f', 'pl', 'ins',), ()),
        (u'elėse',   u'', ('f', 'pl', 'loc',), ()),
        (u'elės',    u'', ('f', 'pl', 'voc',), ()),
    ],
    u'BASE__nam/eliukas': [
        (u'eliukas',   u'', ('m', 'sg', 'nom',), ()),
        (u'eliuko',    u'', ('m', 'sg', 'gen',), ()),
        (u'eliukui',   u'', ('m', 'sg', 'dat',), ()),
        (u'eliuką',    u'', ('m', 'sg', 'acc',), ()),
        (u'eliuku',    u'', ('m', 'sg', 'ins',), ()),
        (u'eliuke',    u'', ('m', 'sg', 'loc',), ()),
        (u'eliuke',    u'', ('m', 'sg', 'voc',), ()),
        (u'eliukai',   u'', ('m', 'pl', 'nom',), ()),
        (u'eliukų',    u'', ('m', 'pl', 'gen',), ()),
        (u'eliukams',  u'', ('m', 'pl', 'dat',), ()),
        (u'eliukus',   u'', ('m', 'pl', 'acc',), ()),
        (u'eliukais',  u'', ('m', 'pl', 'ins',), ()),
        (u'eliukuose', u'', ('m', 'pl', 'loc',), ()),
        (u'eliukai',   u'', ('m', 'pl', 'voc',), ()),

        (u'eliukė',     u'', ('f', 'sg', 'nom',), ()),
        (u'eliukės',    u'', ('f', 'sg', 'gen',), ()),
        (u'eliukei',    u'', ('f', 'sg', 'dat',), ()),
        (u'eliukę',     u'', ('f', 'sg', 'acc',), ()),
        (u'eliuke',     u'', ('f', 'sg', 'ins',), ()),
        (u'eliukėje',   u'', ('f', 'sg', 'loc',), ()),
        (u'eliuke',     u'', ('f', 'sg', 'voc',), ()),
        (u'eliukės',    u'', ('f', 'pl', 'nom',), ()),
        (u'eliukių',    u'', ('f', 'pl', 'gen',), ()),
        (u'eliukėms',   u'', ('f', 'pl', 'dat',), ()),
        (u'eliukes',    u'', ('f', 'pl', 'acc',), ()),
        (u'eliukėmis',  u'', ('f', 'pl', 'ins',), ()),
        (u'eliukėse',   u'', ('f', 'pl', 'loc',), ()),
        (u'eliukės',    u'', ('f', 'pl', 'voc',), ()),
    ],
    u'BASE__bern/užėlis': [
        (u'užėlis',    u'', ('m', 'sg', 'nom',), ()),
        (u'užėlio',    u'', ('m', 'sg', 'gen',), ()),
        (u'užėliui',   u'', ('m', 'sg', 'dat',), ()),
        (u'užėlį',     u'', ('m', 'sg', 'acc',), ()),
        (u'užėliu',    u'', ('m', 'sg', 'ins',), ()),
        (u'užėlyje',   u'', ('m', 'sg', 'loc',), ()),
        (u'užėli',     u'', ('m', 'sg', 'voc',), ()),
        (u'užėliai',   u'', ('m', 'pl', 'nom',), ()),
        (u'užėlių',    u'', ('m', 'pl', 'gen',), ()),
        (u'užėliams',  u'', ('m', 'pl', 'dat',), ()),
        (u'užėlius',   u'', ('m', 'pl', 'acc',), ()),
        (u'užėliais',  u'', ('m', 'pl', 'ins',), ()),
        (u'užėliuose', u'', ('m', 'pl', 'loc',), ()),
        (u'užėliai',   u'', ('m', 'pl', 'voc',), ()),

        (u'užėlė',     u'', ('f', 'sg', 'nom',), ()),
        (u'užėlės',    u'', ('f', 'sg', 'gen',), ()),
        (u'užėlei',    u'', ('f', 'sg', 'dat',), ()),
        (u'užėlę',     u'', ('f', 'sg', 'acc',), ()),
        (u'užėle',     u'', ('f', 'sg', 'ins',), ()),
        (u'užėlėje',   u'', ('f', 'sg', 'loc',), ()),
        (u'užėle',     u'', ('f', 'sg', 'voc',), ()),
        (u'užėlės',    u'', ('f', 'pl', 'nom',), ()),
        (u'užėlių',    u'', ('f', 'pl', 'gen',), ()),
        (u'užėlėms',   u'', ('f', 'pl', 'dat',), ()),
        (u'užėles',    u'', ('f', 'pl', 'acc',), ()),
        (u'užėlėmis',  u'', ('f', 'pl', 'ins',), ()),
        (u'užėlėse',   u'', ('f', 'pl', 'loc',), ()),
        (u'užėlės',    u'', ('f', 'pl', 'voc',), ()),
    ],
    u'BASE__bank/ininkas': [
        (u'ininkas',   u'', ('m', 'sg', 'nom',), ()),
        (u'ininko',    u'', ('m', 'sg', 'gen',), ()),
        (u'ininkui',   u'', ('m', 'sg', 'dat',), ()),
        (u'ininką',    u'', ('m', 'sg', 'acc',), ()),
        (u'ininku',    u'', ('m', 'sg', 'ins',), ()),
        (u'ininke',    u'', ('m', 'sg', 'loc',), ()),
        (u'ininke',    u'', ('m', 'sg', 'voc',), ()),
        (u'ininkai',   u'', ('m', 'pl', 'nom',), ()),
        (u'ininkų',    u'', ('m', 'pl', 'gen',), ()),
        (u'ininkams',  u'', ('m', 'pl', 'dat',), ()),
        (u'ininkus',   u'', ('m', 'pl', 'acc',), ()),
        (u'ininkais',  u'', ('m', 'pl', 'ins',), ()),
        (u'ininkuose', u'', ('m', 'pl', 'loc',), ()),
        (u'ininkai',   u'', ('m', 'pl', 'voc',), ()),

        (u'ininkė',    u'', ('f', 'sg', 'nom',), ()),
        (u'ininkės',   u'', ('f', 'sg', 'gen',), ()),
        (u'ininkei',   u'', ('f', 'sg', 'dat',), ()),
        (u'ininkę',    u'', ('f', 'sg', 'acc',), ()),
        (u'ininke',    u'', ('f', 'sg', 'ins',), ()),
        (u'ininkėje',  u'', ('f', 'sg', 'loc',), ()),
        (u'ininke',    u'', ('f', 'sg', 'voc',), ()),
        (u'ininkės',   u'', ('f', 'pl', 'nom',), ()),
        (u'ininkių',   u'', ('f', 'pl', 'gen',), ()),
        (u'ininkėms',  u'', ('f', 'pl', 'dat',), ()),
        (u'ininkes',   u'', ('f', 'pl', 'acc',), ()),
        (u'ininkėmis', u'', ('f', 'pl', 'ins',), ()),
        (u'ininkėse',  u'', ('f', 'pl', 'loc',), ()),
        (u'ininkės',   u'', ('f', 'pl', 'voc',), ()),
    ],

    u'BASE__bais/ybė': [
        (u'ybė',     u'', ('f', 'sg', 'nom',), ()),
        (u'ybės',    u'', ('f', 'sg', 'gen',), ()),
        (u'ybei',    u'', ('f', 'sg', 'dat',), ()),
        (u'ybę',     u'', ('f', 'sg', 'acc',), ()),
        (u'ybe',     u'', ('f', 'sg', 'ins',), ()),
        (u'ybėje',   u'', ('f', 'sg', 'loc',), ()),
        (u'ybe',     u'', ('f', 'sg', 'voc',), ()),
        (u'ybės',    u'', ('f', 'pl', 'nom',), ()),
        (u'ybių',    u'', ('f', 'pl', 'gen',), ()),
        (u'ybėms',   u'', ('f', 'pl', 'dat',), ()),
        (u'ybes',    u'', ('f', 'pl', 'acc',), ()),
        (u'ybėmis',  u'', ('f', 'pl', 'ins',), ()),
        (u'ybėse',   u'', ('f', 'pl', 'loc',), ()),
        (u'ybės',    u'', ('f', 'pl', 'voc',), ()),
    ],

    u'BASE__bern/ystė': [
        (u'ystė',     u'', ('m', 'sg', 'nom',), ()),
        (u'ystės',    u'', ('m', 'sg', 'gen',), ()),
        (u'ystei',    u'', ('m', 'sg', 'dat',), ()),
        (u'ystę',     u'', ('m', 'sg', 'acc',), ()),
        (u'yste',     u'', ('m', 'sg', 'ins',), ()),
        (u'ystėje',   u'', ('m', 'sg', 'loc',), ()),
        (u'yste',     u'', ('m', 'sg', 'voc',), ()),
        (u'ystės',    u'', ('m', 'pl', 'nom',), ()),
        (u'ysčių',    u'', ('m', 'pl', 'gen',), ()),
        (u'ystėms',   u'', ('m', 'pl', 'dat',), ()),
        (u'ystes',    u'', ('m', 'pl', 'acc',), ()),
        (u'ystėmis',  u'', ('m', 'pl', 'ins',), ()),
        (u'ystėse',   u'', ('m', 'pl', 'loc',), ()),
        (u'ystės',    u'', ('m', 'pl', 'voc',), ()),

        (u'ystė',     u'', ('f', 'sg', 'nom',), ()),
        (u'ystės',    u'', ('f', 'sg', 'gen',), ()),
        (u'ystei',    u'', ('f', 'sg', 'dat',), ()),
        (u'ystę',     u'', ('f', 'sg', 'acc',), ()),
        (u'yste',     u'', ('f', 'sg', 'ins',), ()),
        (u'ystėje',   u'', ('f', 'sg', 'loc',), ()),
        (u'yste',     u'', ('f', 'sg', 'voc',), ()),
        (u'ystės',    u'', ('f', 'pl', 'nom',), ()),
        (u'ysčių',    u'', ('f', 'pl', 'gen',), ()),
        (u'ystėms',   u'', ('f', 'pl', 'dat',), ()),
        (u'ystes',    u'', ('f', 'pl', 'acc',), ()),
        (u'ystėmis',  u'', ('f', 'pl', 'ins',), ()),
        (u'ystėse',   u'', ('f', 'pl', 'loc',), ()),
        (u'ystės',    u'', ('f', 'pl', 'voc',), ()),
    ],

    u'BASE__bais/ingas': [
        (u'ingas',    u'', ('m', 'sg', 'nom',), ()),
        (u'ingo',     u'', ('m', 'sg', 'gen',), ()),
        (u'ingam',    u'', ('m', 'sg', 'dat',), ()),
        (u'ingą',     u'', ('m', 'sg', 'acc',), ()),
        (u'ingu',     u'', ('m', 'sg', 'ins',), ()),
        (u'ingame',   u'', ('m', 'sg', 'loc',), ()),
        (u'ingasis',  u'', ('m', 'sg', 'voc',), ()),
        (u'ingi',     u'', ('m', 'pl', 'nom',), ()),
        (u'ingų',     u'', ('m', 'pl', 'gen',), ()),
        (u'ingiems',  u'', ('m', 'pl', 'dat',), ()),
        (u'ingus',    u'', ('m', 'pl', 'acc',), ()),
        (u'ingais',   u'', ('m', 'pl', 'ins',), ()),
        (u'inguose',  u'', ('m', 'pl', 'loc',), ()),
        (u'ingi',     u'', ('m', 'pl', 'voc',), ()),

        (u'inga',     u'', ('f', 'sg', 'nom',), ()),
        (u'ingos',    u'', ('f', 'sg', 'gen',), ()),
        (u'ingai',    u'', ('f', 'sg', 'dat',), ()),
        (u'ingą',     u'', ('f', 'sg', 'acc',), ()),
        (u'inga',     u'', ('f', 'sg', 'ins',), ()),
        (u'ingoje',   u'', ('f', 'sg', 'loc',), ()),
        (u'inga',     u'', ('f', 'sg', 'voc',), ()),
        (u'ingos',    u'', ('f', 'pl', 'nom',), ()),
        (u'ingų',     u'', ('f', 'pl', 'gen',), ()),
        (u'ingoms',   u'', ('f', 'pl', 'dat',), ()),
        (u'ingas',    u'', ('f', 'pl', 'acc',), ()),
        (u'ingomis',  u'', ('f', 'pl', 'ins',), ()),
        (u'ingose',   u'', ('f', 'pl', 'loc',), ()),
        (u'ingos',    u'', ('f', 'pl', 'voc',), ()),
    ],

    u'BASE__auks/iškas': [
        (u'iškas',   u'', ('m', 'sg', 'nom',), ()),
        (u'iško',    u'', ('m', 'sg', 'gen',), ()),
        (u'iškam',   u'', ('m', 'sg', 'dat',), ()),
        (u'išką',    u'', ('m', 'sg', 'acc',), ()),
        (u'išku',    u'', ('m', 'sg', 'ins',), ()),
        (u'iške',    u'', ('m', 'sg', 'loc',), ()),
        (u'iške',    u'', ('m', 'sg', 'voc',), ()),
        (u'iškai',   u'', ('m', 'pl', 'nom',), ()),
        (u'iškų',    u'', ('m', 'pl', 'gen',), ()),
        (u'iškams',  u'', ('m', 'pl', 'dat',), ()),
        (u'iškus',   u'', ('m', 'pl', 'acc',), ()),
        (u'iškais',  u'', ('m', 'pl', 'ins',), ()),
        (u'iškuose', u'', ('m', 'pl', 'loc',), ()),
        (u'iškai',   u'', ('m', 'pl', 'voc',), ()),

        (u'iška',     u'', ('f', 'sg', 'nom',), ()),
        (u'iškos',    u'', ('f', 'sg', 'gen',), ()),
        (u'iškai',    u'', ('f', 'sg', 'dat',), ()),
        (u'išką',     u'', ('f', 'sg', 'acc',), ()),
        (u'iška',     u'', ('f', 'sg', 'ins',), ()),
        (u'iškoje',   u'', ('f', 'sg', 'loc',), ()),
        (u'iška',     u'', ('f', 'sg', 'voc',), ()),
        (u'iškos',    u'', ('f', 'pl', 'nom',), ()),
        (u'iškų',     u'', ('f', 'pl', 'gen',), ()),
        (u'iškoms',   u'', ('f', 'pl', 'dat',), ()),
        (u'iškas',    u'', ('f', 'pl', 'acc',), ()),
        (u'iškomis',  u'', ('f', 'pl', 'ins',), ()),
        (u'iškose',   u'', ('f', 'pl', 'loc',), ()),
        (u'iškos',    u'', ('f', 'pl', 'voc',), ()),
    ],

    u'BASE__nam/inis': [
        (u'inis',    u'', ('m', 'sg', 'nom',), ()),
        (u'inio',    u'', ('m', 'sg', 'gen',), ()),
        (u'iniui',   u'', ('m', 'sg', 'dat',), ()),
        (u'inį',     u'', ('m', 'sg', 'acc',), ()),
        (u'iniu',    u'', ('m', 'sg', 'ins',), ()),
        (u'inyje',   u'', ('m', 'sg', 'loc',), ()),
        (u'ini',     u'', ('m', 'sg', 'voc',), ()),
        (u'iniai',   u'', ('m', 'pl', 'nom',), ()),
        (u'inių',    u'', ('m', 'pl', 'gen',), ()),
        (u'iniams',  u'', ('m', 'pl', 'dat',), ()),
        (u'inius',   u'', ('m', 'pl', 'acc',), ()),
        (u'iniais',  u'', ('m', 'pl', 'ins',), ()),
        (u'iniuose', u'', ('m', 'pl', 'loc',), ()),
        (u'iniai',   u'', ('m', 'pl', 'voc',), ()),

        (u'inė',     u'', ('f', 'sg', 'nom',), ()),
        (u'inės',    u'', ('f', 'sg', 'gen',), ()),
        (u'inei',    u'', ('f', 'sg', 'dat',), ()),
        (u'inę',     u'', ('f', 'sg', 'acc',), ()),
        (u'ine',     u'', ('f', 'sg', 'ins',), ()),
        (u'inėje',   u'', ('f', 'sg', 'loc',), ()),
        (u'ine',     u'', ('f', 'sg', 'voc',), ()),
        (u'inės',    u'', ('f', 'pl', 'nom',), ()),
        (u'inių',    u'', ('f', 'pl', 'gen',), ()),
        (u'inėms',   u'', ('f', 'pl', 'dat',), ()),
        (u'ines',    u'', ('f', 'pl', 'acc',), ()),
        (u'inėmis',  u'', ('f', 'pl', 'ins',), ()),
        (u'inėse',   u'', ('f', 'pl', 'loc',), ()),
        (u'inės',    u'', ('f', 'pl', 'voc',), ()),
    ],


    #18: u'in(i)ai',

    #19: u'ėtas',
    u'BASE__kaul/ėtas': [
        (u'ėtas',   u'', ('m', 'sg', 'nom',), ()),
        (u'ėto',    u'', ('m', 'sg', 'gen',), ()),
        (u'ėtam',   u'', ('m', 'sg', 'dat',), ()),
        (u'ėtą',    u'', ('m', 'sg', 'acc',), ()),
        (u'ėtu',    u'', ('m', 'sg', 'ins',), ()),
        (u'ėte',    u'', ('m', 'sg', 'loc',), ()),
        (u'ėte',    u'', ('m', 'sg', 'voc',), ()),
        (u'ėtai',   u'', ('m', 'pl', 'nom',), ()),
        (u'ėtų',    u'', ('m', 'pl', 'gen',), ()),
        (u'ėtams',  u'', ('m', 'pl', 'dat',), ()),
        (u'ėtus',   u'', ('m', 'pl', 'acc',), ()),
        (u'ėtais',  u'', ('m', 'pl', 'ins',), ()),
        (u'ėtuose', u'', ('m', 'pl', 'loc',), ()),
        (u'ėtai',   u'', ('m', 'pl', 'voc',), ()),

        (u'ėta',     u'', ('f', 'sg', 'nom',), ()),
        (u'ėtos',    u'', ('f', 'sg', 'gen',), ()),
        (u'ėtai',    u'', ('f', 'sg', 'dat',), ()),
        (u'ėtą',     u'', ('f', 'sg', 'acc',), ()),
        (u'ėta',     u'', ('f', 'sg', 'ins',), ()),
        (u'ėtoje',   u'', ('f', 'sg', 'loc',), ()),
        (u'ėta',     u'', ('f', 'sg', 'voc',), ()),
        (u'ėtos',    u'', ('f', 'pl', 'nom',), ()),
        (u'ėtų',     u'', ('f', 'pl', 'gen',), ()),
        (u'ėtoms',   u'', ('f', 'pl', 'dat',), ()),
        (u'ėtas',    u'', ('f', 'pl', 'acc',), ()),
        (u'ėtomis',  u'', ('f', 'pl', 'ins',), ()),
        (u'ėtose',   u'', ('f', 'pl', 'loc',), ()),
        (u'ėtos',    u'', ('f', 'pl', 'voc',), ()),
    ],

    #20: u'(u)otas',
    u'BASE__auks/uotas': [
        (u'uotas',   u'', ('m', 'sg', 'nom',), ()),
        (u'uoto',    u'', ('m', 'sg', 'gen',), ()),
        (u'uotui',   u'', ('m', 'sg', 'dat',), ()),
        (u'uotą',    u'', ('m', 'sg', 'acc',), ()),
        (u'uotu',    u'', ('m', 'sg', 'ins',), ()),
        (u'uote',    u'', ('m', 'sg', 'loc',), ()),
        (u'uote',    u'', ('m', 'sg', 'voc',), ()),
        (u'uotai',   u'', ('m', 'pl', 'nom',), ()),
        (u'uotų',    u'', ('m', 'pl', 'gen',), ()),
        (u'uotams',  u'', ('m', 'pl', 'dat',), ()),
        (u'uotus',   u'', ('m', 'pl', 'acc',), ()),
        (u'uotais',  u'', ('m', 'pl', 'ins',), ()),
        (u'uotuose', u'', ('m', 'pl', 'loc',), ()),
        (u'uotai',   u'', ('m', 'pl', 'voc',), ()),
    ],
}


MORPHOLOGY = {
    # Daiktavardis
    1: [
        (u'Daiktavardžio įpatumai', {
             4: (u'Tikriniškumas', {
                  1: u'Bendrinis',
                  2: ('ant', u'Asmenvardis-vardas'),
                  3: u'Ne tikrinis, bet  "iš pagarbos" ir pan. gali būti traktuojamas (t.y. rašomas iš didžiosios) kaip tikrinis (pvz., Dievas, Altingas, Koranas ir pan.)',
                  4: ('top', u'Tikrinis geografinis vardas - miestas, kaimas, šalis, gyvenvietė, t.y. toks, iš kurio galimi vediniai su -ietis(-ė) ir pan.'),
                  5: ('org', u'Kiti tikriniai vardai, pvz., firmų pavadinimai'),
                  6: ('hyd', u'Tikrinis geografinis vardas: upės, ežerai, kalnai ir pan.'),
                  7: u'Subendrinėjęs asmenvardis-vardas (gali būti rašomas ir iš mažosios, ir iš didžiosios), pvz., Eskulapas-eskulapas',
                  8: u'Subendrinėjęs tikrinis geografinis vardas (gali būti rašomas tiek mažosios, tiek iš didžiosios), pvz., Kvirinalas-kvirinalas',
                  9: u'Subendrinėjęs kitas tikrinis vardas (pvz., antikinių švenčių), pvz., herėjos-Herėjos',
             }),
             5: (u'Neigiamumas', {
                  1: u'Daiktavardis žodynuose be neigiančio prefikso, neigiančių prefiksų turėti negali',
                  2: u'Turi neigiantį prefiksą a-; be šito prefikso jis nevartojamas; pvz.: alogizmas',
                  3: u'Turi neigiantį prefiksą an-; be šito prefikso jis nevartojamas; pvz...: analfabetizmas',
                  4: u'Turi neigiantį prefiksą a-; yra atitinkamas dktv ir be šito prefikso; pvz...: aneurinas',
                  5: u'Turi neigiantį prefiksą be-; yra atitinkamas dktv ir be šito prefikso; pvz...: besotumas',
                  6: u'Turi neigiantį prefiksą ne-; yra atitinkamas dktv ir be šito prefikso; pvz...: neakivaizdininkas',
                  7: u'Turi neigiantį prefiksą ne-; be šito prefikso jis nevartojamas; pvz...: nerimas',
                  8: u'Turi neigiantį prefiksą be-; be šito prefikso jis nevartojamas; bedalis',
                  9: u'Daiktavardis žodynuose be neigiančio prefikso; gali turėti neigiančius prefiksus ne-, nebe- ir pan.; pvz...: abejingumas-neabejingumas',
             }),
             6: (u'Kiti ypatumai (daiktavardžio pobūdis)', {
                  1: u'Eilinis daiktavardis',
                  2: u'Etnonimas (tautietis)',
                  3: u'Fleksiškai nekaitomas, (paprastai?) kitų kalbų, bendrinis, pvz., kredo',
                  4: u'Teksto vienetas-užsienio k. įterpinys (dažniausiai posakiuose, pvz. lotyniškuose, ir pan.), kuriam lietuvių k. gramatinės kategorijos (giminė, linksnis, kalbos d. ir pan.) neturi prasmės arba turi ją sąlyginai; priskyrimas daiktavardžiams [dažniausiai] irgi yra sąlyginis; pvz.: allegro, coupe, entree',
                  5: u'Vyriškos giminės "moteriškai" linksniuojamas, žr. DLKG97 §104 e) ir f)',
                  6: u'Vyriškos giminės, sudaiktavardėjęs iš būdvardžio, pvz jaunasis',
                  7: u'Vyriškos giminės, sudaiktavardėjęs iš dalyvio, pvz., išrinktasis, palaimintasis, pažįstamas, laukiamasis, mylimasis, kaltinamasis, nežinomasis, dirbantysis, suaugęs',
                  8: u'Moteriškos giminės, sudaiktavardėjęs iš būdvardžio, pvz., jaunoji, gulsčioji, baltosios, lygiosios',
                  9: u'Moteriškos giminės, sudaiktavardėjęs iš dalyvio, pvz., palaimintoji, pažįstama, kertamoji, kuliamoji, mylimoji, dirbančioji, sprogtinoji',
                 10: u'Bendrosios giminės "vyriškai" linksniuojamas',
                 11: u'Bendrosios giminės "moteriškai" linksniuojamas',
             }),
        }),
        (u'Kaitybos charakteristika', {
             7: (u'Linksniavimo charakteristika', {
                  0: u'Daiktavardis nekaitomas, nelinksniuojamas',
                  1: Paradigm(u'(i)a linksniuotė, paradigma nr. 1 (žiūr DLKG97 psl.70)', [
                          (u'as',   u'as', ('m', 'sg', 'nom',), ()),
                          (u'o',    u'as', ('m', 'sg', 'gen',), ()),
                          (u'ui',   u'as', ('m', 'sg', 'dat',), ()),
                          (u'ą',    u'as', ('m', 'sg', 'acc',), ()),
                          (u'u',    u'as', ('m', 'sg', 'ins',), ()),
                          (u'e',    u'as', ('m', 'sg', 'loc',), ()),
                          (u'e',    u'as', ('m', 'sg', 'voc',), ()),
                          (u'ai',   u'as', ('m', 'pl', 'nom',), ()),
                          (u'ų',    u'as', ('m', 'pl', 'gen',), ()),
                          (u'ams',  u'as', ('m', 'pl', 'dat',), ()),
                          (u'us',   u'as', ('m', 'pl', 'acc',), ()),
                          (u'ais',  u'as', ('m', 'pl', 'ins',), ()),
                          (u'uose', u'as', ('m', 'pl', 'loc',), ()),
                          (u'ai',   u'as', ('m', 'pl', 'voc',), ()),

                          (u'ė',    u'as', ('f', 'sg', 'nom',), ()),
                          (u'ės',   u'as', ('f', 'sg', 'gen',), ()),
                          (u'ei',   u'as', ('f', 'sg', 'dat',), ()),
                          (u'ę',    u'as', ('f', 'sg', 'acc',), ()),
                          (u'e',    u'as', ('f', 'sg', 'ins',), ()),
                          (u'ėje',  u'as', ('f', 'sg', 'loc',), ()),
                          (u'e',    u'as', ('f', 'sg', 'voc',), ()),
                          (u'ės',   u'as', ('f', 'pl', 'nom',), ()),
                          (u'ių',   u'as', ('f', 'pl', 'gen',), ()),
                          (u'ėms',  u'as', ('f', 'pl', 'dat',), ()),
                          (u'es',   u'as', ('f', 'pl', 'acc',), ()),
                          (u'ėmis', u'as', ('f', 'pl', 'ins',), ()),
                          (u'ėse',  u'as', ('f', 'pl', 'loc',), ()),
                          (u'ės',   u'as', ('f', 'pl', 'voc',), ()),
                      ]),
                  2: Paradigm(u'(i)a linksniuotė, paradigma nr. 2 (žiūr DLKG97 psl.71)', [
                          (u'as',   u'as', ('m', 'sg', 'nom',), ()),
                          (u'o',    u'as', ('m', 'sg', 'gen',), ()),
                          (u'ui',   u'as', ('m', 'sg', 'dat',), ()),
                          (u'ą',    u'as', ('m', 'sg', 'acc',), ()),
                          (u'u',    u'as', ('m', 'sg', 'ins',), ()),
                          (u'uje',  u'as', ('m', 'sg', 'loc',), ()),
                          (u'au',   u'as', ('m', 'sg', 'voc',), ()),
                          (u'ai',   u'as', ('m', 'pl', 'nom',), ()),
                          (u'ų',    u'as', ('m', 'pl', 'gen',), ()),
                          (u'ams',  u'as', ('m', 'pl', 'dat',), ()),
                          (u'us',   u'as', ('m', 'pl', 'acc',), ()),
                          (u'ais',  u'as', ('m', 'pl', 'ins',), ()),
                          (u'uose', u'as', ('m', 'pl', 'loc',), ()),
                          (u'ai',   u'as', ('m', 'pl', 'voc',), ()),

                          (u'a',    u'as', ('f', 'sg', 'nom',), ()),
                          (u'os',   u'as', ('f', 'sg', 'gen',), ()),
                          (u'ai',   u'as', ('f', 'sg', 'dat',), ()),
                          (u'ą',    u'as', ('f', 'sg', 'acc',), ()),
                          (u'a',    u'as', ('f', 'sg', 'ins',), ()),
                          (u'oje',  u'as', ('f', 'sg', 'loc',), ()),
                          (u'a',    u'as', ('f', 'sg', 'voc',), ()),
                          (u'os',   u'as', ('f', 'pl', 'nom',), ()),
                          (u'ų',    u'as', ('f', 'pl', 'gen',), ()),
                          (u'oms',  u'as', ('f', 'pl', 'dat',), ()),
                          (u'as',   u'as', ('f', 'pl', 'acc',), ()),
                          (u'omis', u'as', ('f', 'pl', 'ins',), ()),
                          (u'ose',  u'as', ('f', 'pl', 'loc',), ()),
                          (u'os',   u'as', ('f', 'pl', 'voc',), ()),
                      ], {
                      u'BASE__nam/elis': (u'BASE__artoj/ėlis', [
                          (u'ėlis',    u'', ('m', 'sg', 'nom',), ()),
                          (u'ėlio',    u'', ('m', 'sg', 'gen',), ()),
                          (u'ėliui',   u'', ('m', 'sg', 'dat',), ()),
                          (u'ėlį',     u'', ('m', 'sg', 'acc',), ()),
                          (u'ėliu',    u'', ('m', 'sg', 'ins',), ()),
                          (u'ėlyje',   u'', ('m', 'sg', 'loc',), ()),
                          (u'ėli',     u'', ('m', 'sg', 'voc',), ()),
                          (u'ėliai',   u'', ('m', 'pl', 'nom',), ()),
                          (u'ėlių',    u'', ('m', 'pl', 'gen',), ()),
                          (u'ėliams',  u'', ('m', 'pl', 'dat',), ()),
                          (u'ėlius',   u'', ('m', 'pl', 'acc',), ()),
                          (u'ėliais',  u'', ('m', 'pl', 'ins',), ()),
                          (u'ėliuose', u'', ('m', 'pl', 'loc',), ()),
                          (u'ėliai',   u'', ('m', 'pl', 'voc',), ()),

                          (u'ėlė',     u'', ('f', 'sg', 'nom',), ()),
                          (u'ėlės',    u'', ('f', 'sg', 'gen',), ()),
                          (u'ėlei',    u'', ('f', 'sg', 'dat',), ()),
                          (u'ėlę',     u'', ('f', 'sg', 'acc',), ()),
                          (u'ėle',     u'', ('f', 'sg', 'ins',), ()),
                          (u'ėlėje',   u'', ('f', 'sg', 'loc',), ()),
                          (u'ėle',     u'', ('f', 'sg', 'voc',), ()),
                          (u'ėlės',    u'', ('f', 'pl', 'nom',), ()),
                          (u'ėlių',    u'', ('f', 'pl', 'gen',), ()),
                          (u'ėlėms',   u'', ('f', 'pl', 'dat',), ()),
                          (u'ėles',    u'', ('f', 'pl', 'acc',), ()),
                          (u'ėlėmis',  u'', ('f', 'pl', 'ins',), ()),
                          (u'ėlėse',   u'', ('f', 'pl', 'loc',), ()),
                          (u'ėlės',    u'', ('f', 'pl', 'voc',), ()),
                      ]),
                      u'BASE__nam/eliukas': (u'BASE__artoj/ėliukas', [
                          (u'ėliukas',   u'', ('m', 'sg', 'nom',), ()),
                          (u'ėliuko',    u'', ('m', 'sg', 'gen',), ()),
                          (u'ėliukui',   u'', ('m', 'sg', 'dat',), ()),
                          (u'ėliuką',    u'', ('m', 'sg', 'acc',), ()),
                          (u'ėliuku',    u'', ('m', 'sg', 'ins',), ()),
                          (u'ėliuke',    u'', ('m', 'sg', 'loc',), ()),
                          (u'ėliuke',    u'', ('m', 'sg', 'voc',), ()),
                          (u'ėliukai',   u'', ('m', 'pl', 'nom',), ()),
                          (u'ėliukų',    u'', ('m', 'pl', 'gen',), ()),
                          (u'ėliukams',  u'', ('m', 'pl', 'dat',), ()),
                          (u'ėliukus',   u'', ('m', 'pl', 'acc',), ()),
                          (u'ėliukais',  u'', ('m', 'pl', 'ins',), ()),
                          (u'ėliukuose', u'', ('m', 'pl', 'loc',), ()),
                          (u'ėliukai',   u'', ('m', 'pl', 'voc',), ()),

                          (u'ėliukė',     u'', ('f', 'sg', 'nom',), ()),
                          (u'ėliukės',    u'', ('f', 'sg', 'gen',), ()),
                          (u'ėliukei',    u'', ('f', 'sg', 'dat',), ()),
                          (u'ėliukę',     u'', ('f', 'sg', 'acc',), ()),
                          (u'ėliuke',     u'', ('f', 'sg', 'ins',), ()),
                          (u'ėliukėje',   u'', ('f', 'sg', 'loc',), ()),
                          (u'ėliuke',     u'', ('f', 'sg', 'voc',), ()),
                          (u'ėliukės',    u'', ('f', 'pl', 'nom',), ()),
                          (u'ėliukių',    u'', ('f', 'pl', 'gen',), ()),
                          (u'ėliukėms',   u'', ('f', 'pl', 'dat',), ()),
                          (u'ėliukes',    u'', ('f', 'pl', 'acc',), ()),
                          (u'ėliukėmis',  u'', ('f', 'pl', 'ins',), ()),
                          (u'ėliukėse',   u'', ('f', 'pl', 'loc',), ()),
                          (u'ėliukės',    u'', ('f', 'pl', 'voc',), ()),
                      ]),
                      }),
                  3: u'(i)a linksniuotė, paradigma nr. 3 (žiūr DLKG97 psl.71)',
                  4: u'(i)u linksniuotė, paradigma nr. 4 (žiūr DLKG97 psl.72)',
                  5: u'(i)u linksniuotė, paradigma nr. 5 (žiūr DLKG97 psl.73)',
                  6: u'(i)o linksniuotė, paradigma nr. 6 (žiūr DLKG97 psl.74)',
                  7: u'(i)o linksniuotė, paradigma nr. 7 (žiūr DLKG97 psl.74)',
                  8: u'ė linksniuotė, paradigma nr. 8 (žiūr DLKG97 psl.75)',
                  9: u'i linksniuotė, paradigma nr. 9 (žiūr DLKG97 psl.76)',
                 10: u'i linksniuotė, paradigma nr. 10(žiūr DLKG97 psl.77)',
                 11: u'i linksniuotė, paradigma nr. 11(žiūr DLKG97 psl.77)',
                 12: u'i linksniuotė, paradigma nr. 12(žiūr DLKG97 psl.78)',
                 13: u'Paradigma daiktavardžiui petys;',
                 14: u'Paradigma daiktavardžiui žmogus (žmonės);',
                 15: u'Paradigma daiktavardžiui pats;',
                 16: u'Paradigma daiktavardžiui viešpats;',
                 17: u'Paradigma daiktavardžiui mėnuo;',
                 18: u'Paradigma vyr. g. daiktavardžiams iš sudaiktavardėjusių įvardžiuotinių būdvardžių bei dalyvių su -asis, pvz., jaunasis, palaimintasis, miegamasis, laukiamasis, mylimasis, nežinomasis',
                 19: u'Paradigma vyr. g. daiktavardžiams iš sudaiktavardėjusių įvardžiuotinių būdvardžių ar dalyvių su -[t]ysis, pvz., pėstysis, vyresnysis, dirbantysis',
                 20: u'Paradigma vyr. g. daiktavardžiams iš sudaiktavardėjusių neįvardžiuotinių dalyvių su -[..]as, pvz., pažįstamas',
                 21: u'Paradigma vyr. g. daiktavardžiams iš sudaiktavardėjusių neįvardžiuotinių dalyvių su -ęs, pvz., suaugęs',
                 22: u'Paradigma mot. g. daiktavardžiams iš sudaiktavardėjusių įvardžiuotinių būdvardžių bei dalyvių su -(i)oji, pvz., jaunoji, palaimintoji, gulsčioji, kaltinamoji, kuliamoji, mylimoji, dirbančioji, sprogtinoji',
                 23: u'Paradigma vyr. g. sangrąžiniams daiktavardžiams iš sangrąžinių veiksmažodžių su ‑asis, pvz., barimasis(-osi, -uisi, ...)',
             }),
             8: (u'Giminės charakteristika', {
                  1: u'Eilinis vyr. gim. daiktavardis',
                  2: u'Vyr. gim. dktv; turi atitikmenį mot. gim., pvz., informatikas->informatikė',
                  3: u'Daiktavardis nekaitomas; tradiciškai laikoma, kad tai vyr. gim., nors tai ne visais atvejais akivaizdu., pvz., kredo, taksi',
                  4: u'Dažniausiai [tradiciškai?] laikoma, kad daiktavardis yra vyr. gim., bet iš principo (teoriškai) jis gali būti tiek vyr., tiek ir mot.giminės, pvz., kai kurie nekaitomi dktv: buržua, atašė, portjė ar kaitomi: junga, buožė ',
                  5: u'Eilinis mot. gim. daiktavardis',
                  6: u'Eilinis bendr. gim. daiktavardis',
                  7: u'Daiktavardis nekaitomas; gali būti laikoma, kad tai mot. gim., nors tai ne visais atvejais akivaizdu; pvz.: bezė',
                  8: u'Mot. gim. daiktavardis; turi atitikmenį vyr. gim. pvz., aulininkė->aulininkas',
                  9: u'Daiktavardis nekaitomas; apie jo giminę ką nors pasakyti sunku (teksto vienetai-užsienio k. įterpiniai ir kt.)',
             }),
             9: (u'Skaičiaus charakteristika', {
                  0: u'Daiktavardis nekaitomas, (gali būti laikoma, kad) skaičiaus kategorijos neturi',
                  1: u'Normalus abiskaitinis, pvz., namas',
                  2: u'Abiskaitinis "tipo analgetikai": nors žodynuose (dažniausiai) pateikiamas daugiskaitoje, gali įgyti ir "normalias" vienaskaitos formas, pvz., analgetikai-analgetikas',
                  3: u'Daugiskaitinis, pvz., miltai, žirklės',
                  4: u'"Normalus" vienaskaitinis',
                  5: u'"Labiau vienaskaitinis" nei abiskaitinis, nes tai tikrinis vardas, pvz., Achilas',
                  6: u'"Labiau daugiskaitinis" nei abiskaitinis, pvz. Parkos (tikrinis iš TŽŽ)',
             }),
            10: (u'Sangrąžiškumo charakteristika', {
                  0: u'Daiktavardis neturi sangrąžiškumo požymio (=sangrąžiškumo požymis daiktavardžiui neturi prasmės), pvz., namas',
                  # Padarytiems iš veiksmažodžių daiktavardžiams:
                  1: u'Žodynuose (paprastai) pateikiamas nesangrąžinis, tačiau galimos ir sangrąžinės formos, pvz., apgulimas',
                  2: u'Žodynuose pateikiamas nesangrąžinis, sangrąžinių formų neturi (arba sangrąžiškumo požymio daiktavardis iš vis neturi, o čia kalbam apie sangrąžiškumą dėl to, kad dktv padarytas iš veiksmažodžio), pvz., liudijimas, mokytojas',
                  3: u'Žodynuose pateikiamas sangrąžinis; nesangrąžinių formų neturi, pvz., juokimasis, kėsinimasis',
            }),
        }),
        (u'Darybos charakteristika', {
            11: (None, {
                  0: u'pamatinis, nepadarytas iš nieko daiktavardis: namas',
                  1: u'padarytas iš daiktavardžio su priesaga -ininkas[ė]: aulininkas',
                  2: u'mažybinis, padarytas iš daiktavardžio su priesaga -elis[ė]: balnelis',
                  3: u'padarytas iš daiktavardžio su priesaga -ingumas: balsingumas',
                  4: u'padarytas iš daiktavardžio su priesaga -ystė',
                  5: u'mažybinis, padarytas iš daiktavardžio su priesaga -iokas[ė]: berniokas',
                  6: u'mažybinis, padarytas iš daiktavardžio su priesaga -iukas[ė]: berniukas',
                  7: u'mažybinis, padarytas iš daiktavardžio su priesaga -iūkštis[tė]: berniūkštis',
                  8: u'mažybinis, padarytas iš daiktavardžio su priesaga -ytis[tė]: bernytis',
                  9: u'mažybinis, padarytas iš daiktavardžio su priesaga -užis[ė]: bernužis',
                 10: u'mažybinis, padarytas iš daiktavardžio su priesaga -aitis[tė]: dievaitis',
                 11: u'padarytas iš daiktavardžio su priesaga -iškumas: dieviškumas',
                 12: u'mažybinis, padarytas iš daiktavardžio su priesaga -ukas[ė]: dievukas',
                 13: u'mažybinis, padarytas iš daiktavardžio su priesaga -utis[tė]: gužutis',
                 14: u'mažybinis, padarytas iš daiktavardžio su priesaga -ėkas[ė]: paršėkas',
                 15: u'mažybinis, padarytas iš daiktavardžio su priesaga -ėlis[ė]: avinėlis',
                 16: u'mažybinis, padarytas iš daiktavardžio su priesaga -okas[ė]: bėrokas',
                 17: u'mažybinis, padarytas iš daiktavardžio su priesaga -elytis[tė]: žodelytis',
                 18: u'mažybinis, padarytas iš daiktavardžio su priesaga -ulis[ė]: tėtulis',
                 19: u'padarytas iš daiktavardžio su priesaga -ie-tis[tė]: azerbaidžanietis',
                 20: u'padarytas iš daiktavardžio su priesaga -iškis[ė]: birštoniškė',
                 21: u'mažybinis, padarytas iš daiktavardžio su priesaga -ikė[is?]: mergikė',
                 22: u'mažybinis, padarytas iš daiktavardžio su priesaga -io-tė[tis?]: mergiotė',
                 23: u'padarytas iš būdvardžio su priesaga -umas: abipusiškumas',
                 24: u'padarytas iš būdvardžio su priesaga -ybė: akylybė',
                 25: u'padarytas iš daiktavardžio su priesaga -ingumas ir su priešdėliu ne-: neturtingumas',
                 26: u'padarytas iš daiktavardžio su priesaga -ystė ir su priešdėliu ne-: neturtystė',
                 27: u'padarytas iš daiktavardžio su priesaga -iškumas ir su priešdėliu be-: beglobiškumas',
                 28: u'padarytas iš daiktavardžio su priesaga -ystė ir su priešdėliu be-: bepinigystė',
                 29: u'padarytas iš daiktavardžio su priesaga -ininkas[ė] ir su priešdėliu ne-: nepriemokininkas',
                 30: u'mažybinis, padarytas iš daiktavardžio su priesaga -ėlis[ė] ir su priešdėliu ne-: nelaimėlė',
                 31: u'padarytas iš daiktavardžio su priesaga -iškumas ir su priešdėliu ne-: nemokšiškumas',
                 32: u'padarytas iš daiktavardžio su priesaga -umas ir su neig. pref. a-: apolitiškumas',
                 33: u'padarytas iš būdvardžio su priesaga -umas ir su priešdėliu be-: beidėjiškumas',
                 34: u'padarytas iš būdvardžio su priesaga -umas ir su priešdėliu ne-: nedorumas',
                 35: u'padarytas iš būdvardžio su priesaga -iškumas: savitarpiškumas',
                 36: u'padarytas iš būdvardžio su priesaga -ybė ir su priešdėliu be-: bekraštybė',
                 37: u'padarytas iš skaitvardžio su priesaga -ybė: pirmenybė',
                 38: u'padarytas iš skaitvardžio su priesaga -umas: pirmumas',
                 39: u'mažybinis, padarytas iš skaitvardžio su priesaga -ukas[ė]: vienetukas, vienukė',
                 40: u'padarytas iš skaitvardžio su priesaga -ystė: vienystė',
                 41: u'mažybinis, padarytas iš skaitvardžio su priesaga -utėlis: vienutėlis',
                 42: u'mažybinis, padarytas iš skaitvardžio su priesaga -utis: vienutis',
                 43: u'mažybinis, padarytas iš skaitvardžio su priesaga -utukas: vienutukas',
                 44: u'padarytas iš skaitvardžio su priesaga -ulė[is?]: trijulė',
                 45: u'mažybinis, padarytas iš skaitvardžio su priesaga -iukė[as?]: šešiukė',
                 46: u'padarytas iš įvardžio su priesaga -umas: saviškumas',
                 47: u'padarytas iš veiksmažodžio su -imas(ymas)  plius su priešdėliu ap-: apgulimas',
                 48: u'padarytas iš veiksmažodžio su -imas(ymas)  plius su prefiksu apsi-: apsikalimas',
                 49: u'padarytas iš veiksmažodžio su -imas(-imasis) (be prefikso)',
                 50: u'padarytas iš veiksmažodžio su -imas  plius su priešdėliu iš-: išbarimas',
                 51: u'padarytas iš veiksmažodžio su -inėjimas  plius su priešdėliu iš-: iškalinėjimas',
                 52: u'padarytas iš veiksmažodžio su -imas  plius su priešdėliu į-: įgnybimas',
                 53: u'padarytas iš veiksmažodžio su -ėjas(a) (be prefikso)',
                 54: u'padarytas iš veiksmažodžio su -ikas(ė) (be prefikso)',
                 55: u'padarytas iš veiksmažodžio su -imas  plius su priešdėliu nu-: nugulimas',
                 56: u'padarytas iš veiksmažodžio su -imas  plius su priešdėliu pa-: pabarimas',
                 57: u'padarytas iš veiksmažodžio su -imas  plius su priešdėliu per-: perkalimas',
                 58: u'padarytas iš veiksmažodžio su -imas  plius su priešdėliu pra-: prakalimas',
                 59: u'padarytas iš veiksmažodžio su -imas  plius su priešdėliu pri-: prigulimas',
                 60: u'padarytas iš veiksmažodžio su -inėjimas  plius su priešdėliu pri-: prikalinėjimas',
                 61: u'padarytas iš veiksmažodžio su -imas  plius su priešdėliu su-: sugulimas',
                 62: u'padarytas iš veiksmažodžio su -imas  plius su priešdėliu už-: užgulimas',
                 63: u'padarytas iš veiksmažodžio su -inėjimas  plius su priešdėliu už-: užkalinėjimas',
                 64: u'padarytas iš veiksmažodžio su -imas  plius su prefiksu užsi-: užsigulimas',
                 65: u'padarytas iš veiksmažodžio su -ėjas(a)  plius su priešdėliu ap-: apdirbėja',
                 66: u'padarytas iš veiksmažodžio su -imas  plius su priešdėliu at-: atlupimas',
                 67: u'padarytas iš veiksmažodžio su -inėjimas(-inėjimasis ?) (be prefikso)',
                 68: u'padarytas iš veiksmažodžio su -tinumas (be prefikso)',
                 69: u'padarytas iš veiksmažodžio su -ėjas(a)  plius su priešdėliu iš-: išdirbėja',
                 70: u'padarytas iš veiksmažodžio su -ėjas(a)  plius su priešdėliu pa-: padirbėja',
                 71: u'padarytas iš veiksmažodžio su -inėjimas  plius su priešdėliu pa-: padirbinėjimas',
                 72: u'padarytas iš veiksmažodžio su -inėjimas  plius su priešdėliu per-: perdirbinėjimas',
                 73: u'padarytas iš veiksmažodžio su -imas  plius su prefiksu persi-: persidirbimas',
                 74: u'padarytas iš veiksmažodžio su -tojas(a) (be prefikso): aiškintojas',
                 75: u'padarytas iš veiksmažodžio su -tojas(a)  plius su priešdėliu ap-: apdulkintoja',
                 76: u'padarytas iš veiksmažodžio su -imas  plius su priešdėliu api-: apibendrinimas',
                 77: u'padarytas iš veiksmažodžio su -imas  plius su priešdėliu ati-: atitolinimas',
                 78: u'padarytas iš veiksmažodžio su -imas  plius su prefiksu atsi-: atsisveikinimas',
                 79: u'padarytas iš veiksmažodžio su -tojas(a)  plius su priešdėliu iš-: išaiškintojas',
                 80: u'padarytas iš veiksmažodžio su -tojas(a)  plius su priešdėliu į-: įdukrintojas',
                 81: u'padarytas iš veiksmažodžio su -imas  plius su prefiksu įsi-: įsigilinimas',
                 82: u'padarytas iš veiksmažodžio su -[(i)a,i,o]mumas  plius su prefiksu nepa-: nepakaltinamumas',
                 83: u'padarytas iš veiksmažodžio su -imas  plius su prefiksu nusi-: nusigyvenimas',
                 84: u'padarytas iš veiksmažodžio su -tojas(a)  plius su priešdėliu pa-: pagreitintoja',
                 85: u'padarytas iš veiksmažodžio su -[(i)a,i,o]mumas  plius su prefiksu pa-: pakaltinamumas, pastebimumas',
                 86: u'padarytas iš veiksmažodžio su -imas  plius su prefiksu par-: pargabenimas',
                 87: u'padarytas iš veiksmažodžio su -imas  plius su prefiksu pasi-: pasiaiškinimas',
                 88: u'iš vksm su -toj-as(a)  plius su prefiksu pasi-: pasisavintoja',
                 89: u'padarytas iš veiksmažodžio su -imas  plius su prefiksu prasi-: prasigyvenimas',
                 90: u'padarytas iš veiksmažodžio su -imas  plius su prefiksu prisi-: prisigretinimas',
                 91: u'mažybinis, padarytas iš vksm su -tojėlis(ė) (be prefikso)',
                 92: u'padarytas iš veiksmažodžio su -[(i)a,i,o]mumas  plius su prefiksu su-: sugyvenamumas',
                 93: u'iš vksm su -tojas(a) su pa-: suniekintintoja',
                 94: u'iš vksm su -imas su susi-: susirūpinimas',
                 95: u'iš vksm su -[(i)a,i,o]mumas bepref: virškinamumas, tariamumas, regimumas',
                 96: u'iš vksm su -inėjimas su į-: įtarinėjimas',
                 97: u'iš vksm su -imas su nesu-: nesutarimas',
                 98: u'iš vksm su -[(i)a,i,o]myb-ė bepref: tariamybė,regimybė',
                 99: u'iš vksm su -ėjas(a) su už-: užgrobėjas',
                100: u'iš vksm su -ikas(ė) su už-: užgrobikas',
                101: u'iš vksm su -telėjimas bepref: aiktelėjimas',
                102: u'iš vksm su -terėjimas bepref: aisterėjimas',
                103: u'iš vksm su -tybė su at-: atsietybė',
                104: u'iš vksm su -imas su išsi-: išsiliejimas',
                105: u'iš vksm su -tojas(a) su per-: perįgaliotojas',
                106: u'iš vksm su -tojas(a) su pra-: praleidinėtojas',
                107: u'iš vksm su -tojas(a) su už-: užrašinėtojas',
                108: u'iš vksm su -imas(-imasis) ir su be-: bedievėjimas',
                109: u'iš vksm su -[(i)a,i,o]mumas su neį-: neįkainojamumas, neįtikimumas',
                110: u'iš vksm su -tojas(a) su par-: pardavinėtojas',
                111: u'iš vksm su -tojas(a) su pri-: prigaudinėtojas',
                112: u'iš vksm su -[(i)a,i,o]mumas su ne-: nemirštamumas',
                113: u'iš vksm su -inėjimas su at-: atkalbinėjimas',
                114: u'iš vksm su -[(i)a,i,o]myb-ė su ne-: nejudamybė',
                115: u'iš vksm su -ėjas(a) su pra-: pradėjėjas',
                116: u'iš vksm su -[(i)a,i,o]mybė su iš-: ištikimybė',
                117: u'iš vksm su -[(i)a,i,o]mumas su iš-: ištikimumas',
                118: u'iš vksm su -[(i)a,i,o]mybė su į-: įtikimybė',
                119: u'iš vksm su -[(i)a,i,o]mumas su į-: įtikimumas',
                120: u'iš vksm su -tinumas su ne-: netikėtinumas',
                121: u'iš vksm su -tybė su ne-: netikėtybė',
                122: u'iš vksm su -(ė)tumas su ne-: netikėtumas',
                123: u'iš vksm su -[(i)a,i,o]mybė su pa-: patikimybė',
                124: u'iš vksm su -[(i)a,i,o]mumas su per-: perregimumas,pereinamumas',
                125: u'iš vksm su -imas su neapsi-: neapsižiūrėjimas',
                126: u'iš vksm su -tojas(a) su nu-: nugalėtojas',
                127: u'iš vksm su -inėjimas su pasi-: pasibėginėjimas',
                128: u'iš vksm su -tumas bepref: baigtumas',
                129: u'iš vksm su -ėjas(a) su į-: įdiegėjas',
                130: u'iš vksm su -[(i)a,i,o]myb-ė su nepa-: nepabaigiamybė',
                131: u'iš vksm su -ėjas(a) su per-: perjungėjas',
                132: u'iš vksm su -tinumas su pri-: primygtinumas',
                133: u'iš vksm su -[(i)a,i,o]myb-ė su neiš-: neišvengiamybė',
                134: u'iš vksm su -[(i)a,i,o]mumas su neiš-: neišvengiamumas',
                135: u'iš vksm su -[(i)a,i,o]mumas su nepri-: neprieinamumas',
                136: u'iš vksm su -[(i)a,i,o]myb-ė su par-: pareinamybė',
                137: u'iš vksm su -[(i)a,i,o]mumas su par-: pareinamumas',
                138: u'iš vksm su -[(i)a,i,o]mumas su pra-: praeinamumas',
                139: u'iš vksm su -[(i)a,i,o]mumas su pri-: prieinamumas',
                140: u'iš vksm su -inėjimas su ap-: apsakinėjimas',
                141: u'iš vksm su -[(i)a,i,o]mybė su at-: atsakomybė',
                142: u'iš vksm su -inėjimas su atsi-: atsiprašinėjimas',
                143: u'iš vksm su -[(i)a,i,o]mumas su neati-: neatitaisomumas',
                144: u'iš vksm su -[(i)a,i,o]myb-ė su neiš-: nepriklausomybė',
                145: u'iš vksm su -[(i)a,i,o]mumas su nesu-: nesulaikomumas',
                146: u'iš vksm su -inėjimas su nu-: nudarinėjimas',
                147: u'iš vksm su -toj-as(a) su prasi-: prasimanytojas',
                148: u'iš vksm su -[(i)a,i,o]myb-ė su pri-: priklausomybė',
                149: u'iš vksm su -inėjimas su su-: surašinėjimas',
                150: u'iš vksm su -inėjimas su susi-: susirašinėjimas',
                151: u'iš vksm su -tybė su ati-: atitrauktybė',
                152: u'iš vksm su -inėjimas su išsi-: išsisukinėjimas',
                153: u'iš vksm su -tinybė su atsi-: atsitiktinybė',
                154: u'iš vksm su -tinumas su atsi-: atsitiktinumas',
                155: u'iš vksm su -imas su ne-: netekimas',
                156: u'iš vksm su -[(i)a,i,o]mumas su už-: užtenkamumas',
                157: u'iš vksm su -ėjas(a) su su-: surinkėjas',
                158: u'iš vksm su -tinumas su iš-: išimtinumas',
                159: u'iš vksm su -ėjas(a) su pri-: priėmėja',
                160: u'iš vksm su -ikas(ė) su iš-: išdavikas',
                161: u'iš vksm su -ikas(ė) su į-: įdavikas',
                162: u'iš vksm su -ėjas(a) su par-: pardavėja',
                163: u'iš vksm su -ikas(ė) su par-: pardavikas',
                164: u'iš vksm su -inėjimas su par-: pardavinėjimas',
                165: u'iš vksm su -tumas su su-: suinteresuotumas',
                166: u'iš vksm su -ėjas(a) su at-: atradėjas',
                167: u'iš vksm su -tumas su ap-: apšviestumas',
                168: u'iš vksm su -ėjas(a) su nu-: nuleidėjas',
                169: u'iš vksm su -inėjimas su pra-: praleidinėjimas',
                170: u'iš vksm su -inėjimas su apsi-: apsimetinėjimas',
                171: u'iš vksm su -imas su nesusi-: nesusipratimas',
                172: u'iš vksm su -[(i)a,i,o]mumas su nenu-: nenuilstamumas',
                173: u'iš vksm su -ikas(ė) su pri-: prigavikas',
                174: u'iš vksm su -tinybė bepref: būtinybė',
                175: u'iš vksm su -tybė bepref: būtybė',
                176: u'iš ištikt su -telėjimas: pakštelėjimas',
            }),
        }),
        (u'Derivacijos charakteristika', {
            12: (u'Demunityviniai vediniai', {
                  1: u'Deminutyvų neturi',
                  2: u'Turi normalius deminutyvus; deminutyvų abiejose giminėse (kaip kad pvz. meška-meškutis-meškutė) neturi',
                  3: u'Turi deminutyvus abiejose giminėse, pvz., meška-meškutis-meškutė',
                  4: u'Daiktavardžiai nekaitomi (nėra linksniuojami), nors kai kurie jų, ypač dažniau vartojami ir ypač šnek. kalboje, "lietuviškas" kai kurių linksnių galūnes gali ir įgyti; laikom, kad kai kurie tokie nekait. dktv. kartais gali įgyti mažybines formas, bet kaip būtent mažybinės priesagos prie tokių nekait. dktv. "lipdomos", šiame darbo etape toks suklasifikavimas daromas nebuvo (tai [galbūt] yra ateities etapų užduotis), pvz., atašė, buržua',
                  5: u'Kaip ir 2 (turi normalius deminutyvus; deminutyvų abiejose giminėse neturi); tik: pats jau yra mažybinis, pvz., balnelis (dviračio)',
            }),
            13: (u'Daiktavardžio vedinių su -ininkas(-ė) galimumas', {
                0: u'tokių vedinių neturi',
                1: u'turi',
            }),
            14: (u'Daiktavardžio vedinių su -ybė galimumas', {
                0: u'tokių vedinių neturi',
                1: u'turi',
            }),
            15: (u'Daiktavardžio vedinių su -ystė galimumas', {
                0: u'tokių vedinių neturi',
                1: u'turi',
            }),
            16: (u'Būdvardžio vedinių su -ingas galimumas', {
                0: u'tokių vedinių neturi',
                1: u'turi',
            }),
            17: (u'Būdvardžio vedinių su -iškas galimumas', {
                0: u'tokių vedinių neturi',
                1: u'turi',
            }),
            18: (u'Būdvardžio vedinių su -inis galimumas', {
                0: u'tokių vedinių neturi',
                1: u'turi',
            }),
            19: (u'Prieveiksmio vedinių su -in(i)ai galimumas', {
                0: u'tokių vedinių neturi',
                1: u'turi',
            }),
            20: (u'vedinių su -ėtas galimumas', {
                0: u'tokių vedinių neturi',
                1: u'turi',
            }),
            21: (u'Būdvardžio vedinių su -(u)otas galimumas', {
                0: u'tokių vedinių neturi',
                1: u'turi',
            }),
            # PREFIXES
            22: (u'Prefiksiniai vediniai', {
                 0: u'',
                 1: u'E,N/E;E/S,N/E/S',
                 2: u'E,N/E;',
                 3: u';E/S,N/E/S',
                 4: u'+,N;',
                 5: u';+,N/S',
                 6: u'+,N;+,N/S',
                 7: u'+,N,F,N/F;+,N/S,F/S,N/F/S',
                 8: u'E,N/E;ap/S,N/ap/S',
                 9: u'E,N/E;at/S,N/at/S',
                10: u'+,N,F,N/F;',
                11: u'+,B;',
                12: u'N/E;',
                13: u'+,N,R,N/R;',
                14: u'N;',
                15: u'E,N/E;E/S_,N/E/S_',
                16: u'+, N_,N/B_;+, N/S_,N/B/S_',
                17: u'+,N;N,N/S',
                18: u';+,N/S,F/S,N/F/S',
                19: u'+,N,H,N/H;N/S,G/S,N/G/S',
                20: u'+,N,G,N/G;+,N/S,G/S,N/G/S',
                21: u'+,N,K,N/K;',
                22: u'+,N;',
            }),
        }),
    ],

    # Būdvardis
    2: [
        (u'Kaitybos charakteristika', {
             4: (u'Linksniavimo charakteristika', {
                  0: u'Būdvardis nekaitomas, nelinksniuojamas, pvz.: bordo',
                  1: u'(i)a linksniuotė, paradigma nr. 1 (žiūr DLKG97 psl.179), pvz.: geras',
                  2: u'(i)a linksniuotė, paradigma nr. 2 (žiūr DLKG97 psl.179), pvz.: žalias',
                  3: u'(i)a linksniuotė, paradigma nr. 3 (žiūr DLKG97 psl.179-180), pvz.: kairys, paskesnis',
                  4: u'(i)a linksniuotė, paradigma nr. 4 (žiūr DLKG97 psl.180), pvz.: paskutinis',
                  5: u'(i)u linksniuotė, paradigma nr. 5 (žiūr DLKG97 psl.181), pvz.: gražus',
                  6: u'Paradigma būdvardžiui vėlus, pvz.: vėlus(-as)',
                  7: u'Paradigma būdvardžiams iš subūdvardėjusių veik. r. esamojo l. dalyvių su  -antis, ‑intis, pvz.: sekantis, pasiturintis',
                  8: u'Paradigma būdvardžiams iš subūdvardėjusių veik. r. būtojo l. dalyvių su  -ęs, pvz.: pasileidęs',
                  9: u'Paradigma būdvardžiams iš subūdvardėjusių neveik. r. esamojo l. įvardžiuotinių dalyvių su [-(i)am-, -im-, -om-] +  -asis, pvz.: patariamasis, stojamasis, mokomasis',
                 10: u'Paradigma būdvardžiams iš subūdvardėjusių neveik. r. būtojo l. įvardžiuotinių dalyvių su  -tasis, pvz.: išrinktasis',
                 11: u'Paradigma būdvardžiui iš skaitvardžio abu su  -oks, pvz.: abejoks',
             }),
             5: (u'Laipsniavimo charakteristika', {
                 0: u'Būdvardis nekaitomas, nelaipsniuojamas; gali būti laikoma, kad laipsnio kategorijos neturi arba kad yra nelyginamojo laipsnio, pvz.: bordo',
                 1: u'laipsniuojamas, įgyja visus laipsnius, pvz.: gražus',
                 2: u'nelaipsniuojamas; žodynuose pateikiamas nelyginamojo laipsnio, pvz.: aukštielninkas',
                 3: u'nelaipsniuojamas; žodynuose pateikiamas aukščiausiojo laipsnio, pvz.: apačiausias',
                 4: u'laipsniuojamas, bet nelyg. lpsn. neturi; žodynuose pateikiamas aukštesniojo laipsnio, pvz.: paskesnis',
                 5: u'laipsniuojamas, bet nelyg. lpsn. neturi; žodynuose pateikiamas aukščiausiojo laipsnio, pvz.: viršiausias',
                 6: u'laipsniuojamas, bet nelyg. lpsn. neturi; žodynuose pateikiamas aukštėlesniojo laipsnio, pvz.: viršėlesnis',
             }),
             6: (u'Apibrėžtumas (įvardžiuotinumas)', {
                 0: u'būdvardis nekaitomas: apibrėžtumo požymio neturi, pvz.: bordo',
                 1: u'įgyja ir neįvardžiuotines, ir įvardžiuotines formas; žodynuose pateikiamas neįvardžiuotinės formos, pvz.: gražus',
                 2: u'įgyja ir neįvardžiuotines, ir įvardžiuotines formas; žodynuose pateikiamas įvardžiuotine forma, pvz.: gotiškasis',
                 3: u'nelyg. laipsnyje turi tik neįvardžiuotines formas; kituose - ir tokias, ir tokias, pvz.: didelis: didesnis,  ‑esnysis, ‑iausiasis',
                 4: u'turi tik neįvardžiuotines formas, pvz.: dvišakas',
                 5: u'žodynuose pateikiamas įvardžiuotine forma; turi tik įvardžiuotines formas, pvz.: taikomasis',
             }),
             7: (u'Kaitymas gimine', {
                 0: u'būdvardis nekaitomas; galima laikyti, kad giminės kategorijos neturi, pvz.: bordo',
                 1: u'turi visas gimines: vyr., mot., bevard., pvz.: gražus',
                 2: u'įgyja visas gimines (teoriškai) - vyr., mot., bevard.; žodynuose pateikiamas ir paprastai vartojamas moteriškąja gimine, pvz.: nėščia',
                 3: u'įgyja vyr., mot. gim; bevardės neturi, pvz.: baltažiedis',
                 4: u'turi vyr, mot. gim. (bevard. neturi); žodynuose pateikiamas ir paprastai vartojamas moteriškąja gimine, pvz.: barbitūrinė, šviežiapienė',
                 5: u'įgyja visas gimines: vyr., mot., bevard.; išskyrus nelyginamąjį laipsnį, kuriame bevardės giminės nėra, pvz.: kairys, dešinys',
             }),
             8: (u'Prefiksavimas', {
                 0: u'žodynuose pateikiamas be neig. prefikso; neigiamų formų neturi, pvz.: ekstra, bruto',
                 1: u'žodynuose pateikiamas be neig. prefikso; gali turėti: beprefiksines formas, formas su ne- , nebe- , tebe- ir t.t., pvz.: gražus: gražus; negražus, nebegražus, tebegražus',
                 2: u'žodyne pateiktas su neig. prefiksu a-; vartojamas ir be šito prefikso; gali turėti: beprefiksines formas, formas su a-, formas su ne-, nebe-, tebe- ir t.t., pvz.: atipiškas: tipiškas; atipiškas; netipiškas, nebetipiškas, tebetipiškas ir t.t.',
                 3: u'žodyne pateiktas su neig. prefiksu be-; vartojamas ir be šito prefikso; gali turėti: beprefiksines formas, formas su be-, formas su ne-, nebe-, tebe- ir t.t., pvz.: beatodairiškas: atodairiškas; beatodairiškas; neatodairiškas, nebeatodairiškas, tebeatodairiškas ir t.t.',
                 4: u'žodyne pateiktas su neig. prefiksu be-; be šito prefikso jis nevartojamas; gali turėti: formas su be-, formas su nebe-, tebebe- ir t.t.:  , pvz.: beširdiškas: nebeširdiškas-nebebeširdiškas ir t.t.',
                 5: u'žodyne pateiktas su neig. prefiksu ne-; vartojamas ir be šito prefikso; gali turėti: beprefiksines formas, formas su ne- , nebe- , tebe- ir t.t., pvz.: neblogas: blogas-neblogas-nebeblogas-tebeblogas ir t.t.',
                 6: u'žodyne pateiktas su neig. prefiksu ne-; be šito prefikso jis nevartojamas; gali turėti: formas su ne-, formas su tebene- , pvz.: nerimastingas: nerimastingas-tebenerimastingas',
                 7: u'žodyne pateiktas su neig. prefiksu anti-; vartojamas ir be šito prefikso; gali turėti: beprefiksines formas, formas su anti-, formas su neanti- , nebeanti- , tebeanti- ir t.t., pvz.: antihigieninis: higieninis, antihigieninis, neantihigieninis-nebeantihigieninis, tebeantihigieninis ir t.t.',
             }),
             9: (u'Darybos charakteristika', {
                  0: u'pamatinis, nepadarytas iš nieko būdvardis, pvz.: geras',
                  1: u'padarytas iš daiktavardžio su priesaga ‑iškas, pvz.: angliškas',
                  2: u'padarytas iš daiktavardžio su priesaga ‑inis, pvz.: auksinis',
                  3: u'padarytas iš daiktavardžio su priesaga ‑uotas, pvz.: ginkluotas',
                  4: u'padarytas iš daiktavardžio su priesaga ‑ingas, pvz.: grėsmingas',
                  5: u'padarytas iš daiktavardžio su priesaga ‑ėtas, pvz.: kaulėtas',
                  6: u'padarytas iš daiktavardžio su priesaga ‑ietiškas, pvz.: rytietiškas',
                  7: u'padarytas iš daiktavardžio su priesaga ‑otas, pvz.: pilvotas',
                  8: u'mažybinis, padarytas iš būdvardžio su priesaga ‑utėlis, pvz.: aklutėlis',
                  9: u'padarytas iš būdvardžio su priešdėliu apy‑, pvz.: apymažis',
                 10: u'padarytas iš būdvardžio su priesaga ‑okas, pvz.: mažokas',
                 11: u'mažybinis, padarytas iš būdvardžio su priesaga ‑ėlis, pvz.: mažėlis',
                 12: u'mažybinis, padarytas iš būdvardžio su priesaga ‑iukas, pvz.: mažiukas',
                 13: u'mažybinis, padarytas iš būdvardžio su priesaga ‑iulis, pvz.: mažiulis',
                 14: u'mažybinis, padarytas iš būdvardžio su priesaga ‑ylis, pvz.: mažylis',
                 15: u'mažybinis, padarytas iš būdvardžio su priesaga ‑ytis, pvz.: mažytis',
                 16: u'mažybinis, padarytas iš būdvardžio su priesaga ‑utis, pvz.: mažutis',
                 17: u'mažybinis, padarytas iš būdvardžio su priesaga ‑utytis, pvz.: mažutytis',
                 18: u'mažybinis, padarytas iš būdvardžio su priesaga ‑ytėlis, pvz.: plonytėlis',
                 19: u'padarytas iš būdvardžio su priešdėliu po‑, pvz.: pomažis',
                 20: u'padarytas iš būdvardžio su priešdėliu prie‑, pvz.: priekvailis',
                 21: u'mažybinis, padarytas iš būdvardžio su priesaga ‑utėlaitis, pvz.: sausutėlaitis',
                 22: u'mažybinis, padarytas iš būdvardžio su priesaga ‑ulis, pvz.: apskritulis',
                 23: u'mažybinis, padarytas iš būdvardžio su priesaga ‑ytėlaitis, pvz.: baltytėlaitis',
                 24: u'mažybinis, padarytas iš būdvardžio su priesaga ‑užėlis, pvz.: raitužėlis (KZ kld)',
                 25: u'padarytas iš būdvardžio su ‑ut, pvz.: naujut',
                 26: u'padarytas iš būdvardžio su priesaga ‑iškas, pvz.: savitarpiškas',
                 27: u'padarytas iš skaitvardžio su priesaga ‑inis, pvz.: pirminis',
                 28: u'padarytas iš skaitvardžio su priesaga ‑opas, pvz.: vieneriopas',
                 29: u'padarytas iš skaitvardžio su priesaga ‑gubas, pvz.: viengubas',
                 30: u'padarytas iš skaitvardžio su priesaga ‑linkas, pvz.: vienlinkas',
                 31: u'padarytas iš skaitvardžio su priesaga ‑oks, pvz.: abejoks',
                 32: u'padarytas iš skaitvardžio su priesaga ‑ainis, pvz.: dvejetainis',
                 33: u'padarytas iš skaitvardžio su priesaga ‑gubinis, pvz.: dvigubinis',
                 34: u'padarytas iš įvardžio su priesaga ‑iškas, pvz.: jūsiškas',
                 35: u'padarytas iš įvardžio su priesaga ‑opas, pvz.: keleriopas',
                 36: u'padarytas iš įvardžio su priesaga ‑gubas, pvz.: keliagubas',
                 37: u'padarytas iš įvardžio su priesaga ‑inis, pvz.: kelintinis',
                 38: u'subūdvardėjęs, iš dalyvio, pvz.: sukalbamas, užkrečiamas, suaugęs, išrinktasis',
                 39: u'padarytas iš ko nors su priešdėliu a-, pvz.: atipiškas',
                 40: u'padarytas iš ko nors su priešdėliu be-, pvz.: beatodairiškas',
                 41: u'padarytas iš ko nors su priešdėliu ne-, pvz.: neblogas',
                 42: u'subūdvardėjęs iš dalyvio; plius su priešd. ne-, pvz.: nesukalbamas, neabejojamas, nelyginamasis',
                 43: u'padarytas iš būdvardžio su priesaga -elis, pvz.: didelis',
                 44: u'padarytas iš ko nors su priešdėliu anti-, pvz.: antihigieninis',
                 45: u'padarytas iš daiktavardžio su priesaga -ingas; plius su neigiamu priešdėliu ne-, pvz.: neturtingas',
                 46: u'padarytas iš daiktavardžio su priesaga -iškas; plius su neigiamu priešdėliu be-, pvz.: bedieviškas, bejėgiškas',
                 47: u'padarytas iš daiktavardžio su priesaga -inis; plius su neigiamu priešdėliu a-, pvz.: asimetrinis',
                 48: u'padarytas iš daiktavardžio su priesaga -iškas; plius su neigiamu priešdėliu a-, pvz.: asimetriškas',
                 49: u'padarytas iš daiktavardžio su priesaga -inis; plius su neigiamu priešdėliu ne-, pvz.: nepartinis',
                 50: u'padarytas iš daiktavardžio su -iškas; plius su neigiamu priešdėliu ne-, pvz.: nemokšiškas',
                 51: u'mažybinis, padarytas iš būdvardžio su priesaga -utis; plius su neigiamu priešdėliu ne-, pvz.: nekaltutis, nedidutis',
             }),
        }),
        (u'Derivacijos charakteristika', {
            10: (u'Deminutyviniai vediniai', {
                0: u'būdvardis tokių vedinių neturi',
                1: u'turi',
            }),
            11: (u'Daiktavardžio vediniai su ‑okas', {
                0: u'būdvardis tokių vedinių neturi',
                1: u'turi',
            }),
            12: (u'Daiktavardžio vediniai su ‑umas', {
                0: u'būdvardis tokių vedinių neturi',
                1: u'turi',
            }),
            13: (u'Daiktavardžio vediniai su ‑ybė', {
                0: u'būdvardis tokių vedinių neturi',
                1: u'turi',
            }),
            14: (u'Daiktavardžio vediniai su ‑ystė', {
                0: u'būdvardis tokių vedinių neturi',
                1: u'turi',
            }),
            15: (u'Prieveiksmio vediniai su ‑(i)ai', {
                0: u'būdvardis tokių vedinių neturi',
                1: u'turi',
            }),
            16: (u'Prieveiksmio vediniai su ‑yn', {
                0: u'būdvardis tokių vedinių neturi',
                1: u'turi',
            }),
            17: (u'Būdvardžio vediniai su priešdėliais apy‑ (api‑), po‑', {
                0: u'būdvardis tokių vedinių neturi',
                1: u'turi',
            }),
        }),
    ],

    # Skaitvardis
    3: [
        (u'Skaitvardžio ypatumai', {
             4: (u'Skyrius', {
                 1: u'kiekiniai',
                 2: u'dauginiai',
                 3: u'kuopiniai',
                 4: u'kelintiniai',
             }),
             5: (u'Linksnio ir skaičiaus valdymas', {
                 0: u'Nieko nevaldo',
                 1: u'Reikalauja vienaskaitos kilmininko',
                 2: u'Reikalauja daugiskaitos kilmininko',
                 3: u'Reikalauja dviskaitos',
             }),
        }),
        (u'Kaitybos charakteristika', {
             6: (u'Linksniavimo charakteristika', {
                  1: u'Žiūr. DLKG §711 psl. 245: vyr.g.vnsk.K: -o; vyr.g.dgsk.K: -ų; mot.g.vnsk.K: -os; mot.g.dgsk.K: -ų, pvz.: pusantro',
                  2: u'Žiūr. DLKG §711 psl. 245: vyr.g.vnsk.K: -io; vyr.g.dgsk.K: -ių; mot.g.vnsk.K: -ios; mot.g.dgsk.K: -ių, pvz.: pustrečio',
                  3: u'Kaip a (vyr.g.) ir o (mot.g.) linksniuočių būdvardžiai: vyr.g. - bdv linksniavimo 1 paradigma pgl (žiūr. DLKG §552 psl.179); mot.g. - bdv linksniavimo 6 paradigma pgl (žiūr. DLKG §556 psl.182), pvz.: dušimtas, pirmas, vienas, ketvirtas',
                  4: u'Kaip ia (vyr.g.) ir io (mot.g.) linksniuočių būdvardžiai: vyr.g. - bdv linksniavimo 3 paradigma pgl (žiūr. DLKG §552 psl.179); mot.g. - bdv linksniavimo 9 paradigma pgl (žiūr. DLKG §556 psl.184), pvz.: pirmesnis, vieneri',
                  5: u'Kaip ia (vyr.g.) ir io (mot.g.) linksniuočių būdvardžiai: vyr.g. - bdv linksniavimo 2 paradigma pgl (žiūr. DLKG §552 psl.179); mot.g. - bdv linksniavimo 7 paradigma pgl (žiūr. DLKG §556 psl.183), pvz.: pirmiausias, trečias',
                  6: u'Kaip a linksniuotės daiktavardžiai, linksniavimo 1 paradigma (žiūr.DLKG §119 psl.70), pvz.: abejetas, šimtas',
                  7: u'Žiūr. DLKG §718 psl. 247, pvz.: abu, du',
                  8: u'Žiūr. DLKG §719 psl. 247, pvz.: trys',
                  9: u'Žiūr. DLKG §720 psl. 247, pvz.: keturi',
                 10: u'dešimt(-s, -is): žiūr. DLKG §711psl.245, §721psl.248:; kaip mot.g. i linksniuotės dktv (plg. paslaptis: 9 paradigma pgl. žiūr DLKG §131psl.76; plius turi nelinksniuojamą formą dešimt(s), pvz.: dešimt(-s, -is)',
                 11: u'11-19: žiūr. DLKG §722 psl. 248, pvz.: vienuolika, devyniolika',
                 12: u'1000: žiūr. DLKG §723 psl.248: kaip (i)a linksniuotės daiktavardžiai, linksniavimo 3 paradigma pgl žiūr.DLKG §119 psl.71, pvz.: tūkstantis',
             }),
             7: (u'Giminės charakteristika', {
                 1: u'Turi vyr. ir mot. giminę, pvz.: pusantro, pustrečio',
                 2: u'Turi vyr., mot. ir bevardę giminę, pvz.: trečias',
                 3: u'Giminėmis nekaitomas (galima traktuoti, kad giminės kategorijos neturi ?); linksniuojamas įgyja daiktavardiškas vyr. g. formas, pvz.: abejetas, šimtas',
                 4: u'Giminėmis nekaitomas (galima traktuoti, kad giminės kategorijos neturi ?); linksniuojamas įgyja daiktavardiškas mot. g. formas; žiūr. DLKG §709, psl.244., pvz.: dešimt(is), vienuolika',
             }),
             8: (u'Skaičiaus charakteristika', {
                 1: u'Turi vienaskaitą ir daugiskaitą, pvz.: pusantro',
                 2: u'Skaičiumi nekaitomas; galima traktuoti, kad turi tik daugiskaitą, pvz.: vieneri, trys',
                 3: u'Skaičiumi nekaitomas; galima traktuoti, kad turi tik vienaskaitą (linksniuojamas įgyja vyr. g. vnsk. formas), pvz.: abejetas',
                 4: u'Skaičiumi nekaitomas; galima traktuoti, kad turi tik daugiskaitą (ar dviskaitą - čia priklauso nuo to kaip pažiūrėsi / sutraktuosi), pvz.: abu, du, dvi',
                 5: u'Skaičiumi nekaitomas; galima traktuoti, kad turi tik vienaskaitą (linksniuojamas įgyja mot. g. vnsk. formas), pvz.: vienuolika',
             }),
             9: (u'Laipsniavimo charakteristika', {
                 0: u'Laipsnio formų neturi (galima laikyti, kad laipsnio kategorija jam neturi prasmės), pvz.: pusantro',
                 1: u'Turi nelyg., aukštesnįjį, aukštėlesnįjį ir aukščiausiąjį laipsnius, pvz.: pirmas',
                 2: u'Žodynuose pateikiamas aukštesniojo laipsnio, taigi, traktuojamas kaip savarankiška leksema; galimas traktavimas, kad turi taip pat nelyg., aukštėlesn. ir aukščiaus. laipsnius, pvz.: pirmesnis',
                 3: u'Žodynuose pateikiamas aukščiausiojo laipsnio, taigi, traktuojamas kaip savarankiška leksema; galimas traktavimas, kad turi taip pat nelyg., aukštesn. ir aukštėlesnįjį laipsnius, pvz.: pirmiausias',
             }),
            10: (u'Apibrėžtumo (įvardžiuotinumo) charakteristika', {
                 0: u'Įvardžiuotinių formų neturi; galima laikyti, kad įvardžiuotinumo (apibrėžtumo) požymis neturi prasmės, pvz.: pusantro',
                 1: u'Įgyja tiek neįvardžiuotines,  tiek ir įvardžiuotines formas, pvz.: dušimtas',
            }),
        }),
        (u'Darybos charakteristika', {
            11: (None, {
                 1: u'trupmeninis sktv su dėmeniu pus- [DLKG §711 psl. 245, pvz.: pusantro',
                 2: u'kelintinis sktv iš atitinkamo kiekinio sktv kamieno, pvz.: aštuoniašimtas, trečias',
                 3: u'kelintinis sktv su savarankišku kamienu, pvz.: pirmas, antras',
                 4: u'kelintinio sktv aukštesniojo laipsnio forma iš nelyginamojo laipsnio, pvz.: pirmesnis',
                 5: u'kelintinio sktv aukščiausiojo laipsnio forma iš nelyg laipsnio, pvz.: pirmiausias',
                 6: u'kiekinis sktv su savarankišku kamienu, pvz.: vienas, du, trys, šimtas',
                 7: u'dauginis sktv iš atitinkamo kiekinio sktv kamieno, pvz.: vieneri',
                 8: u'kuopinis sktv iš atitinkamo kiekinio, pvz.: abejetas',
                 9: u'11-19: sktv su sandu -lika (DLKG §709 psl. 244), pvz.: vienuolika, devyniolika',
                10: u'10-90: kiekiniai dešimčių pavadinimai su sandu ()‑dešimt(-s, -is), pvz.: dešimt(-s, -is)',
            }),
        }),
        (u'Derivacijos charakteristika', {
            12: (u'Atitikmenų buvimas kituose skyriuose', {
                 1: u'Kiekinis, atitikmenų kituose skyriuose neturi, pvz.: pusantro',
                 2: u'Kelintinis, atitikmenų kituose skyriuose neturi, pvz.: dušimtas',
                 3: u'Kelintinis, turi atitikmenis kiekinių ir dauginių skaitvardžių skyriuose, pvz.: pirmas',
                 4: u'Kiekinis, turi atitikmenis dauginių ir kelintinių skaitvardžių skyriuose, pvz.: vienas',
                 5: u'Dauginis, turi atitikmenis kiekinių ir kelintinių skaitvardžių skyriuose, pvz.: vieneri',
                 6: u'Kuopinis, turi atitikmenis kiekinių ir dauginių skaitvardžių skyriuose, pvz.: abejetas',
                 7: u'Dauginis, turi atitikmenis kiekinių ir kuopinių skaitvardžių skyriuose, pvz.: abeji',
                 8: u'Kiekinis, turi atitikmenis kuopinių ir dauginių skaitvardžių skyriuose, pvz.: abu',
                 9: u'Kelintinis, turi atitikmenis kiekinių, dauginių ir kuopinių skaitvardžių skyriuose (t.y. visuose), pvz.: antras',
                10: u'Kiekinis, turi atitikmenis kelintin, dauginių ir kuopinių skaitvardžių skyriuose (t.y. visuose), pvz.: du, trys',
                11: u'Kuopinis, turi atitikmenis kiekinių, kelintinių ir dauginių skaitvardžių skyriuose (t.y. visuose), pvz.: dvejetas, trejetas',
                12: u'Dauginis, turi atitikmenis kiekinių, kelintinių ir kuopinių skaitvardžių skyriuose (t.y. visuose), pvz.: dveji, treji',
                13: u'Kiekinis, turi atitikmenį kelintinių skaitvardžių skyriuje, pvz.: dešimt, šimtas',
                14: u'Kelintinis, turi atitikmenį kiekinių skaitvardžių skyriuje, pvz.: dešimtas, tūkstantas',
            }),
            13: (u'Deminutyviniai vediniai', {
                1: u'Mažybinių vedinių neturi, pvz.: pusantro',
                2: u'Turi atitikmenis (=iš jų gali būti išvedami) daiktavardžius deminutyvus penktukas, penktukėlis ir t.t. iš penktas; dešimtukas iš dešimtis (dešimtas?);, pvz.: šimtelis iš šimtas',
            }),
            14: (u'Būdvardžio vedinių su -iškas galimumas', {
                0: u'tokių vedinių neturi',
                1: u'turi',
            }),
            15: (u'Būdvardžio vedinių su -inis galimumas', {
                0: u'tokių vedinių neturi',
                1: u'turi',
            }),
            16: (u'Prieveiksmio vedinių su -in(i)ai galimumas', {
                0: u'tokių vedinių neturi',
                1: u'turi',
            }),
        }),
    ],

    # Įvardis
    4: [
        (u'Grupė', {
             4: (None, {
                  1: u'apibendrinamasis teigiamasis, funkcija: gali atlikti tiek būdvardžio, tiek ir daiktavardžio funkciją',
                  2: u'klausiamasis santykinis, funkcija: dktv',
                  3: u'neapibrėžiamasis nežymimasis, funkcija: dktv',
                  4: u'neapibrėžiamasis nežymimasis, funkcija: bdv',
                  5: u'asmeninis savybinis, funkcija: bdv',
                  6: u'apibendrinamasis neigiamasis, funkcija: dktv',
                  7: u'klausiamasis santykinis neapibrėžiamasis nežymimasis, funkcija: ir bdvr, ir dktv',
                  8: u'apibendrinamasis teigiamasis, funkcija: dktv',
                  9: u'asmeninis pagrindinis, funkcija: dktv',
                 10: u'apibendrinamasis neigiamasis, funkcija: ir bdvr, ir dktv',
                 11: u'neapibrėžiamasis nežymimasis, funkcija: ir bdvr, ir dktv',
                 12: u'klausiamasis santykinis neapibrėžiamasis nežymimasis, funkcija: dktv',
                 13: u'parodomasis apibrėžiamasis, funkcija: bdvr',
                 14: u'apibendrinamasis neigiamasis, funkcija: bdvr',
                 15: u'neapibrėžiamasis atskiriamasis, funkcija: bdvr',
                 16: u'klausiamasis santykinis neapibrėžiamasis nežymimasis, funkcija: bdvr',
                 17: u'apibendrinamasis teigiamasis, funkcija: bdvr',
                 18: u'neapibrėžiamasis atskiriamasis, funkcija: ir bdvr, ir dktv',
                 19: u'asmeninis pagrindinis neapibrėžiamasis pabrėžiamasis, funkcija: ir bdvr, ir dktv',
                 20: u'parodomasis apibrėžiamasis, funkcija: ir bdvr, ir dktv',
                 21: u'parodomasis apibrėžiamasis, funkcija: ',
                 22: u'asmeninis pagrindinis; negimininis, funkcija: dktv',
                 23: u'sangrąžinis; negimininis, funkcija: dktv',
             }),
        }),
        (u'Kaitybos charakteristika', {
             5: (u'Linksniavimo charakteristika', {
                  1: u'vyr: Įvardžių linksniavimo 2 paradigma pagal DLKG §797 psl.274; mot: Įvardžių linksniavimo 6 paradigma pagal DLKG §800 psl.276; pvz.: ikvienas, tamsta',
                  2: u'vyr: 1 paradigma pagal DLKG §797 psl.274 su vienu (nesavybiniu) kilmininku; mot: 6 paradigma pagal DLKG §800 psl.276; pvz.: kas, katras',
                  3: u'vyr: 4 paradigma pagal DLKG §797 psl.275; mot: 8 paradigma pagal DLKG §800 psl.277; pvz.: kuris, jis',
                  4: u'Žiūr. DLKG97 §801 psl.278; pvz.: maniškis',
                  5: u'vyr: 3 paradigma pagal DLKG §797 psl.275; mot: 7 paradigma pagal DLKG §800 psl.276; pvz.: anoks',
                  6: u'vyr: Žiūr. DLKG97 §806-7 psl.281-2; mot: Žiūr. DLKG97 §806-7 psl.281-2; pvz.: manasis',
                  7: u'vyr: 5 paradigma pagal DLKG §799 psl.276; mot: 8 paradigma pagal DLKG §800 psl.277; pvz.: pats',
                  8: u'Dviskaitos linksniavimo 2 paradigma, žiūr. DLKG §804 psl.280; pvz.: jiedu',
                  9: u'Žiūr. DLKG97 §795 psl.272-3; pvz.: aš',
                 10: u'Dviskaitos linksniavimo 1 paradigma, žiūr. DLKG §804 psl.279; pvz.: mudu',
                 11: u'Žiūr. DLKG97 §795 psl.272-3; pvz.: tu',
                 12: u'Žiūr. DLKG97 §795 psl.272; pvz.: savęs',
                 13: u'1 paradigma pagal DLKG §797 psl.274 su dviem kilmininkais: nesavybiniu (pvz., ko) ir savybiniu (pvz., kieno); pvz.: kas (kieno)',
                 14: u'Žiūr. DLKG97 §801 psl.278; pvz.: keleri',
                 15: u'Žiūr. DLKG97 §801 psl.278; pvz.: keletas',
                 16: u'Žiūr. DLKG97 §801 psl.278; pvz.: keli',
                 17: u'Žiūr. DLKG97 §801 psl.278; pvz.: kelintas',
                 18: u'Linksniavimo paradigma įvardžiui keliasdešimt(-s, -is); pvz.: keliasdešimt (-s, -is)',
                 19: u'Žiūr. DLKG97 §801 psl.278; pvz.: keliolika',
             }),
             6: (u'Giminės charakteristika', {
                 0: u'Giminė neapibrėžta (galima laikyti, kad giminės kategorija jam neturi prasmės); pvz.: kame',
                 1: u'Turi vyr., mot. ir bevardę giminę; pvz.: ikvienas',
                 2: u'Giminėmis nekaitomas (galima traktuoti, kad giminės kategorijos neturi); linksniuojamas įgyja daiktavardiškas mot. g. formas); pvz.: tamsta',
                 3: u'Turi vyr. ir mot. gim. (bevardės neturi); pvz.: katras',
                 4: u'Giminėmis nekaitomas (galima traktuoti, kad giminės kategorijos neturi); linksniuojamas įgyja daiktavardiškas vyr. g. formas); pvz.: keletas',
             }),
             7: (u'Skaičiaus charakteristika', {
                 0: u'Skaičius neapibrėžtas (galima laikyti, kad skaičiaus kategorija jam neturi prasmės); pvz.: kame',
                 1: u'Turi vienaskaitą ir daugiskaitą; pvz.: ikvienas',
                 2: u'Turi vienaskaitą, daugiskaitą ir dviskaitą; pvz.: jie',
                 3: u'Įvardžio dviskaita; galimos atitinkamos vnsk. ir dgsk. formos; pvz.: jiedu',
                 4: u'Skaičiumi nekaitomas; galima traktuoti, kad turi tik daugiskaitą; pvz.: keleri',
                 5: u'Skaičiumi nekaitomas; galima traktuoti, kad turi tik vienaskaitą; pvz.: keletas',
             }),
             8: (u'Apibrėžtumo (įvardžiuotinumo) charakteristika', {
                 0: u'Įvardžiuotinių formų neturi (=įvardžiuotinumo (apibrėžtumo) požymis jam neturi prasmės); pvz.: ikvienas',
                 1: u'Neįvardžiuotinis, gali įgyti įvardžiuotines formas; pvz.: manas',
                 2: u'Įvardžiuotinis, turi neįvardžiuotinius atitikmenis; pvz.: manasis',
                 3: u'Neįvardžiuotinis; įvardžiuotinę įgyja tik vyr.g. vnsk V formą (DLKG97 §807, psl.282); pvz.: pats',
             }),
        }),
        (u'Derivacijos charakteristika', {
             9: (u'Priešdėlio ne- galimumas', {
                 0: u'tokių vedinių neturi',
                 1: u'turi',
             }),
            10: (u'Deminutyviniai vediniai', {
                1: u'Mažybinių vedinių neturi; pvz.: katras',
                2: u'Iš jų gali būti išvedamos mažybinės formos; pvz.: tamsta-tamstelė',
            }),
        }),
    ],
    # Veiksmažodis
    5: [
        (u'Kaitybos charakteristika', {
              # Veiksmažodžių kaitybos (asmenavimo) charakteristika (nusakoma pagal žiūr. DLKG97 psl.334-337). {
              4: (u'tipo nr., pagal kamieno sandarą; galimos reikšmės: žiūr. DLKG97 psl.325', {
                  1: u'',
                  2: u'',
                  3: u'',
              }),
              5: (u'asmenuotės nr.; galimos reikšmės: žiūr. DLKG97 psl.334-337', {
                  1: u'',
                  2: u'',
                  3: u'',
              }),
              6: (u'grupės nr. asmenuotėje; galimos reikšmės: žiūr. DLKG97 psl.334-337; II-oje asmenuotėje veiksmažodžiai negrupuojami - šiuo atveju grupės nr. visada lygus 1', {
                  1: u'',
                  2: u'',
                  3: u'',
                  4: u'',
              }),
              7: (u'pogrupio nr. grupėje; galimos reikšmės: žiūr. DLKG97 psl.334-337; pogrupio nr. lygus 1, jei asmenuotėje veiksmažodžiai negrupuojami ar grupės neskaidomos į pogrupius; pogrupio nr. lygus 0, jei jį nustatyti automatiškai pasirodė neįmanoma', {
                  0: u'',
                  1: u'',
                  2: u'',
                  3: u'',
                  4: u'',
                  5: u'',
                  6: u'',
                  7: u'',
                  8: u'',
              }),
              # }
              8: (u'Prefiksas', {
                   0: u'',
                   1: u'ap',
                   2: u'api',
                   3: u'at',
                   4: u'atsi',
                   5: u'iš',
                   6: u'išsi',
                   7: u'į',
                   8: u'nu',
                   9: u'pa',
                  10: u'per',
                  11: u'pra',
                  12: u'prasi',
                  13: u'pri',
                  14: u'su',
                  15: u'už',
                  16: u'užsi',
                  17: u'ati',
                  18: u'persi',
                  19: u'apsi',
                  20: u'įsi',
                  21: u'ne',
                  22: u'nusi',
                  23: u'par',
                  24: u'pasi',
                  25: u'prisi',
                  26: u'sune',
                  27: u'susi',
                  28: u'neapsi',
                  29: u'parsi',
                  30: u'nesi',
                  31: u'neap',
              }),
              9: (u'Prefiksavimo charakteristika', {
                   1: u'p, Np, NBp, Bp, BNp, Tp, TBp, TBNp; pS, NpS, NBpS, BpS, BNpS, TpS, TBpS, TBNpS; pvz.: apgulti, aparti, išlipti, iškoneveikti',
                   2: u'api, Napi, NBapi, Bapi, BNapi, Tapi, TBapi, TBNapi; apS, NapS, NBapS, BapS, BNapS, TapS, TBapS, TBNapS; pvz.: apibarti, apiburbti',
                   3: u'p, Np, NBp, Bp, BNp, Tp,     TBp, TBNp; nėra; pvz.: atgulti, atidirbti, atlipti, apibaubėti, apeiti',
                   4: u'nėra; pS, NpS, NBpS, BpS, BNpS, TpS,    TBpS, TBNpS; pvz.: atsigulti, įsiloti, išsigiedrinti',
                   5: u'+, N, NB, B, BN, T, TN, TB, TBN; +, NS, NBS, BS, BNS, TS, TNS, TBS, TBNS; pvz.: barti, čiulpti, groti, koneveikti',
                   6: u'+, N, NB, B, BN, T, TN, TB, TBN; nėra; pvz.: kalti, lipti, aiktelėti, baubti, dantinėti',
                   7: u'nėra; +, NS, NBS, BS, BNS, TS, TNS, TBS, TBNS; pvz.: kaltis, gaidrintis, žentintis',
                   8: u'+, N, NB, B, BN, T, TN, TB, TBN; su priešdėliais: f, Nf, NBf, Bf, BNf, Tf, TBf, TBNf; +, NS, NBS, BS, BNS, TS, TNS, TBS, TBNS; su priešd: fS, NfS, NBfS, BfS, BNfS, TfS, TBfS, TBNfS; pvz.: absoliutinti',
                   9: u'+, N, NB, B, BN, T, TN, TB,  TBN; su priešdėliais: h, Nh, NBh, Bh, BNh, Th, TBh, TBNh; +, NS, NBS, BS, BNS, TS, TNS, TBS, TBNS; su priešd: gS, NgS, NBgS, BgS, BNgS, TgS, TBgS, TBNgS; pvz.: anodinti',
                  10: u'ati, Nati, NBati, Bati, BNati, Tati, TBati, TBNati; atS, NatS, NBatS, BatS, BNatS, TatS, TBatS, TBNatS; pvz.: atidanginti',
                  11: u'+,  N, NB, B, BN, T, TN, TB, TBN; su priešdėliais: g,  Ng, NBg, Bg, BNg, Tg,     TBg, TBNg; +, NS, NBS, BS, BNS, TS, TNS, TBS, TBNS; su priešd: gS, NgS, NBgS, BgS, BNgS, TgS, TBgS, TBNgS; pvz.: automatinti',
                  12: u'+, N, NB, B, BN, T, TN, TB, TBN; su priešdėliais: f, Nf, NBf, Bf, BNf, Tf, TBf, TBNf; fS, NfS, NBfS, BfS, BNfS, TfS, TBfS, TBNfS; pvz.: azartinti',
                  13: u'+, N, NB, B, BN, T, TN, TB, TBN; su priešdėliais: g, Ng, NBg, Bg, BNg, Tg,     TBg, TBNg; su priešdėliais: gS, NgS, NBgS, BgS, BNgS, TgS, TBgS, TBNgS; pvz.: bolševikinti',
                  14: u'+, N, NB, B, BN, T, TN, TB, TBN; su priešdėliais: r, Nr, NBr, Br, BNr Tr, TBr, TBNr; +, NS, NBS, BS, BNS, TS, TNS, TBS, TBNS; su priešdėliais: gS, NgS, NBgS, BgS, BNgS, TgS,    TBgS, TBNgS; pvz.: fluorinti',
                  15: u'N, NB, BN, TN, TBN; nėra; pvz.: neraminti, negeruoti',
                  16: u'+, N, NB, B, BN, T, TN, TB,  TBN; su priešdėliais: h, Nh, NBh, Bh, BNh, Th, TBh, TBNh; su priešdėliais: gS, NgS, NBgS, BgS, BNgS, TgS, TBgS, TBNgS; pvz.: revoliucinti',
                  17: u'pN, BpN, TpN, TBpN; pSN, BpSN, TpSN, TBpSN; pvz.: sunepatoginti',
                  18: u'pN, BpN, TpN, TBpN; nėra; pvz.: sunegražėti',
                  19: u'+, N, NB, B, BN, T, TN, TB,  TBN; su priešdėliais: r, Nr, NBr, Br, BNr, Tr,     TBr, TBNr; nėra; pvz.: bitumėti',
                  20: u'N; nėra; pvz.: negandotis',
                  21: u'nėra; NapS, NBapS, BNapS, TNapS, TBNapS; pvz.: neapsižiūrėti',
                  22: u'pS_, NpS_, NBpS_, BpS_, BNpS_, TpS_, TBpS_, TBNpS_; nėra; pvz.: apsieiti',
                  23: u'+, N_, NB_, B_, BN_, T_, TN_, TB_, TBN_; NS_, NBS_, BS_, BNS_, TS_, TNS_, TBS_, TBNS_; pvz.: eiti',
                  24: u'p, Np, NBp, Bp, BNp, Tp, TBp, TBNp; pS_, NpS_, NBpS_, BpS_, BNpS_, TpS_, TBpS_, TBNpS_; pvz.: sueiti',
                  25: u'nėra; +, NS, NBS, BS, BNS, TS, TNS, TBS, TBNS; su priešdėliais: fS, NfS, NBfS, BfS, BNfS, TfS, TBfS, TBNfS; pvz.: abortuotis',
                  26: u'nėra; +, NS, NBS, BS, BNS, TS, TNS, TBS, TBNS; su priešdėliais: gS, NgS, NBgS, BgS, BNgS, TgS,    TBgS, TBNgS; pvz.: asimiliuotis',
                  27: u'+, N, NB, B, BN, T, TN, TB,  TBN; su priešdėliais: x, Nx, NBx, Bx, BNx, Tx,     TBx, TBNx; su priešdėliais: uS, NuS, NBuS, BuS, BNuS, TuS, TBuS, TBNuS; pvz.: blokuoti',
                  28: u'+, N, NB, B, BN, T, TN, TB,  TBN; su priešdėliais: u, Nu, NBu, Bu, BNu, Tu,     TBu, TBNu; NS, NBS, BS, BNS, TS, TNS, TBS, TBNS; su priešdėliais: uS, NuS, NBuS, BuS, BNuS, TuS,    TBuS, TBNuS; pvz.: cementuoti',
                  29: u'+, N, NB, B, BN, T, TN, TB,  TBN; su priešdėliais: v, Nv, NBv, Bv, BNv, Tv,     TBv, TBNv; NS, NBS, BS, BNS, TS, TNS, TBS, TBNS; su priešdėliais: vS, NvS, NBvS, BvS, BNvS, TvS,    TBvS, TBNvS; pvz.: deleguoti',
                  30: u'+, N, NB, B, BN, T, TN, TB,  TBN; su priešdėliais: z, Nz, NBz, Bz, BNz, Tz,     TBz, TBNz; NS, NBS, BS, BNS, TS, TNS, TBS, TBNS; su priešdėliais: kS, NkS, NBkS, BkS, BNkS, TkS,    TBkS, TBNkS; pvz.: dezinfekuoti',
                  31: u'+, N, NB, B, BN, T, TN, TB,  TBN; su priešdėliais: m, Nm, NBm, Bm, BNm, Tm,     TBm, TBNm; NS, NBS, BS, BNS, TS, TNS, TBS, TBNS; su priešdėliais: nS, NnS, NBnS, BnS, BNnS, TnS,    TBnS, TBNnS; pvz.: diriguoti',
                  32: u'+, N, NB, B, BN, T, TN, TB,  TBN; su priešdėliais: n, Nn, NBn, Bn, BNn, Tn,     TBn, TBNn; NS, NBS, BS, BNS, TS, TNS, TBS, TBNS; su priešdėliais: nS, NnS, NBnS, BnS, BNnS, TnS,    TBnS, TBNnS; pvz.: koduoti',
                  33: u'+, N, NB, B, BN, T, TN, TB,  TBN; su priešdėliais: w, Nw, NBw, Bw, BNw, Tw,     TBw, TBNw; NS, NBS, BS, BNS, TS, TNS, TBS, TBNS; su priešdėliais: kS, NkS, NBkS, BkS, BNkS, TkS,    TBkS, TBNkS; pvz.: reguliuoti',
                  34: u'+, N, NB, B, BN, T, TN, TB,  TBN; su priešdėliais: n, Nn, NBn, Bn, BNn, Tn,     TBn, TBNn; su priešdėliais: nS, NnS, NBnS, BnS, BNnS, TnS,    TBnS, TBNnS; pvz.: piketuoti',
                  35: u'+, N, NB, B, BN, T, TN, TB,  TBN; su priešdėliais: c, Nc, NBc, Bc, BNc, Tc,     TBc, TBNc; NS, NBS, BS, BNS, TS, TNS, TBS, TBNS; su priešdėliais: cS, NcS, NBcS, BcS, BNcS, TcS,    TBcS, TBNcS; pvz.: pilotuoti',
                  36: u'+, N, NB, B, BN, T, TN, TB,  TBN; su priešdėliais: d, Nd, NBd, Bd, BNd, Td,     TBd, TBNd; NS, NBS, BS, BNS, TS, TNS,TBS, TBNS; su priešdėliais: cS, NcS, NBcS, BcS, BNcS, TcS,    TBcS, TBNcS; pvz.: transplantuoti',
                  37: u'nėra; NS, NBS, BNS, TNS, TBNS; pvz.: nesitverti',
                  38: u'Nap, NBap, BNap, TBNap; nėra; pvz.: neapkęsti',
                  39: u'bendračiai ir būtajam l.: +, N, NB, B, T, TB, TBN; esamajam l.: a) variantui "yra": n(ėra), Nb(ėra), b(ėra),  t(ėra),  Tb(ėra), TBn(ėra), b) variantui "esti": N_, NB_, B_, T_, TB_, TBN_; nėra; pvz.: tik: būti-yra(esti)-buvo',
                  40: u'+, N, NB, B, BN, T, TN, TB,  TBN; su priešdėliais: c, Nc, NBc, Bc, BNc, Tc,     TBc, TBNc; su priešdėliais: cS, NcS, NBcS, BcS, BNcS, TcS,    TBcS, TBNcS; pvz.: migruoti',
              }),
             10: (u'Sangrąžiškumas', {
                 1: u'nesangrąžinis',
                 2: u'sangrąžinis',
             }),
             11: (u'Sangrąžiavimo charakteristika', {
                 1: u'Žodynuose nesangrąžinis; galimos sangrąžinės formos; pvz.: barti, eiti, sueiti',
                 2: u'Žodynuose nesangrąžinis; sangrąžiškumo formos negalimos; pvz.: neraminti, revoliucinti, aiktelėti, sunegražėti,',
                 3: u'Žodynuose sangrąžinis; nesangrąžinės formos negalimos; pvz.: gaidrintis, abortuotis, atsisveikinti',
             }),
             12: (u'Tranzityvumas', {
                 0: u'veiksmažodis intranzityvus (ne galininkinis)',
                 1: u'veiksmažodis tranzityvus (galininkinis)',
             }),
             13: (u'Ar veiksmažodis turi kelis pagrindinių formų variantus, pvz., kristi (krenta/krinta), krito.', {
                 0: u'neturi',
                 1: u'turi',
             }),
         }),
        (u'Derivacijos charakteristika', {
             14: (u'Ar iš vksm galima padaryti priesagos -tumas vedinius', {
                 0: u'negalima',
                 1: u'galima',
             }),
             15: (u'Ar iš vksm galima padaryti priesagų -tel(ė)ti, -ter(ė)ti vedinius', {
                 0: u'negalima',
                 1: u'galima',
             }),
             16: (u'Darybos charakteristika : padarymo būdo numeris', {
                   0: u'iš nieko nepadarytas veiksmažodis be prefikso',
                   1: u'priesagos -inti veiksmažodis be prefikso',
                   2: u'iš nieko nepadarytas veiksmažodis su priešdėliu ap-',
                   3: u'iš nieko nepadarytas veiksmažodis su priešdėliu api-',
                   4: u'iš nieko nepadarytas veiksmažodis su priešdėliu at-',
                   5: u'iš nieko nepadarytas veiksmažodis su prefiksu atsi-',
                   6: u'iš nieko nepadarytas veiksmažodis su priešdėliu iš-',
                   7: u'iš nieko nepadarytas veiksmažodis su prefiksu išsi-',
                   8: u'iš nieko nepadarytas veiksmažodis su priešdėliu į-',
                   9: u'iš nieko nepadarytas veiksmažodis su priešdėliu nu-',
                  10: u'iš nieko nepadarytas veiksmažodis su priešdėliu pa-',
                  11: u'iš nieko nepadarytas veiksmažodis su priešdėliu per-',
                  12: u'iš nieko nepadarytas veiksmažodis su priešdėliu pra-',
                  13: u'iš nieko nepadarytas veiksmažodis su prefiksu prasi-',
                  14: u'iš nieko nepadarytas veiksmažodis su priešdėliu pri-',
                  15: u'iš nieko nepadarytas veiksmažodis su priešdėliu su-',
                  16: u'iš nieko nepadarytas veiksmažodis su priešdėliu už-',
                  17: u'iš nieko nepadarytas veiksmažodis su prefiksu užsi-',
                  18: u'iš nieko nepadarytas veiksmažodis su priešdėliu ati-',
                  19: u'iš nieko nepadarytas veiksmažodis su prefiksu persi-',
                  20: u'priesagos -inti veiksmažodis su priešdėliu ap-',
                  21: u'priesagos -inti veiksmažodis su priešdėliu api-',
                  22: u'priesagos -inti veiksmažodis su prefiksu apsi-',
                  23: u'priesagos -inti veiksmažodis su priešdėliu at-',
                  24: u'priesagos -inti veiksmažodis su priešdėliu ati-',
                  25: u'priesagos -inti veiksmažodis su prefiksu atsi-',
                  26: u'priesagos -inti veiksmažodis su priešdėliu iš-',
                  27: u'priesagos -inti veiksmažodis su prefiksu išsi-',
                  28: u'priesagos -inti veiksmažodis su priešdėliu į-',
                  29: u'priesagos -inti veiksmažodis su prefiksu įsi-',
                  30: u'priesagos -inti veiksmažodis su priešdėliu ne-',
                  31: u'priesagos -inti veiksmažodis su priešdėliu nu-',
                  32: u'priesagos -inti veiksmažodis su prefiksu nusi-',
                  33: u'priesagos -inti veiksmažodis su priešdėliu pa-',
                  34: u'priesagos -inti veiksmažodis su priešdėliu par-',
                  35: u'priesagos -inti veiksmažodis su prefiksu pasi-',
                  36: u'priesagos -inti veiksmažodis su priešdėliu per-',
                  37: u'priesagos -inti veiksmažodis su prefiksu persi-',
                  38: u'priesagos -inti veiksmažodis su priešdėliu pra-',
                  39: u'priesagos -inti veiksmažodis su prefiksu prasi-',
                  40: u'priesagos -inti veiksmažodis su priešdėliu pri-',
                  41: u'priesagos -inti veiksmažodis su prefiksu prisi-',
                  42: u'priesagos -inti veiksmažodis su priešdėliu su-',
                  43: u'priesagos -inti veiksmažodis su prefiksu sune-',
                  44: u'priesagos -inti veiksmažodis su prefiksu susi-',
                  45: u'priesagos -inti veiksmažodis su priešdėliu už-',
                  46: u'priesagos -inti veiksmažodis su prefiksu užsi-',
                  47: u'iš nieko nepadarytas veiksmažodis su prefiksu įsi-',
                  48: u'iš nieko nepadarytas veiksmažodis su prefiksu nusi-',
                  49: u'iš nieko nepadarytas veiksmažodis su priešdėliu par-',
                  50: u'iš nieko nepadarytas veiksmažodis su prefiksu pasi-',
                  51: u'iš nieko nepadarytas veiksmažodis su prefiksu prisi-',
                  52: u'iš nieko nepadarytas veiksmažodis su prefiksu susi-',
                  53: u'priesagos -telėti veiksmažodis be prefikso',
                  54: u'priesagos -terėti veiksmažodis be prefikso',
                  55: u'iš nieko nepadarytas veiksmažodis su prefiksu apsi-',
                  56: u'priesagos -(i)oti veiksmažodis be prefikso',
                  57: u'priesagos -ėti veiksmažodis be prefikso',
                  58: u'priesagos -(i)oti veiksmažodis su priešdėliu ap-',
                  59: u'priesagos -ėti veiksmažodis su priešdėliu ap-',
                  60: u'priesagos -ėti veiksmažodis su priešdėliu api-',
                  61: u'priesagos -(i)oti veiksmažodis su priešdėliu api-',
                  62: u'priesagos -(i)oti veiksmažodis su prefiksu apsi-',
                  63: u'priesagos -ėti veiksmažodis su priešdėliu at-',
                  64: u'priesagos -(i)oti veiksmažodis su priešdėliu ati-',
                  65: u'priesagos -(i)oti veiksmažodis su priešdėliu at-',
                  66: u'priesagos -ėti veiksmažodis su prefiksu atsi-',
                  67: u'priesagos -(i)oti veiksmažodis su prefiksu atsi-',
                  68: u'priesagos -ėti veiksmažodis su priešdėliu iš-',
                  69: u'priesagos -(i)oti veiksmažodis su priešdėliu iš-',
                  70: u'priesagos -(i)oti veiksmažodis su prefiksu išsi-',
                  71: u'priesagos -ėti veiksmažodis su prefiksu išsi-',
                  72: u'priesagos -ėti veiksmažodis su priešdėliu į-',
                  73: u'priesagos -(i)oti veiksmažodis su priešdėliu į-',
                  74: u'priesagos -(i)oti veiksmažodis su prefiksu įsi-',
                  75: u'priesagos -ėti veiksmažodis su prefiksu įsi-',
                  76: u'priesagos -ėti veiksmažodis su priešdėliu nu-',
                  77: u'priesagos -(i)oti veiksmažodis su priešdėliu nu-',
                  78: u'priesagos -(i)oti veiksmažodis su prefiksu nusi-',
                  79: u'priesagos -ėti veiksmažodis su prefiksu nusi-',
                  80: u'priesagos -ėti veiksmažodis su priešdėliu pa-',
                  81: u'priesagos -(i)oti veiksmažodis su priešdėliu pa-',
                  82: u'priesagos -(i)oti veiksmažodis su priešdėliu par-',
                  83: u'priesagos -(i)oti veiksmažodis su prefiksu pasi-',
                  84: u'priesagos -ėti veiksmažodis su prefiksu pasi-',
                  85: u'priesagos -ėti veiksmažodis su priešdėliu per-',
                  86: u'priesagos -(i)oti veiksmažodis su priešdėliu per-',
                  87: u'priesagos -ėti veiksmažodis su priešdėliu pra-',
                  88: u'priesagos -(i)oti veiksmažodis su priešdėliu pra-',
                  89: u'priesagos -ėti veiksmažodis su prefiksu prasi-',
                  90: u'priesagos -(i)oti veiksmažodis su prefiksu prasi-',
                  91: u'priesagos -ėti veiksmažodis su priešdėliu pri-',
                  92: u'priesagos -(i)oti veiksmažodis su priešdėliu pri-',
                  93: u'priesagos -ėti veiksmažodis su prefiksu prisi-',
                  94: u'priesagos -(i)oti veiksmažodis su prefiksu prisi-',
                  95: u'priesagos -ėti veiksmažodis su priešdėliu su-',
                  96: u'priesagos -(i)oti veiksmažodis su priešdėliu su-',
                  97: u'priesagos -ėti veiksmažodis su prefiksu sune-',
                  98: u'priesagos -(i)oti veiksmažodis su prefiksu susi-',
                  99: u'priesagos -ėti veiksmažodis su prefiksu susi-',
                 100: u'priesagos -ėti veiksmažodis su priešdėliu už-',
                 101: u'priesagos -(i)oti veiksmažodis su priešdėliu už-',
                 102: u'priesagos -(i)oti veiksmažodis su prefiksu užsi-',
                 103: u'priesagos -ėti veiksmažodis su prefiksu užsi-',
                 104: u'priesagos -(i)oti veiksmažodis su priešdėliu ne-',
                 105: u'priesagos -(i)oti veiksmažodis su prefiksu persi-',
                 106: u'iš nieko nepadarytas veiksmažodis su priešdėliu ne-',
                 107: u'iš nieko nepadarytas veiksmažodis su prefiksu sune-',
                 108: u'iš nieko nepadarytas veiksmažodis su prefiksu neapsi-',
                 109: u'priesagos -yti veiksmažodis be prefikso',
                 110: u'priesagos -yti veiksmažodis su priešdėliu ap-',
                 111: u'priesagos -yti veiksmažodis su priešdėliu api-',
                 112: u'priesagos -yti veiksmažodis su priešdėliu ati-',
                 113: u'priesagos -yti veiksmažodis su priešdėliu iš-',
                 114: u'priesagos -yti veiksmažodis su prefiksu išsi-',
                 115: u'priesagos -yti veiksmažodis su prefiksu įsi-',
                 116: u'priesagos -yti veiksmažodis su priešdėliu į-',
                 117: u'priesagos -yti veiksmažodis su priešdėliu nu-',
                 118: u'priesagos -yti veiksmažodis su priešdėliu pa-',
                 119: u'priesagos -yti veiksmažodis su prefiksu pasi-',
                 120: u'priesagos -yti veiksmažodis su priešdėliu per-',
                 121: u'priesagos -yti veiksmažodis su priešdėliu pri-',
                 122: u'priesagos -yti veiksmažodis su prefiksu prisi-',
                 123: u'priesagos -yti veiksmažodis su priešdėliu su-',
                 124: u'priesagos -yti veiksmažodis su prefiksu susi-',
                 125: u'priesagos -yti veiksmažodis su priešdėliu už-',
                 126: u'priesagos -yti veiksmažodis su prefiksu užsi-',
                 127: u'priesagos -yti veiksmažodis su priešdėliu at-',
                 128: u'priesagos -yti veiksmažodis su prefiksu persi-',
                 129: u'priesagos -yti veiksmažodis su priešdėliu pra-',
                 130: u'priesagos -yti veiksmažodis su prefiksu prasi-',
                 131: u'iš nieko nepadarytas veiksmažodis su prefiksu parsi-',
                 132: u'priesagos -(i)uoti veiksmažodis be prefikso',
                 133: u'priesagos -enti veiksmažodis be prefikso',
                 134: u'priesagos -enti veiksmažodis su priešdėliu ap-',
                 135: u'priesagos -enti veiksmažodis su priešdėliu at-',
                 136: u'priesagos -enti veiksmažodis su priešdėliu ati-',
                 137: u'priesagos -enti veiksmažodis su priešdėliu iš-',
                 138: u'priesagos -enti veiksmažodis su priešdėliu į-',
                 139: u'priesagos -enti veiksmažodis su prefiksu įsi-',
                 140: u'kt. priesagos veiksmažodis be prefikso',
                 141: u'priesagos -enti veiksmažodis su priešdėliu nu-',
                 142: u'priesagos -enti veiksmažodis su prefiksu nusi-',
                 143: u'priesagos -enti veiksmažodis su priešdėliu pa-',
                 144: u'priesagos -enti veiksmažodis su priešdėliu par-',
                 145: u'priesagos -enti veiksmažodis su priešdėliu per-',
                 146: u'priesagos -enti veiksmažodis su priešdėliu pra-',
                 147: u'priesagos -enti veiksmažodis su prefiksu prasi-',
                 148: u'priesagos -enti veiksmažodis su priešdėliu pri-',
                 149: u'priesagos -enti veiksmažodis su priešdėliu su-',
                 150: u'kt. priesagos veiksmažodis su priešdėliu su-',
                 151: u'priesagos -enti veiksmažodis su prefiksu susi-',
                 152: u'priesagos -enti veiksmažodis su priešdėliu už-',
                 153: u'kt. priesagos veiksmažodis su priešdėliu už-',
                 154: u'priesagos -enti veiksmažodis su prefiksu užsi-',
                 155: u'priesagos -enti veiksmažodis su prefiksu pasi-',
                 156: u'priesagos -(i)uoti veiksmažodis su priešdėliu ap-',
                 157: u'priesagos -(i)uoti veiksmažodis su priešdėliu api-',
                 158: u'priesagos -(i)uoti veiksmažodis su prefiksu apsi-',
                 159: u'priesagos -(i)uoti veiksmažodis su priešdėliu at-',
                 160: u'priesagos -(i)uoti veiksmažodis su prefiksu atsi-',
                 161: u'priesagos -(i)uoti veiksmažodis su priešdėliu iš-',
                 162: u'priesagos -(i)uoti veiksmažodis su prefiksu išsi-',
                 163: u'priesagos -(i)uoti veiksmažodis su priešdėliu į-',
                 164: u'priesagos -(i)uoti veiksmažodis su prefiksu įsi-',
                 165: u'priesagos -(i)uoti veiksmažodis su priešdėliu ne-',
                 166: u'priesagos -(i)uoti veiksmažodis su priešdėliu nu-',
                 167: u'priesagos -(i)uoti veiksmažodis su prefiksu nusi-',
                 168: u'priesagos -(i)uoti veiksmažodis su priešdėliu pa-',
                 169: u'priesagos -(i)uoti veiksmažodis su prefiksu pasi-',
                 170: u'priesagos -(i)uoti veiksmažodis su priešdėliu per-',
                 171: u'priesagos -(i)uoti veiksmažodis su priešdėliu pra-',
                 172: u'priesagos -(i)uoti veiksmažodis su priešdėliu pri-',
                 173: u'priesagos -(i)uoti veiksmažodis su prefiksu prisi-',
                 174: u'priesagos -(i)uoti veiksmažodis su priešdėliu su-',
                 175: u'priesagos -(i)uoti veiksmažodis su prefiksu sune-',
                 176: u'priesagos -(i)uoti veiksmažodis su prefiksu susi-',
                 177: u'priesagos -(i)uoti veiksmažodis su priešdėliu už-',
                 178: u'priesagos -(i)uoti veiksmažodis su prefiksu užsi-',
                 179: u'priesagos -(i)uoti veiksmažodis su priešdėliu ati-',
                 180: u'priesagos -(i)uoti veiksmažodis su priešdėliu par-',
                 181: u'iš nieko nepadarytas veiksmažodis su prefiksu nesi-',
                 182: u'iš nieko nepadarytas veiksmažodis su prefiksu neap-',
                 183: u'priesagos -(i)auti veiksmažodis be prefikso',
                 184: u'priesagos -(i)auti veiksmažodis su priešdėliu iš-',
                 185: u'priesagos -(i)auti veiksmažodis su priešdėliu nu-',
                 186: u'priesagos -(i)auti veiksmažodis su priešdėliu pa-',
                 187: u'priesagos -(i)auti veiksmažodis su priešdėliu pra-',
                 188: u'priesagos -(i)auti veiksmažodis su priešdėliu pri-',
                 189: u'priesagos -(i)auti veiksmažodis su prefiksu prisi-',
                 190: u'priesagos -(i)auti veiksmažodis su prefiksu susi-',
                 191: u'priesagos -(i)auti veiksmažodis su priešdėliu su-',
                 192: u'priesagos -(i)auti veiksmažodis su priešdėliu už-',
                 193: u'priesagos -(i)auti veiksmažodis su priešdėliu ap-',
                 194: u'priesagos -(i)auti veiksmažodis su priešdėliu at-',
                 195: u'priesagos -(i)auti veiksmažodis su priešdėliu ati-',
                 196: u'priesagos -(i)auti veiksmažodis su prefiksu išsi-',
                 197: u'priesagos -(i)auti veiksmažodis su prefiksu įsi-',
                 198: u'priesagos -(i)auti veiksmažodis su priešdėliu ne-',
                 199: u'priesagos -(i)auti veiksmažodis su prefiksu nusi-',
                 200: u'priesagos -(i)auti veiksmažodis su priešdėliu par-',
                 201: u'priesagos -(i)auti veiksmažodis su prefiksu pasi-',
                 202: u'priesagos -(i)auti veiksmažodis su priešdėliu per-',
                 203: u'padarytas iš veiksmažodžio priesagos -inėti veiksmažodis be prefikso',
                 204: u'padarytas iš veiksmažodžio priesagos -inėti veiksmažodis su priešdėliu iš-',
                 205: u'padarytas iš veiksmažodžio priesagos -inėti veiksmažodis su priešdėliu į-',
                 206: u'padarytas iš veiksmažodžio priesagos -inėti veiksmažodis su priešdėliu pri-',
                 207: u'padarytas iš veiksmažodžio priesagos -inėti veiksmažodis su priešdėliu su-',
                 208: u'padarytas iš veiksmažodžio priesagos -telėti veiksmažodis be prefikso',
                 209: u'padarytas iš veiksmažodžio priesagos -inėti veiksmažodis su priešdėliu už-',
                 210: u'padarytas iš veiksmažodžio priesagos -inėti veiksmažodis su priešdėliu ap-',
                 211: u'padarytas iš veiksmažodžio priesagos -inėti veiksmažodis su priešdėliu nu-',
                 212: u'padarytas iš veiksmažodžio priesagos -inėti veiksmažodis su priešdėliu pa-',
                 213: u'padarytas iš veiksmažodžio priesagos -inėti veiksmažodis su priešdėliu per-',
                 214: u'padarytas iš veiksmažodžio priesagos -inėti veiksmažodis su priešdėliu at-',
                 215: u'padarytas iš veiksmažodžio priesagos -inėti veiksmažodis su prefiksu išsi-',
                 216: u'padarytas iš veiksmažodžio priesagos -inėti veiksmažodis su priešdėliu ne-',
                 217: u'padarytas iš veiksmažodžio priesagos -inėti veiksmažodis su priešdėliu api-',
                 218: u'padarytas iš veiksmažodžio priesagos -inėti veiksmažodis su priešdėliu pra-',
                 219: u'padarytas iš veiksmažodžio priesagos -inėti veiksmažodis su prefiksu nusi-',
                 220: u'padarytas iš veiksmažodžio priesagos -inėti veiksmažodis su prefiksu pasi-',
                 221: u'padarytas iš veiksmažodžio priesagos -inėti veiksmažodis su prefiksu atsi-',
                 222: u'padarytas iš veiksmažodžio priesagos -inėti veiksmažodis su prefiksu susi-',
                 223: u'padarytas iš veiksmažodžio priesagos -inėti veiksmažodis su priešdėliu ati-',
                 224: u'padarytas iš veiksmažodžio priesagos -inėti veiksmažodis su priešdėliu par-',
                 225: u'padarytas iš veiksmažodžio priesagos -inėti veiksmažodis su prefiksu apsi-',
                 226: u'padarytas iš ištiktuko priesagos -telėti veiksmažodis be prefikso',
             }),
         }),
    ],

    # Prieveiksmis
    6: [
        (u'Kaitybos charakteristika', {
            4: (u'Laipsniavimas', {
                0: u'Laipsnio formų neturi (=galima traktuoti, kad laipsnio kategorija jam neturi prasmės), pvz.: greta',
                1: u'Yra nelyginamojo laipsnio; turi nelyg., aukštesn., aukštėlsesn. ir aukščiaus. laipsnius, pvz.: daug',
                2: u'Yra aukštesniojo laipsnio; turi nelyg., aukštesn., aukštėlsesn. ir aukščiaus. laipsnius, pvz.: daugiau',
                3: u'Yra aukštėlesniojo laipsnio; turi nelyg., aukštesn., aukštėlsesn. ir aukščiaus. laipsnius, pvz.: tolėliau',
                4: u'Yra aukštesniojo laipsnio; turi aukštesn., aukštėlsesn. ir aukščiaus. laipsnius (be nelyg.), pvz.: įšiauriau',
                5: u'Yra aukštėlesniojo laipsnio; turi aukštesn., aukštėlsesn. ir aukščiaus. laipsnius (be nelyg.), pvz.: kalnėliau',
                6: u'Yra aukščiausiojo laipsnio; turi aukštesn., aukštėlsesn. ir aukščiaus. laipsnius (be nelyg.), pvz.: apačiausiai',
                7: u'Yra aukščiausiojo laipsnio; kitų laipsnių neturi, pvz.: galiausiai',
            }),
        }),
        (u'Darybos charakteristika', {
            5: (None, {
                  0: u'bepref, be ypatingo galo; apie padarymo būdą nieko pasakyti negalim; pvz.: daug',
                  1: u'bepref,  aukštesniojo l. prv. iš atitinkamo žemesnio l. prieveiksmio, su priesaga -iau; pvz.: daugiau',
                  2: u'su ne- ir be ypatingo galo; pvz.: nedaug',
                  3: u'su ne-, baigiasi -i; pvz.: netoli',
                  4: u'bepref, aukštėlesn. l. prv. iš atitinkamo žemesnio l. prieveiksmio, su priesaga -ėliau; pvz.: tolėliau',
                  5: u'bepref, baigiasi -i; pvz.: toli',
                  6: u'bepref, baigiasi -(i)ui; pvz.: paskui',
                  7: u'aukštesniojo l. prv. iš kažko (gal iš dktv, gal iš ko kito), su priesaga -iau; pvz.: įšiauriau',
                  8: u'bepref, aukščiaus. l. prv. iš atitinkamo žemesnio l. prieveiksmio, su priesaga -iausiai; pvz.: apačiausiai',
                  9: u'bepref, baigiasi -(i)a; pvz.: greta, šalia',
                 10: u'su ne-, baigiasi -(i)a; pvz.: negana',
                 11: u'bepref, baigiasi -e; pvz.: apytekine',
                 12: u'bepref, baigiasi -iai; pvz.: tiesiogiai',
                 13: u'bepref, baigiasi -ei; pvz.: ikšiolei',
                 14: u'bepref, baigiasi -(i)ui; pvz.: aplinkui',
                 15: u'su ne-, baigiasi -am; pvz.: neilgam',
                 16: u'bepref, baigiasi -am; pvz.: ilgam',
                 17: u'bepref, baigiasi -(i)o; pvz.: kaipo,  tolydžio',
                 18: u'bepref, baigiasi -(i)ais; pvz.: juokais, priešpriešiais',
                 19: u'su ne-, baigiasi -(i)ais; pvz.: nejuokais',
                 20: u'bepref, baigiasi -(i)omis; pvz.: aklomis,  užkuriomis',
                 21: u'su ne-, baigiasi -(i)omis; pvz.: nemačiomis',
                 22: u'bepref, baigiasi -(i)os; pvz.: kitados,  atgalios',
                 23: u'bepref, baigiasi -us; pvz.: abipus',
                 24: u'su ne-, baigiasi -us; pvz.: netrukus',
                 25: u'bepref, baigiasi -(i)ant; pvz.: bematant',
                 26: u'su ne-, baigiasi -(i)ant; pvz.: nepaisant,  nedelsiant',
                 27: u'bepref, baigiasi -int; pvz.: beregint',
                 28: u'bepref, baigiasi -(i)u; pvz.: atstu,  apyryčiu',
                 29: u'su ne-, baigiasi -(i)u; pvz.: nelygu',
                 30: u'bepref, baigiasi -(i)uoju; pvz.: piktuoju,  gražiuoju',
                 31: u'su be- ir be ypatingo galo; pvz.: bereik',
                 32: u'bepref, iš dktv su -iškai; pvz.: daržiškai',
                 33: u'bepref, iš dktv su -ingai; pvz.: vaidingai',
                 34: u'su ne-, iš dktv su -ingai; pvz.: neturtingai',
                 35: u'bepref, iš dktv su -(i)uotai; pvz.: tarpuotai',
                 36: u'su be-, iš dktv su -iškai; pvz.: bedieviškai',
                 37: u'bepref, iš dktv su -ietiškai; pvz.: suvalkietiškai',
                 38: u'bepref, iš dktv su -ėtai; pvz.: eglėtai',
                 39: u'bepref, iš dktv su -otai; pvz.: miglotai',
                 40: u'su ne-, iš dktv su -iškai; pvz.: nemokšiškai',
                 41: u'bepref, iš bdv, su -(i)ai; pvz.: akylai,  dideliai',
                 42: u'iš bdv su apy- ir su -iai; pvz.: apydažniai',
                 43: u'su be-, iš bdv su -(i)ai; pvz.: bereikalingai',
                 44: u'bepref, iš bdv su -yn; pvz.: blogyn',
                 45: u'bepref, iš bdv su -okai; pvz.: dažnokai',
                 46: u'su ne-, iš bdv su -(i)ai; pvz.: nedorai',
                 47: u'bepref, aukštesniojo l. prv. iš bdv, su priesaga ‑iau; pvz.: žemiau',
                 48: u'su a-, iš bdv su -(i)ai; pvz.: amoraliai',
                 49: u'iš bdv su po- ir su -iai; pvz.: pogiliai',
                 50: u'bepref, iš bdv dalyvino ar daiktavardinio, su ‑imai; pvz.: įtikimai',
                 51: u'su ne-, iš bdv dalyvino ar daiktavardinio, su ‑imai; pvz.: neįtikimai',
                 52: u'bepref, iš bdv dalyvino ar daiktavardinio, su ‑tinai; pvz.: galutinai',
                 53: u'bepref,  iš bdv, su -iškai; pvz.: savitarpiškai',
                 54: u'bepref,  aukščiaus. l. prv., iš bdv, su priesaga ‑iausiai; pvz.: galiausiai',
                 55: u'bepref, iš sktv su -yn; pvz.: pirmyn',
                 56: u'bepref, iš sktv su -(i)aip; pvz.: vienaip',
                 57: u'bepref, iš sktv su -(i)opai; pvz.: vieneriopai',
                 58: u'bepref, iš sktv su -ok; pvz.: vienok',
                 59: u'bepref, iš sktv su -ok(i)ai; pvz.: vienokai',
                 60: u'bepref, iš sktv su -ur; pvz.: antrur',
                 61: u'bepref, iš sktv su -i(e)se; pvz.: dviese',
                 62: u'bepref, iš sktv su -gubai; pvz.: dvigubai',
                 63: u'bepref, iš sktv su -linkai; pvz.: dvilinkai',
                 64: u'bepref, iš įvrd su -ur; pvz.: ničniekur',
                 65: u'bepref, iš įvrd su -(i)aip; pvz.: niekaip',
                 66: u'bepref, iš įvrd su -ai; pvz.: jūsiškai',
                 67: u'bepref, iš įvrd su -iopai; pvz.: keleriopai',
                 68: u'bepref, iš įvrd su -gubai; pvz.: keliagubai',
                 69: u'bepref, iš įvrd su -iese; pvz.: keliese',
                 70: u'bepref, iš vksm.bndr. su -tinai; pvz.: dirbtinai',
                 71: u'su nepa- iš vksm.neveik.r.es.l.dlv. su -(i)amai; pvz.: nepajudinamai, nepabaigiamai',
                 72: u'su pa- iš vksm.neveik.r.es.l.dlv. su -(i)amai; pvz.: patenkinamai',
                 73: u'su su- iš vksm.bndr. su -tinai; pvz.: sutartinai',
                 74: u'bepref, iš vksm.neveik.r.es.l.dlv. su -(i)amai; pvz.: tariamai',
                 75: u'su ne- iš vksm.bndr. su -tinai; pvz.: nedovanotinai',
                 76: u'su pa- iš vksm.bndr. su -tinai; pvz.: pakartotinai',
                 77: u'su pasi- iš vksm.bndr. su -tinai; pvz.: pasibaisėtinai',
                 78: u'su nenu- nenuginčijamai iš vksm.neveik.r.es.l.dlv. su -(i)amai; pvz.: nenukrypstamai',
                 79: u'su išsi- iš vksm.bndr. su -tinai; pvz.: išsimokėtinai',
                 80: u'su ne- iš vksm.neveik.r.es.l.dlv. su -(i)amai; pvz.: nemokamai',
                 81: u'su pri- iš vksm.neveik.r.es.l.dlv. su -(i)amai; pvz.: prideramai',
                 82: u'su pri- iš vksm.veik.r.es.l.dlv. su -(i)ančiai; pvz.: priderančiai',
                 83: u'su atsi- iš vksm.būt.l.pdlv. su -(i)usiai; pvz.: atsidėjusiai',
                 84: u'su iš- iš vksm.neveik.r.es.l.dlv. su -imai; pvz.: ištikimai',
                 85: u'su nepa- iš vksm.neveik.r.es.l.dlv. su -imai; pvz.: nepatikimai',
                 86: u'su ne- iš vksm.neveik.r.būt.l.dlv. su -tai; pvz.: netikėtai',
                 87: u'su pasi- iš vksm.neveik.r.es.l.dlv. su -imai; pvz.: pasiturimai',
                 88: u'su pasi- iš vksm.veik.r.es.l.dlv. su -inčiai; pvz.: pasiturinčiai',
                 89: u'su pa- iš vksm.neveik.r.es.l.dlv. su -imai; pvz.: pastebimai',
                 90: u'bepref, iš vksm.neveik.r.es.l.dlv. su -imai; pvz.: regimai',
                 91: u'su pri- iš vksm.bndr. su -tinai; pvz.: primygtinai',
                 92: u'su neiš- iš vksm.neveik.r.es.l.dlv. su -(i)amai; pvz.: neišvengiamai',
                 93: u'su nepri- iš vksm.neveik.r.es.l.dlv. su -(i)amai; pvz.: neprieinamai',
                 94: u'su at- iš vksm.veik.r.es.l.dlv. su -(i)ančiai; pvz.: atsakančiai',
                 95: u'su į- iš vksm.neveik.r.es.l.dlv. su -omai; pvz.: įmanomai',
                 96: u'su neap- iš vksm.neveik.r.es.l.dlv. su -omai; pvz.: neapsakomai',
                 97: u'su neati- iš vksm.neveik.r.es.l.dlv. su -omai; pvz.: neatitaisomai',
                 98: u'su nepa- iš vksm.neveik.r.es.l.dlv. su -omai; pvz.: nepamainomai',
                 99: u'su nepri- iš vksm.neveik.r.es.l.dlv. su -omai; pvz.: nepriklausomai',
                100: u'su nesu- iš vksm.neveik.r.es.l.dlv. su -omai; pvz.: nesulaikomai',
                101: u'su ne- iš vksm.neveik.r.es.l.dlv. su -omai; pvz.: nevaržomai',
                102: u'su neiš- iš vksm.neveik.r.es.l.dlv. su -omai; pvz.: neišdildomai',
                103: u'su pa- iš vksm.neveik.r.es.l.dlv. su -omai; pvz.: papildomai',
                104: u'su į- iš vksm.bndr. su -tinai; pvz.: įskaitytinai',
                105: u'bepref, iš vksm.neveik.r.es.l.dlv. su -omai; pvz.: matomai',
                106: u'bepref, iš vksm.neveik.r.būt.l.dlv. su -tyn; pvz.: lenktyn',
                107: u'su ati- iš vksm.neveik.r.es.l.dlv. su -(i)amai; pvz.: atitinkamai',
                108: u'su atsi- iš vksm.bndr. su -tinai; pvz.: atsitiktinai',
                109: u'su ne- iš vksm.būt.l.pdlv. su -(i)usiai; pvz.: netikusiai',
                110: u'su pa- iš vksm.būt.l.pdlv. su -(i)usiai; pvz.: patrakusiai',
                111: u'su per- iš vksm.bndr. su -tinai; pvz.: pertektinai',
                112: u'su už- iš vksm.neveik.r.es.l.dlv. su -(i)amai; pvz.: užtenkamai',
                113: u'su ne- iš vksm.būt.l.pdlv. su -(i)usiai; pvz.: nevykusiai',
                114: u'bepref, iš vksm.būt.l.pdlv. su -(i)usiai; pvz.: vykusiai',
                115: u'su iš- iš vksm.bndr. su -tinai; pvz.: išpirktinai',
                116: u'su at- iš vksm.neveik.r.es.l.dlv. su -(i)amai; pvz.: atmenamai',
                117: u'su at- iš vksm.bndr. su -tinai; pvz.: atmintinai',
                118: u'su neįsi- iš vksm.neveik.r.es.l.dlv. su -(i)amai; pvz.: neįsivaizduojamai',
                119: u'su į- iš vksm.neveik.r.es.l.dlv. su -(i)amai; pvz.: įskiriamai',
                120: u'su neper- iš vksm.neveik.r.es.l.dlv. su -(i)amai; pvz.: neperskiriamai',
                121: u'su su- iš vksm.neveik.r.es.l.dlv. su -(i)amai; pvz.: suprantamai',
                122: u'su į- iš vksm.būt.l.pdlv. su -(i)usiai; pvz.: įniršusiai',
            }),
        }),
        (u'Derivacijos charakteristika', {
            6: (u'Prefiksavimas', {
                 0: u'bepref; su prefiksais formų neįgyja ; pvz.: paskui',
                 1: u'bepref; galimos formos su ne-, nebe-, tebene- ir pan. ; pvz.: daug',
                 2: u'su ne-; įmanomi atitinkami neneigiami prv (be ne-); įmanomi atitinkami neigiami prv su (nebe-, tebene-) ir pan. ; pvz.: nedaug, neabejotinai, nemokamai',
                 3: u'su ne-; neneigiamų prv (be ne-) nėra (arba yra, bet ne ta "supreveiksmėjusia" prasme); įmanomi atitinkami neigiami prv su (nebe-, tebene-) ir pan. ; pvz.: negirdom, nedovanotinai',
                 4: u'su be-; prv be be- nėra; su ne-, nebe-, ir pan. nėra ; pvz.: bereik',
                 5: u'su be-; yra ir forma be be-; galimos formos su ne-, nebe-, ir pan.; pvz.: bedieviškai, bereikalingai',
                 6: u'su be-; prv be be- nėra; galimos formos su ne-, nebe-, ir pan.; pvz.: bejėgiškai, beskoniškai',
                 7: u'su apy-; su ne-, nebe-, ir pan. nėra; yra atitinkamas prv iš bdv su ‑(i)ai be apy-; pvz.: apydažniai',
                 8: u'su a-; yra ir forma be a-; galimos formos su ne-, nebe-, ir pan. ; pvz.: amoraliai',
                 9: u'su po-; su ne-, nebe-, ir pan. nėra; yra atitinkamas prv iš bdv su ‑(i)ai be po-; pvz.: pogiliai',
                10: u'su ne- + priešd.; neneigiamų prv su šiuo priešd (be ne-) nėra (arba yra, bet ne ta "supreveiksmėjusia" prasme); įmanomi atitinkami prv su (nebe-, tebene- ir pan.) + šitas priešd. ; pvz.: nepajudinamai',
                11: u'su priešd; įmanomi atitinkami neigiami prv su (ne-, nebe-, tebene‑) + šitas priešd. ir pan. ; pvz.: patenkinamai',
                12: u'su priešd + si-; įmanomi atitinkami neigiami prv su (ne-, nebe-, tebene- ir pan.) + šitas priešd ir si- ; pvz.: pasibaisėtinai',
                13: u'su ne- + priešd; įmanomi neneigiami prv su šiuo priešd (be ne-); įmanomi atitinkami prv su (nebe-, tebene- ir pan.) + šitas priešd. ; pvz.: nenukrypstamai',
                14: u'su ne- + priešd + si-; neneigiamų prv su šiuo priešd (be ne-) nėra (arba yra, bet ne ta "supreveiksmėjusia" prasme); įmanomi atitinkami prv su (nebe-, tebene-) + šitas priešd.+si ir pan.; pvz.: neįsivaizduojamai',
            }),
        }),
    ],

    # Dalelytė
    7: [
        (u'Darybos charakteristika', {
            4: (None, {
                1: u'be ne-; pvz.: ag',
                2: u'su ne-; pvz.: nejau, nelyg',
            }),
        }),
    ],

    # Prielinksnis
    8: [
        (u'Prielinksnio ypatumai', {
            4: (None, {
                1: u'reikalauja kilmininko, polinksniu nebūna; pvz.: ant',
                2: u'reikalauja galininko, polinksniu nebūna; pvz.: aplink',
                3: u'reikalauja kilmininko, gali būti polinksniu; pvz.: dėka',
                4: u'reikalauja K arba G, polinksniu nebūna; pvz.: apsukui',
                5: u'reikalauja K, G arba Įn, polinksniu nebūna; pvz.: po',
                6: u'reikalauja naudininko, polinksniu nebūna; pvz.: priešingai',
                7: u'reikalauja įnagininko, polinksniu nebūna; pvz.: su',
            }),
        }),
        (u'Darybos charakteristika', {
            5: (None, {
                0: u'Apie prielinksnio padarymą nieko pasakyti negalim (šiame darbo etape to dar nenagrinėjome); pvz.: abipus, anot',
                1: u'Prielinksnis su ne-; pvz.: nepaisant, netoli',
            }),
        }),
    ],

    # Jungtukas
    9: [
        (u'Darybos charakteristika', {
            4: (None, {
                0: u'Apie jungtuko padarymą nieko pasakyti negalim (šiame darbo etape to dar nenagrinėjome); pvz.: ar, betgi, būtent',
                1: u'Jungtukas su ne-; pvz.: nekaip, nelyg',
            }),
        }),
    ],

    # Jaustukas
    10: [],

    # Ištiktukas
    11: [
        (u'Derivacijos charakteristika', {
            4: (None, {
                0: u'Veiksmažodinių derivacijų su -tel-,-ter- ir pan. neturi; pvz.: cha',
                1: u'Turi veiksmažodines derivacijas su -tel-, -ter- ir pan.; derivuojant -tel-, -ter- pridedami prie ištiktuko galo; pvz.: paukš',
                2: u'Turi derivacijas su -tel-, -ter- ir pan.; derivuojant, ištiktuko galo t susilieja su -tel-, -ter-; pvz.: braukšt',
            }),
        }),
    ],
}


def read_data(lmdb):
    with open(lmdb) as f:
        for line in f:
            yield line



def gen_symbols(indent):
    for n, c in POS.values():
        yield '%s<sdef n=%-10s c="%s"/>' % (
            indent, '"%s"' % n, c
        )

    for pos, posrules in MORPHOLOGY.items():
        for category, rules in posrules:
            yield ''
            yield '%s<!-- %s -->' % (indent, category)
            for name, options in rules.values():
                yield ''
                if name:
                    yield '%s<!-- %s -->' % (indent, name)
                for option in options.values():
                    if isinstance(option, tuple):
                        n, c = option
                        yield '%s<sdef n=%-10s c="%s"/>' % (
                            indent, '"%s"' % n, c
                        )


def dump_properties(i, lexeme, lemma, pos, params, fields):
    print i
    print ('%s -> %s' % (lexeme, lemma)).encode('utf-8')

    posm = POS[pos][0]
    print posm
    for category, rules in MORPHOLOGY[pos]:
        print category.encode('utf-8')
        for n, (name, options) in rules.items():
            n = n - 4
            if name:
                print '  %s' % name.encode('utf-8')
            else:
                print '  -'
            if isinstance(options[params[n]], basestring):
                print ('    %d: [%s] -> %s' % (n+4, params[n], options[params[n]])).encode('utf-8')
            else:
                print '    %d: [%s] -> %r' % (n+4, params[n], options[params[n]])


def get_fields(pos, params):
    fields = {}
    for category, rules in MORPHOLOGY[pos]:
        for n, (name, options) in rules.items():
            fields[n] = int(params[n-4])
    return fields


def get_values(pos, params):
    fields = {}
    for category, rules in MORPHOLOGY[pos]:
        for n, (name, options) in rules.items():
            fields[n] = options[int(params[n-4])]
    return fields


def validate_entry(i, line, pos, params):
    try:
        assert pos in MORPHOLOGY
        for category, rules in MORPHOLOGY[pos]:
            for n, (name, options) in rules.items():
                n = n - 4
                assert n < len(params), ('%s not in params: %r' % (n, params))
                assert params[n] in options, ('%s not in %r' % (params[n], options))
    except AssertionError:
        print '%d: %s' % (i, line.encode('utf-8'))
        raise

def check_filter(symbols, filters):
    slen = len(symbols)
    for i, fltr in enumerate(filters):
        if i+1 > slen:
            return False
        if fltr and fltr != symbols[i]:
            return True

def gen_paradigm(indent, name, forms, filters):
    yield '%s<pardef n="%s">' % (indent, name)
    for lft, rgt, symbols, includes in forms:
        if check_filter(symbols, filters): continue
        yield '%s  <e><p><l>%s</l><r>%s%s</r></p>%s</e>' % (
            indent, lft, rgt,
            ''.join(['<s n="%s"/>' % n for n in symbols]),
            ''.join(['<par n="%s"/>' % n for n in includes])
        )
    yield '%s</pardef>' % indent


def parse_noun(fields, values):
    key = []
    filters = []
    includes = []

    if fields[5] == 1:
        # Neigiančių prefiksų neturi
        key.append(1)
    elif fields[5] in (2, 3, 7, 8):
        # TODO: pridėti neigiamą simbolį
        key.append(1)
    elif fields[5] in (4, 5, 6):
        # TODO: pridėti neigiamą simbolį
        key.append(2)
    else:
        assert False

    if fields[6] in (1, 2):
        # Eilinis daiktavardžio pobūdis
        key.append(1)
    else:
        assert False

    # Linksniavimo charakteristika
    key.append(fields[7])

    if fields[8] in (1, 3):
        # Tik vyriška giminė
        key.append(1)
        filters.append('m')
    elif fields[8] == 2:
        key.append(2)
        filters.append(None)
    else:
        assert False

    if fields[9] in (1, 2, 5, 6):
        # Abiskaitinis, turi vienaskaitą ir daugiskaitą
        key.append(1)
        filters.append(None)
    elif fields[9] == 3:
        key.append(2)
        filters.append('pl')
    elif fields[9] == 4:
        key.append(3)
        filters.append('sg')
    else:
        assert False

    if fields[10] == 0:
        # Sąngražinių formų neturi
        key.append(1)
    else:
        assert False

    if fields[11] == 0:
        # Pamatinis iš nieko nepadarytas daiktavardis
        key.append(1)
    else:
        assert False

    if fields[12] == 1:
        # Deminutyvų neturi
        key.append(1)
    elif fields[12] == 2:
        # Turi normalius vienos giminės deminutyvus
        key.append(2)
        includes.extend([
            # TODO: nurodyti vieną giminę
            u'BASE__nam/elis', u'BASE__nam/eliukas', u'BASE__bern/užėlis'
        ])
    elif fields[12] == 3:
        # Turi deminutyvus abiejose giminėse
        key.append(3)
        includes.extend([
            u'BASE__nam/elis', u'BASE__nam/eliukas', u'BASE__bern/užėlis'
        ])
    else:
        assert False

    # Vediniai
    derivations = {
        13: u'BASE__bank/ininkas',
        14: u'BASE__bais/ybė',
        15: u'BASE__bern/ystė',
        16: u'BASE__bais/ingas',
        17: u'BASE__auks/iškas',
        18: u'BASE__nam/inis',
        19: u'in(i)ai',
        20: u'BASE__kaul/ėtas',
        21: u'BASE__auks/uotas',
    }
    k = 0
    for j in range(13, 22):
        k <<= 1
        if fields[j] == 1:
            if j == 19: continue  # Prieveiksmio vedinių su -in(i)a ???
            assert derivations[j] in PARADIGMS
            includes.append(derivations[j])
            k |= 1
    key.append(k)


    if fields[22] == 0:
        # Daiktavardis prefiksinių junginių neturi
        key.append(1)
    else:
        assert False


    if isinstance(values[7], Paradigm):
        paradigm = values[7]
    else:
        assert False

    return key, paradigm, includes, filters


def parse_line(i, line):
    fields = line.split()
    params = map(int, fields[4:])
    lexeme, source, lemma, pos = fields[:4]
    lemma = lexeme if lemma == '-' else lemma
    pos = int(pos)

    validate_entry(i, line, pos, params)

    fields = get_fields(pos, params)
    values = get_values(pos, params)

    posm = POS[pos][0]
    try:
        if posm == 'n':
            key, paradigm, includes, filters = parse_noun(fields, values)
        else:
            assert False
    except AssertionError:
        dump_properties(i, lexeme, lemma, pos, params, fields)
        raise

    return lexeme, key, paradigm, includes, filters


def gen_paradigms(lmdb, indent):
    paradigms = set()
    data = read_data(lmdb)
    #data = ['jogas 1 - 1 1 1 1 1 2 1 0 0 2 0 0 0 0 1 1 1 0 0 0',
    #        'namas 1 - 1 1 1 1 1 1 1 0 0 2 0 0 0 0 0 1 0 0 0 0']
    #data = ['namas 1 - 1 1 1 1 1 1 1 0 0 2 0 0 0 0 0 1 0 0 0 0']
    #data = ['baisas 1 - 1 1 1 1 1 1 1 0 0 2 1 1 0 1 0 1 1 0 0 0']
    #data = ['bernas 1 - 1 1 1 1 1 1 1 0 0 2 0 0 1 0 1 1 0 0 0 0']
    #data = ['kursai 3 - 1 1 1 1 1 1 3 0 0 2 0 0 0 0 1 1 0 0 0 0']
    #data = ['artojas 1 - 1 1 1 1 2 1 1 0 0 2 0 0 0 0 1 1 0 0 0 0']
    for i, line in enumerate(data):
        line = line.strip().decode('cp1257')
        lexeme, key, paradigm, includes, filters = parse_line(i, line)

        rgt = paradigm.forms[0][1]
        namesfx = '_'.join(filter(None, ['n']+filters))
        parname = '%s/%s__%s' % (lexeme[:-len(rgt)], rgt, namesfx)

        parforms = list(paradigm.forms)
        for incl in includes:
            if incl in paradigm.overrides:
                incl, forms = paradigm.overrides[incl]
            else:
                forms = PARADIGMS[incl]
            inclname = '%s__%s' % (incl, namesfx)
            parforms.append((u'', rgt, (), (inclname,)))
            if inclname in paradigms: continue
            paradigms.add(inclname)
            for line in gen_paradigm(indent, inclname, forms, filters):
                yield line

        key = tuple(key)
        if key not in paradigms:
            paradigms.add(key)
            for line in gen_paradigm(indent, parname, parforms, filters):
                yield line

        #print (u'%s<e lm="%s"><i>žuvininkys</i><par n="abiturien/tė__n"/></e>' % (
        #    indent, lemma
        #)).encode('utf-8')


def build_file(lmdb):
    yield u'<?xml version="1.0" encoding="UTF-8"?>'
    yield u'<dictionary>'
    yield u'  <alphabet>AĄBCČDEĘĖFGHIĮYJKLMNOPRSŠTUŲŪVZŽaąbcčdeęėfghiįyjklmnoprsštuųūvzž</alphabet>'
    yield u'  <sdefs>'
    for line in gen_symbols('    '):
        yield line
    yield u'  </sdefs>'
    yield u'  <pardefs>'

    #for name, forms in PARADIGMS:
    #    for line in gen_paradigm('    ', name, forms):
    #        yield line

    for line in gen_paradigms(lmdb, '    '):
        yield line

    yield u'  </pardefs>'
    yield u'  <section id="main" type="standard">'

    yield u'    <e lm="namas"><i>nam</i><par n="nam/as__n_m"/></e>'
    yield u'    <e lm="auksas"><i>auks</i><par n="auks/as__n_m"/></e>'
    yield u'    <e lm="anglas"><i>angl</i><par n="angl/as__n_m"/></e>'
    yield u'    <e lm="bankas"><i>bank</i><par n="bank/as__n_m"/></e>'
    yield u'    <e lm="jogas"><i>jog</i><par n="jog/as__n"/></e>'
    yield u'    <e lm="baisas"><i>bais</i><par n="bais/as__n_m"/></e>'
    yield u'    <e lm="bernas"><i>bern</i><par n="bern/as__n_m"/></e>'
    yield u'    <e lm="kaulas"><i>kaul</i><par n="kaul/as__n_m"/></e>'
    yield u'    <e lm="kursai"><i>kurs</i><par n="kurs/as__n_m_pl"/></e>'
    yield u'    <e lm="artojas"><i>artoj</i><par n="artoj/as__n_m"/></e>'

    #for line in gen_entries(lmdb, '    '):
    #    yield line
    yield u'  </section>'
    yield u'</dictionary>'



def expand(lmdb):
    with open('temp.dix', 'w') as f:
        for line in build_file(lmdb):
            f.write('%s\n' % line.encode('utf-8'))

    subprocess.call('lt-expand temp.dix', shell=True)


def generate(lmdb):
    for line in build_file(lmdb):
        print line.encode('utf-8')



def main(lmdb):
    expand(lmdb)



if __name__ == '__main__':
    lmdb = sys.argv[1]
    main(lmdb)

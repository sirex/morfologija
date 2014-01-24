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


class LMDBParser(object):
    def __init__(self, lmdb_file, lmdb, mdb, paradigms):
        self.lmdb_file = lmdb_file
        self.lmdb = lmdb
        self.mdb = mdb
        self.paradigms = paradigms

    def build_symbols(self):
        for node in self.mdb:
            symbol = node.get('symbol')
            if symbol is not None:
                yield '<sdef n=%-10s c="%s"/>' % (
                    '"%s"' % node['symbol'], node['label']
                )
            else:
                yield '<!-- sdef n=%-10s c="%s"/ -->' % (
                    '"%s"' % '', node['label']
                )

        for paradigm in self.paradigms:
            if paradigm['type'] == 'symbol':
                yield '<sdef n=%-10s c="%s"/>' % (
                    '"%s"' % paradigm['key'], paradigm['label']
                )

    def validate_entry(self, i, line, pos, params):
        try:
            assert pos in MORPHOLOGY
            for category, rules in MORPHOLOGY[pos]:
                for n, (name, options) in rules.items():
                    n = n - 4
                    assert n < len(params), ('%s not in params: %r' % (n, params))
                    assert params[n] in options, ('%s not in %r' % (params[n], options))
        except AssertionError:
            print('%d: %s' % (i, line))
            raise

    def parse_line(self, i, line):
        fields = line.split()
        params = map(int, fields[4:])
        lexeme, source, lemma, pos = fields[:4]
        lemma = lexeme if lemma == '-' else lemma
        pos = int(pos)
        self.validate_entry(i, line, pos, params)

    def build_paradigms(self):
        for i, line in enumerate(self.lmdb):
            line = line.strip()
            if line.endswith('1 1 1 1 3 1 1 0 0 2 0 0 0 0 1 1 0 0 0 0'):
                print(line)
                yield '<pardef />'

                # <pardef n="BASE__bais/ingas">
                #   <e><p><l>ingas</l><r><s n="m"/><s n="sg"/><s n="nom"/></r></p></e>
                # </pardef>

                break

    def build_idx(self):
        yield '<?xml version="1.0" encoding="UTF-8"?>'
        yield '<dictionary>'
        yield '  <alphabet>AĄBCČDEĘĖFGHIĮYJKLMNOPRSŠTUŲŪVZŽaąbcčdeęėfghiįyjklmnoprsštuųūvzž</alphabet>'
        yield '  <sdefs>'
        for line in self.build_symbols():
            yield '    ' + line
        yield '  </sdefs>'
        yield '  <pardefs>'

        #for name, forms in LMDB.items():
        #    for line in gen_paradigm('    ', name, forms, []):
        #        yield line

        for line in self.build_paradigms():
            yield '    ' + line

        yield '  </pardefs>'
        yield '  <section id="main" type="standard">'

        #for line in gen_entries(lmdb, '    '):
        #    yield line

        yield '  </section>'
        yield '</dictionary>'



def main(lmdb_file):
    with open('lmdb.yaml', encoding='utf-8') as f:
        mdb = yaml.load(f)

    with open('paradigms.yaml', encoding='utf-8') as f:
        paradigms = yaml.load(f)

    with open(lmdb_file, encoding='cp1257') as lmdb, \
         open('build.dix', 'w', encoding='utf-8') as dix:
        parser = LMDBParser(lmdb_file, lmdb, mdb, paradigms)
        for line in parser.build_idx():
            dix.write(line + '\n')

    with open('build.dix') as f:
        print(f.read())



if __name__ == '__main__':
    lmdb_file = sys.argv[1]
    main(lmdb_file)

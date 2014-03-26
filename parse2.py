#!/usr/bin/env python3

import sys

import yaml

from fn.iters import head

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


first = head


class Entry(object):
    def __init__(self, mdb, line):
        fields = line.split()
        params = list(map(int, fields[4:]))
        self.lexeme, self.source, lemma, pos = fields[:4]
        self.lemma = None if lemma == '-' else lemma
        self.pos = mdb.get(code=int(pos))
        assert self.pos is not None
        self.fields = []
        for field, value in zip(self.pos.query(code__isnull=False), params):
            self.fields.append(field.get(code=value))


class Node(object):
    def check_isnull(node, k, v):
        value = getattr(node, k, None)
        return (value is None) == v

    check = dict(
        isnull=check_isnull,
    )

    def __init__(self, node, parent=None):
        self.code = node.get('code')
        self.label = node.get('label')
        self.symbol = node.get('symbol')
        self.inflective = node.get('inflective', None)
        self.parent = parent
        self.fields = []
        self._init_fields(node.get('fields', []))

    def _init_fields(self, fields):
        for node in fields:
            self.fields.append(Node(node, self))

    def match(self, **kwargs):
        for k, v in kwargs.items():
            if '__' in k:
                k, check = k.split('__')
                if not Node.check[check](self, k, v):
                    return False
            else:
                if getattr(self, k, None) != v:
                    return False
        return True

    def query(self, **kwargs):
        for node in self.fields:
            if node.match(**kwargs):
                yield node
            else:
                for child in node.query(**kwargs):
                    yield child

    def parents(self, **kwargs):
        parent = self.parent
        while parent is not None:
            if parent.match(**kwargs):
                yield parent
            parent = parent.parent

    def get(self, **kwargs):
        for node in self.query(**kwargs):
            return node


class LMDBParser(object):
    def __init__(self, lmdb_file, lmdb, mdb, paradigms):
        self.lmdb_file = lmdb_file
        self.lmdb = lmdb
        self.mdb = mdb
        self.paradigms = paradigms

    def build_symbols(self):
        for node in self.mdb.fields:
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

    def get_field_values(self, node, params):
        fields = []
        for node in node.fields:
            if 'code' in node:
                code = node['code']
                n = code - 4
                assert n < len(params), ('%s not in params: %r' % (n, params))
                value_node = self.get_node_by_field(
                    node.get('fields', []), 'code', params[n]
                )
                assert value_node is not None, (
                    '%s not in %r' % (params[n], node))
                fields.append((node, value_node))
            else:
                fields.extend(self.get_field_values(node, params))
        return fields

    def build_paradigms(self):
        for i, line in enumerate(self.lmdb):
            line = line.strip()
            #if line.endswith('1 1 1 1 3 1 1 0 0 2 0 0 0 0 1 1 0 0 0 0'):
            if line.startswith('vabalas '):
                print(line)
                entry = Entry(self.mdb, line)
                for f in entry.fields:
                    parent = first(f.parents(code__isnull=False))
                    print('{:2}: {}'.format(parent.code, parent.label))
                    print('    {}: {}'.format(f.code, f.label[:72]))
                    print()

                #for node in self.mdb.

                yield '<pardef />'

                # <pardef n="BASE__bais/ingas">
                #   <e><p><l>ingas</l><r><s n="m"/><s n="sg"/><s n="nom"/></r></p></e>
                # </pardef>

                break

    def build_dix(self):
        yield '<?xml version="1.0" encoding="UTF-8"?>'
        yield '<dictionary>'

        yield '  <alphabet>AĄBCČDEĘĖFGHIĮYJKLMNOPRSŠTUŲŪVZŽaąbcčdeęėfghiįyjklmnoprsštuųūvzž</alphabet>'

        yield '  <sdefs>'
        #for line in self.build_symbols():
        #    yield '    ' + line
        yield '  </sdefs>'

        yield '  <pardefs>'
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
    mdb = Node(dict(fields=mdb))

    with open('paradigms.yaml', encoding='utf-8') as f:
        paradigms = yaml.load(f)

    with open(lmdb_file, encoding='cp1257') as lmdb, \
         open('build.dix', 'w', encoding='utf-8') as dix:
        parser = LMDBParser(lmdb_file, lmdb, mdb, paradigms)
        for line in parser.build_dix():
            dix.write(line + '\n')

    with open('build.dix') as f:
        print(f.read())



if __name__ == '__main__':
    # For vim users:
    # set makeprg=PYTHONIOENCODING=utf_8\ env/bin/python\ parse2.py\ lmdb.txt
    lmdb_file = sys.argv[1]
    main(lmdb_file)

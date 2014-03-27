def main():
    with open('lmdb.yaml', encoding='utf-8') as f:
        mdb = yaml.load(f)
    mdb = Node(dict(fields=mdb))

    with open('paradigms.yaml', encoding='utf-8') as f:
        paradigms = yaml.load(f)

    with open(lmdb_file, encoding='utf-8') as lmdb, \
         open('build.dix', 'w', encoding='utf-8') as dix:
        parser = Converter(lmdb_file, lmdb, mdb, paradigms)
        for line in parser.build_dix():
            dix.write(line + '\n')

    with open('build.dix') as f:
        print(f.read())

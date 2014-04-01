from .utils import assign
from .utils import getnested


class Symbol(object):
    pass


class Paradigm(object):
    def __init__(self, paradigms, paradigm):
        self.paradigms = paradigms
        assign(self, paradigm, (
            ('key', None),
            ('symbols', []),
            ('type', None),
            ('label', ''),
            ('define', dict()),
            ('extends', []),
            ('kind', None),
            ('name', None),
            ('override-symbols', True),
        ))

    def normalize_forms(self, forms):
        forms = forms if isinstance(forms, list) else [forms]
        forms = [a if isinstance(a, list) else [a] for a in forms]
        return forms

    def replace(self, ext, kind, symkey, symbol, forms):
        repl = getnested(ext, ('replace', kind, symkey), {})
        if symbol in repl:
            if repl[symbol] is None:
                return None
            else:
                return self.normalize_forms(repl[symbol])
        return forms

    def prefix(self, ext, kind, symkey, symbol, affix):
        prefix = getnested(ext, ('prefix', kind))
        if prefix is None:
            return affix
        if isinstance(prefix, str):
            return [prefix] + affix
        prefix = getnested(prefix, (symkey, symbol))
        if prefix is not None:
            return [prefix] + affix
        return affix

    def definitions(self, kind, ext=None):
        ext = ext or {}
        affixes = self.define.get(kind, dict())
        for symkey, affixes in affixes.items():
            symbols = self.paradigms.get(symkey).symbols
            for symbol, forms in zip(symbols, affixes):
                forms = self.normalize_forms(forms)
                forms = self.replace(ext, kind, symkey, symbol, forms)
                if forms is None: continue
                forms = [
                    self.prefix(ext, kind, symkey, symbol, affix)
                    for affix in forms
                ]
                yield forms, dict(self.symbols, **{symkey: symbol})

    def extensions(self, kind, ext=None):
        for extension in self.extends:
            keys = extension['keys']
            keys = keys if isinstance(keys, list) else [keys]
            for key in keys:
                paradigm = self.paradigms.get(key)
                for forms, symbols in paradigm.affixes(kind, extension):
                    yield forms, symbols

    def affixes(self, kind, ext=None):
        for forms, symbols in self.definitions(kind, ext):
            yield forms, symbols

        for forms, symbols in self.extensions(kind, ext):
            yield forms, symbols




class ParadigmCollection(object):
    def __init__(self, paradigms):
        self.paradigms = dict()
        for paradigm in paradigms:
            key = paradigm.get('key')
            assert key is not None
            self.paradigms[key] = Paradigm(self, paradigm)

    def get(self, key):
        return self.paradigms[key]

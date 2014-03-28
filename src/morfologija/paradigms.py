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
        ))

    def replace(self, ext, kind, symkey, symbol, affix):
        repl = getnested(ext, ('replace', kind, symkey), {})
        if symbol in repl:
            if repl[symbol] is None:
                return None
            else:
                return [repl[symbol]]
        return affix

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
        for symkey, suffixes in affixes.items():
            symbols = self.paradigms.get(symkey).symbols
            for symbol, affix in zip(symbols, suffixes):
                affix = [affix]
                affix = self.replace(ext, kind, symkey, symbol, affix)
                if affix is None: continue
                affix = self.prefix(ext, kind, symkey, symbol, affix)
                yield affix, [symbol] + self.symbols

    def extensions(self, ext=None):
        for extension in self.extends:
            keys = extension['keys']
            keys = keys if isinstance(keys, list) else [keys]
            for key in keys:
                paradigm = self.paradigms.get(key)
                for affix, symbols in paradigm.suffixes(extension):
                    yield affix, symbols

    def suffixes(self, ext=None):
        for suffix, symbols in self.definitions('suffixes', ext):
            yield suffix, symbols

        for suffix, symbols in self.extensions(ext):
            yield suffix, symbols




class ParadigmCollection(object):
    def __init__(self, paradigms):
        self.paradigms = dict()
        for paradigm in paradigms:
            key = paradigm.get('key')
            assert key is not None
            self.paradigms[key] = Paradigm(self, paradigm)

    def get(self, key):
        return self.paradigms[key]

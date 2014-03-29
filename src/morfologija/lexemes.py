from .utils import first


class Lexeme(object):
    """Morphological database entry.

    lexeme
        A word form, mostly lemma form.

    lemma
        Word lemma form, None if lemma is same as lexeme.

    source
        Source from where information about this lexeme is taken.

    pos
        Part of speech node from grammar tree.

    properties
        Part of speech properties as nodes from grammar tree.

    names
        Dictionary of flattened property and value names for this lexeme.

    """

    def __init__(self, grammar, sources, line):
        fields = line.split()
        params = list(map(int, fields[4:]))
        self.lexeme, source, lemma, pos = fields[:4]
        self.source = sources.get(code=int(source))
        self.lemma = None if lemma == '-' else lemma
        self.pos = grammar.query(code__isnull=False).get(code=int(pos))
        assert self.pos is not None
        self.properties = []
        for field, value in zip(self.pos.query(code__isnull=False), params):
            prop = field.query(code__isnull=False).get(code=value)
            if prop is None:
                raise Exception(
                    'Unknown value {val} for field {fld} ({label}) in {line}.'.
                    format(val=value, fld=field.code, line=line,
                           label=field.label)
                )
            self.properties.append(prop)
        self.names = dict(self.get_names())
        self.symbols = dict(self.get_symbols())

    def get_names(self):
        for node in self.properties:
            if node.name is not None:
                key = first(node.parents(name__isnull=False)).name
                val = node.name
                yield key, val

    def get_symbols(self):
        for node in self.properties:
            if node.symbol is not None:
                key = first(node.parents(name__isnull=False)).name
                val = node.symbol
                yield key, val

    def check_properties(self, properties):
        for k, v in properties.items():
            if k not in self.names or self.names[k] != v:
                return False
        return True

    def get_pardefs(self, node):
        """Exctract paradigm definition keys from node ``pardefs`` property.

        Node ``pardefs`` property example:

        .. code-block:: yaml

           pardefs:
           - - key: Jon/as
               properties:
                 properness: name
             - key: vyr/as
           - - key: eln/ias
               endswith: ias
             - key: vėj/as
           - vyr/ai

        Each ``pardefs`` list item can be string or list. If it is string, then
        paradigm definition key is added immediately, if it is list, then first
        matching item is added.

        To know if item matches, these fields are used:

        properties
            Checks if filter for all part of speech properties matches given
            values. See ``get_names`` method to understand where values for
            filter is taken from.

        endswith
            Checks if lexeme ends with specified string.

        """
        for pardef in node.pardefs:
            if isinstance(pardef, list):
                for item in pardef:
                    if (
                        'properties' in item and
                        not self.check_properties(item['properties'])
                    ):
                        continue
                    if (
                        'endswith' in item and
                        not self.lexeme.endswith(item['endswith'])
                    ):
                        continue
                    yield item['key']
                    break
            else:
                yield pardef

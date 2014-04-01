import unittest


VOWELS = set('aąeęėiįyouųū')

S = set('szšž')
T = set('pbtdkgcč') & {'dz', 'dž'}
R = set('lmnrvj')

STRULES = {'STR', 'ST', 'SR', 'TR'}


def itersounds(word):
    last = ''
    for char in word:
        if char in {'z', 'ž'} and last == 'd':
            yield last + char
            last = ''
            continue
        if last:
            yield last
        last = char
    if last:
        yield last


def tostr(sound):
    if sound in S:
        return 'S'
    if sound in T:
        return 'T'
    if sound in R:
        return 'R'
    return '?'


def syllabicate(word):
    syllables = []
    consonants = []
    syllable = ''
    STR = ''
    is_vowel = False
    for sound in itersounds(word):
        if sound in VOWELS and is_vowel:
            syllable += sound
        elif sound in VOWELS:
            carry_consonants = (
                (consonants and len(syllables) == 0) or
                (len(consonants) == 1) or
                (consonants and STR in STRULES)
            )
            if carry_consonants:
                syllables.append(syllable)
                syllable = ''.join(consonants)
            else:
                syllable += ''.join(consonants)
                syllables.append(syllable)
                syllable = ''
            STR = ''
            consonants = []
            syllable += sound
        else:
            STR += tostr(sound)
            consonants.append(sound)
            if len(STR) > 3:
                syllable += consonants.pop(0)
                STR = STR[1:]
        is_vowel = sound in VOWELS
    if syllable:
        syllables.append(syllable + ''.join(consonants))
    elif consonants and syllables:
        syllables[-1] += ''.join(consonants)
    return tuple(filter(None, syllables))


class SyllabicationTest(unittest.TestCase):
    def assertSyllabication(self, word, expected):
        self.assertEqual(syllabicate(word), expected)

    def test_(self):
        self.assertSyllabication('medus', ('me', 'dus'))
        self.assertSyllabication('siena', ('sie', 'na'))
        self.assertSyllabication('kalnai', ('kaln', 'ai'))

    def test_itersounds(self):
        self.assertEqual(list(itersounds('džinas')), ['dž', 'i', 'n', 'a', 's'])

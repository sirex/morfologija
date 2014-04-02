import re
import unittest
import collections


VOWELS = set('aąeęėiįyouųū')

S = set('szšž')
T = set('pbtdkgcč') | {'dz', 'dž'}
R = set('lmnrvj')

STRULES = {'STR', 'ST', 'SR', 'TR'}

Template = collections.namedtuple('Template', 'template example')

SYLLABIFICATION_TEMPLATES = [
    Template(template='*s-dešimt*', example=['trisdešimt', 'keturiasdešimt']),
]


def split_sounds(word):
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


#def compile_template(tmpl):
#    regex = ''
#    if tmpl.template.startswith('*'):
#
#
#
#_compiled_templates = None
#def compile_templates():
#    global _compiled_templates
#    if _compiled_templates is None:
#        _compiled_templates = [
#            compile_template(tmpl) for tmpl in SYLLABIFICATION_TEMPLATES
#        ]
#    return _compiled_templates
#
#
#def apply_template(word):
#    for template in SYLLABIFICATION_TEMPLATES:
#        t


def syllabificate(word):
    syllables = []
    consonants = []
    syllable = ''
    STR = ''
    is_vowel = False
    for sound in split_sounds(word):
        if sound in VOWELS and is_vowel:
            syllable += sound
        elif sound in VOWELS:
            carry_consonants = (
                (consonants and len(syllables) == 0) or
                (len(consonants) == 1) or
                (STR in STRULES)
            )
            if carry_consonants:
                syllables.append(syllable)
                syllable = ''.join(consonants)
            elif len(STR) > 2 and STR[-2:] in STRULES:
                syllable += ''.join(consonants[:-2])
                syllables.append(syllable)
                syllable = ''.join(consonants[-2:])
            elif len(STR) > 1:
                syllable += ''.join(consonants[:-1])
                syllables.append(syllable)
                syllable = ''.join(consonants[-1:])
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
    return filter(None, syllables)


class SyllabificationTest(unittest.TestCase):
    def assertSyllabification(self, word):
        expected = word.split('-')
        word = word.replace('-', '')
        self.assertEqual(list(syllabificate(word)), expected)

    def test_(self):
        self.assertSyllabification('me-dus')
        self.assertSyllabification('sie-na')
        self.assertSyllabification('kal-nai')
        self.assertSyllabification('a-kis')
        self.assertSyllabification('skra-ba-las')
        self.assertSyllabification('per-kirs')
        self.assertSyllabification('var-gams')
        self.assertSyllabification('link-sta')
        self.assertSyllabification('gy-vy-bė')
        # All these words bellow requires dictionary with exceptional forms.
        #self.assertSyllabification('ke-tu-rias-de-šimt')
        #self.assertSyllabification('a-bi-tu-ri-en-tas')
        #self.assertSyllabification('in-du-iz-mas')
        #self.assertSyllabification('su-i-ro')
        #self.assertSyllabification('juod-že-mis')

    def assertSplitSounds(self, sounds):
        word = ''.join(sounds)
        self.assertEqual(list(split_sounds(word)), sounds)

    def test_itersounds(self):
        self.assertSplitSounds(['dž', 'i', 'n', 'a', 's'])
        self.assertSplitSounds(['j', 'u', 'o', 'dž', 'e', 'm', 'i', 's'])

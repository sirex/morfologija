from .utils import first
from .sounds import iter_vowels
from .sounds import BACK_VOWELS


def affrication(stem, suffix):
    stem_ending = stem[-1]
    changes = {'d': 'dž', 't': 'č'}
    vowels = (first(iter_vowels(suffix)) or '')[:2]
    triggers = ['i' + s for s in BACK_VOWELS]
    if stem_ending in ('d', 't') and vowels in triggers:
        return stem[:-len(stem_ending)] + changes[stem_ending]
    else:
        return stem

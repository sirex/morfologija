VOWELS = 'aąeęėiįyouųū'
FRON_VOWELS = 'iįyeęė'
BACK_VOWELS = 'aąouųū'


def itervowels(chars):
    vowels = []
    for c in chars:
        vowel = c in VOWELS
        if vowel:
            vowels.append(c)
        else:
            yield ''.join(vowels)
            vowels = []
    if vowels:
        yield ''.join(vowels)

from googletrans import Translator
import pattern.text.de
from pattern.text.de import PAST, PARTICIPLE, PRESENT, SINGULAR, PLURAL


def translate(x):
    p = Translator()

    text = x

    k = p.translate(text, src='de', dest='en')

    translated = str(k.text)

    return translated


class conjugate_de:

    def __init__(self, word: str, pronoun: str, tense: str):

        assert pronoun.lower() in ['ich', 'du', 'er', 'sie', 'es', 'wir', 'ihr']
        assert tense.lower() in ['present', 'past', 'perfect', 'future']

        self.word = word
        self.pronoun = pronoun
        self.tense = tense

    def conjugation(self):

        tense_ref = ''
        ref_num = 0
        typ = ''

        dict_pn = {'ich': [1, SINGULAR], 'du': [2, SINGULAR], 'er': [3, SINGULAR], 'sie': [3, SINGULAR],
                   'es': [3, SINGULAR], 'wir': [1, PLURAL], 'ihr': [2, PLURAL]}

        dict_tn = {'present': PRESENT, 'perfect': PAST + PARTICIPLE, 'past': PAST}

        for key, val in dict_pn.items():

            if self.pronoun == 'Sie':
                ref_num = 3
                typ = PLURAL

            elif self.pronoun == key:
                ref_num = val[0]
                typ = val[1]

        for key, val in dict_tn.items():
            if self.tense == key:
                tense_ref = val

        return pattern.text.de.conjugate(self.word, tense_ref, ref_num, typ)

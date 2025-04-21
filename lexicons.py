import os
from spacy.lang.en import English

BASE_DIR = os.path.dirname(__file__)
nlp = English()
def load_wordlist(filename):
    with open(os.path.join(BASE_DIR, "lexicons", filename), "r") as f:
        return [nlp.make_doc(phrase.strip().lower()) for phrase in f]

def load_nrc_emotions(filename):
    emotion_words = []
    with open(os.path.join(BASE_DIR, "lexicons", filename), "r") as f:
        for line in f:
            word, emotion, value = line.strip().split('\t')
            if int(value) == 1:
                emotion_words.append(nlp.make_doc(word.lower()))
    return emotion_words

HEDGE_WORDS = load_wordlist("hedges.txt")
WEASEL_WORDS = load_wordlist("weasel.txt")
BUZZWORDS_WORDS = load_wordlist("buzzwords.txt")
EMOTION_WORDS = load_nrc_emotions("unique_words.txt")
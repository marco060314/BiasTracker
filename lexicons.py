import os
import spacy
from spacy.tokens import DocBin

BASE_DIR = os.path.dirname(__file__)
nlp = spacy.load("en_core_web_sm")

def load_wordlist(filename):
    #keep as make_doc or do i have to full nlp
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
EMOTION_WORDS = load_nrc_emotions("NRC_Emotion_Lexicon.txt")
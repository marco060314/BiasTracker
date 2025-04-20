import run_scraper
import torch
import nltk
import math
nltk.download("punkt")
from transformers import pipeline
from nltk.tokenize import sent_tokenize
import spacy
from spacy.tokens import DocBin
from lexicons import HEDGE_WORDS, WEASEL_WORDS, BUZZWORDS_WORDS, EMOTION_WORDS
from spacy.matcher import PhraseMatcher


classifier = pipeline("sentiment-analysis", model="distilbert-base-uncased-finetuned-sst-2-english")

def sentiment_analysis(article):
    sentences = sent_tokenize(article[0]["article"])
    results = classifier(sentences)
    #add polarity for headline
    polarity = 0
    polarity_list = []
    
    if not results:
        return 0,0
    
    for i in results:
        if i["label"] == "POSITIVE":
            polarity += i["score"]
            polarity_list.append(i["score"])
        else:
            polarity -= i["score"]
            polarity_list.append(i["score"] * -1)
    avg_polarity = polarity / len(results)
    standard_dev = 0
    for i in polarity_list:
        standard_dev+=abs(avg_polarity - i)
    standard_dev = math.sqrt(standard_dev / len(results))
    return avg_polarity, standard_dev

#spaCy section
def bias_analysis(article):
    sentences = sent_tokenize(article[0]["article"])
    nlp = spacy.load("en_core_web_sm")
    title_doc = nlp(article[0]["headline"])
    BATCH_SIZE = 8
    docs = list(nlp.pipe(sentences, batch_size=BATCH_SIZE)) #batch processing size
    word_count = len(article[0]["article"].split())
    emotion_count = 0
    weasel_count = 0
    buzzwords_count = 0
    hedge_count = 0

    for sent in docs.sents:
        for token in sent:
            if token.lemma_.lower() in EMOTION_WORDS:
                emotion_count += 1
            if token.lemma_.lower() in WEASEL_WORDS:
                weasel_count += 1
            if token.lemma_.lower() in HEDGE_WORDS:
                hedge_count += 1
            if token.lemma_.lower() in BUZZWORDS_WORDS:
                buzzwords_count += 1
    metrics = {
        "active": active,
        "passive": passive,
        "agent": agent,
        "emotion": emotion_count,
        "weasel": weasel_count,
        "hedge": hedge_count,
        "buzzwords": buzzwords_count
        }
    return metrics


    
#check for passive voice vs active voice, and check for when the agent is omitted
def agent_analysis(docs):
    active_count = 0
    passive_count = 0
    omitted_agent_count = 0
    for sent in docs.sents:
        passive = False
        agent = False
        nsubj = False
        nsubjpass = False
        auxpass = False
    
        for token in sent:
            if token.dep_ == "nsubj":
                nsubj = True
            if token.dep_ == "nsubjpass":
                nsubjpass = True
            if token.dep_ == "auxpass":
                auxpass = True
            if token.dep_ == "agent":
                for child in token.children:
                    if child.dep_ == "pobj":
                        agent = True
    if nsubjpass and auxpass:
        passive = True
        passive_count += 1
        if not agent:
            omitted_agent_count += 1
    elif nsubj:
        active_count += 1

    return active_count, passive_count, omitted_agent_count


#misinformation section
def misinformation_analysis(article):

    return 0


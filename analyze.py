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
import os
from sentence_transformers import SentenceTransformer, util


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
    active, passive, agent = agent_analysis(docs)

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


def is_important(sent):
    has_entity = any(ent.label_ in {"PERSON", "ORG", "GPE", "DATE", "PERCENT", "MONEY"} for ent in sent.ents)
    has_subject = any(tok.dep_ == "nsubj" for tok in sent)
    has_object = any(tok.dep_ in {"dobj", "obj"} for tok in sent)
    has_modal = any(tok.lemma_.lower() in {"must", "will", "prove", "confirm"} for tok in sent)

    score = sum([has_entity, has_subject and has_object, has_modal])
    return score >= 2  # mark as important if 2+ signals are true

#find key statements and remove similar statements
def find_statements(docs):
    sentences = []
    for sent in docs.sents:
        if is_important(sent):
            sentences.append(sent)
    unique_sentences = []
    model = SentenceTransformer("all-MiniLM-L6-v2")
    embeddings = model.encode(sentences, convert_to_tensor=True)
    cosine_scores = util.pytorch_cos_sim(embeddings, embeddings)
    for i, sentence in enumerate(sentences):
        is_duplicate = False
        for kept_idx in range(len(unique_sentences)):
            score = util.cos_sim(embeddings[i], embeddings[kept_idx])[0][0]
            if score > 0.85:
                is_duplicate = True
                break
        if not is_duplicate:
            unique_sentences.append(i)

    return [sentences[i] for i in unique_sentences]



#misinformation section
def misinformation_analysis(article):
    with open(os.path.join(os.path.dirname(__file__), "lexicons", "API"), "r") as f:
        API_KEY = [line.strip() for line in f][0]
    return 0


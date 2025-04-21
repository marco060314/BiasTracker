import run_scraper
import torch
import math
from transformers import pipeline
import spacy
from spacy.tokens import DocBin
from lexicons import HEDGE_WORDS, WEASEL_WORDS, BUZZWORDS_WORDS, EMOTION_WORDS
from spacy.matcher import PhraseMatcher
import os
from sentence_transformers import SentenceTransformer, util
import requests
import json


nlp = spacy.load("en_core_web_sm")
classifier = pipeline("sentiment-analysis", model="distilbert-base-uncased-finetuned-sst-2-english")


                                         
def get_docs(article):
    BATCH_SIZE = 8
    #article length is empty twin its cooked
    docs = nlp(article[0]["article"])
    return docs

def sentiment_analysis(docs):
    sentences = [sent.text for sent in docs.sents]
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
def bias_analysis(docs):
    emotion_count = 0
    weasel_count = 0
    buzzwords_count = 0
    hedge_count = 0
    active, passive, agent = agent_analysis(docs)
    matcher = PhraseMatcher(nlp.vocab)
    #for sent in docs.sents:#TODO: is it better to do by sentences or just all at once
    matcher.add("EMOTION", EMOTION_WORDS)
    matcher.add("WEASEL", WEASEL_WORDS)
    matcher.add("HEDGE", HEDGE_WORDS)
    matcher.add("BUZZWORDS", BUZZWORDS_WORDS)
    #NLP the lexicons and then do the phrasematcher thingy
    matches = matcher(docs)
    for id, start, end in matches:
        if (nlp.vocab.strings[id] == "EMOTION"):
            emotion_count+=1
        elif (nlp.vocab.strings[id] == "WEASEL"):
            weasel_count_count+=1
        elif (nlp.vocab.strings[id] == "HEDGE"):
            hedge_count+=1
        elif (nlp.vocab.strings[id] == "BUZZ"):
            buzzwords_count_count+=1
        

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
    model = SentenceTransformer("all-MiniLM-L6-v2")
    embeddings = model.encode(sentences, convert_to_tensor=True)
    unique_sentences = []
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
#TODO: check if this takes too long
'''
def misinformation_analysis(docs):
    ans = {}
    with open(os.path.join(os.path.dirname(__file__), "lexicons", "API.txt"), "r") as f:
        API_KEY = [line.strip() for line in f][0]
    claims = find_statements(docs)
    print("AHAHHAHAHAHHAHAHA")
    print(claims)
    for i in claims[:5]:
        query = "%20".join(i.split(" "))
        API_LINK = f"https://factchecktools.googleapis.com/v1alpha1/claims:search?query={query}&key={API_KEY}"
        result = requests.get(API_LINK)
        if result.status_code == 200:
            data = result.json()
            if (len(data) == 0):
                continue
            ans[i] = data["claims"][0]["claimReview"][0]["textualRating"]
    return ans

'''
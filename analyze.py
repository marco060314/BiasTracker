import run_scraper
import torch
import nltk
import math
nltk.download("punkt")
from transformers import pipeline
from nltk.tokenize import sent_tokenize
import spacy
from spacy.tokens import DocBin


classifier = pipeline("sentiment-analysis", model="distilbert-base-uncased-finetuned-sst-2-english")

def sentiment_analysis(article):
    sentences = sent_tokenize(article)
    results = classifier(sentences)
    
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
    nlp = spacy.load("en_core_web_md")
    title_doc = nlp(article[0]["headline"])
    doc = nlp(article[0]["article"])
    





#misinformation section



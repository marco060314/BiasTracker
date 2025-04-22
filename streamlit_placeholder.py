import run_scraper
import analyze

def run_program(url):
    article = run_scraper.run_scraper(url)
    print(article)
    docs = analyze.get_docs(article)
    avg_polarity, std_dev = analyze.sentiment_analysis(docs)
    metrics = analyze.bias_analysis(docs)
    active_count, passive_count, agent_omitted_count = analyze.agent_analysis(docs)
    #misinfo = analyze.misinformation_analysis(docs)
   #print("scraped headline:", article[0]["headline"])
    #print(avg_polarity)
    #print(metrics)
    #print(misinfo)
    return avg_polarity, std_dev, metrics

run_program("https://www.foxnews.com/media/supreme-court-consider-whether-parents-can-opt-out-kids-reading-lgbtq-books-classroom")


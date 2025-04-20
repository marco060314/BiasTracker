import run_scraper
import analyze

def run_program(url):
    article = run_scraper.run_scraper(url)
    print(article)
    docs = analyze.get_docs(article)
    avg_polarity, std_dev = analyze.sentiment_analysis()
    metrics = analyze.bias_analysis()
    active_count, passive_count, agent_omitted_count = analyze.agent_analysis()
    misinfo = analyze.misinformation_analysis()
    print("scraped headline:", article[0]["headline"])
    print(avg_polarity)
    print(metrics)
    print(active_count, passive_count, agent_omitted_count)
    print(misinfo)

run_program("https://www.cnn.com/2025/04/20/politics/democrat-crisis-recruitment-campaigns/index.html")


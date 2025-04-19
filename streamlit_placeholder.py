import run_scraper
def run_program(url):
    article = run_scraper(url)
    print("scraped headline:", article[0]["headline"])

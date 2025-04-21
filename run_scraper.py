from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from biastracker_scraper.biastracker_scraper.spiders.article_spider import ArticleSpider
from custom_pipeline import CustomPipeline
from scrapy.signalmanager import dispatcher
from scrapy import signals

def run_scraper(target_url):
    scraped_data = []

    def collect_item(item, **kwargs):
        print("📥 Signal captured item:", item["url"])
        scraped_data.append(item)

    dispatcher.connect(collect_item, signal=signals.item_passed)
    
    #pipeline = CustomPipeline()

    process = CrawlerProcess(settings={
        **get_project_settings(),
        "LOG_ENABLED": False,
        "REDIRECT_ENABLED": True,
        "DONT_REDIRECT": False,
        "HTTPERROR_ALLOWED_CODES": [301, 302],
        "ITEM_PIPELINES": {"custom_pipeline.CustomPipeline": 1}, 
    })

    process.crawl(ArticleSpider, url=target_url)
    process.start()

    return scraped_data

#print(run_scraper("https://www.cnn.com/2025/04/20/politics/democrat-crisis-recruitment-campaigns/index.html"))

    
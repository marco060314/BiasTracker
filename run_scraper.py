from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from biastracker_scraper.biastracker_scraper.spiders.article_spider import ArticleSpider

def run_scraper(target_url):
    scraped_data = []

    class CustomPipeline:
        def process_item(self, item, spider):
            scraped_data.append(item)
            return item
        
    process = CrawlerProcess(settings={
        **get_project_settings(),
        "LOG_ENABLED": False,
        "ITEM_PIPELINES": {"__main__:CustomPipeline": 1},
    })

    process.crawl(ArticleSpider, url=target_url)
    process.start()

    return scraped_data
    
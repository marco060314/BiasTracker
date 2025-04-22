# scrapy_spider_runner.py
import sys
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from biastracker_scraper.spiders.article_spider import ArticleSpider  # assuming your spider is called ArticleSpider

if __name__ == "__main__":
    url = sys.argv[1]
    process = CrawlerProcess(get_project_settings())
    process.crawl(ArticleSpider, start_url=url)
    process.start()

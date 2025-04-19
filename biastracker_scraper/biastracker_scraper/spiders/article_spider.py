import scrapy
from readability import Document
from bs4 import BeautifulSoup

class ArticleSpider(scrapy.Spider):
    name = "article"
    
    def __init__(self, url=None, *args, **kwargs):
        super(ArticleSpider, self).__init__(*args, **kwargs)
        if url:
            self.start_urls = [url]
        else:
            raise ValueError("Invalid url provided")
        
        def parse(self, response):
            #use readability to extract article from website
            doc = Document(response.text)
            headline = doc.short_title()

            soup = BeautifulSoup(doc.summary, "html.parser")
            paragraphs = soup.find_all("p")
            article_text = " ".join(p.get_text(strip=True) for p in paragraphs if p.get_text(strip=True))
            yield {
                "url": response.url,
                "headline": headline,
                "article": article_text
            }

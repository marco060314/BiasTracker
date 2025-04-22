import scrapy
from readability import Document


class ArticleSpider(scrapy.Spider):
    name = "article"
    
    def __init__(self, url=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if url:
            self.start_urls = [url]
        else:
            raise ValueError("Invalid url provided")
    def handle_error(self, failure):
        print("ERROR OCCURRED:", failure)

    def start_requests(self):
        headers = {
            "User-Agent": (
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/123.0.0.0 Safari/537.36"
            )
        }

        for url in self.start_urls:
            yield scrapy.Request(
                url=url,
                headers=headers,
                callback=self.parse,
                errback=self.handle_error,
                dont_filter=True
            )
    def parse(self, response):
        print("parsing")
        #use readability to extract article from website
        doc = Document(response.text)
        headline = doc.short_title()

        selector = scrapy.Selector(text=doc.summary())
        
        paragraphs = selector.css("p::text").getall()
        print("ehllo")
        article_text = " ".join(p.strip() for p in paragraphs if p.strip())
        print("Headline:", headline)
        print("Paragraph count:", len(paragraphs))
        print("Article length:", len(article_text))

        yield {
            "url": response.url,
            "headline": headline,
            "article": article_text
        }
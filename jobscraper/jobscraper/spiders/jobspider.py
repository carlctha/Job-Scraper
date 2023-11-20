import scrapy


class JobspiderSpider(scrapy.Spider):
    name = "jobspider"
    allowed_domains = ["se.linkedin.com"]
    start_urls = ["https://se.linkedin.com/jobs"]

    def parse(self, response):
        pass

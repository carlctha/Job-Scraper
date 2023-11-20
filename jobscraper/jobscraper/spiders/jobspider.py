import scrapy


class JobspiderSpider(scrapy.Spider):
    name = "jobspider"
    api_url = "https://se.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?keywords=Junior%2BBackend%2BSoftware%2BEngineer&location=Sverige&locationId=&geoId=105117694&f_TPR=r604800&start="

    start_urls = [api_url + "0"]

    def parse(self, response):
        first_job = response.meta.get('first_job', 0)
        data = {}
        jobs = response.css("li")
        returned_jobs = len(jobs)

        for job in jobs:
            data['job_title'] = job.css("h3::text").get(default='not-found').strip()
            data['job_detail_url'] = job.css(".base-card__full-link::attr(href)").get(default='not-found').strip()
            data['job_listed'] = job.css('time::text').get(default='not-found').strip()
            data['company_name'] = job.css('h4 a::text').get(default='not-found').strip()
            data['company_link'] = job.css('h4 a::attr(href)').get(default='not-found')
            data['company_location'] = job.css('.job-search-card__location::text').get(default='not-found').strip()
            yield data

        if returned_jobs > 0:
            next_page = int(first_job) + 25
            yield scrapy.Request(url=self.api_url + str(next_page), callback=self.parse, meta={'first_job': next_page})
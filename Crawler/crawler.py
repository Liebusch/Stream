# crawler.py
# Main code for crawler
# requires Scrapy package


from scrapy.spiders import Spider
from scrapy import Request
from scrapy.crawler import CrawlerProcess
from scrapy.utils import log


class Crawler:
    def runSpider(char):
        # Define a Scrapy Spider, which can accept *args or **kwargs
        # https://doc.scrapy.org/en/latest/topics/spiders.html#spider-arguments
        class PythonSpider(Spider):
            name = 'myspider'

            def __init__(self, character=None, *args, **kwargs):
                super(PythonSpider, self).__init__(*args, **kwargs)
                self.character = character
                self.download_delay = 1
                self.allowed_domains = ["secure.tibia.com"]
                self.start_url = "http://www.tibia.com/community/?subtopic=characters&name=%s" % character.name


            def start_requests(self):
                yield Request(url=self.start_url, callback=self.parse)

            def parse(self, response):
                self.character.level = response.xpath('.//*/tr[contains(td[1], "Level:")]/td[2]/text()').extract()[0]
                self.character.world = response.xpath('.//*/tr[contains(td[1], "World:")]/td[2]/text()').extract()[0]
                self.character.voc = response.xpath('.//*/tr[contains(td[1], "Vocation:")]/td[2]/text()').extract()[0]
                self.character.sex = response.xpath('.//*/tr[contains(td[1], "Sex:")]/td[2]/text()').extract()[0]
                self.character.achievement = response.xpath('.//*/tr[contains(td[1], "Achievement Points:")]/td[2]/text()').extract()[0]
                self.character.residence = response.xpath('.//*/tr[contains(td[1], "Residence:")]/td[2]/text()').extract()[0]
                self.character.guild = response.xpath('.//*/tr[contains(td[1], "Guild Membership:")]/td[2]/text()').extract()[0]

        process = CrawlerProcess({
            'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
        }, False)
        log.dictConfig({
            'version': 1,
            'disable_existing_loggers': True,
            'loggers': {
                'scrapy': {
                    'level': 'CRITICAL',
                }
            }
        })

        process.crawl(PythonSpider, character=char)
        process.start()  # the script will block here until the crawling is finished





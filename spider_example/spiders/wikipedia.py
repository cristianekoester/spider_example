from urllib.parse import urljoin

import scrapy

from spider_example.items import Wikipedia, Wiki


class WikipediaSite(scrapy.Spider):
    name = 'Wikipedia'

    base_url = 'https://pt.wikipedia.org/wiki'

    def start_requests(self):
        yield scrapy.Request(urljoin(self.base_url, '/wiki/Wikip%C3%A9dia:P%C3%A1gina_principal'),
                             callback=self.parse_wikipedia)

    def parse_wikipedia(self, response):
        wikis = []
        for td in response.xpath('//table[contains(@class, "portalen")]//td'):
            name, partial_url = td.xpath('.//span/text()').extract_first(), td.xpath('./a/@href').extract_first()
            url = urljoin(self.base_url, partial_url)
            wikis.append(Wiki(name=name.strip(), url=url.strip()))

        yield Wikipedia(wikis=wikis)

import re

import scrapy

from scrapy.loader import ItemLoader
from ..items import NovumbankgroupItem
from itemloaders.processors import TakeFirst


class NovumbankgroupSpider(scrapy.Spider):
	name = 'novumbankgroup'
	start_urls = ['https://www.novumbankgroup.com/news']

	def parse(self, response):
		post_links = response.xpath('//div[@class="row"]//a[@id]/@href').getall()
		yield from response.follow_all(post_links, self.parse_post)

	def parse_post(self, response):
		title = response.xpath('//h1/text()').get()
		description = response.xpath('//div[@class="col-md-8 col-sm-8"]//text()[normalize-space() and not(ancestor::h1 |ancestor::div[@class="newsAdditional"])]').getall()
		description = [p.strip() for p in description]
		description = ' '.join(description).strip()
		date = response.xpath('//div[@class="newsAdditional"]/text()').get()
		date = re.findall(r'[A-Za-z]+\s\d+, \d{4}', date)

		item = ItemLoader(item=NovumbankgroupItem(), response=response)
		item.default_output_processor = TakeFirst()
		item.add_value('title', title)
		item.add_value('description', description)
		item.add_value('date', date)

		return item.load_item()

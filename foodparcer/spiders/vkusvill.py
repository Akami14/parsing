import scrapy
from scrapy.http import HtmlResponse
from foodparcer.items import FoodparcerItem

class VkusvillSpider(scrapy.Spider):
    name = 'vkusvill'
    allowed_domains = ['vkusvill.ru']
    start_urls = ['https://vkusvill.ru/offers/yellow/', 'https://vkusvill.ru/offers/orange/',
                  'https://vkusvill.ru/offers/red/', 'https://vkusvill.ru/offers/dostupno-kazhdomu/']

    def parse(self, response:HtmlResponse):
        next_page = response.xpath('//div/a[contains(@data-page, "2")][2]/@href').get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)
        links = response.xpath('//a[contains(@class, "ProductCard__link")]/@href').getall()
        for link in links:
           yield response.follow(link, callback=self.foodparse)


    def foodparse(self, response:HtmlResponse ):
        url = response.url
        name = response.xpath('//h1/text()').get()
        price = response.xpath('//span[contains(@class, "Price__value")]/text()').get()
        time_up_to = response.xpath('//div[contains(@class, "AccentText")]/text()').get()
        yield FoodparcerItem(name=name, url=url, price=price, time_up_to=time_up_to)
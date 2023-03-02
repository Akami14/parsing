import scrapy
from scrapy.http import HtmlResponse
from Cygnus.items import CygnusItem
from scrapy.loader import ItemLoader


class CygnustechnologiesSpider(scrapy.Spider):
    name = 'cygnustechnologies'
    allowed_domains = ['cygnustechnologies.com']
    start_urls = ['https://www.cygnustechnologies.com/products.html']

    def parse(self, response: HtmlResponse, **kwargs):
        next_page = response.xpath('//a[@class="action  next"]/@href').get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)
        links = response.xpath('//a[@class="product-item-link"]/@href').getall()
        for link in links:
            yield response.follow(link, callback=self.cg_parse)



    def cg_parse(self, response: HtmlResponse):
        loader = ItemLoader(item=CygnusItem(), response=response)
        loader.add_xpath('name', "//h1/span/text()")
        loader.add_value('url', response.url)
        loader.add_xpath('photos', "//img/@src")
        loader.add_xpath('cat_number', '//td[@class="col item"]/span/text()')
        loader.add_xpath('price', '//div[contains(@class, "price-box price-final_price")]/span/span/span/text()')
        yield loader.load_item()

        #url = response.url
       # name1 = response.xpath('//h1/span/text()').getall()
       # name = ''.join(name1)
       # photos = response.xpath('//img/@src').getall()[3]
       # cat_number = response.xpath('//td[@class="col item"]/span/text()').get()
        #yield CygnusItem(name=name, url=url, photos=photos, cat_number=cat_number)



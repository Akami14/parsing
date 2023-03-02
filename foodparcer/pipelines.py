# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from pymongo import MongoClient

class FoodparcerPipeline:

    def __init__(self):
        client = MongoClient('localhost', 27017)
        self.mongo_base = client.food.food

    def process_item(self, item, spider):
        item['price'] = self.pre_process_price(item['price'])
        collections = self.mongo_base[spider.name]
        collections.insert_one(item)
        return item

    def pre_process_price(self, price):
        return int(price)


# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import scrapy
# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.pipelines.images import ImagesPipeline
from pymongo import MongoClient

class CygnusPipeline:

    def __init__(self):
        client = MongoClient('localhost', 27017)
        self.mongo_base = client.Cygnus



    def process_item(self, item, spider):
        item['name'] = ''.join(item['name']).replace('Request a Quote', '')
        item['photos'] = item['photos'][2]
        collections = self.mongo_base[spider.name]
        collections.insert_one(item)
        return item


class CygnusPipelinePhoto(ImagesPipeline):

    def get_media_requests(self, item, info):
        if item['photos']:
            for el in item['photos']:
                try:
                    yield scrapy.Request(el)
                except Exception as exp:
                    print(exp)

    def item_completed(self, results, item, info):
        item['photos'] = [it[1] for it in results if it[0]]
        return item

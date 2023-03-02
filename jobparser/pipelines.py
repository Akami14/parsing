# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from pymongo import MongoClient


class JobparserPipeline:
    def __init__(self):
        client = MongoClient('localhost', 27017)
        self.mongo_base = client.HHRU.vacancy_2023_03



    def process_item(self, item, spider):
        item['salary'] = self.process_salary(item['salary']) # вызваем функцию для обработки поля salary

        vacancy = {
            'name': item['name'],
            'min': item['salary'][0],
            'max': item['salary'][1],
            'currency': item['salary'][2],
            'url': item['url'],
        } # создаем словарик со своими именаме полей в который сложим -item

        collection = self.mongo_base[spider.name]
        collection.insert_one(vacancy) # прогружаем значения в базу
        return vacancy

    def process_salary(self, salary):


        for i in range(len(salary)):
            salary[i] = salary[i].replace(u'\xa0', u'') #замена разделителя тысяч xa0


        if salary[0] == 'з/п не указана':
            min_money = None
            max_money = None
            currency = None
        elif salary[0] == 'от ' and salary[2] == ' до ': # общий случай задан весь интервал зп от и до
            min_money = int(salary[1])
            max_money = int(salary[3])
            currency = salary[5]
        elif salary[0] == 'от ':  #  случай когда задана зп только от
            min_money = int(salary[1])
            max_money = None
            currency = salary[3]
        else:
            min_money = None #  случай когда задана только до
            max_money = int(salary[1])
            currency = salary[3]

        result = [
            min_money,
            max_money,
            currency]

        return result

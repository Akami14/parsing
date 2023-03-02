import scrapy
from scrapy.http import HtmlResponse
from jobparser.items import JobparserItem


class HhruSpider(scrapy.Spider):
    name = 'hhru'
    allowed_domains = ['hh.ru']


    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.start_urls = [
            f'https://vladimir.hh.ru/search/vacancy?area=2&search_field=name&search_field=company_name\
            &search_field=description&text={kwargs.get("search")}&items_on_page=20&no_magic=true&L_save_area=true',
            f'https://vladimir.hh.ru/search/vacancy?area=1&search_field=name&search_field=company_name\
            &search_field=description&text={kwargs.get("search")}&items_on_page=20&no_magic=true&L_save_area=true',
            f'https://vladimir.hh.ru/search/vacancy?area=1438&search_field=name&search_field=company_name\
            &search_field=description&text={kwargs.get("search")}&items_on_page=20&no_magic=true&L_save_area=true']
# url взяли для 3 областей мск санкт питербург и краснодарский край
    def parse(self, response: HtmlResponse, **kwargs):
        next_page = response.xpath("//a[@data-qa='pager-next']/@href").get()
        if next_page:
            yield response.follow(next_page, callback=self.parse) # follow асинхроный метод,
            # callback функция ожидающая ответа от сервера
            # сам метод follow идет дальше до тех пор пока может (существует next_page)
            # в даном случае callback есть исходная функция поскольку мы смотрим есть ли стр а это условие прописано выше
        links = response.xpath("//a[@data-qa='serp-item__title']/@href").getall()
        for link in links:
            yield response.follow(link, callback=self.vacancy_parse) # follow асинхроный метод
            # callback функция ожидающая ответа от сервера сам метод follow идет дальше до тех пор пока есть вакансии
            # callback тут передает собраный ответ от сервера в другую функцию  в которой мы уже выбераем интересующие нас поля

    def vacancy_parse(self, response: HtmlResponse):
        name = response.xpath("//h1/text()").get()
        salary = response.xpath("//div[@data-qa='vacancy-salary']//text()").getall()
        url = response.url
        yield JobparserItem(name=name, salary=salary, url=url)

# Поскольку при сборе большого количества данных с сайтов держать все в
# оперативной памяти не возможно фреймворк скрапи использует  yield (генератор фунция) в своих пауках
# за счет функции генератора и возможен сбор болбшого количества данных.
# так же исп return вернуло бы лишь сылку под индексом 0

from twisted.internet import reactor
from scrapy.crawler import CrawlerRunner
from scrapy.utils.project import get_project_settings
from scrapy.utils.log import configure_logging
from Cygnus.spiders.cygnustechnologies import CygnustechnologiesSpider

if __name__=='__main__':
    configure_logging()
    setings = get_project_settings()
    runner = CrawlerRunner(setings)
    runner.crawl(CygnustechnologiesSpider)
    join = runner.join()
    join.addBoth(lambda _:reactor.stop())
    reactor.run()

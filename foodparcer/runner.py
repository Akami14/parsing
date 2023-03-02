import sys

from twisted.internet import reactor
from scrapy.crawler import CrawlerRunner
from scrapy.utils.project import get_project_settings
from foodparcer.spiders.vkusvill import VkusvillSpider
from scrapy.utils.log import configure_logging


if __name__ == '__main__':
    configure_logging()
    settings = get_project_settings()
    runner = CrawlerRunner(settings)
    runner.crawl(VkusvillSpider)
   # runner.join()
    reactor.run()
    #d.addBoth(lambda _:reactor.stop())
#    sys.exit(main())

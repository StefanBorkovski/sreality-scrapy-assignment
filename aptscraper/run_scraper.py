import os

from dotenv import load_dotenv
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

from aptscraper.spiders.aptspider import ApartmentsSpider


class Scraper:
    """Wrapper class for running spyders.
    """
    def __init__(self):
        settings_file_path = 'aptscraper.settings' 
        os.environ.setdefault('SCRAPY_SETTINGS_MODULE', settings_file_path)
        self.process = CrawlerProcess(get_project_settings())
        self.spider = ApartmentsSpider

    def run_spiders(self):
        self.process.crawl(self.spider)
        self.process.start() 


if __name__=="__main__":
    # load environmental variables
    load_dotenv()
    # run spiders
    t_scraper = Scraper()
    t_scraper.run_spiders() 
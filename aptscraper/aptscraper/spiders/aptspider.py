import json
from typing import Generator

import scrapy
import unidecode
from aptscraper.items import ApartmentItem
from requests_html import HTMLSession

class ApartmentsSpider(scrapy.Spider):
    """Spider class for scraping apartments from defined API
    """
    name = 'apartments'
    allowed_domains = ['www.sreality.cz']
    start_urls = ['https://www.sreality.cz/api/en/v2/estates?category_main_cb=1&category_type_cb=1&page=0&per_page=100&locality_country_id=112']

    session = HTMLSession()
    
    def parse(self, response) -> Generator[ApartmentItem, None, None]:
        """Main parsing function

        Args:
            response (_type_): url response

        Yields:
            Generator[AppartmentItem, None, None]: apartment item
        """
        response_json = json.loads(response.body)
        for apt_item in response_json.get('_embedded').get('estates'):
            api_url = 'https://www.sreality.cz/api' + apt_item['_links']['self']['href']
            yield self.parse_apt_metadata_json(self.session.get(api_url).json())

    def parse_apt_metadata_json(self, response_json) -> ApartmentItem:
        """Parsing helper function.

        Args:
            response_json (_type_): url json response

        Returns:
            AppartmentItem: apartment item
        """
        apt_item = ApartmentItem()
        apt_item['title'] = unidecode.unidecode(response_json.get('name').get('value')) 
        apt_item['price'] = response_json.get('price_czk').get('value_raw')
        t_img = response_json.get('_embedded').get('images')[0].get('_links').get('dynamicDown').get('href')
        t_img = t_img.replace('{width}', '500')
        apt_item['img_url'] =  t_img.replace('{height}', '400')
        return apt_item

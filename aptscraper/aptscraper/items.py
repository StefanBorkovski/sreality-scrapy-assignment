import scrapy

class ApartmentItem(scrapy.Item):
    """Class that definse the fields of the scraped items.
    """
    title = scrapy.Field()
    price = scrapy.Field()
    img_url = scrapy.Field()

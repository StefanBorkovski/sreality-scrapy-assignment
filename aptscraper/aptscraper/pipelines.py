import os

import psycopg2
from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem
from scrapy.item import Item


class ConvertPricePipeline:
    """Pipeline class that converts item price from CZK to EUR with fixed rate.
    """
    CZK_TO_EUR = 0.039

    def process_item(self, item, spider) -> Item:
        adapter = ItemAdapter(item)
        if adapter.get('price') is not None:
            # convert the price
            adapter['price'] = int(adapter['price']) * self.CZK_TO_EUR
            return item
        else:
            raise DropItem(f"Missing price for item {item}")

class CleanDuplicatesPipeline:
    """Pipeline class that checks if scraped item was already scrapped in the current session
    """
    def __init__(self):
        self.seen_titles = dict()

    def process_item(self, item, spider) -> Item:
        adapter = ItemAdapter(item)
        if adapter['title'] in self.seen_titles and adapter['price']==self.seen_titles[adapter['title']]:
            raise DropItem(f"Duplicate appartment found: {item}")
        else:
            self.seen_titles[adapter['title']] = adapter['price']
            return item
        
class SavingPostgresPipeline(object):
    """Pipeline class that imports the scraped items in the DB
    """
    def __init__(self):
        self.create_connection()

    def create_connection(self) -> psycopg2.extensions.connection:
        """Connects to the database using predefined configuration in .env file.

        Returns:
            psycopg2.extensions.connection: postgres connection
        """
        self.connection = psycopg2.connect(
            host=os.environ['HOST'],
            port=os.environ['PORT'],
            database=os.environ['DB_NAME'],
            user=os.environ['USER'],
            password=os.environ['PASSWORD']
            )
        self.curr = self.connection.cursor()

    def process_item(self, item, spider) -> Item:
        self.store_db(item)
        return item

    def store_db(self, item):
        try:
            self.curr.execute(
                """ insert into public.apartments (title, price, img_url) values (%s, %s, %s)""", 
                (
                    item["title"],
                    item["price"],
                    item["img_url"]
                )
            )
            self.connection.commit()
        except BaseException as e:
            print(e)
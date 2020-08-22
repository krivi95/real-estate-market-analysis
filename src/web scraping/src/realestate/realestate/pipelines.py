# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

# Standard library imports
import json

# Local package imports
from .db_connection.connection import Connection
from .db_connection.sql_statements import SqlStatements

class ApartmentsSalePostgres:
    """Pipeline for storring scraped content in postgres database."""

    def __init__(self):
        self.num_of_requests_in_pipeline = 0

    def open_spider(self, spider):
        """When spider is opened, opens db connection as well."""
        with open('../../db_connetion.json') as db_file:
            # Loading db connection parameters 
            parameters = json.load(db_file)

            # Opening db connection (if run for first time db and tables are created)
            self.connection_utils = Connection(parameters)
            self.conn = self.connection_utils.open_connection()
            self.curr = self.conn.cursor()

    def close_spider(self, spider):
        """Before spider exiteds, closes db connection."""
        self.curr.close()
        self.connection_utils.close_connection(self.conn)

    def process_item(self, item, spider):
        """Storring scrapped item, info for apartment on sale, to database."""
        self.curr.execute(
            SqlStatements.insert_apartment(),
            (
                item['price'],
                item['location_city'],
                item['location_city_district'],
                item['location_lat'],
                item['location_long'],
                item['area_property'],
                item['construction_type'],
                item['num_floors_building'],
                item['apartment_floor'],
                item['registered'],
                item['heating_type'],
                item['num_rooms'],
                item['source'],
            )
        )
        self.conn.commit()
        self._log_progress()
        return item

    def _log_progress(self):
        """Printing progress of scraped data that went through."""
        self.num_of_requests_in_pipeline += 1
        if self.num_of_requests_in_pipeline % 20 == 0:
            print('-' * 200)
            print(f'DB PIPELINE: {self.num_of_requests_in_pipeline} items wenth though pipeline.')
            print('-' * 200)
         

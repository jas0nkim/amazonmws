import datetime

from peewee import *


azmws_db = MySQLDatabase('amazonmws', user='atewriteuser', password='20itSiT15', host='127.0.0.1')

class ScraperAmazonItem(Model):
    scraper_id = IntegerField()
    amazon_item_id = IntegerField()
    asin = CharField()
    created_at = DateTimeField()
    updated_at = DateTimeField()

    class Meta:
        database = azmws_db
        db_table = '__scraper_amazon_items'


class LookupAmazonItem(Model):
    lookup_id = IntegerField()
    amazon_item_id = IntegerField()
    asin = CharField()
    created_at = DateTimeField()
    updated_at = DateTimeField()

    class Meta:
        database = azmws_db
        db_table = 'lookup_amazon_items'


def run():
    for sai in ScraperAmazonItem.select().where(ScraperAmazonItem.scraper_id == 1001):
        lookup_ai = LookupAmazonItem(lookup_id=1, 
            amazon_item_id=sai.amazon_item_id, 
            created_at=datetime.datetime.now(),
            updated_at=datetime.datetime.now())
        lookup_ai.save()


if __name__ == "__main__":
    run()
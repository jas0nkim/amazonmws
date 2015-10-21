import datetime
import re

from peewee import *


azmws_db = MySQLDatabase('amazonmws', user='atewriteuser', password='20itSiT15', host='127.0.0.1')

class AmazonItem(Model):
    id = IntegerField()
    url = TextField()
    asin = CharField()
    category = CharField()
    subcategory = CharField()
    title = TextField()
    price = DecimalField(15, 2)
    description = TextField()
    review_count = IntegerField()
    avg_rating = FloatField()
    status = IntegerField()
    created_at = DateTimeField()
    updated_at = DateTimeField()

    class Meta:
        database = azmws_db
        db_table = 'amazon_items'

def run():
    for item in AmazonItem.select():
        item.description = re.sub(r'<!--(.*?)-->', '', item.description).strip()
        item.save()

if __name__ == "__main__":
    run()

import sys, os

sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

import uuid, json

from ebaysdk.trading import Connection as Trading
from ebaysdk.exception import ConnectionError

from amazonmws import settings
from amazonmws.models import StormStore, EbayStore
from amazonmws.loggers import GrayLogger as logger, StaticFieldFilter, get_logger_name



def get_api_access_rules(ebay_store):
    ret = False

    obj = {
        "MessageID": uuid.uuid4()
    }

    try:
        token = None if settings.APP_ENV == 'stage' else ebay_store.token
        api = Trading(debug=True, warnings=True, domain=settings.EBAY_TRADING_API_DOMAIN, token=token, config_file=os.path.join(settings.CONFIG_PATH, 'ebay.yaml'))
        api.execute('GetApiAccessRules', obj)

        if api.response.content:
            data = json.loads(api.response.json())

            print json.dumps(data, indent=4, sort_keys=True)
        else:
            print "No response"

    except ConnectionError as e:
        print str(e)

if __name__ == "__main__":
    ebay_stores = StormStore.find(EbayStore)

    if ebay_stores.count() > 0:
        for ebay_store in ebay_stores:
            print "\n"
            print "*"*30
            print ebay_store.username
            print "*"*30
            print "\n"

            get_api_access_rules(ebay_store)

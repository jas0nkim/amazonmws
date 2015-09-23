import pprint

from boto.mws.connection import MWSConnection

SELLER_ID = "A2I4JVBHOAUINI"
# MARKETPLACE_ID = "A2EUQ1WTGCTBG2" # CA
MARKETPLACE_ID = "ATVPDKIKX0DER" # US

# pp = pprint.PrettyPrinter(indent=4)

def getMatchingProduct(asin_list):

    conn = MWSConnection(SellerId=SELLER_ID)

    response = conn.get_matching_product(MarketplaceId=MARKETPLACE_ID, ASINList=asin_list)
    # pprint.pprint(response)

    if response.GetMatchingProductResult:
        for result in response.GetMatchingProductResult:
            print result.Error # print any error occurs
            print result.Product # print product object

if __name__ == "__main__":
    getMatchingProduct(["B005JFNE8G", "B00CI6J3HA", "B004S8F7QM"])
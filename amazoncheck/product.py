import pprint
from decimal import Decimal

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

def findLowestPrice(asin_list):

    conn = MWSConnection(SellerId=SELLER_ID)

    # print "*"*10
    # print "*"*10 + "Competitve Pricing" + "*"*10
    # print "*"*10
    response = conn.get_competitive_pricing_for_asin(MarketplaceId=MARKETPLACE_ID, ASINList=asin_list)
    
    if response.GetCompetitivePricingForASINResult:
        for result in response.GetCompetitivePricingForASINResult:
            if result.Error != None: # skip if any error on response
                continue
            
            for compatitive_prices in result.Product.CompetitivePricing:
                for compatitive_price in compatitive_prices.CompetitivePrices.CompetitivePrice:
                    if compatitive_price['condition'] != 'New': # skip not NEW products
                        continue

                    # most recent price
                    print Decimal(float(compatitive_price.Price.LandedPrice)).quantize(Decimal('1.00'))

def __getProductCategoryDetail(product_category, show_parent=False):
    if product_category.ProductCategoryName != "Categories":
        print product_category.ProductCategoryName  
    
    if show_parent and product_category.Parent != None:
        return __getProductCategoryDetail(product_category.Parent)

def getProductCategories(asin):

    conn = MWSConnection(SellerId=SELLER_ID)

    print "*"*10
    print "*"*10 + "Product Categories" + "*"*10
    print "*"*10
    response = conn.get_product_categories_for_asin(MarketplaceId=MARKETPLACE_ID, ASIN=asin)
    # print response
    print response.GetProductCategoriesForASINResult.Self
    
    __getProductCategoryDetail(response.GetProductCategoriesForASINResult.Self[0])
    # for product_category in response.GetProductCategoriesForASINResult.Self:
    #     __getProductCategoryDetail(product_category)


    # if response.GetProductCategoriesForASINResponse.GetProductCategoriesForASINResult:
        # print 'test'
        # print response.GetProductCategoriesForASINResult.Self

        # for compatitive_prices in result.Product.CompetitivePricing:
        #     for compatitive_price in compatitive_prices.CompetitivePrices.CompetitivePrice:
        #         if compatitive_price['condition'] != 'New': # skip not NEW products
        #             continue

        #         # most recent price
        #         print Decimal(float(compatitive_price.Price.LandedPrice)).quantize(Decimal('1.00'))

if __name__ == "__main__":
    # getMatchingProduct(["B005JFNE8G", "B00CI6J3HA", "B004S8F7QM"])
    # findLowestPrice(["B005JFNE8G", "B00CI6J3HA", "B004S8F7QM"])
    getProductCategories("B00CI6J3HA")
    getProductCategories("B004S8F7QM")
    # getMatchingProduct(["B00CI6J3HA"])
    # findLowestPrice(["B00CI6J3HA"])
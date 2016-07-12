import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from api.orders.models import get_unplaced_orders


if __name__ == "__main__":

    orders = get_unplaced_orders(ebay_store_id=1)
    
    print(orders)

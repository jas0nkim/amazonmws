import json

from flask import Blueprint, abort, jsonify, request
from .models import get_unplaced_orders, create_new_amazon_order

order = Blueprint('order', __name__)

@order.route('/', methods=['GET'])
def list():
    try:
        result = {
            'success': True,
            'data': get_unplaced_orders(ebay_store_id=1),
        }
        return jsonify(**result)

    except Exception as e:
        print(str(e))
        abort(500)

@order.route('/amazon_orders/', methods=['POST'])
def create_amazon_order():
    try:
        data = request.form
        if create_new_amazon_order(amazon_account_id=request.form.get('amazon_account_id', 0),
                amazon_order_id=request.form.get('amazon_order_id', ''),
                ebay_order_id=request.form.get('ebay_order_id', ''),
                asin=request.form.get('asin', ''),
                item_price=request.form.get('item_price', 0.00),
                shipping_and_handling=request.form.get('shipping_and_handling', 0.00),
                tax=request.form.get('tax', 0.00),
                total=request.form.get('total', 0.00)):
            result = {
                'success': True,
                'data': None,
            }
        else:
            result = {
                'success': False,
                'data': None,
            }
        return jsonify(**result)

    except Exception as e:
        print(str(e))
        abort(500)

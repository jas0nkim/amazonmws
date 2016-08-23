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
        data = json.loads(request.data)
        if create_new_amazon_order(**data):
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

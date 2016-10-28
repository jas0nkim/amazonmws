import json

from flask import Blueprint, abort, jsonify, request
from .models import get_unplaced_orders, update_ebay_order, create_new_amazon_order, create_new_order_tracking

order = Blueprint('order', __name__)


@order.route('/<start_record_number>/<limit>', methods=['GET'])
def list():
    try:
        start_record_number = int(start_record_number)
        limit = int(limit)
        if start_record_number < 1:
            start_record_number = None
        _r = get_unplaced_orders(ebay_store_id=1,
                    start_record_number=start_record_number,
                    limit=limit)
        result = {
            'success': True,
            'data': _r['data'],
            'last_record_number': _r['last_record_number'],
        }
        return jsonify(**result)

    except Exception as e:
        print(str(e))
        abort(500)


@order.route('/<order_id>', methods=['PUT'])
def update(order_id):
    try:
        result = {
            'success': True,
            'data': update_ebay_order(order_id=order_id,
                feedback_left=request.form.get('feedback_left', False)),
        }
        return jsonify(**result)

    except Exception as e:
        print(str(e))
        abort(500)


@order.route('/amazon_orders/', methods=['POST'])
def create_amazon_order():
    try:
        if create_new_amazon_order(amazon_account_id=request.form.get('amazon_account_id', 0),
                amazon_order_id=request.form.get('amazon_order_id', ''),
                ebay_order_id=request.form.get('ebay_order_id', ''),
                items=json.loads(request.form.get('items', '')),
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


@order.route('/trackings/', methods=['POST'])
def create_order_tracking():
    try:
        if create_new_order_tracking(ebay_store_id=1,
                ebay_order_id=request.form.get('ebay_order_id', ''),
                carrier=request.form.get('carrier', ''),
                tracking_number=request.form.get('tracking_number', '')):
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

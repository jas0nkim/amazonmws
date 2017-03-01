import sys, traceback
import json

from flask import Blueprint, abort, jsonify, request
from .models import *

order_return = Blueprint('order_return', __name__)

@order_return.route('/<start_return_id>/<limit>', methods=['GET'])
def list(start_return_id=0, limit=200):
    try:
        _r = get_order_returns(ebay_store_id=1,
                    start_return_id=start_return_id,
                    limit=int(limit))
        result = {
            'success': True,
            'data': _r['data'],
            'last_return_id': _r['last_return_id'],
        }
        return jsonify(**result)

    except Exception as e:
        traceback.print_exc(file=sys.stdout)
        abort(500)


@order_return.route('/amazon_returns/', methods=['POST'])
def create_amazon_order_return():
    try:
        if create_new_amazon_order_return(amazon_account_id=request.form.get('amazon_account_id', 0),
                amazon_order_id=request.form.get('order_id', ''),
                asin=request.form.get('asin', ''),
                ebay_return_id=json.loads(request.form.get('ebay_return_id', '')),
                return_id=request.form.get('return_id', None),
                rma=request.form.get('rma', None)):
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
        traceback.print_exc(file=sys.stdout)
        abort(500)

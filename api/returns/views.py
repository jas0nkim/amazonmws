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

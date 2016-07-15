from flask import Blueprint, abort, jsonify
from .models import get_unplaced_orders

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

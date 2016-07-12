from flask import Blueprint, abort, jsonify
from .models import get_unplaced_orders

order = Blueprint('order', __name__)

@order.route('/', methods=['GET'])
def list():
    try:
        return jsonify(**get_unplaced_orders(ebay_store_id=1))

    except Exception as e:
        logger.exception("Failed to fetch orders - {}".format(str(e)))
        abort(500)

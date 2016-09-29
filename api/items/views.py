import json

from flask import Blueprint, abort, jsonify, request
from .models import get_item_stats

ebay_item = Blueprint('ebay_item', __name__)


@ebay_item.route('/stats/<days>', methods=['GET'])
def list_stats(days=3):
    try:
        result = {
            'success': True,
            'data': get_item_stats(ebay_store_id=1, days=days),
        }
        return jsonify(**result)

    except Exception as e:
        print(str(e))
        abort(500)

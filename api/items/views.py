import sys, traceback
import json

from flask import Blueprint, abort, jsonify, request
from .models import get_item_performances

ebay_item = Blueprint('ebay_item', __name__)


@ebay_item.route('/performances/<days>', methods=['GET'])
def list_performances(days=3):
    try:
        result = {
            'success': True,
            'data': get_item_performances(ebay_store_id=1, days=days),
        }
        return jsonify(**result)

    except Exception as e:
        traceback.print_exc(file=sys.stdout)
        abort(500)

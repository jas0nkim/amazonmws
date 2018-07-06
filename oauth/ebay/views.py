import sys, traceback
import json

from flask import Blueprint, abort, jsonify, request

ebay_oauth = Blueprint('ebay_oauth', __name__)


@ebay_oauth.route('/index', methods=['GET'])
def oauth_default():
    return "Index page"


@ebay_oauth.route('/accepted', methods=['GET'])
def oauth_accepted():
    try:
        state = request.args.get('state', default=None)
        code = request.args.get('code', default=None)

        return "state: {s}, code: {c}".format(s=state, c=code)

    except Exception as e:
        traceback.print_exc(file=sys.stdout)
        abort(500)

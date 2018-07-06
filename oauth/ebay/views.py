import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
import json

from flask import Blueprint, abort, jsonify, request

from atoe.actions import EbayOauthAction

ebay_oauth = Blueprint('ebay_oauth', __name__)


@ebay_oauth.route('/index', methods=['GET'])
def oauth_default():
    return "Index page"


@ebay_oauth.route('/accepted', methods=['GET'])
def oauth_accepted():
    try:
        state = request.args.get('state', default=None)
        code = request.args.get('code', default=None)

        if code is None:
            raise Exception("auth code not passed from eBay ({c})".format(c=code))

        action = EbayOauthAction()
        user_access = action.exchange_to_user_access(auth_code=code)
        if user_access:
            # TODO: store refresh token in db

        return "succeeded"

    except Exception as e:
        traceback.print_exc(file=sys.stdout)
        abort(500)

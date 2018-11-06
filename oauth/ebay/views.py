import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'rfi'))

from amazonmws import django_cli
django_cli.execute()

import json
import traceback

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
            # TODO: store refresh token in db.. but we can't. don't know related eBay username.
            return json.dumps(user_access)
        else:
            return "failed"
        # return "succeeded"

    except Exception as e:
        traceback.print_exc(file=sys.stdout)
        abort(500)
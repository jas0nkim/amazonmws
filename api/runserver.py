import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from flask import Flask


application = Flask(__name__)
application.config.from_object('api.settings')

from orders.views import order

application.register_blueprint(order, url_prefix="/api/orders")
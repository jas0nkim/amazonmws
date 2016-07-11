from flask import Flask

application = Flask(__name__)
application.config.from_object('settings')

from orders.views import order

application.register_blueprint(order, url_prefix="/api/orders")
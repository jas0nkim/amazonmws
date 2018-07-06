import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

from flask import Flask

application = Flask(__name__)
application.config.from_object('api.settings')

from views import ebay_oauth

""" 
    www.affiliationship.com/oauth
"""
application.register_blueprint(ebay_oauth, url_prefix="/oauth")
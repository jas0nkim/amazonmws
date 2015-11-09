import re
import random
import base64
import logging

from stem import Signal
from stem.control import Controller

class TorProxyMiddleware(object):
    proxy = None
    tor_controlport = None
    tor_password = None

    def __init__(self, settings):
        self.proxy = settings.get('HTTP_PROXY')
        self.tor_controlport = settings.get('TOR_CONTROLPORT_LISTENER_PORT')
        self.tor_password = settings.get('TOR_PASSWORD')
        self._renew_connection()

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings)

    def process_request(self, request, spider):
        request.meta['proxy'] = self.proxy

    def process_response(request, response, spider):
        # if robot check screen shows up, renew connection
        title = response.css('title::text')[0].extract().strip().lower()
        if title == 'robot check':
            logging.error('IP caught by amazon.com <%s> - renewing connection' % request.meta['proxy'])
            self._renew_connection()

    def process_exception(self, request, exception, spider):
        logging.error('Proxy failed <%s> - renewing connection' % request.meta['proxy'])
        self._renew_connection()

    def _renew_connection(self):
        with Controller.from_port(port=self.tor_controlport) as controller:
            controller.authenticate(password=self.tor_password)
            controller.signal(Signal.NEWNYM)


class RandomProxyMiddleware(object):
    def __init__(self, settings):
        self.proxy_list = settings.get('PROXY_LIST')
        fin = open(self.proxy_list)

        self.proxies = {}
        for line in fin.readlines():
            parts = re.match('(\w+:\w+@)?(.+)', line)
            
            # Cut trailing @
            if parts.group(1):
                user_pass = parts.group(1)[:-1]
            else:
                user_pass = ''

            self.proxies['http://%s' % parts.group(2)] = user_pass

        fin.close()

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings)

    def process_request(self, request, spider):
        # Don't overwrite with a random one (server-side state for IP)
        if 'proxy' in request.meta:
            return None

        proxy_address = random.choice(self.proxies.keys())
        proxy_user_pass = self.proxies[proxy_address]

        request.meta['proxy'] = proxy_address
        if proxy_user_pass:
            basic_auth = 'Basic ' + base64.encodestring(proxy_user_pass)
            request.headers['Proxy-Authorization'] = basic_auth
        return None

    def process_exception(self, request, exception, spider):
        proxy = request.meta['proxy']
        logging.error('Removing failed proxy <%s>, %d proxies left' % (
                    proxy, len(self.proxies)))
        try:
            del self.proxies[proxy]
        except ValueError:
            pass
        return None

class RandomUserAgentMiddleware(object):
    def __init__(self, settings):
        self.ua_list = settings.get('USER_AGENT_LIST')

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings)

    def process_request(self, request, spider):
        if self.ua_list:
            request.headers.setdefault('User-Agent', self.ua_list)

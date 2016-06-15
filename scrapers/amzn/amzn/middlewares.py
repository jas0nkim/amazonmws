import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', '..'))

import re
import random
import base64
import logging

from amazonmws import settings as amazonmws_settings, utils as amazonmws_utils


class TorProxyMiddleware(object):
    proxy = None

    def __init__(self, settings):
        self.proxy = 'http://%s:%d' % (amazonmws_settings.APP_HOST, amazonmws_settings.PRIVOXY_LISTENER_PORT)
        amazonmws_utils.renew_tor_connection()
        logging.debug('Tor connection renewed')

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings)

    def process_request(self, request, spider):
        if self._is_enabled_for_request(request, spider):
            request.meta['proxy'] = self.proxy
        return None

    def process_response(self, request, response, spider):
        if not self._is_enabled_for_request(request, spider):
            return response

        if response.status == 503:
            logging.error('Service Unavailable <%s> HTTP status %d - renewing Tor connection' % (request.url, response.status))
            amazonmws_utils.renew_tor_connection()
            logging.debug('Tor connection renewed')
            return request

        # if robot check screen shows up, renew connection
        if len(response.css('title::text')) > 0:
            title = response.css('title::text')[0].extract().strip().lower()
            if title == 'robot check':
                logging.error('IP caught by amazon.com <%s> - renewing Tor connection' % request.url)
                amazonmws_utils.renew_tor_connection()
                logging.debug('Tor connection renewed')
                return request
        return response

    def process_exception(self, request, exception, spider):
        if not self._is_enabled_for_request(request, spider):
            return None

        logging.exception(exception)
        logging.error('Tor Proxy failed <%s> - renewing Tor connection' % request.meta['proxy'])
        amazonmws_utils.renew_tor_connection()
        logging.debug('Tor connection renewed')
        return None

    def _is_enabled_for_request(self, request, spider):
        return 'dont_proxy' not in request.meta and getattr(spider, 'tor_privoxy_enabled', False)


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
    crawlera_enabled = False

    def __init__(self, settings):
        self.ua_list = amazonmws_settings.USER_AGENT_LIST

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings)

    def process_request(self, request, spider):
        if self._is_enabled_for_request(spider):
            ua = random.choice(self.ua_list)
            if ua:
                request.headers.setdefault('User-Agent', ua)
                if self.crawlera_enabled:
                    request.headers['X-Crawlera-UA'] = 'desktop'


    def _is_enabled_for_request(self, spider):
        self.crawlera_enabled = getattr(spider, 'crawlera_enabled', False)
        return getattr(spider, 'rand_user_agent_enabled', False)

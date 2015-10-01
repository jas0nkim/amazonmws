import urllib2
from os.path import basename

from .loggers import GrayLogger as logger


def validate_url(url):
    ret = False

    try:
        urllib2.urlopen(url)
        ret = True

    except urllib2.HTTPError, e:
        logger.exception(e)

    except urllib2.URLError, e:
        logger.exception(e)

    return ret

def dict_to_unicode(dictionary):
	return str(dictionary).decode('unicode-escape')
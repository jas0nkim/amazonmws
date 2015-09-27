import urllib2

def validate_url(url):

    ret = False

    try:
        urllib2.urlopen(url)
        ret = True

    except urllib2.HTTPError, err:
        print err.code

    except urllib2.URLError, err:
        print err.args

    return ret
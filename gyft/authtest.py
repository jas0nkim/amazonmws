import sys, httplib, hashlib, time, urllib, json, urlparse

host = 'apitest.gyft.com'
apiKey = '225fef04-1aef-4181-94d2-e0c6d874f111'
apiSecret = '#n3t7nF!vMY9YC$'


timestamp = str(long(round(time.time())))
stringToSign = apiKey + apiSecret + timestamp
signature =  hashlib.sha256(stringToSign).hexdigest()

conn = httplib.HTTPSConnection(host)

##### get account information

# path = "/mashery/v1/reseller/account?api_key=%s&sig=%s" % (apiKey, signature)
# # path = "/mashery/v1/reseller/merchants?api_key=%s&sig=%s" % (apiKey, signature)
# conn.putrequest("GET", path)
# conn.putheader("x-sig-timestamp", timestamp)
# conn.endheaders()
# response = conn.getresponse()
# data = response.read()
# print data
# conn.close()


##### purchase a gift card (amazon.com)

# path = "/mashery/v1/partner/purchase/gift_card_direct"
path = "/mashery/v1/partner/purchase/gift_card_direct?api_key=%s&sig=%s" % (apiKey, signature)
params = urllib.urlencode({
    'shop_card_id': 4605,
    'to_email': 'jason.kim.jiho@gmail.com',
})
headers = {
    "x-sig-timestamp": timestamp,
}
conn.request("POST", path, params, headers)
response = conn.getresponse()
data = response.read()
print data
jsoned_data = json.loads(data)
print jsoned_data['url']
urlquerys = urlparse.parse_qs(urlparse.urlparse(jsoned_data['url']).fragment.lstrip('/?'))
print str(urlquerys)
token = None
if 'c' in urlquerys:
    token = urlquerys['c'][0]
if token:
    ##### retrieve claim code (amazon.com)
    path_claimcode = "/redemption/token/{}?reveal=true".format(token)
    conn = httplib.HTTPSConnection('services-test.gyft.com')
    conn.putrequest("GET", path_claimcode)
    conn.endheaders()
    response = conn.getresponse()
    data = response.read()
    print data
    jsoned_data = json.loads(data)
    print jsoned_data['cardDetails']['credentials']['card_number']['value']
    print jsoned_data['cardDetails']['credentials']['pin']['value']
conn.close()


# https://services-test.gyft.com/redemption/token/$NDY1NDI4MzhmODRhNDljYmIzNDRkYTQ4NzI5NTU4MDRkNmNlZWM0NzFiZDA0YzVhYmZhYjhkOGRmNWFlZDVkMDNE?reveal=true

##### url to redeem claim code (at amazon.com)
# https://www.amazon.com/gc/redeem?ref=asv_b_m_t_red


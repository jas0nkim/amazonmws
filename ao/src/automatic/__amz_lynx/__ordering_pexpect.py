import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', '..', '..'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

import time
import pexpect

from amazonmws import settings as amazonmws_settings, utils as amazonmws_utils
from amazonmws.loggers import GrayLogger as logger, StaticFieldFilter, get_logger_name

KEY_UP = '\x1b[A'
KEY_DOWN = '\x1b[B'
KEY_RIGHT = '\x1b[C'
KEY_LEFT = '\x1b[D'
KEY_ESCAPE = '\x1b'
KEY_BACKSPACE = '\x7f'


_input = {
    'asin': 'B003IG8RQW',
    'ebay_order_id': '2134135343453-23428347238',
    'amazon_user': 'redflagitems.0020@gmail.com',
    'amazon_pass': '12ReDF002AZIt!em!s',
    'billing_addr_zip': 'M5B0A5',
    'buyer_fullname': 'Floyd Braswell',
    'buyer_shipping_address1': '605 Westover Hills Blvd',
    'buyer_shipping_address2': 'Apt K',
    'buyer_shipping_city': 'Richmond',
    'buyer_shipping_state': 'VA',
    'buyer_shipping_postal': '23225-4573',
    'buyer_shipping_phone': '8043973629',
}


child = pexpect.spawn('elinks http://www.amazon.com/dp/' + _input['asin'])

# print child.readline()

# child.expect('Allow')
# print 'cookie Allow found'
# child.sendline('a') # allow cookies always
# print 'a key entered'
# child.sendline('') # enter Add to Cart button

print '** first screen **'

# child.expect('Add to Cart')
print 'search for Add to Cart button'
child.sendline('/Add to Cart')
# child.send('') # enter Add to Cart button
child.send(KEY_RIGHT) # enter Add to Cart button
child.send('') # confirm

print 'Add to Cart clicked'

print 'sleeping for 2 sec'
time.sleep(2)

print '** second screen **'

# print child.before
# print child.after


# print child.readline()

child.sendline('/Cart subtotal')
print child.readline()

# print child.read_nonblocking(size=100000, timeout=30)
# print child.readline()
# print child.readline()
# print child.readline()
# print child.readline()
# print child.readline()
# print child.readline()
# print child.readline()
# print child.readline()
# print child.readline()

print 'quiting'
child.send('q')
child.send('y')
child.close()
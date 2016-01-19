import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', '..', '..'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

import shlex, subprocess
import random

from amazonmws import settings as amazonmws_settings, utils as amazonmws_utils

asins = ['B003IG8RQW', 'B0008F6CBS', 'B00IE71910', 'B0017DA3W4', 'B000XAL0O2']
asin = random.choice(asins)

print asin

print_filename_1 = 'print_1.txt'
print_filename_2 = 'print_2.txt'

proxy = 'http://{}:{}'.format(amazonmws_settings.APP_HOST, amazonmws_settings.PRIVOXY_LISTENER_PORT)
command_line = 'export http_proxy=' + proxy + ' && lynx -cmd_script=lynx_ordering.log -accept_all_cookies http://www.amazon.com/dp/' + random.choice(asins)
args = shlex.split(command_line)

order_number = None
item_price = None
shipping_price = None
tax = None
total = None

try:
    if os.path.isfile(print_filename_1):
        os.remove(print_filename_1)

    if os.path.isfile(print_filename_2):
        os.remove(print_filename_2)

    subprocess.check_call(command_line, shell=True)
    # subprocess.check_call(command_line, shell=True)
    if os.path.isfile(print_filename_1):
        with open(print_filename_1, 'r') as f:
            lines = f.readlines()
            for line in lines:
                if 'Items:' in line and item_price == None:
                    print '****ITEM_PRICE**** ' + line.strip() + ' ****'
                    item_price = amazonmws_utils.str_to_float(line.strip())

                elif 'Shipping & handling:' in line and shipping_price == None:
                    print '****SHIPPING_PRICE**** ' + line.strip() + ' ****'
                    shipping_price = amazonmws_utils.str_to_float(line.strip())

                elif 'Estimated tax to be collected:' in line and tax == None:
                    print '****TAX**** ' + line.strip() + ' ****'
                    tax = amazonmws_utils.str_to_float(line.strip())

                elif 'Total:' in line and total == None:
                    print '****TOTAL**** ' + line.strip() + ' ****'
                    total = amazonmws_utils.str_to_float(line.strip())

                else:
                    continue

    if os.path.isfile(print_filename_2):
        with open(print_filename_2, 'r') as f:
            lines = f.readlines()
            for line in lines:
                if 'Order Number:' in line:
                    print '****ORDER_NUMBER**** ' + line.strip() + ' ****'
                    order_number = amazonmws_utils.extract_amz_order_num(line.strip())
                    break

                else:
                    continue

except subprocess.CalledProcessError as e:
    raise e

finally:
    # remove print files
    if os.path.isfile(print_filename_1):
        os.remove(print_filename_1)

    if os.path.isfile(print_filename_2):
        os.remove(print_filename_2)


print ''
print ''
print '****ORDER_NUMBER**** ' + str(order_number) + ' ****'
print '****ITEM_PRICE**** ' + str(item_price) + ' ****'
print '****SHIPPING_PRICE**** ' + str(shipping_price) + ' ****'
print '****TAX**** ' + str(tax) + ' ****'
print '****TOTAL**** ' + str(total) + ' ****'

#!/bin/bash

PATH=/virtualenvs/amazonmws/bin:/home/jason/.local/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local/games

source /home/jason/.profile
cd /applications/amazonmws/ao/bin
/virtualenvs/amazonmws/bin/python /applications/amazonmws/ao/bin/amazon_order_tracking.py
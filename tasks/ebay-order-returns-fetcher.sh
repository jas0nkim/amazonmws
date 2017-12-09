#!/bin/bash

PATH=/virtualenvs/amazonmws/bin:/home/jason/.local/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local/games

source /home/jason/.profile
cd /applications/amazonmws/atoe/tasks
/virtualenvs/amazonmws/bin/python /applications/amazonmws/atoe/tasks/ebay_order_returns_fetcher.py
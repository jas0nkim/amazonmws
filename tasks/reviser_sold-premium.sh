#!/bin/bash

PATH=/virtualenvs/amazonmws/bin:/home/jason/.local/bin:/home/jason/.local/bin:/home/jason/.local/bin:/home/jason/.local/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local/games

source /home/jason/.profile
cd /applications/amazonmws/scrapers/amzn/amzn/tasks
/virtualenvs/amazonmws/bin/python /applications/amazonmws/scrapers/amzn/amzn/tasks/run_reviser_sold.py -e 1
#!/bin/bash

PATH=/virtualenvs/amazonmws/bin:/home/jason/.local/bin:/home/jason/.local/bin:/home/jason/.local/bin:/home/jason/.local/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local/games

source /home/jason/.profile
cd /applications/amazonmws/scrapers/amzn/amzn/tasks
flock -n /applications/amazonmws/locks/reviser-e-1-p-1.lock /virtualenvs/amazonmws/bin/python /applications/amazonmws/scrapers/amzn/amzn/tasks/run_reviser.py -i -e 1 -p 1 > /var/log/cron/reviser-e-1-p-1-`date +\%Y\%m\%d\%H\%M\%S`.log 2>&1
flock -n /applications/amazonmws/locks/reviser-e-1-p-2.lock /virtualenvs/amazonmws/bin/python /applications/amazonmws/scrapers/amzn/amzn/tasks/run_reviser.py -i -e 1 -p 2 > /var/log/cron/reviser-e-1-p-2-`date +\%Y\%m\%d\%H\%M\%S`.log 2>&1
flock -n /applications/amazonmws/locks/reviser-e-1-p-3.lock /virtualenvs/amazonmws/bin/python /applications/amazonmws/scrapers/amzn/amzn/tasks/run_reviser.py -i -e 1 -p 3 > /var/log/cron/reviser-e-1-p-3-`date +\%Y\%m\%d\%H\%M\%S`.log 2>&1
flock -n /applications/amazonmws/locks/reviser-e-1-p-4.lock /virtualenvs/amazonmws/bin/python /applications/amazonmws/scrapers/amzn/amzn/tasks/run_reviser.py -i -e 1 -p 4 > /var/log/cron/reviser-e-1-p-4-`date +\%Y\%m\%d\%H\%M\%S`.log 2>&1
flock -n /applications/amazonmws/locks/reviser-e-1-p-5.lock /virtualenvs/amazonmws/bin/python /applications/amazonmws/scrapers/amzn/amzn/tasks/run_reviser.py -i -e 1 -p 5 > /var/log/cron/reviser-e-1-p-5-`date +\%Y\%m\%d\%H\%M\%S`.log 2>&1
flock -n /applications/amazonmws/locks/reviser-e-1-p-6.lock /virtualenvs/amazonmws/bin/python /applications/amazonmws/scrapers/amzn/amzn/tasks/run_reviser.py -i -e 1 -p 6 > /var/log/cron/reviser-e-1-p-6-`date +\%Y\%m\%d\%H\%M\%S`.log 2>&1
flock -n /applications/amazonmws/locks/reviser-e-1-p-7.lock /virtualenvs/amazonmws/bin/python /applications/amazonmws/scrapers/amzn/amzn/tasks/run_reviser.py -i -e 1 -p 7 > /var/log/cron/reviser-e-1-p-7-`date +\%Y\%m\%d\%H\%M\%S`.log 2>&1
flock -n /applications/amazonmws/locks/reviser-e-1-p-8.lock /virtualenvs/amazonmws/bin/python /applications/amazonmws/scrapers/amzn/amzn/tasks/run_reviser.py -i -e 1 -p 8 > /var/log/cron/reviser-e-1-p-8-`date +\%Y\%m\%d\%H\%M\%S`.log 2>&1
flock -n /applications/amazonmws/locks/reviser-e-1-p-9.lock /virtualenvs/amazonmws/bin/python /applications/amazonmws/scrapers/amzn/amzn/tasks/run_reviser.py -i -e 1 -p 9 > /var/log/cron/reviser-e-1-p-9-`date +\%Y\%m\%d\%H\%M\%S`.log 2>&1
flock -n /applications/amazonmws/locks/reviser-e-1-p-10.lock /virtualenvs/amazonmws/bin/python /applications/amazonmws/scrapers/amzn/amzn/tasks/run_reviser.py -i -e 1 -p 10 > /var/log/cron/reviser-e-1-p-10-`date +\%Y\%m\%d\%H\%M\%S`.log 2>&1

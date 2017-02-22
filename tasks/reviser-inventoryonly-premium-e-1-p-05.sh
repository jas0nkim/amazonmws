#!/bin/bash

PATH=/virtualenvs/amazonmws/bin:/home/jason/.local/bin:/home/jason/.local/bin:/home/jason/.local/bin:/home/jason/.local/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local/games

source /home/jason/.profile
cd /applications/amazonmws/scrapers/amzn/amzn/tasks
flock -n /applications/amazonmws/locks/reviser-e-1-p-05.lock -c '/virtualenvs/amazonmws/bin/python /applications/amazonmws/scrapers/amzn/amzn/tasks/run_reviser.py -i -e 1 -p 5 > /var/log/cron/reviser-e-1-p-05-`date +\%Y\%m\%d\%H\%M\%S`.log 2>&1'
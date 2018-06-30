#!/bin/bash

PATH=/virtualenvs/amazonmws/bin:/home/jason/.local/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local/games

source /home/jason/.profile
cd /applications/amazonmws/scrapers/amzn/amzn/tasks
flock -n /applications/amazonmws/locks/reviser-e-8-p-01.lock -c '/virtualenvs/amazonmws/bin/python /applications/amazonmws/scrapers/amzn/amzn/tasks/run_reviser.py -i -e 8 -p 1 > /var/log/cron/reviser-e-8-p-01-`date +\%Y\%m\%d\%H\%M\%S`.log 2>&1'

flock -n /applications/amazonmws/locks/reviser-e-8-p-02.lock -c '/virtualenvs/amazonmws/bin/python /applications/amazonmws/scrapers/amzn/amzn/tasks/run_reviser.py -i -e 8 -p 2 > /var/log/cron/reviser-e-8-p-02-`date +\%Y\%m\%d\%H\%M\%S`.log 2>&1'

flock -n /applications/amazonmws/locks/reviser-e-8-p-03.lock -c '/virtualenvs/amazonmws/bin/python /applications/amazonmws/scrapers/amzn/amzn/tasks/run_reviser.py -i -e 8 -p 3 > /var/log/cron/reviser-e-8-p-03-`date +\%Y\%m\%d\%H\%M\%S`.log 2>&1'

flock -n /applications/amazonmws/locks/reviser-e-8-p-04.lock -c '/virtualenvs/amazonmws/bin/python /applications/amazonmws/scrapers/amzn/amzn/tasks/run_reviser.py -i -e 8 -p 4 > /var/log/cron/reviser-e-8-p-04-`date +\%Y\%m\%d\%H\%M\%S`.log 2>&1'

flock -n /applications/amazonmws/locks/reviser-e-8-p-05.lock -c '/virtualenvs/amazonmws/bin/python /applications/amazonmws/scrapers/amzn/amzn/tasks/run_reviser.py -i -e 8 -p 5 > /var/log/cron/reviser-e-8-p-05-`date +\%Y\%m\%d\%H\%M\%S`.log 2>&1'

flock -n /applications/amazonmws/locks/reviser-e-8-p-06.lock -c '/virtualenvs/amazonmws/bin/python /applications/amazonmws/scrapers/amzn/amzn/tasks/run_reviser.py -i -e 8 -p 6 > /var/log/cron/reviser-e-8-p-06-`date +\%Y\%m\%d\%H\%M\%S`.log 2>&1'

flock -n /applications/amazonmws/locks/reviser-e-8-p-07.lock -c '/virtualenvs/amazonmws/bin/python /applications/amazonmws/scrapers/amzn/amzn/tasks/run_reviser.py -i -e 8 -p 7 > /var/log/cron/reviser-e-8-p-07-`date +\%Y\%m\%d\%H\%M\%S`.log 2>&1'

flock -n /applications/amazonmws/locks/reviser-e-8-p-08.lock -c '/virtualenvs/amazonmws/bin/python /applications/amazonmws/scrapers/amzn/amzn/tasks/run_reviser.py -i -e 8 -p 8 > /var/log/cron/reviser-e-8-p-08-`date +\%Y\%m\%d\%H\%M\%S`.log 2>&1'

flock -n /applications/amazonmws/locks/reviser-e-8-p-09.lock -c '/virtualenvs/amazonmws/bin/python /applications/amazonmws/scrapers/amzn/amzn/tasks/run_reviser.py -i -e 8 -p 9 > /var/log/cron/reviser-e-8-p-09-`date +\%Y\%m\%d\%H\%M\%S`.log 2>&1'

flock -n /applications/amazonmws/locks/reviser-e-8-p-10.lock -c '/virtualenvs/amazonmws/bin/python /applications/amazonmws/scrapers/amzn/amzn/tasks/run_reviser.py -i -e 8 -p 10 > /var/log/cron/reviser-e-8-p-10-`date +\%Y\%m\%d\%H\%M\%S`.log 2>&1'

flock -n /applications/amazonmws/locks/reviser-e-8-p-11.lock -c '/virtualenvs/amazonmws/bin/python /applications/amazonmws/scrapers/amzn/amzn/tasks/run_reviser.py -i -e 8 -p 11 > /var/log/cron/reviser-e-8-p-11-`date +\%Y\%m\%d\%H\%M\%S`.log 2>&1'

flock -n /applications/amazonmws/locks/reviser-e-8-p-12.lock -c '/virtualenvs/amazonmws/bin/python /applications/amazonmws/scrapers/amzn/amzn/tasks/run_reviser.py -i -e 8 -p 12 > /var/log/cron/reviser-e-8-p-12-`date +\%Y\%m\%d\%H\%M\%S`.log 2>&1'

flock -n /applications/amazonmws/locks/reviser-e-8-p-13.lock -c '/virtualenvs/amazonmws/bin/python /applications/amazonmws/scrapers/amzn/amzn/tasks/run_reviser.py -i -e 8 -p 13 > /var/log/cron/reviser-e-8-p-13-`date +\%Y\%m\%d\%H\%M\%S`.log 2>&1'

flock -n /applications/amazonmws/locks/reviser-e-8-p-14.lock -c '/virtualenvs/amazonmws/bin/python /applications/amazonmws/scrapers/amzn/amzn/tasks/run_reviser.py -i -e 8 -p 14 > /var/log/cron/reviser-e-8-p-14-`date +\%Y\%m\%d\%H\%M\%S`.log 2>&1'

flock -n /applications/amazonmws/locks/reviser-e-8-p-15.lock -c '/virtualenvs/amazonmws/bin/python /applications/amazonmws/scrapers/amzn/amzn/tasks/run_reviser.py -i -e 8 -p 15 > /var/log/cron/reviser-e-8-p-15-`date +\%Y\%m\%d\%H\%M\%S`.log 2>&1'

flock -n /applications/amazonmws/locks/reviser-e-8-p-16.lock -c '/virtualenvs/amazonmws/bin/python /applications/amazonmws/scrapers/amzn/amzn/tasks/run_reviser.py -i -e 8 -p 16 > /var/log/cron/reviser-e-8-p-16-`date +\%Y\%m\%d\%H\%M\%S`.log 2>&1'

flock -n /applications/amazonmws/locks/reviser-e-8-p-17.lock -c '/virtualenvs/amazonmws/bin/python /applications/amazonmws/scrapers/amzn/amzn/tasks/run_reviser.py -i -e 8 -p 17 > /var/log/cron/reviser-e-8-p-17-`date +\%Y\%m\%d\%H\%M\%S`.log 2>&1'

flock -n /applications/amazonmws/locks/reviser-e-8-p-18.lock -c '/virtualenvs/amazonmws/bin/python /applications/amazonmws/scrapers/amzn/amzn/tasks/run_reviser.py -i -e 8 -p 18 > /var/log/cron/reviser-e-8-p-18-`date +\%Y\%m\%d\%H\%M\%S`.log 2>&1'

flock -n /applications/amazonmws/locks/reviser-e-8-p-19.lock -c '/virtualenvs/amazonmws/bin/python /applications/amazonmws/scrapers/amzn/amzn/tasks/run_reviser.py -i -e 8 -p 19 > /var/log/cron/reviser-e-8-p-19-`date +\%Y\%m\%d\%H\%M\%S`.log 2>&1'

flock -n /applications/amazonmws/locks/reviser-e-8-p-20.lock -c '/virtualenvs/amazonmws/bin/python /applications/amazonmws/scrapers/amzn/amzn/tasks/run_reviser.py -i -e 8 -p 20 > /var/log/cron/reviser-e-8-p-20-`date +\%Y\%m\%d\%H\%M\%S`.log 2>&1'

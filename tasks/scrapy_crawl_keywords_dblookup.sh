#!/bin/bash

source /home/jason/.profile
cd /applications/amazonmws
PATH=$PATH:/usr/local/bin
export PATH
scrapy crawl keywords_dblookup
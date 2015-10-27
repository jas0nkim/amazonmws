#!/bin/bash

cd /applications/amazonmws
PATH=$PATH:/usr/local/bin
export PATH
scrapy crawl keywords_dblookup
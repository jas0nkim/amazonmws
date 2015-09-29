#!/bin/bash
mysql -u atewriteuser -p -e "CREATE DATABASE `amazonmws` CHARACTER SET utf8 COLLATE utf8_general_ci;"

SQLFILES=./db_updates/*.sql | sort -n

for f in SQLFILES
do
	echo "Proceessing $f file..."
	cat $f

	mysql -u atewriteuser -p amazonmws < $f
done

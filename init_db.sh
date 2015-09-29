#!/bin/bash
stty -echo
printf "database password? "
read INPUT_PASS
stty echo
printf "\n"

mysql -u atewriteuser -p$INPUT_PASS -e "CREATE DATABASE amazonmws CHARACTER SET utf8 COLLATE utf8_general_ci;"

SQLFILES=./db_updates/*.sql

for f in $SQLFILES
do
	echo "Proceessing $f file..."
	cat $f

	mysql -u atewriteuser -p$INPUT_PASS amazonmws < $f
done

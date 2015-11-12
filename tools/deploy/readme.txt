- USE blueprint - https://github.com/devstructure/blueprint - for reverse-engineering server package installing and configurations

- database dump
	mysqldump --databases amazonmws --single-transaction --add-drop-database --triggers --routines --events --user=atewriteuser --password > tools/db_dump/xxxxxxxx-amazonmws.sql

- database restore
	mysql -u amazonmws -p < tools/db_dump/xxxxxxxx-amazonmws.sql

- dump data only
	mysqldump -u atewriteuser -p --no-create-info amazonmws a b c d > tools/db_dump/xxxxxxxx-xxxx.sql

- dump structure only
	mysqldump -u atewriteuser -p --no-data amazonmws a b c d > tools/db_dump/xxxxxxxx-xxxx.sql
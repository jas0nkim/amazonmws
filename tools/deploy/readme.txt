- USE blueprint - https://github.com/devstructure/blueprint - for reverse-engineering server package installing and configurations

- database dump
	mysqldump --databases amazonmws --single-transaction --add-drop-database --triggers --routines --events --user=atewriteuser --password > tools/db_dump/xxxxxxxx-amazonmws.sql

- database restore
	mysql -u amazonmws -p < tools/db_dump/xxxxxxxx-amazonmws.sql
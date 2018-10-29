#!/bin/sh
now="$(date +\%Y\%m\%d\%H\%M\%S)"
filename="$now-amazonmws-db_backup".gz
structureonlyfilename="$now-amazonmws-db_backup-structureonly".sql
backupfolder="/applications/db_backups/amazonmws"
fullpathbackupfile="$backupfolder/$filename"
fullpathbackupfilestructureonly="$backupfolder/$structureonlyfilename"
logfile="$backupfolder/"backup_log_"$(date +'%Y_%m')".txt
echo "mysqldump started at $(date +'%d-%m-%Y %H:%M:%S')" >> "$logfile"
mysqldump --complete-insert -h 172.104.23.33 -u atewriteuser -p20itSiT15 --default-character-set=utf8 --ignore-table=amazonmws.amazon_scrape_tasks --ignore-table=amazonmws.amazon_scrape_errors --ignore-table=amazonmws.ebay_trading_api_errors amazonmws | gzip > "$fullpathbackupfile"
mysqldump --no-data -h 172.104.23.33 -u atewriteuser -p20itSiT15 --default-character-set=utf8 --replace --skip-add-drop-table amazonmws > "$fullpathbackupfilestructureonly"
sed -i 's/CREATE TABLE/CREATE TABLE IF NOT EXISTS/g' "$fullpathbackupfilestructureonly"
echo "mysqldump finished at $(date +'%d-%m-%Y %H:%M:%S')" >> "$logfile"
chown jason "$fullpathbackupfile"
chown jason "$logfile"
echo "file permission changed" >> "$logfile"
find "$backupfolder" -name *-amazonmws-db_backup.gz -mtime +15 -exec rm {} \;
echo "old files deleted" >> "$logfile"
echo "operation finished at $(date +'%d-%m-%Y %H:%M:%S')" >> "$logfile"
echo "*****************" >> "$logfile"
exit 0

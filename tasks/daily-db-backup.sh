#!/bin/sh
now="$(date +\%Y\%m\%d\%H\%M\%S)"
filename="$now-amazonmws-db_backup".gz
backupfolder="/applications/db_backups/amazonmws"
fullpathbackupfile="$backupfolder/$filename"
logfile="$backupfolder/"backup_log_"$(date +'%Y_%m')".txt
echo "mysqldump started at $(date +'%d-%m-%Y %H:%M:%S')" >> "$logfile"
mysqldump --complete-insert -h 45.79.178.128 -u atewriteuser -p20itSiT15 --default-character-set=utf8 amazonmws | gzip > "$fullpathbackupfile"
echo "mysqldump finished at $(date +'%d-%m-%Y %H:%M:%S')" >> "$logfile"
chown jason "$fullpathbackupfile"
chown jason "$logfile"
echo "file permission changed" >> "$logfile"
find "$backupfolder" -name *-amazonmws-db_backup.gz -mtime +10 -exec rm {} \;
echo "old files deleted" >> "$logfile"
echo "operation finished at $(date +'%d-%m-%Y %H:%M:%S')" >> "$logfile"
echo "*****************" >> "$logfile"
exit 0

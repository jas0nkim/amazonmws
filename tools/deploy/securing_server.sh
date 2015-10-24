#!/bin/bash
stty -echo
printf "jason's password? "
read USERPASS
stty echo
printf "\n"

USERNAME="jason"
USERPUBKEY="$(cat <<EOF
ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQD44vH48/cQuGNkp9tp9C0GYsFu43qNeu0J7tKRafbyQEV0DSLy0AeCgwaVov9Mq9WPPPMFP+TCxQ+llvougGrXF635uuOvknUjylhsfCwe1SNrfnIZe3CU5C/CuMyAAXrj4UowQNu2mEWZKhOVLQvBG9zIdOgjJF2tuD/uj3OJqoly8WylGwvGmMBVX1lQ8n9KOsTw3sbzlaHwl57P4HpOmLs/Z8Gr7+eT4byChmWnoOmpHp2MK0WT4T1Y/3Pg2/dD0+bsXV/wBTkCBTHaGDUt3MeVPmZsQrGVwJzV8z6TZLFDMNa9M7eT2BmoJOW7bBHKqr+zSuxMbRJb4kUvsJB/ jason.kim.jiho@gmail.com
EOF
)"

my_dir="$PWD"
. "$my_dir/utils.sh"

logfile="/root/log.txt"
export logfile

#
# 1. update system
# 
system_update
echo "System updated" >> $logfile

#
# 2. add new sudo user
# 
user_add_sudo $USERNAME $USERPASS
echo "New sudo user - $USERNAME - added" >> $logfile

#
# 3. add user publickey
# 
user_add_pubkey $USERNAME "$USERPUBKEY"
echo "Pubkey added for user - $USERNAME" >> $logfile

#
# 4. root ssh disable
# 
ssh_disable_root
echo "SSH disabled for root" >> $logfile

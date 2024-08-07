#!/bin/bash

clear
echo -e "\n\033[1m\033[4m\033[33mSyncing project to server...\033[0m"

# Sync and replace existing files with rsync and ssh as root

# main.py
echo -e "\033[33mSyncing main.py...\033[0m"
rsync -azP --no-o --no-g --no-p main.py root@192.168.1.32:/var/www/webApp/webApp > /dev/null

# website folder
echo -e "\033[33mSyncing website folder...\033[0m"
rsync -azP --no-o --no-g --no-p website root@192.168.1.32:/var/www/webApp/webApp > /dev/null

# restart apache2 server
echo -e "\033[1m\033[32mRestarting apache2 server...\033[0m"
ssh root@192.168.1.32 'systemctl restart apache2' > /dev/null
echo -e "\033[1m\033[32mDone!\033[0m"


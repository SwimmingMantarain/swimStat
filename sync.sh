#!/bin/bash
# This script will sync this project to my server which is running on
# 192.168.1.32 and the directory for it is /var/www/webApp/webApp

# Sync and replace existing files with rsync and ssh as root

# main.py
rsync -avzP --progress main.py root@192.168.1.32:/var/www/webApp/webApp

# website folder
rsync -avzP --progress website root@192.168.1.32:/var/www/webApp/webApp

# restart apache2 server
ssh root@192.168.1.32 'systemctl restart apache2'

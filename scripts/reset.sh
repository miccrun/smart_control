#!/bin/bash

mysql -u root --password="root_password" -e "drop database db;"
mysql -u root --password="root_password" -e "create database db;"
echo "no" | python /var/www/smartcontrol/manage.py syncdb
echo "import scripts.init_db" | python /var/www/smartcontrol/manage.py shell
echo "\n"

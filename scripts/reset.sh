#!/bin/bash

mysql -u root --password="root_password" -e "drop database db;"
mysql -u root --password="root_password" -e "create database db;"
echo "no" | python ~/code/manage.py syncdb
echo "import scripts.init_db" | python ~/code/manage.py shell
echo "\n"

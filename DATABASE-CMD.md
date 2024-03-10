## MySQL setup


Install mysql server in codespace 
> mysql doesnot have default password, leave it blank if you **RE-PROMPTED** in for first entry. Be sure to change it
```bash
sudo apt-get update
sudo apt-get install mysql-server
sudo service mysql start 
sudo mysql -u root -p
```
Possible error: `ERROR 2002 (HY000): Can't connect to local MySQL server through socket '/var/run/mysqld/mysqld.sock' (13)`. Follow below steps. If it doesnot work remove(for first time user only. Data will be lost if you do be sure to backup if you already have database): `sudo apt-get remove --purge mysql` and install mysql-server
```bash
@realsanjeev ➜ /workspaces/Scrapy (main) $ sudo service mysql start 
 * Starting MySQL database server mysqld                                                                                                              [ OK ] 
@realsanjeev ➜ /workspaces/Scrapy (main) $ mysql
ERROR 2002 (HY000): Can't connect to local MySQL server through socket '/var/run/mysqld/mysqld.sock' (13)
@realsanjeev ➜ /workspaces/Scrapy (main) $ sudo mysql -u root -p
Enter password: 
Welcome to the MySQL monitor.  Commands end with ; or \g.
Your MySQL connection id is 11
Server version: 8.0.33-0ubuntu0.20.04.4 (Ubuntu)

Copyright (c) 2000, 2023, Oracle and/or its affiliates.

Oracle is a registered trademark of Oracle Corporation and/or its
affiliates. Other names may be trademarks of their respective
owners.

Type 'help;' or '\h' for help. Type '\c' to clear the current input statement.

mysql> 
```
## SQL command

```sql
- display all database present
mysql> show databases;
- create database <database-name>
mysql> create database bookdb
- enter to <database>
mysql> use bookdb;
```

## To view port number used in process
```bash
$ netstat -tupln
```

```bash
mysql > SHOW GLOBAL VARIABLES LIKE 'PORT';
```

To fix issue: **raise get_mysql_exception(
mysql.connector.errors.ProgrammingError: 1698 (28000): Access denied for user 'root'@'localhost'**

In `mysql`
```bash
use mysql;
update user set authentication_string=PASSWORD("") where user = "root";
update user set plugin="mysql_native_password" where user = "root";
flush privileges;
```
Replace 2nd command with `UPDATE user SET authentication_string = "" WHERE user = "root";`

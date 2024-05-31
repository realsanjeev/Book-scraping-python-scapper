## MySQL Setup

### Installing MySQL Server

To install MySQL server in Codespaces:

> **Note:** MySQL does not have a default password. If you are prompted for a password during the initial setup, leave it blank. Be sure to set a password afterward for security.

1. Update package lists and install MySQL server:
    ```bash
    sudo apt-get update
    sudo apt-get install mysql-server
    ```
2. Start the MySQL service:
    ```bash
    sudo service mysql start
    ```
3. Log in to MySQL as the root user:
    ```bash
    sudo mysql -u root -p
    ```

### Troubleshooting

If you encounter the error `ERROR 2002 (HY000): Can't connect to local MySQL server through socket '/var/run/mysqld/mysqld.sock' (13)`, follow these steps:

1. Start the MySQL service again:
    ```bash
    sudo service mysql start
    ```
2. If the problem persists, consider removing and reinstalling MySQL server (note: this will delete all existing databases, so back up your data if necessary):
    ```bash
    sudo apt-get remove --purge mysql-server
    sudo apt-get install mysql-server
    ```

### Example Session

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

### Basic SQL Commands

To interact with the MySQL server, use the following commands(Here we create two databases of `bookdb` and `quotesdb`):

```sql
-- Display all databases present
SHOW DATABASES;

-- Create a new database
CREATE DATABASE bookdb;
CREATE DATABASE quotesdb

-- Select the database to use
USE bookdb;
```

### Changing the Root User Password

If you encounter the error `mysql.connector.errors.ProgrammingError: 1698 (28000): Access denied for user 'root'@'localhost'`, change the root user password:

1. Log in to MySQL:
    ```bash
    sudo mysql -u root -p
    ```
2. Execute the following commands:
    ```sql
    USE mysql;
    UPDATE user SET authentication_string=PASSWORD('new_password') WHERE user='root';
    UPDATE user SET plugin='mysql_native_password' WHERE user='root';
    FLUSH PRIVILEGES;
    ```

   Replace `new_password` with your desired password.

### Viewing the Port Number

To check the port number used by MySQL:

1. Use `netstat` to view network statistics:
    ```bash
    netstat -tupln
    ```

2. In MySQL, run:
    ```sql
    SHOW GLOBAL VARIABLES LIKE 'PORT';
    ```

This README provides the necessary steps to set up and troubleshoot MySQL on Codespaces. For more detailed information, consult the MySQL documentation.
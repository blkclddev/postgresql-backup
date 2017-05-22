#PostgreSQL Backup

##Requirements
* See requirements.txt for more details

##Description
This script will backup a PostgreSQL database. It currently only supports the pg_dumpall command for full backups.

##Usage
~~~~
usage: postgresql-backup.py [-h] --dbhost DBHOST --dbun DBUN --dbpass DBPASS
                            [--local LOCAL] [--remote REMOTE]

Backup a PostgreSQL database

Note: The following arguments are required: --dbhost, --dbun, --dbpass

optional arguments:
  -h, --help       show this help message and exit
  --dbhost DBHOST  Set the database hostname or IP address
  --dbun DBUN      Set the username for connecting to the database
  --dbpass DBPASS  Set the password for connecting to the database
  --local LOCAL    Set the local location of the backup file. EX:
                   /path/to/folder
  --remote REMOTE  Set the remote location of the backup file. EX: gce or s3

~~~~
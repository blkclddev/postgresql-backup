#PostgreSQL Backup

##Requirements
* See requirements.txt for more details

##Description
This script will backup a PostgreSQL database. It currently only supports the pg_dumpall command for full backups. There are built in provisions to encrypt the backup and upload the encrypted file to GCE or S3 storage.

##Usage
~~~~
usage: postgresql-backup.py [-h] [--action {backup,decrypt}] [--key KEY]
                            [--dbhost DBHOST] [--dbun DBUN] [--dbpass DBPASS]
                            [--local LOCAL] [--remote {gce,s3}]
                            [--project PROJECT] [--bucket BUCKET]

Backup a PostgreSQL database

optional arguments:
  -h, --help            show this help message and exit
  --action {backup,decrypt}
                        Action to take
  --key KEY             Key used for encrypting the backup files
  --dbhost DBHOST       Used for backups. Set the database hostname or IP
                        address
  --dbun DBUN           Used for backups. Set the username for connecting to
                        the database
  --dbpass DBPASS       Used for backups. Set the password for connecting to
                        the database
  --local LOCAL         Set the local location of the backup file. EX:
                        /path/to/folder
  --remote {gce,s3}     Used for backups. Set the remote location of the
                        backup fileValid options are gce or s3
  --project PROJECT     Used for backups. GCE project name
  --bucket BUCKET       Used for backups. Cloud storage bucket name
~~~~
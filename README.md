#PostgreSQL Backup

##Requirements
* See requirements.txt for more details

##Description
This script will backup a PostgreSQL database. It currently only supports the pg_dumpall command for full backups. There are built in provisions to upload the backup to GCE or S3 storage.

##A Note About Encryption
Previous versions of this script included code to encrypt the backup on the client side before upload to the cloud. This was an experiment and the code should not be considered secure. My stance is that I put more trust in use the GCE or AWS server side encryption. If you have a need for client side encryptio, feel free to roll your own but the previous encryption code in this repo should not be considered secure.

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
import os
import sys
import time
import argparse
import subprocess
import gcestorage
import credentials


################################################################################
# Pseudocode
################################################################################
# Handle GCE errors
# Transfer file to S3
################################################################################
# Main function
def main():
    # Check if the script is running as standalone
    if __name__ == "__main__":
        # Setup argument parser
        parser = argparse.ArgumentParser(description='Backup a PostgreSQL database')
        parser.add_argument('--dbhost', action='store', required=True,
                            help='Used for backups. Set the database hostname or IP address')
        parser.add_argument('--local', action='store',
                            help='Set the local location of the backup file. EX: /path/to/folder')
        parser.add_argument('--remote', action='store', choices=['gce', 's3'],
                            help='Used for backups. Set the remote location of the backup fileValid options are gce or s3')
        parser.add_argument('--project', action='store', help='Used for backups. GCE project name')
        parser.add_argument('--bucket', action='store', help='Used for backups. Cloud storage bucket name')
        args = parser.parse_args()

        # Check if no arguments are passed
        if len(sys.argv) == 1:
            parser.print_help()
            parser.exit()

        # Set database variables
        db_host = args.dbhost
        db_username = str(credentials.psql_username)
        db_password = str(credentials.psql_password)

        # Check if GOOGLE_APPLICATION_CREDENTIALS environment variable is set
        if 'GOOGLE_APPLICATION_CREDENTIALS' in os.environ:
            print("[*] WARNING: GOOGLE_APPLICATION_CREDENTIALS environment variable already set!")
        else:
            os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = str(credentials.gce_keyfile)

        # Set the local backup file destination
        if not args.local:
            # If the --local argument is empty, set the backup destination to the current directory
            local_dest = str(os.getcwd())
            print("[+] Setting local backup destination to: " + local_dest)
        else:
            # Otherwise use the provided directory as the destination
            local_dest = str(args.local)
            print("[+] Setting local backup destination to: " + local_dest)

        # Create the backup file name & full path
        backup_filename = str(
            "{host}_full_backup_{date}_{time}.psql".format(host=db_host, date=time.strftime("%d%m%Y"),
                                                           time=time.strftime("%H%M%S")))
        backup_full_path = local_dest + "/" + backup_filename
        print("[+] Setting full path to: " + backup_full_path)

        # Run database backup
        print("[+] Running database backup")
        psql_full_dump(db_host, db_username, db_password, backup_full_path)

        # Check if GCE was set as the remote backup destination
        if args.remote == "gce":
            # Upload encrypted file to GCE bucket
            print("[+] Uploading backup to GCE storage")
            gcestorage.upload_to_bucket(args.project, args.bucket, backup_full_path,
                                        backup_filename)
        elif args.remote == "s3":
            # Upload encrypted file to S3 bucket
            print("[-] WARNING: S3 storage is not currently supported")
        else:
            # Invalid remote string provided
            print("[-] Invalid --remote option! Skipping cloud upload")

        # Remove local backup file
        print("[+] Deleting local backup file: " + backup_full_path)
        os.remove(backup_full_path)


# Function for rull PostgreSQL backup
def psql_full_dump(dbhost, dbun, dbpass, destination):
    # Set PGPASSWORD environment variable so that pg_dumpall does not prompt for a password
    os.environ["PGPASSWORD"] = dbpass

    # Run the backup
    backup_contents = subprocess.getoutput('pg_dumpall -h ' + dbhost + ' -U ' + dbun)

    # Save output to the file
    backup_file = open(destination, 'w')

    for line in backup_contents:
        backup_file.write(line)

    backup_file.close()


# Run the main function
main()

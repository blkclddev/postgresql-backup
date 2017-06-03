import os
import sys
import time
import datetime
import argparse
import subprocess
import encryption
import gcestorage

################################################################################
# Pseudocode
################################################################################
# XSetup arguments: Host, user, pass, GCE, S3
# XSet variables: db_host, db_user, db_password, backup location
# XCreate backup file name: [db_host]_full_backup_datetime
# XRun backup with pdumpall command [Pass username, password & host]
# XStore output in a variable
# Check if there was and error when running the backup
# XWrite output to a file
# XCompress & encrypt the file
# XTransfer file to GCE
# Handle GCE errors
# Transfer file to S3
################################################################################
# Main function
def main():
	# Check if the script is running as standalone
	if __name__ == "__main__":
		# Setup argument parser
		parser = argparse.ArgumentParser(description='Backup a PostgreSQL database')
		parser.add_argument('--action', action='store', required=False, choices=['backup', 'decrypt'], help='Action to take')
		parser.add_argument('--key', action='store', required=False, help='Key used for encrypting the backup files')
		parser.add_argument('--dbhost', action='store', required=False, help='Used for backups. Set the database hostname or IP address')
		parser.add_argument('--dbun', action='store', required=False, help='Used for backups. Set the username for connecting to the database')
		parser.add_argument('--dbpass', action='store', required=False, help='Used for backups. Set the password for connecting to the database')
		parser.add_argument('--local', action='store', help='Set the local location of the backup file. EX: /path/to/folder')
		parser.add_argument('--remote', action='store', choices=['gce', 's3'], help='Used for backups. Set the remote location of the backup fileValid options are gce or s3')
		parser.add_argument('--project', action='store', help='Used for backups. GCE project name')
		parser.add_argument('--bucket', action='store', help='Used for backups. Cloud storage bucket name')
		args = parser.parse_args()

		# Check if no arguments are passed
		if len(sys.argv) == 1:
			parser.print_help()
			parser.exit()

		# Set database variables
		db_host = args.dbhost
		db_username = args.dbun
		db_password = args.dbpass

		# Set the local backup file destination
		if args.local == "":
			# If the --local argument is empty, set the backup destination to the current directory
			local_backup_dest = str(args.local)
			print("[+] Setting local backup destination to: " + local_backup_dest)
		else:
			# Otherwise use the provided directory as the destination
			local_backup_dest = str(os.getcwd())
			print("[+] Setting local backup destination to: " + local_backup_dest)

		# Create the backup file name & full path
		backup_filename = str("{host}_full_backup_{date}_{time}.psql".format(host=db_host, date=time.strftime("%d%m%Y"), time=time.strftime("%H%M%S")))
		backup_full_path = local_backup_dest + "/" + backup_filename
		print("[+] Setting full path to: " + backup_full_path)

		# Create the encrypted backup file name & full path
		encrypted_backup_file_name = "ENCRYPTED_" + backup_filename
		encrypted_backup_full_path = local_backup_dest + "/" + encrypted_backup_file_name
		
		# Run database backup
		psql_full_dump(db_host, db_username, db_password, backup_full_path)

		# Encrypt file
		print("[+] Encrypting backup file")
		encryption.encrypt_file(args.key, backup_filename)

		# Delete Plain text file
		print("[+] Deleting the plain text file " + backup_full_path)
		os.remove(backup_full_path)

		# Check if GCE was set as the remote backup destination
		if args.remote == "gce":
			# Upload encrypted file to GCE bucket
			print("[+] Uploading encrypted file to GCE storage")
			gcestorage.upload_to_bucket(args.project, args.bucket, encrypted_backup_full_path, encrypted_backup_file_name)
		elif args.remote == "s3":
			# Upload encrypted file to S3 bucket
			print("[+] Uploading encrypted file to AWS S3 storage")
		else:
			# Invalid remote string provided
			print("[-] Invalid --remote option! Skipping cloud upload")

		# Download encrypted file from GCE bucket
		#print("[+] Downloading encrypted file from GCE storage")
		#gcestorage.download_from_bucket(gce_storage_project, gce_storage_bucket, backup_filename, backup_filename)

		# Decrypt files
		#print("[+] Decrypting backup file")
		#encryption.decrypt_file(encryption_key, "ENCRYPTED_127.0.0.1_full_backup_24052017_181215.psql")

# Function for rull PostgreSQL backup
def psql_full_dump(dbhost, dbun, dbpass, destination):
	# Set PGPASSWORD environment variable so that pg_dumpall does not prompt for a password
	os.environ["PGPASSWORD"] = dbpass
	
	#Run the backup
	backup_contents = subprocess.getoutput('pg_dumpall -h ' + dbhost + ' -U ' + dbun)

	# Save output to the file
	backup_file = open(destination, 'w')
	
	for line in backup_contents:
		backup_file.write(line)

	backup_file.close()

# Run the main function
main()
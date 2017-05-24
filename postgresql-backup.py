import os
import sys
import time
import datetime
import argparse
import subprocess
import encryption

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
# Compress & encrypt the file
# Transfer file to GCE
# Transfer file to S3
################################################################################
# Main function
def main():
	# Check if the script is running as standalone
	if __name__ == "__main__":
		# Setup argument parser
		parser = argparse.ArgumentParser(description='Backup a PostgreSQL database')
		parser.add_argument('--dbhost', action='store', required=True, help='Set the database hostname or IP address')
		parser.add_argument('--dbun', action='store', required=True, help='Set the username for connecting to the database')
		parser.add_argument('--dbpass', action='store', required=True, help='Set the password for connecting to the database')
		parser.add_argument('--local', action='store', help='Set the local location of the backup file. EX: /path/to/folder')
		parser.add_argument('--remote', action='store', help='Set the remote location of the backup file. EX: gce or s3')
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
			local_backup_dest = str(args.local)
			print("[+] Setting local backup destination to: " + local_backup_dest)
		else:
			local_backup_dest = str(os.getcwd())
			print("[+] Setting local backup destination to: " + local_backup_dest)

		# Create the backup file name & full path
		backup_filename = str("{host}_full_backup_{date}_{time}.psql".format(host=db_host, date=time.strftime("%d%m%Y"), time=time.strftime("%H%M%S")))
		backup_full_path = local_backup_dest + "/" + backup_filename
		print("[+] Setting full path to: " + backup_full_path)
		
		# Run database backup
		psql_full_dump(db_host, db_username, db_password, backup_full_path)

		# Set key/password for encryption
		encryption_key = "password"

		# Encrypt file
		print("[+] Encrypting backup file")
		encryption.encrypt_file(encryption_key, backup_filename)

		# Decrypt files
		print("[+] Decrypting backup file")
		encryption.decrypt_file(encryption_key, "ENCRYPTED_127.0.0.1_full_backup_24052017_181215.psql")

# Function for rull PostgreSQL backup
def psql_full_dump(dbhost, dbun, dbpass, destination):
	# Set PGPASSWORD environment variable so that pg_dumpall does not prompt for a password
	os.environ["PGPASSWORD"] = dbpass
	
	#Run the backup
	#backup_process = subprocess.Popen(['pg_dumpall', '-h', dbhost, '-U', dbun], stdout=subprocess.PIPE)
	backup_contents = subprocess.getoutput('pg_dumpall -h ' + dbhost + ' -U ' + dbun)

	# Save output to the file
	backup_file = open(destination, 'w')
	
	for line in backup_contents:
		backup_file.write(line)

	backup_file.close()

# Run the main function
main()
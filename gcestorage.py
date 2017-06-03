from google.cloud import storage
from google.cloud import client

########################################################################################################################
#
# Google Documentation - https://googlecloudplatform.github.io/google-cloud-python/stable/storage-client.html
#
# By default the GCE tools will look for the GOOGLE_APPLICATION_CREDENTIALS environment variable for authentication
#
########################################################################################################################

# Function to upload a file to a storage bucket
def upload_to_bucket(project, bucket, local_file, remote_file):
	# Establish storage client
	storage_client = storage.Client(project)

	# Select bucket
	gce_storage_bucket = storage_client.get_bucket(bucket)

	# Establish BLOB with destination file name
	blob = gce_storage_bucket.blob(remote_file)

	# Upload data from local file
	try:
		blob.upload_from_filename(filename=local_file)
	except google.cloud.exceptions.Forbidden:
		print("[-] Awwww sheet")

# Function to list all storage buckets
def list_all_buckets(project, bucket):
	# Establish storage client
	storage_client = storage.Client(project)

	# Print bucket names
	print("GCE Storage Buckets:")
	for bucket in storage_client.list_buckets():
		print(bucket)

# Function to download file from a storage bucket
def download_from_bucket(project, bucket, remote_file, local_file):
	# Establish storage client
	storage_client = storage.Client(project)

	# Select bucket
	gce_storage_bucket = storage_client.get_bucket(bucket)

	# Establish BLOB with destination file name
	blob = gce_storage_bucket.blob(remote_file)

	# Download from bucket
	with open(local_file, 'wb') as file_object:
		blob.download_to_file(file_object)

# Main function
def main():
	# Check if the script is running as standalone
	if __name__ == "__main__":
		# Set GCE project name
		project_name = "postgresql-backups"

		# Set the GCE storage bucket
		bucket_name = "bc-psql-backups"

		# Test bucket upload
		#upload_to_bucket("postgresql-backups", "bc-psql-backups", "ENCRYPTED_127.0.0.1_full_backup_25052017_214324.psql", "ENCRYPTED_127.0.0.1_full_backup_25052017_214324.psql")

		# Test bucket download
		#download_from_bucket(project_name, bucket_name, "ENCRYPTED_127.0.0.1_full_backup_02062017_175107.psql", "downloaded_from_gce.psql")

main()
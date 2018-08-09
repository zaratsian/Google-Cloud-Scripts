


###################################################################################################
#
#   Cloud Compute Engine (GCE)
#
#   Google Cloud Platform (GCP)
#
#   References:
#   https://cloud.google.com/sql/docs/mysql/create-instance
#   https://cloud.google.com/sql/docs/mysql/instance-settings
#   https://cloud.google.com/sdk/gcloud/reference/sql/
#
###################################################################################################



# Lists Cloud SQL instances
gcloud sql instances list



# Create Cloud SQL (MySQL) Instance
# https://cloud.google.com/sql/docs/mysql/create-instance
gcloud sql instances create z-mysql-1 \
    --database-version=MYSQL_5_7 \
    --tier=db-n1-standard-1 \
    --region=us-east1



# Set the password for the "root@%" MySQL user:
gcloud sql users set-password root % --instance z-mysql-1 --password mysql_123



# Connect to Cloud SQL (MySQL) Instance
gcloud sql connect z-mysql-1 --user=root



# Create MySQL Database
gcloud sql databases create zdatabase --instance=z-mysql-1



# List MySQL Databases
gcloud sql databases list --instance=z-mysql-1



# Delete Cloud SQL Instance
gcloud sql instances delete z-mysql-1



#ZEND



################################################################################################################
#
#   GCP - Google Cloud Storage
#
#   https://cloud.google.com/storage/docs/
#   https://google-cloud-python.readthedocs.io/en/latest/storage/client.html
#
#   https://cloud.google.com/sdk/docs/
#   https://cloud.google.com/storage/docs/gsutil
#
################################################################################################################


# GCP Project Info
'''
gcloud info
'''



# Create Cloud Storage Bucket
'''
gcloud compute regions list   # List regions
gsutil mb -l us-east1 gs://my-awesome-bucket/
'''



# Load Data into GCP Cloud Storage
'''
gsutil cp dataset.csv gs://zBucket
'''



# List GCP Cloud Storage Dir Structure
'''
gsutil ls gs://
gsutil ls gs://zBucket
'''



#ZEND

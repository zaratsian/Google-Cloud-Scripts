

################################################################################################################
#
#   GCP - Google Cloud Storage
#
#   https://cloud.google.com/storage/docs/
#   https://google-cloud-python.readthedocs.io/en/latest/storage/client.html
#   https://cloud.google.com/storage/docs/gsutil
#
#   https://googleapis.github.io/google-cloud-python/latest/storage/client.html
#   https://googleapis.github.io/google-cloud-python/latest/storage/blobs.html
#
################################################################################################################


from google.cloud import storage
from google.cloud.storage.blob import Blob


################################################################################################################
#
#   Functions
#
################################################################################################################



def gcp_storage_create_bucket(bucket_name, requester_pays=False, project=None):
    '''
        Creates a new bucket
    '''
    try:
        storage_client = storage.Client()
        bucket = storage_client.create_bucket(bucket_name, requester_pays=requester_pays, project=project)
        print('Bucket {} created'.format(bucket.name))
    except Exception as e:
        print('[ ERROR ] {}'.format(e))



def gcp_storage_list_buckets(max_results=None, project=None):
    '''
        List Google Cloud Storage Buckets
        Return list of GCS metadata as JSON
    '''
    try:
        storage_client = storage.Client()
        
        bucket_payloads = []
        for bucket in storage_client.list_buckets(max_results=max_results, page_token=None, prefix=None, projection='noAcl', fields=None, project=project):
            
            bucket_payload = {
                'id':               bucket.id,
                'name':             bucket.name,
                'location':         bucket.location,
                'owner':            bucket.owner,
                'path':             bucket.path,
                'created': '{}'.format(bucket.time_created),
                'retention_period': bucket.retention_period,
                'storage_class':    bucket.storage_class
            }
            
            print('')
            print('Bucket ID:               {}'.format(bucket_payload['id']))
            print('Bucket Name:             {}'.format(bucket_payload['name']))
            print('Bucket Location:         {}'.format(bucket_payload['location']))
            print('Bucket Owner:            {}'.format(bucket_payload['owner']))
            print('Bucket Path:             {}'.format(bucket_payload['path']))
            print('Bucket Create:           {}'.format(bucket_payload['created']))
            print('Bucket Retention Period: {}'.format(bucket_payload['retention_period']))
            print('Bucket Storage Class:    {}'.format(bucket_payload['storage_class']))
            
            bucket_payloads.append(bucket_payload)
        
        return bucket_payloads
    except Exception as e:
        print('[ ERROR ] {}'.format(e))



def gcp_storage_upload_string(source_string, bucket_name, blob_name):
    '''
        Google Cloud Storage - Upload Blob from String
    '''
    try:
        storage_client = storage.Client()
        bucket = storage_client.get_bucket(bucket_name)
        blob = bucket.blob(blob_name)
        blob.upload_from_string(source_string)
    except Exception as e:
        print('[ ERROR ] {}'.format(e))



def gcp_storage_upload_file(input_file, bucket_name, blob_name):
    '''
        Uploads a file to the bucket.
    '''
    try:
        storage_client = storage.Client()
        bucket = storage_client.get_bucket(bucket_name)
        blob = bucket.blob(blob_name)
    
        blob.upload_from_filename(input_file)
        #blob.upload_from_file(input_file)      # Alternative option
    
        print('File {} uploaded to {}.'.format(
            input_file,
            blob_name))
    
    except Exception as e:
        print('[ ERROR ] {}'.format(e))



def gcp_storage_download_as_string(bucket_name, blob_name):
    '''
        Downloads a blob from the bucket, and outputs as a string.
    '''
    try:
        storage_client = storage.Client()
        bucket = storage_client.get_bucket(bucket_name)
        blob = bucket.blob(blob_name)
        blob_content = blob.download_as_string()
        
        return blob_content
    
    except Exception as e:
        print('[ ERROR ] {}'.format(e))



def gcp_storage_download_to_file(blob_name, bucket_name, destination_file_name):
    '''
        Downloads a blob from the bucket, and outputs as file.
    '''
    try:
        storage_client = storage.Client()
        bucket = storage_client.get_bucket(bucket_name)
        blob = bucket.blob(blob_name)
        
        blob.download_to_filename(destination_file_name)
        
        print('Blob {} downloaded to {}.'.format(
            blob_name,
            destination_file_name))
    
    except Exception as e:
        print('[ ERROR ] {}'.format(e))





#ZEND

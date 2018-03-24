

import os,sys,re
import json
import time,datetime
from google.cloud import storage
from google.cloud import pubsub
from google.cloud import bigquery


def check_for_google_creds():
    import os
    try:
        return '[ INFO ] Credential found at ' + str([v for k,v in os.environ.items() if k == 'GOOGLE_APPLICATION_CREDENTIALS'][0])
    except:
        return '[ WARN ] No credentials found. Make sure GOOGLE_APPLICATION_CREDENTIALS env variable points to .json authorization file.'


def check_for_bucket(bucket_name):
    client = storage.Client()
    buckets = client.list_buckets()
    list_of_buckets = [b.name for b in buckets]
    return (bucket_name in list_of_buckets, list_of_buckets)


def create_gcp_bucket(bucket_name):
    client = storage.Client()
    client.create_bucket(bucket_name)
    return '[ INFO ] Created ' + str(bucket_name)


def upload_to_gcp_bucket(bucket_name, blob_name, filename_to_upload):
    client = storage.Client()
    bucket = client.get_bucket(bucket_name)
    blob   = bucket.blob(blob_name)
    blob.upload_from_filename(filename=filename_to_upload)
    return '[ INFO ] Uploaded file to bucket'


#######################################################################################################################
#
#   Cloud Storage Notification
#   Send notification on pub/sub when a change occurs within specified bucket
#
#######################################################################################################################

# Enable Pub/Sub Notifciation
#gsutil notification create -f json gs://<bucket_name>

def pubsub_listen_for_change(topic_name, topic):
    subscriber = pubsub.SubscriberClient()
    
    topic_name = topic_name
    sub_name   = 'projects/dzproject20180301/subscriptions/ztestsub'
    
    subscriber.create_subscription(name=subscription_name, topic=topic_name)
    
    subscription = subscriber.subscribe(subscription_name)
    
    def callback(message):
        print(message.data)
        message.ack()
    
    subscription.open(callback)



#######################################################################################################################
#
#   Load (CSV) from Cloud Storage into BigQuery
#
#######################################################################################################################

def move_gstorage_to_bigquery(bucket_uri, dataset_name, table_name):
    try:
        client      = bigquery.Client()
        dataset_ref = client.dataset(dataset_name)
        job_config  = bigquery.LoadJobConfig()
        job_config.schema = [
            bigquery.SchemaField('name', 'STRING'),
            bigquery.SchemaField('post_abbr', 'STRING')
        ]
        job_config.skip_leading_rows = 1
        job_config.source_format = bigquery.SourceFormat.CSV
        
        load_job = client.load_table_from_uri(  bucket_uri,                     # 'gs://path/to/data.csv',
                                                dataset_ref.table(table_name),
                                                job_config=job_config)
        
        assert load_job.job_type == 'load'
        load_job.result() 
        assert load_job.state == 'DONE'
        return '[ INFO ] Successfully loaded data from Cloud Storage into BigQuery'
    except:
        return '[ ERROR ] There was an issue loading data into BigQuery. Double-check the dataset name and Cloud Storage bucket path'


#######################################################################################################################
#
#   Load (JSON) from Cloud Storage into BigQuery
#
#######################################################################################################################

def load_json_to_bigquery(file, dataset_id):
    try:
        client      = bigquery.Client()
        dataset_ref = client.dataset(dataset_id)
        
        job_config  = bigquery.LoadJobConfig()
        job_config.schema = [
            bigquery.SchemaField('name', 'STRING'),
            bigquery.SchemaField('post_abbr', 'STRING')
        ]
        job_config.source_format = bigquery.SourceFormat.NEWLINE_DELIMITED_JSON
        
        load_job = client.load_table_from_uri(  'gs://cloud-samples-data/bigquery/us-states/us-states.json',
                                                dataset_ref.table('us_states'),
                                                job_config=job_config)  # API request
        
        assert load_job.job_type == 'load'
        load_job.result()  # Waits for table load to complete.
        assert load_job.state == 'DONE'
        return '[ INFO ] Successfully loaded JSON from Cloud Storage into BigQuery'
    except:
        return '[ ERROR ] There was an issue loading JSON into BigQuery. Double-check the dataset name and Cloud Storage bucket path'


'''

Setup:
gcloud auth login
gcloud components update
export GOOGLE_APPLICATION_CREDENTIALS=~/key.json

General References:
https://github.com/GoogleCloudPlatform/google-cloud-python
https://google-cloud-python.readthedocs.io/en/latest/core/auth.html

App Engine Flask App:
https://codelabs.developers.google.com/codelabs/cloud-vision-app-engine/index.html
https://conda.io/docs/user-guide/tasks/manage-environments.html

Cloud Storage Notifications:
https://cloud.google.com/storage/docs/gsutil/commands/notification#watchbucket-examples

Loading Data from Cloud Storage into BigQuery
https://cloud.google.com/bigquery/docs/loading-data-cloud-storage
https://cloud.google.com/bigquery/docs/loading-data-cloud-storage-csv
https://cloud.google.com/bigquery/docs/loading-data-cloud-storage-json

'''


#ZEND
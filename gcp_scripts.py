

###############################################################################################################
#
#   Google Cloud 
#
#   This script contains misc functions and scripts useful for interacting with GCP Services
#
###############################################################################################################


import os,sys,re
import json
import time,datetime
from google.cloud import storage
from google.cloud import pubsub
from google.cloud import bigquery
from google.cloud.bigquery.job import SourceFormat
from google.cloud.bigquery.job import WriteDisposition


###############################################################################################################
#
#   Functions
#
###############################################################################################################


def check_for_google_creds():
    import os
    try:
        return '[ INFO ] Credential found at ' + str([v for k,v in os.environ.items() if k == 'GOOGLE_APPLICATION_CREDENTIALS'][0])
    except:
        return '[ WARN ] No credentials found. Make sure GOOGLE_APPLICATION_CREDENTIALS env variable points to .json authorization file.'


###############################################################################################################
#
#   GCP Cloud Storage
#
###############################################################################################################


def check_for_bucket(bucket_name):
    client = storage.Client()
    buckets = client.list_buckets()
    list_of_buckets = [b.name for b in buckets]
    return (bucket_name in list_of_buckets, list_of_buckets)


def create_gcp_bucket(bucket_name):
    client = storage.Client()
    client.create_bucket(bucket_name)
    return '[ INFO ] Created ' + str(bucket_name)


def upload_file_to_gcp_bucket(bucket_name, blob_name, filename_to_upload):
    client = storage.Client()
    bucket = client.get_bucket(bucket_name)
    blob   = bucket.blob(blob_name)
    blob.upload_from_filename(filename=filename_to_upload)
    return '[ INFO ] Uploaded file to bucket'


def upload_str_to_gcp_bucket(bucket_name, blob_name, record_str):
    client = storage.Client()
    bucket = client.get_bucket(bucket_name)
    blob   = bucket.blob(blob_name)
    blob.upload_from_string(data=record_str, content_type='text/plain')
    return '[ INFO ] Uploaded string to bucket'

#######################################################################################################################
#
#   GCP PubSub
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


def gcp_pubsub_list_topics(project):
    publisher = pubsub.PublisherClient()
    project_path = publisher.project_path(project)
    topics = [topic for topic in publisher.list_topics(project_path)]
    return topics

#gcp_pubsub_list_topics('dzproject20180301')


def gcp_pubsub_create_topic(project, topic_name):
    #https://cloud.google.com/pubsub/docs/admin 
    publisher = pubsub.PublisherClient()
    topic_path = publisher.topic_path(project, topic_name)
    topic = publisher.create_topic(topic_path)
    print('Topic created: {}'.format(topic))

#gcp_pubsub_create_topic('dzproject20180301', 'chicagotraffic')
#gcp_pubsub_list_topics('dzproject20180301')


def gcp_pubsub_publish_message(project, topic_name, payload):
    publisher = pubsub.PublisherClient()
    topic_path = publisher.topic_path(project, topic_name)
    publisher.publish(topic_path, data=payload)
    #print('[ INFO ] Published message')


#######################################################################################################################
#
#   GCP BigQuery
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


def load_json_to_bigquery(bucket_uri, dataset_name, table_name):
    try:
        client      = bigquery.Client()
        dataset_ref = client.dataset(dataset_name)
        
        job_config  = bigquery.LoadJobConfig()
        job_config.schema = [
            bigquery.SchemaField('date', 'DATE'),
            bigquery.SchemaField('calories_consumed', 'INTEGER'),
            bigquery.SchemaField('calories_burned', 'INTEGER'),
            bigquery.SchemaField('heartrate', 'INTEGER'),
            bigquery.SchemaField('sleep', 'INTEGER')
        ]
        job_config.source_format = 'NEWLINE_DELIMITED_JSON'
        
        load_job = client.load_table_from_uri(  bucket_uri,                     # 'gs://path/to/data.csv',
                                                dataset_ref.table(table_name),
                                                job_config=job_config)
        
        assert load_job.job_type == 'load'
        load_job.result()  # Waits for table load to complete.
        assert load_job.state == 'DONE'
        return '[ INFO ] Successfully loaded JSON from Cloud Storage into BigQuery'
    except:
        return '[ ERROR ] There was an issue loading JSON into BigQuery. Double-check the dataset name and Cloud Storage bucket path'




query = '''
SELECT last_updated, count(*) as freq
    FROM `dzproject20180301.chicago_traffic.traffic_segments1`
    GROUP BY last_updated
    ORDER BY last_updated DESC 
    LIMIT 10
'''.replace('\n','')

query = '''
SELECT count(*) as freq
    FROM `dzproject20180301.chicago_traffic.traffic_segments1`
'''

def gcp_query_bigquery(query):
    client      = bigquery.Client()
    query_job   = client.query(query)
    rows        = query_job.result()
    rows_list   = list(rows)
    return rows_list

rows = gcp_query_bigquery(query)
rows[0].get('freq')








'''

Setup:
pip install --upgrade google-cloud-bigquery
gcloud auth login
gcloud components update
export GOOGLE_APPLICATION_CREDENTIALS=~/key.json

General References:
https://github.com/GoogleCloudPlatform/google-cloud-python
https://google-cloud-python.readthedocs.io/en/latest/core/auth.html

App Engine Flask App:
https://codelabs.developers.google.com/codelabs/cloud-vision-app-engine/index.html
https://conda.io/docs/user-guide/tasks/manage-environments.html

App Engine Scheduler (Cron):
https://cloud.google.com/appengine/docs/flexible/python/scheduling-jobs-with-cron-yaml
https://medium.com/google-cloud/google-cloud-functions-scheduling-cron-5657c2ae5212

Cloud Storage Notifications:
https://cloud.google.com/storage/docs/gsutil/commands/notification#watchbucket-examples

Loading Data from Cloud Storage into BigQuery
https://cloud.google.com/bigquery/docs/loading-data-cloud-storage
https://cloud.google.com/bigquery/docs/loading-data-cloud-storage-csv
https://cloud.google.com/bigquery/docs/loading-data-cloud-storage-json
https://stackoverflow.com/questions/44838239/upload-to-bigquery-from-python

NOTE: BigQuery expects JSON newline seperated data, such as
{"name":"dan","age"34}
{"name":"frank","age"54}
{"name":"dean","age"64}


DataFlow:
pip install google-cloud-dataflow
https://cloud.google.com/dataflow/docs/quickstarts/quickstart-python
https://github.com/apache/beam/tree/master/sdks/python
https://beam.apache.org/documentation/sdks/pydoc/2.4.0/
https://stackoverflow.com/questions/46854167/dataflow-streaming-using-python-sdk-transform-for-pubsub-messages-to-bigquery-o
https://medium.com/google-cloud/quickly-experiment-with-dataflow-3d5a0da8d8e9
https://codelabs.developers.google.com/codelabs/cloud-dataflow-nyc-taxi-tycoon/#0
DataSet: http://www.nyc.gov/html/tlc/html/about/trip_record_data.shtml

Datalab:
https://cloud.google.com/datalab/docs/quickstart
gcloud components update
gcloud components install datalab
datalab create dzdatalabinstance1
datalab connect --zone us-east1-d --port 8081 dzdatalabinstance1

'''


#ZEND

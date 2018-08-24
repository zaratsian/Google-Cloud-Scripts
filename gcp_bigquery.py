
################################################################################################################
#
#   GCP - BigQuery
#
#   References:
#   https://cloud.google.com/bigquery/docs/
#   https://github.com/GoogleCloudPlatform/google-cloud-python
#   https://google-cloud-python.readthedocs.io/en/latest/bigquery/usage.html
#   https://cloud.google.com/sdk/docs/
#   https://cloud.google.com/storage/docs/gsutil
#
################################################################################################################

################################################################################################################
#
#   Bash - BigQuery
#
################################################################################################################

# BigQuery: Get active project
'''
bq show
'''


# BigQuery: List datasets
'''
bq ls
'''


# BigQuery: Create new dataset
'''
bq mk <dataset_name>
'''


# BigQuery: Creates or updates a table and loads data in a single step
'''
bq load <dataset_name>.<table_name> <filename.txt> id:string,name:string,age:integer
'''


# BigQuery: View schema of table
'''
bq show <dataset_name>.<table>
'''


# BigQuery: Execute Query
'''
bq query "SELECT count(*) FROM <dataset_name>.<table_name> WHERE age >= 20 ORDER BY count DESC LIMIT 10"
'''


# BigQuery: Remove dataset
'''
bq rm -r <dataset_name>
'''



################################################################################################################
#
#   Python - BigQuery
#
################################################################################################################

'''
pip install --upgrade google-cloud-bigquery
export GOOGLE_APPLICATION_CREDENTIALS="/Users/dzaratsian/gcpkey.json"
'''

import os
from google.cloud import bigquery
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/Users/dzaratsian/gcpkey.json"


def bq_create_dataset(dataset_id):
    ''' Create BigQuery Dataset '''
    
    bigquery_client = bigquery.Client()
    dataset_ref     = bigquery_client.dataset(dataset_id)
    dataset         = bigquery.Dataset(dataset_ref)
    dataset         = bigquery_client.create_dataset(dataset)
    print('[ INFO ] Dataset {} created.'.format(dataset.dataset_id))


table_schema = [
    bigquery.SchemaField('datetimeid',          'STRING',   mode='REQUIRED'),
    bigquery.SchemaField('title',               'STRING',   mode='NULLABLE'),
    bigquery.SchemaField('video_url',           'STRING',   mode='NULLABLE'),
    bigquery.SchemaField('gcs_url',             'STRING',   mode='NULLABLE'),
    bigquery.SchemaField('entity',              'STRING',   mode='NULLABLE'),
    bigquery.SchemaField('category',            'STRING',   mode='NULLABLE'),
    bigquery.SchemaField('start_time_seconds',  'INTEGER',  mode='NULLABLE'),
    bigquery.SchemaField('end_time_seconds',    'INTEGER',  mode='NULLABLE'),
    bigquery.SchemaField('confidence',          'FLOAT',    mode='NULLABLE'),
]


def bq_create_table(dataset_id, table_id, table_schema):
    ''' Create BigQuery Table '''
    
    #table_schema = [
    #    bigquery.SchemaField('full_name', 'STRING', mode='REQUIRED'),
    #    bigquery.SchemaField('age', 'INTEGER', mode='REQUIRED'),
    #]
    
    # BigQuery Client
    bigquery_client = bigquery.Client()
    
    # Dataset object
    dataset_ref     = bigquery_client.dataset(dataset_id)
    
    # Table object and creation
    table_ref       = dataset_ref.table(table_id)
    table           = bigquery.Table(table_ref, schema=table_schema)
    table           = bigquery_client.create_table(table)
    print('[ INFO ] Table {} created.'.format(table.table_id))


bq_create_table('video_analysis1', 'video_metadata1', table_schema)


def bq_query_table(query):
    ''' BigQuery Query Table '''
    
    bigquery_client = bigquery.Client()
    
    #query = ('''select * from video_analysis1.video_metadata1 limit 5''')
    
    query_job = bigquery_client.query(
        query,
        # Location must match that of the dataset(s) referenced in the query.
        location='US')  # API request - starts the query
    
    # Print Results
    for row in query_job:
        # Row values can be accessed by field name or index
        # NOTE: row[0] == row.name == row['name']
        print(row)


query = ('''select * from video_analysis1.video_metadata1 limit 5''')
bq_query_table(query)


#ZEND



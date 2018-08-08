
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

'''
...more here: https://github.com/GoogleCloudPlatform/google-cloud-python/tree/master/bigquery
'''


#ZEND



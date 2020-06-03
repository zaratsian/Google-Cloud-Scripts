
################################################################################################################
#
#   Google Cloud Dataflow
#
#   References:
#   https://cloud.google.com/dataflow/docs/
#
#   Usage:
'''
python bridgestone_dataflow.py \
    --gcp_project zpocdemos \
    --region us-central1 \
    --job_name 'bridgestone-streaming' \
    --gcp_staging_location "gs://zpocdemos-dataflow/staging" \
    --gcp_tmp_location "gs://zpocdemos-dataflow/tmp" \
    --batch_size 10 \
    --input_topic projects/zpocdemos/topics/inventory_events \
    --bq_dataset_name bridgestone \
    --bq_table_name inventory_bato_streaming \
    --runner DataflowRunner &
'''
#   Used for testing:
#   gcp_pubsub_publish_message(project_name, topic_name, json.dumps({"_direction":"NE","street":"108 main st"}).encode('utf-8'))
#
#
#   pip install google-cloud-dataflow
#
################################################################################################################

from __future__ import absolute_import
import logging
import argparse
import json
import apache_beam as beam
from apache_beam import window
from apache_beam.transforms import trigger
from apache_beam.options.pipeline_options import PipelineOptions
from apache_beam.options.pipeline_options import StandardOptions
from apache_beam.options.pipeline_options import SetupOptions
from apache_beam.io import ReadFromText
from apache_beam.io import WriteToText
from past.builtins import unicode


################################################################################################################
#
#   Variables
#
################################################################################################################

bq_schema = {'fields': [
    {'name': 'dealer_six_digit','type': 'STRING', 'mode': 'NULLABLE'},
    {'name': 'article_number',  'type': 'STRING', 'mode': 'NULLABLE'},
    {'name': 'inventory',       'type': 'INT64',  'mode': 'NULLABLE'},
    {'name': 'quantity',        'type': 'INT64',  'mode': 'NULLABLE'}
]}

################################################################################################################
#
#   Functions
#
################################################################################################################

def parse_pubsub(line):
    return json.loads(line)

def convert_inventory_neg_to_pos(event):
    event['inventory'] = int(event['inventory']) if int(event['inventory']) >= 0 else abs(int(event['inventory']))
    return event

def quantity_is_positive(event):
    return int(event['quantity']) >= 0

def convert_datatypes(event):
    new_event={}
    for k,v in event.items():
        new_event[k] = str(v)
    return new_event

def sum_by_group(GroupByKey_tuple):
      (word, list_of_ones) = GroupByKey_tuple
      return {"word":word, "count":sum(list_of_ones)}

def run(argv=None):
    """Build and run the pipeline."""
    parser = argparse.ArgumentParser()
    parser.add_argument('--gcp_project',          required=True,  default='',                   help='GCP Project ID')
    parser.add_argument('--region',               required=True,  default='',                   help='GCP Project ID')
    parser.add_argument('--job_name',             required=True,  default='',                   help='Dataflow Job Name')
    parser.add_argument('--gcp_staging_location', required=True,  default='gs://xxxxx/staging', help='Dataflow Staging GCS location')
    parser.add_argument('--gcp_tmp_location',     required=True,  default='gs://xxxxx/tmp',     help='Dataflow tmp GCS location')
    parser.add_argument('--batch_size',           required=True,  default=10,                   help='Dataflow Batch Size')
    parser.add_argument('--input_topic',          required=True,  default='',                   help='Input PubSub Topic: projects/<project_id>/topics/<topic_name>')
    parser.add_argument('--bq_dataset_name',      required=True,  default='',                   help='Output BigQuery Dataset')
    parser.add_argument('--bq_table_name',        required=True,  default='',                   help='Output BigQuery Table')
    parser.add_argument('--runner',               required=True,  default='DirectRunner',       help='Dataflow Runner - DataflowRunner or DirectRunner (local)')
    
    known_args, pipeline_args = parser.parse_known_args(argv)
    
    pipeline_args.extend([
          '--runner={}'.format(known_args.runner),                          # DataflowRunner or DirectRunner (local)
          '--project={}'.format(known_args.gcp_project),
          '--staging_location={}'.format(known_args.gcp_staging_location),  # Google Cloud Storage gs:// path
          '--temp_location={}'.format(known_args.gcp_tmp_location),         # Google Cloud Storage gs:// path
          '--job_name=' + str(known_args.job_name),
      ])
    
    pipeline_options = PipelineOptions(pipeline_args)
    pipeline_options.view_as(SetupOptions).save_main_session = True
    pipeline_options.view_as(StandardOptions).streaming = True
    
    ###################################################################
    #   DataFlow Pipeline
    ###################################################################
    
    with beam.Pipeline(options=pipeline_options) as p:
        
        logging.info('Ready to process events from PubSub topic: {}'.format(known_args.input_topic))
        
        # Read the pubsub topic into a PCollection.
        events = (
                 p  | beam.io.ReadFromPubSub(known_args.input_topic)
        )
        
        # Print - Used for debugging
        #events | 'Print raw events' >> beam.Map(print)
        
        # Tranform events
        clean_events = (
            events  | beam.Map(parse_pubsub)
                    | beam.Map(convert_inventory_neg_to_pos)
                    | beam.Filter(quantity_is_positive)
        )
        
        # Print results to console (for testing/debugging)
        clean_events | 'Print clean events' >> beam.Map(print)
        
        # Sink/Persist to BigQuery
        clean_events | 'Write to bq' >> beam.io.gcp.bigquery.WriteToBigQuery(
                        table=known_args.bq_table_name,
                        dataset=known_args.bq_dataset_name,
                        project=known_args.gcp_project,
                        schema=bq_schema,
                        batch_size=int(known_args.batch_size)
                        )
         
        # Sink data to PubSub
        #output | beam.io.WriteToPubSub(known_args.output_topic)


################################################################################################################
#
#   Main
#
################################################################################################################

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    run()



'''
# Simulator

python bridgestone_simulator.py --project_id zpocdemos --pubsub_topic inventory_events --delay 1 --csvfilepath "Sample_Inventory_BATO_20200222 - Sample_Inventory_BATO_20200222.csv"

'''



#ZEND

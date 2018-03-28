

################################################################################################################
#
#   Google Cloud Dataflow
#
#   Usage: 
'''
python gcp_dataflow.py \
    --runner DirectRunner \   
    --job_name 'dzdataflowjob1' \
    --batch_size 100 \
    --project_id dzproject20180301 \
    --input_topic projects/dzproject20180301/topics/chicagotraffic \
    --dataset_name chicago_traffic \
    --table_name traffic_segments1 \
    --table_schema 'segmentid:STRING,street:STRING,direction:STRING,from_street:STRING,to_street:STRING,length:FLOAT,street_heading:STRING,start_long:FLOAT,start_lat:FLOAT,end_long:FLOAT,end_lat:FLOAT,speed:FLOAT,last_updated:STRING,comments:STRING'

--table_schema '_direction:STRING,_fromst:STRING,_last_updt:STRING,_length:FLOAT,_lif_lat:FLOAT,_lit_lat:FLOAT,_lit_lon:FLOAT,_strheading:STRING,_tost:STRING,_traffic:STRING,segmentid:STRING,start_lon:FLOAT,street:STRING'
--table_schema 'segmentid:STRING,street:STRING,direction:STRING,from_street:STRING,to_street:STRING,length:FLOAT,street_heading:STRING,start_long:FLOAT,start_lat:FLOAT,end_long:FLOAT,end_lat:FLOAT,speed:FLOAT,last_updated:STRING,comments:STRING'
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
import apache_beam as beam
import apache_beam.transforms.window as window
from apache_beam.options.pipeline_options import PipelineOptions
from apache_beam.options.pipeline_options import StandardOptions
from apache_beam.options.pipeline_options import SetupOptions
from apache_beam.io import ReadFromText
from apache_beam.io import WriteToText


################################################################################################################
#
#   Functions
#
################################################################################################################

def parse_pubsub(line):
    import json
    record = json.loads(line)
    #record = json.loads(json.dumps({"direction":record['_direction'], "street":record['street']}))    #'direction:STRING,state:STRING'
    #return (record['mac']), (record['status']), (record['datetime'])
    return record


def run(argv=None):
    """Build and run the pipeline."""
    
    parser = argparse.ArgumentParser()
    parser.add_argument('--runner',       required=False, default='DirectRunner',       help='Dataflow Runner - DataflowRunner or DirectRunner (local)')
    parser.add_argument('--job_name',     required=False, default='dzdataflowjob1',     help='Dataflow Job Name')
    parser.add_argument('--batch_size',   required=False, default='100',                help='Dataflow Batch Size')
    parser.add_argument('--project_id',   required=False, default='dzproject20180301',  help='GCP Project ID')
    parser.add_argument('--input_topic',  required=False, default='',                   help='Input PubSub Topic: projects/<project_id>/topics/<topic_name>')
    parser.add_argument('--dataset_name', required=False, default='chicago_traffic',    help='Output BigQuery Dataset') 
    parser.add_argument('--table_name',   required=False, default='',                   help='Output BigQuery Table')
    parser.add_argument('--table_schema', required=False, default='',                   help='Output BigQuery Schema')
    
    known_args, pipeline_args = parser.parse_known_args(argv)
    
    pipeline_args.extend([
          # CHANGE 2/5: (OPTIONAL) Change this to DataflowRunner to
          # run your pipeline on the Google Cloud Dataflow Service. DirectRunner (local)
          #'--runner=DirectRunner',
          '--runner=' + str(known_args.runner),
          # CHANGE 3/5: Your project ID is required in order to run your pipeline on
          # the Google Cloud Dataflow Service.
          #'--project=dzproject20180301',
          '--project=' + str(known_args.project_id),
          # CHANGE 4/5: Your Google Cloud Storage path is required for staging local
          # files.
          '--staging_location=gs://tmp_dataflow/staging',
          # CHANGE 5/5: Your Google Cloud Storage path is required for temporary
          # files.
          '--temp_location=gs://tmp_dataflow/tmp',
          #'--job_name=dzdataflowjob1',
          '--job_name=' + str(known_args.job_name),
      ])
    
    pipeline_options = PipelineOptions(pipeline_args)
    pipeline_options.view_as(SetupOptions).save_main_session = True
    pipeline_options.view_as(StandardOptions).streaming = True
    
    ###################################################################
    #   BigQuery Table Schema
    #   https://github.com/apache/beam/blob/474345f5987e47a22d063c7bfcb3638c85a57e64/sdks/python/apache_beam/examples/cookbook/bigquery_schema.py#L49
    ###################################################################
    
    '''
    table_schema = bigquery.TableSchema()
    
    # Fields that use standard types.
    direction_schema = bigquery.TableFieldSchema()
    direction_schema.name = '_direction'
    direction_schema.type = 'string'
    direction_schema.mode = 'nullable'
    table_schema.fields.append(direction_schema)
    
    fromst_schema = bigquery.TableFieldSchema()
    fromst_schema.name = '_fromst'
    fromst_schema.type = 'string'
    fromst_schema.mode = 'required'
    table_schema.fields.append(fromst_schema)
    
    last_updt_schema = bigquery.TableFieldSchema()
    last_updt_schema.name = '_last_updt'
    last_updt_schema.type = 'integer'
    last_updt_schema.mode = 'nullable'
    table_schema.fields.append(last_updt_schema)
    
    length_schema = bigquery.TableFieldSchema()
    length_schema.name = '_length'
    length_schema.type = 'string'
    length_schema.mode = 'nullable'
    table_schema.fields.append(length_schema)
    '''
    
    # Nested Example
    '''
    phone_number_schema = bigquery.TableFieldSchema()
    phone_number_schema.name = 'phoneNumber'
    phone_number_schema.type = 'record'
    phone_number_schema.mode = 'nullable'
    
    area_code = bigquery.TableFieldSchema()
    area_code.name = 'areaCode'
    area_code.type = 'integer'
    area_code.mode = 'nullable'
    phone_number_schema.fields.append(area_code)
    
    number = bigquery.TableFieldSchema()
    number.name = 'number'
    number.type = 'integer'
    number.mode = 'nullable'
    phone_number_schema.fields.append(number)
    table_schema.fields.append(phone_number_schema)
    '''
    
    ###################################################################
    #   DataFlow Pipeline
    ###################################################################
    
    with beam.Pipeline(options=pipeline_options) as p:
        
        # Read the pubsub topic into a PCollection.
        events = ( p | beam.io.ReadStringsFromPubSub(known_args.input_topic) )
        
        # Tranform events
        transformed = (events 
                    | beam.Map(parse_pubsub))
        
        # Windowing
        #transformed | 'PairWithOne' >> beam.Map(lambda x: (x[0], 1))
        #            | 'Test' >> beam.WindowInto(window.FixedWindows(size=60, 0))
        #            | 'Group' >> beam.GroupByKey()
        #            | 'write' >> WriteToText('gs://zgym_fitness_data')
        
        # Persist to BigQuery
        transformed | 'Write' >> beam.io.WriteToBigQuery(
                        table=known_args.table_name,
                        dataset=known_args.dataset_name,
                        project=known_args.project_id,
                        schema=known_args.table_schema,
                        create_disposition=beam.io.BigQueryDisposition.CREATE_IF_NEEDED,
                        write_disposition=beam.io.BigQueryDisposition.WRITE_APPEND,
                        batch_size=int(100)
                        )


################################################################################################################
#
#   Main
#
################################################################################################################

if __name__ == '__main__':
    logging.getLogger().setLevel(logging.INFO)
    run()


################################################################################################################
#
#   References
#
################################################################################################################

'''
https://cloud.google.com/dataflow/docs/quickstarts

https://beam.apache.org/documentation/sdks/pydoc/2.4.0/
https://beam.apache.org/documentation/sdks/pydoc/2.4.0/apache_beam.io.gcp.bigquery.html#apache_beam.io.gcp.bigquery.WriteToBigQuery

https://github.com/apache/beam/tree/master/sdks/python/apache_beam/examples
'''

'''
NOTE: BigQuery expects JSON newline seperated data, such as
{"name":"dan","age"34}
{"name":"frank","age"54}
{"name":"dean","age"64}

'''

#ZEND

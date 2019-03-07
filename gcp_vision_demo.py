

#############################################################################
#
#   Google Cloud Vision (Image Analysis)
#
#   Usage:
#       file.py --youtube_url YOUTUBE_URL --bq_dataset_id BQ_DATASET_ID --bq_table_id BQ_TABLE_ID
#       file.py --youtube_url=https://www.youtube.com/watch?v=imm6OR605UI --bq_dataset_id=video_analysis1 --bq_table_id=video_metadata1
#
#   Dependencies:
#       pip install --upgrade google-cloud-vision
#       pip install --upgrade google-cloud-storage
#       pip install --upgrade google-cloud-bigquery
#
#   References:
#       https://cloud.google.com/vision/docs/libraries
#       https://github.com/nficano/pytube
#       https://github.com/zaratsian/python/blob/master/convert_video_to_images.py
#
#############################################################################



import os,sys,re
import io
import datetime,time
import argparse
import cv2
import requests
import shutil
from bs4 import BeautifulSoup
from pytube import YouTube
from google.cloud import vision
from google.cloud.vision import types
from google.cloud import storage
from google.cloud import bigquery


#os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/home/dzaratsian/key.json"



def save_youtube_video(youtube_url):
    ''' Save Youtube Video to local machine as .mp4 '''
    
    youtube_id       = youtube_url.split('=')[-1]
    youtube_filename = "youtube_{}".format(youtube_id)
    output_path      = '/tmp'
    # Download Youtube Video, save locally
    YouTube(youtube_url) \
        .streams \
        .filter(progressive=True, file_extension='mp4') \
        .first() \
        .download(output_path=output_path, filename=youtube_filename)
    
    local_filepath = "{}/{}.mp4".format(output_path, youtube_filename)
    print('[ INFO ] Complete! Youtube video downloaded to {}'.format(local_filepath))
    return local_filepath



def extract_url_title(url):
    try:
        r = requests.get(url)
        soup = BeautifulSoup(r.text, 'html.parser')
        title = soup.find('title').string
        print('[ INFO ] Successfully extracted Title: {}'.format(title))
        #title = re.sub('[^a-zA-Z0-9 ]','',title).replace(' ','_').lower()
        return title
    except:
        print('[ ERROR ] Issue processing URL. Check the URL and/or internet connection.')
        sys.exit()



def convert_video_to_images(video_filepath, sampling_rate, image_width, output_image_directory, output_image_prefix):
    
    # Create temp directory to store video images
    if os.path.exists(output_image_directory):
        shutil.rmtree(output_image_directory)
    
    os.mkdir(output_image_directory)
    
    print('[ INFO ] Converting {} into images within {}...'.format(video_filepath, output_image_directory))
    time.sleep(3)
    start_time = datetime.datetime.now()
    
    video_obj = cv2.VideoCapture(video_filepath)
    success,image = video_obj.read()
    frame_count = 1
    while success:
        
        video_obj.set(cv2.CAP_PROP_POS_MSEC,(frame_count * sampling_rate))      # CAP_PROP_POS_MSEC is the current position of the video file in milliseconds or video capture timestamp.
        
        (h, w) = image.shape[:2]                                                # Get image height and width
        r = image_width / float(w)
        resized_image = cv2.resize(image, (image_width, int(h * r)))            # Resize image based on image_width, and keep scale / aspect ratio.
        
        # Build frame timestamp, used for image name
        hours, remainder  = divmod((frame_count * (sampling_rate/1000)), 3600)
        minutes, seconds  = divmod(remainder, 60)
        seconds, mseconds = divmod(seconds, 1)
        frame_timestamp   = "{}_{}_{}_{}".format( str(int(hours)).zfill(2), str(int(minutes)).zfill(2), str(int(seconds)).zfill(2), str(int(mseconds)).zfill(2))
        
        cv2.imwrite( os.path.join(output_image_directory, "{}_{}.jpg".format(output_image_prefix, frame_timestamp)), resized_image)               # Save frame as .jpg file
        success,image = video_obj.read()
        frame_count += 1
        if (frame_count % 500) == 0:
            print('[ INFO ] {} frames have been processed.'.format(frame_count))
    
    end_time = datetime.datetime.now()
    run_time = (end_time - start_time).seconds
    print('[ INFO ] Complete - Processed {} frames in {} seconds'.format(frame_count, run_time) )





def bg_streaming_insert(rows_to_insert, bq_dataset_id, bq_table_id):
    ''' BigQuery Streaming Insert - Insert python list into BQ '''
        
    # Note: The table must already exist and have a defined schema
    # rows_to_insert is a list of variables (i.e. (id, date, value1, value2, etc.))
    print('[ INFO ] Inserting records in BigQuery')
    client    = bigquery.Client()
    table_ref = client.dataset(bq_dataset_id).table(bq_table_id)
    table     = client.get_table(table_ref)
    errors    = client.insert_rows(table, rows_to_insert)
    if errors == []:
        print('[ INFO ] Complete. No errors on Big Query insert')
    else:
        print('[ ERROR ] Errors found when inserting data into BigQuery')



def image_label_detection(image_filepath):
    
    # Instantiates a client
    client = vision.ImageAnnotatorClient()
    
    # Loads the image into memory
    with io.open(image_filepath, 'rb') as image_file:
        content = image_file.read()
    
    image = types.Image(content=content)
    
    # Performs label detection on the image file
    response = client.label_detection(image=image)
    labels = response.label_annotations
        
    print('Labels:')
    for label in labels:
        print(label.description)



def image_tag_web_entities(image_filepath, title, youtube_url):
    """Detects web annotations given an image."""
    
    # Create record_id
    record_id = local_filepath.split('/')[-1]
    
    client = vision.ImageAnnotatorClient()
    
    with io.open(image_filepath, 'rb') as image_file:
        content = image_file.read()
    
    image = vision.types.Image(content=content)
    
    # Uncomment - Use these two lines to score images within a GCS uri
    #image = vision.types.Image()
    #image.source.image_uri = uri
    
    response = client.web_detection(image=image)
    annotations = response.web_detection
    
    '''
    if annotations.best_guess_labels:
        for label in annotations.best_guess_labels:
            print('\nBest guess label: {}'.format(label.label))
    '''
    
    '''
    if annotations.pages_with_matching_images:
        print('\n{} Pages with matching images found:'.format(len(annotations.pages_with_matching_images)))
        
        for page in annotations.pages_with_matching_images:
            print('\n\tPage url   : {}'.format(page.url))
            
            if page.full_matching_images:
                print('\t{} Full Matches found: '.format(
                       len(page.full_matching_images)))
                
                for image in page.full_matching_images:
                    print('\t\tImage url  : {}'.format(image.url))
            
            if page.partial_matching_images:
                print('\t{} Partial Matches found: '.format(
                       len(page.partial_matching_images)))
                
                for image in page.partial_matching_images:
                    print('\t\tImage url  : {}'.format(image.url))
    '''
    
    shot_records = []
    if annotations.web_entities:
        
        datetimeid          = datetime.datetime.now().strftime('%Y%m%d_%H%M%S_%f')
        title               = title
        h,m,s,ms            = re.search('[0-9]{2}\_[0-9]{2}\_[0-9]{2}\_[0-9]{2}',image_filepath).group().split('_')
        video_url_at_time   = "{}&t={}h{}m{}s".format(youtube_url, h, m, s)
        start_time_offset   = (int(h)*3600)+(int(m)*60)+(int(s)*1)+int(ms)   # "{}:{}:{}".format(h,m,s)
        end_time_offset     = (int(h)*3600)+(int(m)*60)+(int(s)*1)+int(ms)   # "{}:{}:{}".format(h,m,s)
        
        #print('\n{} Web entities found: '.format(len(annotations.web_entities)))
        
        for entity in annotations.web_entities:
            #print('\n\tScore     : {}'.format(entity.score))
            #print(u'\tDescription: {}'.format(entity.description))
            if entity.description != '' and entity.score >= 0.40:
                shot_records.append( (record_id, datetimeid, title, video_url_at_time, '', entity.description, '', start_time_offset, end_time_offset, entity.score) )
    
    '''
    if annotations.visually_similar_images:
        print('\n{} visually similar images found:\n'.format(len(annotations.visually_similar_images)))
        
        for image in annotations.visually_similar_images:
            print('\tImage url    : {}'.format(image.url))
    '''
    
    return shot_records



def search_entities(search_phase, image_web_entities):
    return [record for record in image_web_entities if re.search(search_phase.lower(),str(record).lower())]



def detect_logos(image_filepath, title, youtube_url):
    """Detects logos in the file."""
    client = vision.ImageAnnotatorClient()
    
    with io.open(image_filepath, 'rb') as image_file:
        content = image_file.read()
    
    image = vision.types.Image(content=content)
    
    response = client.logo_detection(image=image)
    logos = response.logo_annotations
    
    shot_records = []
    for logo in logos:
        #print(logo.description)
        datetimeid          = datetime.datetime.now().strftime('%Y%m%d_%H%M%S_%f')
        title               = title
        h,m,s,ms            = re.search('[0-9]{2}\_[0-9]{2}\_[0-9]{2}\_[0-9]{2}',image_filepath).group().split('_')
        video_url_at_time   = "{}&t={}h{}m{}s".format(youtube_url, h, m, s)
        start_time_offset   = (int(h)*3600)+(int(m)*60)+(int(s)*1)+int(ms)   # "{}:{}:{}".format(h,m,s)
        end_time_offset     = (int(h)*3600)+(int(m)*60)+(int(s)*1)+int(ms)   # "{}:{}:{}".format(h,m,s)
        
        shot_records.append( (datetimeid, title, video_url_at_time, '', logo.description, '', start_time_offset, end_time_offset, logo.score) )
    
    return shot_records



if __name__ == "__main__":
    
    # ONLY used for TESTING - Example Arguments
    #args =  {
    #           "youtube_url":   "https://www.youtube.com/watch?v=uImwC5UheWs",
    #           "bucket_name":   "zmiscbucket1",
    #           "bq_dataset_id": "video_analysis1",
    #           "bq_table_id":   "video_metadata1",
    #           "output_image_directory": '/tmp/tmp_video_images'
    #       }
    
    # Arguments
    ap = argparse.ArgumentParser()
    ap.add_argument("--youtube_url", required=True, help="YouTube URL")
    #ap.add_argument("--bucket_name", required=True, help="Google Cloud Storage bucket name")
    ap.add_argument("--bq_dataset_id", required=True, help="Google BigQuery Dataset ID")
    ap.add_argument("--bq_table_id", required=True, help="Google BigQuery Table ID")
    args = vars(ap.parse_args())
    args['output_image_directory'] = '/tmp/tmp_video_images'
    
    
    # Download Youtube Video to .mp4
    local_filepath = save_youtube_video(args['youtube_url'])
    
    
    # Extract video title from URL
    title   = extract_url_title(args['youtube_url'])
    titleid = re.sub('[^a-zA-Z0-9 ]','',title).replace(' ','_').lower()
    
    
    # Convert video to images
    convert_video_to_images(video_filepath=local_filepath, sampling_rate=2000, image_width=600, output_image_directory=args['output_image_directory'], output_image_prefix=titleid)
    
    
    # Process image filepaths
    images_filepath = [os.path.join(args['output_image_directory'], f) for f in os.listdir(args['output_image_directory']) if re.search('(\.jpg|\.jpeg|\.png|\.tif|\.gif)',f)]
    
    
    # Score images (iterate through image directory)
    start_time = datetime.datetime.now()
    entities   = []
    logos      = []
    for image_filepath in images_filepath:
        #image_label_detection(image_filepath)
        entities = entities + image_tag_web_entities(image_filepath, title, args['youtube_url'])
        #logos    = logos    + detect_logos(image_filepath, title, args['youtube_url'])
    
    end_time   = datetime.datetime.now()
    run_time   = (end_time - start_time).seconds
    print('[ INFO ] Processed {} images within {} seconds'.format(len(images_filepath), run_time))
    
    
    '''
    # Query entities
    search_entities('danny', entities)
    '''
    
    
    # Write to BigQuery
    bg_streaming_insert(rows_to_insert=entities, bq_dataset_id=args['bq_dataset_id'], bq_table_id=args['bq_table_id'])



#ZEND





"""
#############################################################################
#
#   BigQuery Setup
#
#############################################################################
from google.cloud import bigquery
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
"""



#ZEND

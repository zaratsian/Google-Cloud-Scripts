

#######################################################################################
#
#   ...in progress...
#
#
#
#   Google Cloud Video Intelligence (extract relevant segments from Video)
#
#   Video Metadata Tagging + Streaming Insert to BigQuery
#
#   Usage:  file.py --youtube_url YOUTUBE_URL --bucket_name BUCKET_NAME --bq_dataset_id BQ_DATASET_ID --bq_table_id BQ_TABLE_ID
#           file.py --youtube_url=https://www.youtube.com/watch?v=imm6OR605UI --bucket_name=zmiscbucket1 --bq_dataset_id=video_analysis1 --bq_table_id=video_metadata1
#           file.py --youtube_url=https://www.youtube.com/watch?v=7dKownfx75E --bucket_name=zmiscbucket1 --bq_dataset_id=video_analysis1 --bq_table_id=video_metadata1
#
#   Dependencies:
#       pip install --upgrade google-cloud-videointelligence
#       pip install --upgrade google-cloud-storage
#       pip install --upgrade google-cloud-bigquery
#       pip install pytube
#
#   References:
#       https://cloud.google.com/video-intelligence/docs/
#       https://github.com/nficano/pytube
#       The Video Intelligence API supports common video formats, including .MOV, .MPEG4, .MP4, and .AVI
#
#######################################################################################

import os,sys
import argparse
import datetime, time
import requests
from bs4 import BeautifulSoup
from pytube import YouTube

from google.cloud import storage, bigquery, videointelligence

# pip install moviepy
# conda install ffmpeg -c conda-forge
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/home/dzaratsian/zproject201807-d5eb54b6371e.json"






youtube_url = 'https://www.youtube.com/watch?v=7wzPHYZD_Jg'
url = youtube_url
video_url = youtube_url
bucket_name = 'zmiscbucket1'


#######################################################################################
#
#   Functions
#
#######################################################################################


def extract_url_title(url):
    try:
        r = requests.get(url)
        soup = BeautifulSoup(r.text, 'html.parser')
        title = soup.find('title').string
        print('[ INFO ] Successfully extracted Title: {}'.format(title))
        return title
    except:
        print('[ ERROR ] Issue processing URL. Check the URL and/or internet connection.')
        sys.exit()



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



def upload_to_gcs(bucket_name, local_filepath):
    ''' Upload local file (.mp4) to Google Cloud Storage '''
    
    gcs_blob_name  = local_filepath.split('/')[-1]
    gcs_filepath   = 'gs://{}/{}'.format(bucket_name, gcs_blob_name)
    
    storage_client = storage.Client()
    gcs_bucket     = storage_client.get_bucket(bucket_name)
    gcs_blob       = gcs_bucket.blob(gcs_blob_name)
    gcs_blob.upload_from_filename(local_filepath)
    print('[ INFO ] File {} uploaded to {}'.format(
        local_filepath,
        gcs_filepath))
    return gcs_filepath



def extract_video_segment(input_video_path, start_time, end_time):
    '''
    Extract Video Segment
    Returns: Saved video file (to a location on temp, as specified in the printed message)
    '''
    try:
        # Derive output_video_path based on the input_video_path
        video_extension = '.{}'.format(input_video_path.split('.')[-1])
        segment_name = '_segment_{}_{}{}'.format(start_time, end_time, video_extension)
        output_video_path = re.sub(video_extension, segment_name, input_video_path)
        
        ffmpeg_extract_subclip(input_video_path, start_time, end_time, targetname=output_video_path)
        
        print('[ INFO ] Successful created video segment located at {}'.format(output_video_path))
    except Exception as e:
        print('[ WARNING ] Video segment was not created...')
        print('[ WARNING ] {}'.format(e))



def process_video_in_gcs(gcs_filepath, video_url, title):
    ''' Apply Google Video Intelligence API - Tag video metadata shot-by-shot '''
    
    print('[ INFO ] Processing video at {}'.format(gcs_filepath))
    processing_start_time = datetime.datetime.now()
    print('[ INFO ] Start time: {}'.format(processing_start_time.strftime("%Y-%m-%d %H:%M:%S")) )
    
    video_client = videointelligence.VideoIntelligenceServiceClient()
    features     = [videointelligence.enums.Feature.LABEL_DETECTION]
    operation    = video_client.annotate_video(gcs_filepath, features=features)
    result       = operation.result(timeout=600)
    
    segment_labels = result.annotation_results[0].segment_label_annotations
    shots = result.annotation_results[0].shot_label_annotations
    
    # Not needed, the following code will parse this content in a different way
    #shot_metadata = {}
    #for shot in shots:
    #    entity   = shot.entity.description
    #    #category = shot.category_entities[0].description
    #    segments = shot.segments
    #    shot_metadata[entity] = { "count": len(list(segments)), "shot_segments":list(segments) }
    
    shot_records = []
    for shot in shots:
        datetimeid = datetime.datetime.now().strftime('%Y%m%d_%H%M%S_%f')
        entity     = shot.entity.description
        try:
            category = shot.category_entities[0].description
        except:
            category = ''
        segments = shot.segments
        for segment in segments:
            start_time_offset   = segment.segment.start_time_offset.seconds   # Seconds
            start_time_offset_m = int(start_time_offset / 60)
            start_time_offset_s = start_time_offset % 60
            end_time_offset     = segment.segment.end_time_offset.seconds
            confidence          = segment.confidence
            video_url_at_time   = video_url+'&t={}m{}s'.format(start_time_offset_m, start_time_offset_s)
            shot_records.append( (datetimeid, title, video_url_at_time, gcs_filepath, entity, category, start_time_offset, end_time_offset, confidence) )
    
    print('[ INFO ] Processing complete. There were {} shot records found.'.format(len(shot_records)))
    processing_end_time = datetime.datetime.now()
    print('[ INFO ] End time: {}'.format(processing_end_time.strftime("%Y-%m-%d %H:%M:%S")) )
    print('[ INFO ] Run time: {} seconds'.format((processing_end_time - processing_start_time).seconds) )
    return shot_records



if __name__ == "__main__":
    
    # ONLY used for TESTING - Example Arguments
    '''
    args =  {
               "youtube_url":   "https://www.youtube.com/watch?v=7wzPHYZD_Jg",
               "bucket_name":   "zmiscbucket1",
               "bq_dataset_id": "video_analysis1",
               "bq_table_id":   "video_metadata1"
           }
    '''
    
    # Arguments
    ap = argparse.ArgumentParser()
    ap.add_argument("--youtube_url", required=True, help="YouTube URL")
    ap.add_argument("--bucket_name", required=True, help="Google Cloud Storage bucket name")
    ap.add_argument("--bq_dataset_id", required=True, help="Google BigQuery Dataset ID")
    ap.add_argument("--bq_table_id", required=True, help="Google BigQuery Table ID")
    args = vars(ap.parse_args())
    
    title = extract_url_title(url)
    
    local_filepath = save_youtube_video(youtube_url)
    
    gcs_filepath = upload_to_gcs(bucket_name, local_filepath)
    
    shot_records = process_video_in_gcs(gcs_filepath, video_url, title)
    
    seen_shot = []
    for shot in shot_records:
        if (('fish' in shot[4]) or ('fish' in shot[5])) and (shot not in seen_shot):
            
            input_video_path    = local_filepath
            start_time          = shot[6]
            end_time            = shot[7]
            
            if (end_time - start_time) >= 10: # If clip duration is greater or equal to 10 seconds
                
                extract_video_segment(input_video_path, start_time, end_time)
                seen_shot.append(shot)




#ZEND

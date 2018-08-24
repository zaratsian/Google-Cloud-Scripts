
#############################################################################
#
#   Google Cloud Video Intelligence
#
#   Video Metadata Tagging + Streaming Insert to BigQuery
#
#   Usage: file.py --youtube_url YOUTUBE_URL --bucket_name BUCKET_NAME
#          file.py --youtube_url=https://www.youtube.com/watch?v=imm6OR605UI --bucket_name=zmiscbucket1
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
#############################################################################



from google.cloud import storage, bigquery, videointelligence
from pytube import YouTube
import argparse
import datetime, time



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



def process_video_in_gcs(gcs_filepath, video_url):
    ''' Apply Google Video Intelligence API - Tag video metadata shot-by-shot '''
    
    print('[ INFO ] Processing video at {}'.format(gcs_filepath))
    video_client = videointelligence.VideoIntelligenceServiceClient()
    features     = [videointelligence.enums.Feature.LABEL_DETECTION]
    operation    = video_client.annotate_video(gcs_filepath, features=features)
    result       = operation.result(timeout=90)
    
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
            shot_records.append( (datetimeid, video_url_at_time, gcs_filepath, entity, category, start_time_offset, end_time_offset, confidence) )
    
    print('[ INFO ] Processing complete. There were {} shot records found.'.format(len(shot_records)))
    return shot_records



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



if __name__ == "__main__":
    
    # Arguments - Only used for testing
    #args =  {
    #           "youtube_url":   "https://www.youtube.com/watch?v=imm6OR605UI",
    #           "bucket_name":   "zmiscbucket1",
    #           "bq_dataset_id": "video_analysis1",
    #           "bq_table_id":   "video_metadata1"
    #       }
    
    # Arguments
    ap = argparse.ArgumentParser()
    ap.add_argument("--youtube_url", required=True, help="YouTube URL")
    ap.add_argument("--bucket_name", required=True, help="Google Cloud Storage bucket name")
    ap.add_argument("--bq_dataset_id", required=True, help="Google BigQuery Dataset ID")
    ap.add_argument("--bq_table_id", required=True, help="Google BigQuery Table ID")
    args = vars(ap.parse_args())
    
    # Download Youtube video as .mp4 file to local
    local_filepath = save_youtube_video(args["youtube_url"])
    
    # Upload .mp4 file to Google Cloud Storage (GCS)
    gcs_filepath = upload_to_gcs(args["bucket_name"], local_filepath)
    
    # Process .mp4 video file, stored on Google Cloud Storage (GCS)
    shot_records = process_video_in_gcs(gcs_filepath, args["youtube_url"])
    
    # Insert into BigQuery
    bg_streaming_insert(rows_to_insert=shot_records, bq_dataset_id=args['bq_dataset_id'], bq_table_id=args['bq_table_id'])



#ZEND



#############################################################################
#
#   Google Cloud Video Intelligence
#
#   Video Metadata Tagging
#
#   Usage: file.py --youtube_url YOUTUBE_URL --bucket_name BUCKET_NAME
#          file.py --youtube_url=https://www.youtube.com/watch?v=imm6OR605UI --bucket_name=zmiscbucket1
#
#   Dependencies:
#       pip install --upgrade google-cloud-videointelligence
#       pip install --upgrade google-cloud-storage
#       pip install pytube
#
#   References:
#       https://cloud.google.com/video-intelligence/docs/
#       https://github.com/nficano/pytube
#       The Video Intelligence API supports common video formats, including .MOV, .MPEG4, .MP4, and .AVI
#
#############################################################################



from google.cloud import videointelligence
from google.cloud import storage
from pytube import YouTube
import argparse
import time



def save_youtube_video(youtube_url):
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



def process_video_in_gcs(gcs_filepath):
    print('[ INFO ] Processing video at {}'.format(gcs_filepath))
    
    video_client = videointelligence.VideoIntelligenceServiceClient()
    features     = [videointelligence.enums.Feature.LABEL_DETECTION]
    operation    = video_client.annotate_video(gcs_filepath, features=features)
    result       = operation.result(timeout=90)
    
    segment_labels = result.annotation_results[0].segment_label_annotations
    shots = result.annotation_results[0].shot_label_annotations
    
    shot_metadata = {}
    for shot in shots:
        entity   = shot.entity.description
        #category = shot.category_entities[0].description
        segments = shot.segments
        shot_metadata[entity] = { "count": len(list(segments)), "shot_segments":list(segments) }
    
    print('[ INFO ] Printing all identified entities and how many times they were seen in the video...')
    time.sleep(3)
    for k,v in shot_metadata.items():
        print((k, v['count']))
    
    return all_labels_identified



if __name__ == "__main__":
    
    # Arguments - Only used for testing
    #args =  {
    #            "youtube_url": "https://www.youtube.com/watch?v=imm6OR605UI",
    #            "bucket_name": "zmiscbucket1"
    #        }
    
    # Arguments
    ap = argparse.ArgumentParser()
    ap.add_argument("--youtube_url", required=True, help="YouTube URL")
    ap.add_argument("--bucket_name", required=True, help="Google Cloud Storage bucket name")
    args = vars(ap.parse_args())
    
    # Download Youtube video as .mp4 file to local
    local_filepath = save_youtube_video(args["youtube_url"])
    
    # Upload .mp4 file to Google Cloud Storage (GCS)
    gcs_filepath = upload_to_gcs(args["bucket_name"], local_filepath)
    
    # Process .mp4 video file, stored on Google Cloud Storage (GCS)
    process_video_in_gcs(gcs_filepath)



#ZEND

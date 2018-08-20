
#############################################################################
#
#   Google Cloud Video Intelligence API
#
#   References:
#       https://cloud.google.com/video-intelligence/docs/
#       https://github.com/nficano/pytube
#       The Video Intelligence API supports common video formats, including .MOV, .MPEG4, .MP4, and .AVI
#
#
#   Dependencies:
#       pip install --upgrade google-cloud-videointelligence
#       pip install --upgrade google-cloud-storage
#       pip install pytube
#
#
#############################################################################


from google.cloud import videointelligence
from google.cloud import storage
from pytube import YouTube



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
    return local_filepath, youtube_filename



def upload_to_gcs(bucket_name, local_filepath):
    ''' Upload local file (.mp4) to Google Cloud Storage '''
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket_name)
    destination_blob_name = local_filepath.split('/')[-1]
    blob = bucket.blob(destination_blob_name)
    blob.upload_from_filename(local_filepath)
    print('[ INFO ] File {} uploaded to gs://{}/{}'.format(
        local_filepath,
        bucket_name,
        destination_blob_name))



def process_video_in_gcs(gcs_path):
    
    video_client = videointelligence.VideoIntelligenceServiceClient()
    features     = [videointelligence.enums.Feature.LABEL_DETECTION]
    operation    = video_client.annotate_video(gcs_path, features=features)
    result       = operation.result(timeout=90)
    
    segment_labels = result.annotation_results[0].segment_label_annotations
    shots = result.annotation_results[0].shot_label_annotations
    
    shot_metadata = {}
    for shot in shots:
        label    = shot.entity.description
        segments = shot.segments
        shot_metadata[label] = list(segments)
    
    all_labels_identified = list(shot_metadata)
    
    return all_labels_identified



if __name__ == "__main__":
    
    # Arguments
    youtube_url = 'https://www.youtube.com/watch?v=imm6OR605UI'
    bucket_name = 'zmiscbucket1'
    
    local_filepath, youtube_filename = save_youtube_video(youtube_url)
    
    upload_to_gcs(bucket_name, local_filepath)



#ZEND

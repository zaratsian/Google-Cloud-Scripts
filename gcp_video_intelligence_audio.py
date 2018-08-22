

#############################################################################
#
#   Google Cloud Video Intelligence
#
#   Video Audio Transcription
#
#   Usage: 
#
#   Dependencies:
#       pip install --upgrade google-cloud-videointelligence==1.2.0
#       pip install --upgrade google-cloud-storage
#       pip install pytube
#
#   References:
#       https://cloud.google.com/video-intelligence/docs/
#       https://cloud.google.com/video-intelligence/docs/transcription
#       https://github.com/nficano/pytube
#
#############################################################################



from google.cloud import videointelligence_v1p1beta1 as videointelligence
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



def process_videoaudio_in_gcs(gcs_filepath):
    print('[ INFO ] Transcribing video audio at {}'.format(gcs_filepath))
    
    video_client = videointelligence.VideoIntelligenceServiceClient()
    features     = [videointelligence.enums.Feature.SPEECH_TRANSCRIPTION]
    
    config = videointelligence.types.SpeechTranscriptionConfig(
                language_code='en-US',
                #maxAlternatives=1,
                #filterProfanity=False,
                #speechContexts=...,
                #audioTracks=0,
                enable_automatic_punctuation=True
                )
    
    video_context = videointelligence.types.VideoContext(
                speech_transcription_config=config
                )
    
    operation = video_client.annotate_video(
                gcs_filepath, 
                features=features,
                video_context=video_context
                )
    
    print('[ INFO ] Processing video for speech transcription')
    
    result = operation.result(timeout=180)
    
    # There is only one annotation_result since only one video is processed.
    annotation_results   = result.annotation_results[0]
    speech_transcription = annotation_results.speech_transcriptions[0]
    alternatives          = speech_transcription.alternatives
    
    text_blob = ''
    for alternative in alternatives:
        print('Transcript: {}'.format(alternative.transcript))
        print('Confidence: {}\n'.format(alternative.confidence))
        print('Word level information:')
        for word_info in alternative.words:
            word = word_info.word
            start_time = word_info.start_time
            end_time = word_info.end_time
            print('\t{}s - {}s: {}'.format(
                start_time.seconds + start_time.nanos * 1e-9,
                end_time.seconds + end_time.nanos * 1e-9,
                word))
        
        text_blob = text_blob + ' ' + alternative.transcript
    return annotation_results, text_blob




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
    
    # Process .mp4 Audio (within video file), stored on Google Cloud Storage (GCS)
    annotation_results, text_blob = process_videoaudio_in_gcs(gcs_filepath)



#ZEND

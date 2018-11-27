

###############################################################################
#
#   USAGE:
#   download_and_save_video.py --media_url "http://s3-eu-west-1.amazonaws.com/data.spicymango.co.uk/big_buck_bunny_720p_30mb.mp4" --bucket_name "tmp_video_bucket_eurosport"
#
###############################################################################


import requests
import argparse
from google.cloud import storage


def download_url_file(url):
    try:
        print('[ INFO ] Downloading {}'.format(url))
        req = requests.get(url)
        if req.status_code==200:
            # Download and save to /tmp
            output_filepath = '/tmp/{}'.format(url.split('/')[-1])
            open(output_filepath, 'wb').write(req.content)
            print('[ INFO ] Successfully downloaded to /tmp')
            return output_filepath
        else:
            print('[ ERROR ] Status Code: {}'.format(req.status_code))
    except Exception as e:
        print('[ ERROR ] {}'.format(e))



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



if __name__ == "__main__":
    
    # Arguments
    ap = argparse.ArgumentParser()
    ap.add_argument("--media_url",   required=True, help="URL path to video file")
    ap.add_argument("--bucket_name", required=True, help="Google Cloud Storage bucket name")
    args = vars(ap.parse_args())
    
    # Download Youtube video as .mp4 file to local
    local_filepath = download_url_file(url=args["media_url"])
    
    # Upload .mp4 file to Google Cloud Storage (GCS)
    gcs_filepath = upload_to_gcs(args["bucket_name"], local_filepath)




#####################################################################################
#
#   Google Cloud Functions (Python)
#
#   References:
#       https://cloud.google.com/functions/docs/
#
#####################################################################################



# ENV Variables
export cloud_func_name=parse_logs
export cloud_storage_bucket_name=gs://zdataset1



# Create Function (which will be uploaded to Google Cloud Functions)
def parse_cdn_log(data, context):
    """ 
        Background Cloud Function to be triggered by Cloud Storage.
        
        Args:
            data (dict): The Cloud Functions event payload.
            context (google.cloud.functions.Context): Metadata of triggering event.
        Returns:
            None; the output is written to Stackdriver Logging
    """
    
    



# Upload / Deploy function to Google Cloud Functions
# https://cloud.google.com/functions/docs/calling/
gcloud functions deploy $cloud_func_name \
    --runtime python37 \
    --trigger-resource $cloud_storage_bucket_name \
    --trigger-event google.storage.object.finalize



# Delete function from Google Cloud Functions
gcloud functions delete &cloud_func_name



#ZEND

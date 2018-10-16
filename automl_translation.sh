

#####################################################################################
#
#   Google AutoML Translation API
#
#   References:
#       https://cloud.google.com/translate/automl/docs/tutorial
#
#####################################################################################


# Change these to match your project
export PROJECT_ID='zproject201807'
export REGION_NAME='us-central1'


gcloud config set project $PROJECT_ID
gcloud config set compute/region $REGION_NAME


gcloud iam service-accounts create ${PROJECT_ID}-sacct --display-name "${PROJECT_ID}-sacct"
gcloud iam service-accounts list


export GOOGLE_APPLICATION_CREDENTIALS=/home/dzaratsian/zproject201807-2276d47e9c67.json


gcloud projects add-iam-policy-binding $PROJECT_ID \
       --member=serviceAccount:${PROJECT_ID}-sacct@${PROJECT_ID}.iam.gserviceaccount.com \
       --role='roles/automl.editor'


gcloud projects add-iam-policy-binding $PROJECT_ID \
  --member="serviceAccount:custom-vision@appspot.gserviceaccount.com" \
  --role="roles/storage.admin"


gsutil mb -p $PROJECT_ID -c regional -l $REGION_NAME gs://$PROJECT_ID-vcm/


wget https://cloud.google.com/translate/automl/docs/sample/automl-translation-data.zip -O automl-translation-data.zip
unzip automl-translation-data.zip
gsutil cp en*.tsv gs://$PROJECT_ID-vcm/
sed -i -e "s/{project_id}/$PROJECT_ID/g" ./en-es.csv
gsutil cp en-es.csv gs://$PROJECT_ID-vcm/



git clone https://github.com/GoogleCloudPlatform/python-docs-samples.git


'''
Run the create_dataset function to create an empty dataset.
The first parameter gives a name for the dataset (en_es_dataset) and the second and
third parameters specify the source and target languages respectively.
'''
python ./python-docs-samples/translate/automl/automl_translation_dataset.py creat
e_dataset "en_es_dataset" "en" "es"


'''
Run the import_data function to import the training content.
The first parameter is the Dataset ID from the previous step and the second parameter is the URI of en-es.csv.
'''
export DATASET_ID='TRL778149847025493504'
python ./python-docs-samples/translate/automl/automl_translation_dataset.py import_data $DATASET_ID "gs://$PROJECT_ID-vcm/en-es.csv"


'''
Train the Model
'''
python ./python-docs-samples/translate/automl/automl_translation_model.py create_model $DATASET_ID "en_es_test_model"



'''
Evaluate the Model
'''
export MODEL_ID
python ./python-docs-samples/translate/automl/automl_translation_model.py list_model_evaluations $MODEL_ID









#ZEND

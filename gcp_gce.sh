

###################################################################################################
#
#   Cloud Compute Engine (GCE)
#
#   Google Cloud Platform (GCP)
#
#   References:
#   https://cloud.google.com/compute/docs/quickstart-linux
#   https://cloud.google.com/compute/docs/instances/create-start-instance
#   https://cloud.google.com/compute/docs/machine-types#predefined_machine_types
#   https://cloud.google.com/compute/docs/regions-zones/
#
###################################################################################################



# List all of my GCE Instances (both running and stopped instances)
gcloud compute instances list
# Describe status of a certain GCE Instance
gcloud compute instances describe zcompute10



# Create GCE Instance
# https://cloud.google.com/compute/docs/instances/create-start-instance
#
# List available (default) GCE Images
gcloud compute images list | grep -i "ubuntu\|centos\|rhel"
#
#   NAME                            PROJECT            FAMILY  
#   centos-6-v20180716              centos-cloud       centos-6 
#   centos-7-v20180716              centos-cloud       centos-7 
#   ubuntu-1604-xenial-v20180806    ubuntu-os-cloud    ubuntu-1604-lts 
#   ubuntu-1710-artful-v20180612    ubuntu-os-cloud    ubuntu-1710 
#   ubuntu-1804-bionic-v20180806    ubuntu-os-cloud    ubuntu-1804-lts
#   rhel-6-v20180716                rhel-cloud         rhel-6  
#   rhel-7-v20180716                rhel-cloud         rhel-7   
#
#   type = pd-standard OR pd-ssd
#
#   machine-types: https://cloud.google.com/compute/docs/machine-types#predefined_machine_types
#
#   zones: https://cloud.google.com/compute/docs/regions-zones/
#
gcloud compute instances create zcompute10 \
    --image-family ubuntu-1804-lts \
    --image-project ubuntu-os-cloud \
    --create-disk image=ubuntu-1804-bionic-v20180806,image-project=ubuntu-os-cloud,size=20,type=pd-standard \
    --machine-type n1-standard-1 \
    --zone us-east1-c \
    --metadata startup-script='''#! /bin/bash
gsutil cp gs://z-airflow-dags/airflow_simple1.py /tmp/airflow_simple1.py
EOF'''


# Start GCE Intance
gcloud compute instances start zcompute10



# Stop GCE Instance
gcloud compute instances stop zcompute10



# Delete GCE Instance
gcloud compute instances delete zcompute10



#ZEND



######################################################################################
#
#   Google Cloud - Configure Shared VPC for Cloud Composer
#
#   References:
#       https://cloud.google.com/composer/docs/how-to/managing/configuring-shared-vpc
#       
######################################################################################



# Set Host Project (Share VPC) and Service Project (Cloud Composer)
export organization_admin=admin@dynamicprototypes.com
export host_project=zsharedvpc10
export host_admin=admin@dynamicprototypes.com
export service_project=zcloudcomposer10
export shared_network_name=zsharednet
export subnet_region=us-east4



# Prepare Organization
# https://cloud.google.com/vpc/docs/provisioning-shared-vpc#prepare_your_organization
gcloud auth login $organization_admin
gcloud organizations list
echo "Enter Organization ID..."
read organization_id
echo "Using Organization ID: $organization_id"
# Prevent accidental deletion of host projects
gcloud beta resource-manager org-policies enable-enforce --organization $organization_id compute.restrictXpnProjectLienRemoval
# Nominate a Shared VPC Admin
gcloud organizations add-iam-policy-binding $organization_id --member 'user:$host_admin' --role "roles/compute.xpnAdmin"
gcloud auth revoke $organization_admin



# Enable Kubernetes Engine API in your projects 
gcloud services enable container.googleapis.com --project $host_project
gcloud services enable container.googleapis.com --project $service_project



# Create a new network and subnetwork in the host project
gcloud compute networks create $shared_network_name \
    --subnet-mode custom \
    --project $host_project

gcloud compute networks subnets create tier-1 \
    --project $host_project \
    --network $shared_network_name \
    --range 10.0.4.0/22 \
    --region $subnet_region \
    --secondary-range tier-1-services=10.0.32.0/20,tier-1-pods=10.4.0.0/14

gcloud compute networks subnets create tier-2 \
    --project $host_project \
    --network $shared_network_name \
    --range 172.16.4.0/22 \
    --region $subnet_region \
    --secondary-range tier-2-services=172.16.16.0/20,tier-2-pods=172.20.0.0/14 



# Enabling shared VPC and granting roles
gcloud compute shared-vpc enable $host_project



# Attach your first service project to your host project:
gcloud compute shared-vpc associated-projects add \
    $service_project \
    --host-project $host_project



# Get the IAM policy for the tier-1 subnet
gcloud beta compute networks subnets get-iam-policy tier-1 \
   --project $host_project \
   --region $subnet_region

'''
The output contains an etag field. Make a note of the etag value.

Create a file named tier-1-policy.yaml that has this content:

bindings:
- members:
  - serviceAccount:[SERVICE_PROJECT_1_NUM]@cloudservices.gserviceaccount.com
  - serviceAccount:service-[SERVICE_PROJECT_1_NUM]@container-engine-robot.iam.gserviceaccount.com
  role: roles/compute.networkUser
etag: [ETAG_STRING]

where [ETAG_STRING] is the etag value that you noted previously.
'''



# Set the IAM policy for the tier-1 subnet
gcloud beta compute networks subnets set-iam-policy tier-1 \
    tier-1-policy.yaml \
    --project $host_project \
    --region $subnet_region



# Next get the IAM policy for the tier-2 subnet
gcloud beta compute networks subnets get-iam-policy tier-2 \
   --project $host_project \
   --region $subnet_region

'''
The output contains an etag field. Make a note of the etag value.

Create a file named tier-2-policy.yaml that has this content:

bindings:
- members:
  - serviceAccount:[SERVICE_PROJECT_2_NUM]@cloudservices.gserviceaccount.com
  - serviceAccount:service-[SERVICE_PROJECT_2_NUM]@container-engine-robot.iam.gserviceaccount.com
  role: roles/compute.networkUser
etag: [ETAG_STRING]

where: [ETAG_STRING] is the etag value that you noted previously
'''



# Set the IAM policy for the tier-2 subnet
gcloud beta compute networks subnets set-iam-policy tier-2 \
    tier-2-policy.yaml \
    --project $host_project \
    --region $subnet_region



# Granting the Host Service Agent User role
gcloud projects add-iam-policy-binding $host_project \
    --member serviceAccount:service-[SERVICE_PROJECT_1_NUM]@container-engine-robot.iam.gserviceaccount.com \
    --role roles/container.hostServiceAgentUser



# Creating a cluster in your first service project
gcloud beta container clusters create tier-1-cluster \
    --project $service_project \
    --zone=$subnet_region-a \
    --enable-ip-alias \
    --network projects/$host_project/global/networks/$shared_network_name \
    --subnetwork projects/$host_project/regions/$subnet_region/subnetworks/tier-1 \
    --cluster-secondary-range-name tier-1-pods \
    --services-secondary-range-name tier-1-services

gcloud compute instances list --project [SERVICE_PROJECT_1_NUM]



''' ...more... '''



#ZEND



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
export $subnet_region=us-east4



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



#ZEND

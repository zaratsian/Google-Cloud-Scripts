

#####################################################################################
#
#   Setup new Cloud Identity Account & GCP Organization
#   Notes Sep2018
#
#   References:
#       https://domains.google
#       https://cloud.google.com/dns/docs/
#       https://cloud.google.com/identity/
#
#####################################################################################



# Purchase a Domain Name
https://domains.google



# Within GCP, create a GCE instance to host the domain
1. Compute Engine > Create Instance
2. Enable HTTP traffic
3. Instance nginx or similar
# NOTE: You could also grab a pre-built instance from the Marketplace



# Map the domain name to the newly created instance
Follow this quickstart to add DNS Zone: https://cloud.google.com/dns/quickstart
# NOTE: It may take up to 48 hours for changes to propgate.



# Sign-up for Cloud Identity
1. Within GCP Console, goto "IAM & admin" > "Identity & Organization"
2. Click "sign up"
3. Login to https://admin.google.com
4. Within admin.google.com, "verify Domain" (https://support.google.com/a/answer/183895?authuser=2#generic_TXT)
5. Within admin.google.com, "Add Users"



# Create a Project (under the new Organization) within Cloud Console (using the new cloud identity domain and login)
Go to console.cloud.google.com



#ZEND

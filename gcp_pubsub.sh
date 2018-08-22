

#############################################################################
#
#   Google Pub/Sub
#
#   References:
#       https://cloud.google.com/pubsub/docs/overview
#       https://googlecloudplatform.github.io/google-cloud-python/latest/pubsub/
#
#   Dependencies:
#       pip install google-cloud-pubsub
#
#############################################################################


# List PubSub Topics
gcloud pubsub topics list


# List PubSub Subscriptions
gcloud pubsub subscriptions list


# Create PubSub Topic
gcloud pubsub topics create my_topic

###########################################################
#   Subscriber
###########################################################
# To receive messages, you need to create subscriptions. 
# A subscription needs to have a corresponding topic.
# ack-deadline is the amount of time (60 sec) that the subscriber has to acknowledge a message.
gcloud pubsub subscriptions \
    create my_subscriber_name --topic my_topic \
    --ack-deadline=60


# Pull messages from a subscription
gcloud pubsub subscriptions \
    pull --auto-ack --limit=2 my_subscriber_name


###########################################################
#   Publisher
###########################################################
gcloud pubsub topics publish my_topic \
    --message hello


#ZEND

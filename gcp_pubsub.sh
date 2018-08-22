

#############################################################################
#
#   Google Pub/Sub
#
#############################################################################


# Create PubSub Topic
gcloud pubsub topics create my_topic


# To receive messages, you need to create subscriptions. 
# A subscription needs to have a corresponding topic.
gcloud pubsub subscriptions \
    create my_subscriber_name --topic my_topic \
    --ack-deadline=60





#ZEND

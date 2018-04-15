

###################################################################################################
#
#   GCP PubSub Subscriber
#
#   Usage:  pubsub_subscriber.py <project_id> <topic_name> <subscriber_name>
#
###################################################################################################


import sys, os
from google.cloud import pubsub
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/Users/dzaratsian/gcpkey.json"



def gcp_pubsub_subscribe(project_id, topic_name, subscription_name):
    
    subscriber      = pubsub.SubscriberClient()
    topic           = 'projects/' + str(project_id) + '/topics/' + str(topic_name)
    subscriber_name = 'projects/' + str(project_id) + '/subscriptions/' + str(subscription_name)
    
    #subscriber.create_subscription(subscriber_name, topic)
    subscription = subscriber.subscribe(subscriber_name,)
    
    def callback(message):
        print(message.data)
        message.ack()
    
    future = subscription.open(callback)
    future.result()


if __name__ == "__main__":
    
    if len(sys.argv) == 4:
            project_id        = sys.argv[1]
            topic_name        = sys.argv[2]
            subscription_name = sys.argv[3]
    else:
        print('[ Usage ] pubsub_subscriber.py <project_id> <topic_name> <subscriber_name>')
        sys.exit()
    
    gcp_pubsub_subscribe(project_id, topic_name, subscription_name)



#ZEND


################################################################################
#
#   Google Cloud Firestore
#
#   References:
#       https://cloud.google.com/firestore/docs/
#       https://cloud.google.com/firestore/docs/manage-data/add-data
#       https://cloud.google.com/firestore/docs/query-data/get-data
#
#   Dependencies:
#       pip install --upgrade google-cloud-firestore
#
################################################################################


from google.cloud import firestore

firestore_client = firestore.Client()

def add_to_firestore(collection_id, doc_id, dict):
    ''' 
    Add / Write document to Google Cloud Firestore  
    .add() and .set() are equivalent, so use either 
    
    # Example dict
    dict = {
        'first': 'Dan',
        'last':  'Z',
        'msg':   'Test message',
        'value': 123
    }
    '''
    #firestore_client = firestore.Client()
    doc_ref = firestore_client.collection(collection_id).document(doc_id)
    doc_ref.set(dict)


def update_firestore(collection_id, doc_id, dict_update):
    ''' 
    Update document within Google Cloud Firestore
    
    # Example dict
    dict_update = {
        'value': 456
    }
    '''
    #firestore_client = firestore.Client()
    doc_ref = firestore_client.collection(collection_id).document(doc_id)
    doc_ref.update(dict_update)


def query_firestore(collection_id):
    ''' 
    Query Google Cloud Firestore
    
    users_ref = firestore_client.collection('users').where('value', '>', '300')
    '''
    #firestore_client = firestore.Client()
    users_ref = firestore_client.collection(collection_id)
    docs = users_ref.stream()
    
    json_out = {}
    for doc in docs:
        json_out[doc.id] = doc.to_dict()
    
    return json_out


'''
Example:

collection_id = 'users'
doc_id        = 'd.zaratsian@gmail.com'

dict = {
        'first': 'Dan',
        'last':  'Z',
        'msg':   'Test message',
        'value': 123
}

add_to_firestore(collection_id, doc_id, dict)

query_firestore(collection_id)

dict_update = {
        'value': 456
}

update_firestore(collection_id, doc_id, dict_update)

query_firestore(collection_id)


'''
        
        

#ZEND

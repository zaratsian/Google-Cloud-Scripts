
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


def add_to_firestore(collection_id, doc_id, dict):
    ''' 
    Add / Write document to Google Cloud Firestore  
    .add() and .set() are equivalent, so use either 
    
    # Example dict
    dict = {
        'first': 'Dan',
        'last':  'Z',
        'msg':   'Test message'
        'value': 123
    }
    '''
    db = firestore.Client()
    doc_ref = db.collection(collection_id).document(doc_id)
    doc_ref.set(dict)


def update_firestore(collection_id, doc_id, dict_update):
    ''' 
    Update document within Google Cloud Firestore
    
    # Example dict
    dict_update = {
        'value': 456
    }
    '''
    
    db = firestore.Client()
    doc_ref = db.collection(collection_id).document(doc_id)
    doc_ref.update(dict_update)


def query_firestore(collection_id):
    ''' 
    Query Google Cloud Firestore
    
    users_ref = db.collection('users').where('first', '==', 'Dan').where('value', '>', 300).stream()
    '''
    
    db = firestore.Client()
    users_ref = db.collection(collection_id)
    docs = users_ref.get()
    
    for doc in docs:
        print(u'{} => {}'.format(doc.id, doc.to_dict()))


#ZEND

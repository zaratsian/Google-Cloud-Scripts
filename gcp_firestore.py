
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
    ''' Add / Write document to Google Cloud Firestore  '''
    ''' .add() and .set() are equivalent, so use either '''
    
    # Example dict
    #dict = {
    #    u'first': u'Ada',
    #    u'last': u'Lovelace',
    #    u'born': 1815
    #}
    
    db = firestore.Client()
    doc_ref = db.collection(collection_id).document(doc_id)
    doc_ref.set(dict)



def update_firestore(collection_id, doc_id, dict_update):
    ''' Update document within Google Cloud Firestore  '''
    
    # Example Dict
    #dict_update = {
    #    u'field_to_update': 'new_value'
    #}
    
    db = firestore.Client()
    doc_ref = db.collection(collection_id).document(doc_id)
    doc_ref.update(dict_update)



def query_firestore(collection_id):
    ''' Query Google Cloud Firestore '''
    
    db = firestore.Client()
    users_ref = db.collection(collection_id)
    docs = users_ref.get()
    
    for doc in docs:
        print(u'{} => {}'.format(doc.id, doc.to_dict()))



#ZEND

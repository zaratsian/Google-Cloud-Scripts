from google.cloud import spanner


def query_spanner(spanner_instance_id, spanner_database_id, spanner_table, item_id):
    
    spanner_client = spanner.Client()
    instance = spanner_client.instance(spanner_instance_id)
    database = instance.database(spanner_database_id)
    
    with database.snapshot() as snapshot:
        results = snapshot.execute_sql(
            f'''SELECT * 
            FROM {spanner_table}
            WHERE ItemId = '{item_id}'
            '''
        )
        matches = [row for row in results]
    
    return matches


def spanner_insert(spanner_instance_id, spanner_database_id, spanner_table, rows_to_insert):
    '''
    rows_to_insert = [
        {'name':'danny', 'age': 50},
        {'name':'rusty', 'age': 40},
        {'name':'linus', 'age': 30},
    ]
    '''
    spanner_client = spanner.Client()
    instance = spanner_client.instance(spanner_instance_id)
    database = instance.database(spanner_database_id)
    
    column_names = ', '.join(list(rows_to_insert[0]))
    
    query = f'''INSERT INTO {spanner_table} ({column_names}) VALUES '''
    query +=  ', '.join([f"{tuple(row.values())}" for row in rows_to_insert])
    
    def insert_into_spanner(transaction):
        tx = transaction.execute_update(
        f'''INSERT INTO {spanner_table} ({column_names}) VALUES '''
        for row in rows_to_insert:
            f"{tuple(row.values())},"
        )
    
    database.run_in_transaction(insert_into_spanner)

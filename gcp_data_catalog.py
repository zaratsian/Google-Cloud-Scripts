
##########################################################
#
#   Google Cloud Data Catalog (Example)
#
##########################################################
'''
requirements.txt

google-cloud-datacatalog==3.0.0
google-cloud-bigquery==2.7.0
googleapis-common-protos==1.52.0
protobuf==3.14.0
'''

import re
import datetime
from google.cloud import bigquery
from google.cloud import datacatalog_v1
from google.protobuf.timestamp_pb2 import Timestamp


##########################################################
#
#   Config
#
##########################################################

project_id  = 'zproject201807'
location    = 'us-central1'

bq_dataset  = 'medication_ds'
bq_table    = 'medication_reviews'
outdated_if = 10 # days old

tag_template_name = 'DZ Tag Template'
tag_template_id   = re.sub('[^a-zA-Z0-9\_]','_',tag_template_name).lower()
tag_name          = 'dz_tag'

##########################################################
#
#   Functions
#
##########################################################

def bq_query(query, location='US'):
    try:
        client = bigquery.Client()
        
        query_job = client.query(query, location=location)
        
        rows = []
        for i, row in enumerate(query_job):
            rows.append(row)
        
        print('[ INFO ] Query returned {} row(s)'.format( len(rows) ))
        return rows
    except Exception as e:
        print('[ ERROR] {}'.format(e))



##########################################################
#
#   Main
#
##########################################################

datacatalog_client = datacatalog_v1.DataCatalogClient()

# --------------------------------------------------------
# Create a Tag Template
# --------------------------------------------------------
tag_template = datacatalog_v1.types.TagTemplate()

tag_template.display_name = tag_template_name

tag_template.fields['source'] = datacatalog_v1.types.TagTemplateField()
tag_template.fields['source'].display_name = 'Source of data asset'
tag_template.fields['source'].type_.primitive_type = datacatalog_v1.types.FieldType.PrimitiveType.STRING

tag_template.fields['num_rows'] = datacatalog_v1.types.TagTemplateField()
tag_template.fields['num_rows'].display_name = 'Number of rows in data asset'
tag_template.fields['num_rows'].type_.primitive_type = datacatalog_v1.types.FieldType.PrimitiveType.DOUBLE

tag_template.fields['last_updated'] = datacatalog_v1.types.TagTemplateField()
tag_template.fields['last_updated'].display_name = 'Asset last update date'
tag_template.fields['last_updated'].type_.primitive_type = datacatalog_v1.types.FieldType.PrimitiveType.TIMESTAMP

tag_template.fields['outdated'] = datacatalog_v1.types.TagTemplateField()
tag_template.fields['outdated'].display_name = 'Outdated'
tag_template.fields['outdated'].type_.primitive_type = datacatalog_v1.types.FieldType.PrimitiveType.BOOL

tag_template.fields['has_pii'] = datacatalog_v1.types.TagTemplateField()
tag_template.fields['has_pii'].display_name = 'Has PII'
tag_template.fields['has_pii'].type_.primitive_type = datacatalog_v1.types.FieldType.PrimitiveType.BOOL

tag_template.fields['pii_type'] = datacatalog_v1.types.TagTemplateField()
tag_template.fields['pii_type'].display_name = 'PII type'

for display_name in ['EMAIL', 'SOCIAL SECURITY NUMBER', 'NONE']:
    enum_value = datacatalog_v1.types.FieldType.EnumType.EnumValue(display_name = display_name)
    tag_template.fields['pii_type'].type_.enum_type.allowed_values.append(enum_value)

expected_template_name = datacatalog_v1.DataCatalogClient.tag_template_path(project_id, location, tag_template_id)

# Delete any pre-existing Template with the same name
try:
    datacatalog_client.delete_tag_template(name=expected_template_name, force=True)
    print('Deleted template: {}'.format(expected_template_name))
except:
    print('Cannot delete template: {}'.format(expected_template_name))

# Create the Tag Template
try:
    tag_template = datacatalog_client.create_tag_template(
        parent='projects/{}/locations/{}'.format(project_id,location),
        tag_template_id=tag_template_id,
        tag_template=tag_template
    )
    print('Created template: {}'.format(tag_template.name))
except OSError as e:
    print('Cannot create template: {}'.format(tag_template_id))
    print('{}'.format(e))

# --------------------------------------------------------
# Lookup Data Catalog's Entry referring to the table.
# --------------------------------------------------------
resource_name = '//bigquery.googleapis.com/projects/{}/datasets/{}/tables/{}'.format(project_id,bq_dataset,bq_table)
table_entry   = datacatalog_client.lookup_entry(request={"linked_resource": resource_name})

# --------------------------------------------------------
# Attach a Tag to the table.
# --------------------------------------------------------
tag = datacatalog_v1.types.Tag()

# Get BQ Metadata
bq_metadata = bq_query('''SELECT * FROM `zproject201807.medication_ds.__TABLES__` where lower(table_id) = lower('medication_reviews')''', location='US')

tag.template = 'projects/{}/locations/{}/tagTemplates/{}'.format(project_id,location,tag_template_id)
tag.name     = tag_name

tag.fields['source'] = datacatalog_v1.types.TagField()
tag.fields['source'].string_value = 'Created by dz'

tag.fields['num_rows'] = datacatalog_v1.types.TagField()
tag.fields['num_rows'].double_value = bq_metadata[0]['row_count']

timestamp = Timestamp()
timestamp.FromMilliseconds(bq_metadata[0]['last_modified_time'])
tag.fields['last_updated'] = datacatalog_v1.types.TagField()
tag.fields['last_updated'].timestamp_value = timestamp

bq_datetimestamp = datetime.datetime.fromtimestamp(bq_metadata[0]['last_modified_time']/1000)
tag.fields['outdated'] = datacatalog_v1.types.TagField()
tag.fields['outdated'].bool_value = bq_datetimestamp < datetime.datetime.now()-datetime.timedelta(days=outdated_if)
#tag.fields['outdated'].bool_value = bq_datetimestamp < datetime.datetime.strptime('Oct 25, 2020','%b %d, %Y')

tag.fields['has_pii'] = datacatalog_v1.types.TagField()
tag.fields['has_pii'].bool_value = False

tag.fields['pii_type'] = datacatalog_v1.types.TagField()
tag.fields['pii_type'].enum_value.display_name = 'NONE'

tag = datacatalog_client.create_tag(parent=table_entry.name, tag=tag)
print('Created tag: {}'.format(tag.name))




'''

##########################################################
#
#   Data Catalog Search
#
##########################################################

from google.cloud import datacatalog_v1

# Config
project_id    = 'zproject201807'
search_string = 'tag:dz_tag_template.outdated=true'

datacatalog = datacatalog_v1.DataCatalogClient()

scope = datacatalog_v1.types.SearchCatalogRequest.Scope()
scope.include_project_ids.append(project_id)

results = datacatalog.search_catalog(scope=scope,query=search_string)
results

'''



#ZEND

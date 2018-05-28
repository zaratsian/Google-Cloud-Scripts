
################################################################################################################
#
#   GCP - Natural Language API
#
#   https://cloud.google.com/natural-language/
#   https://cloud.google.com/natural-language/quotas
#
#   https://google-cloud-python.readthedocs.io/en/latest/language/usage.html
#   https://github.com/GoogleCloudPlatform/google-cloud-python
#
#   https://cloud.google.com/sdk/docs/
#   https://cloud.google.com/storage/docs/gsutil
#
################################################################################################################

'''
pip install --upgrade google-cloud-bigquery
export GOOGLE_APPLICATION_CREDENTIALS="/Users/dzaratsian/gcpkey.json"
'''

import os
from google.cloud import language

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/Users/dzaratsian/gcpkey.json"

client = language.LanguageServiceClient()

################################################################################################################
#   Entity Extraction
################################################################################################################

document = language.types.Document(
    content='Michelangelo Caravaggio, Italian painter, is '
            'known for "The Calling of Saint Matthew".',
    type=language.enums.Document.Type.PLAIN_TEXT,
)


response = client.analyze_entities(
    document=document,
    encoding_type='UTF32',
)

################################################################################################################
#   Sentiment
################################################################################################################

document = language.types.Document(
    content='Dan said jogging is not very fun. Boxing and lifting weights are my favorite!',
    type='PLAIN_TEXT',
    )

response = client.analyze_sentiment(
    document=document,
    encoding_type='UTF32',
)

response = client.analyze_entity_sentiment(
    document=document,
    encoding_type='UTF32',
)


################################################################################################################
#   Sentiment
################################################################################################################

document = language.types.Document(
    content='''At some point in the future, while riding along in a car, a kid may ask their parent about a distant time in the past when people used steering wheels and pedals to control an automobile. Of course, the full realization of the “auto” part of the word — in the form of fully autonomous automobiles — is a long way off, but there are nonetheless companies trying to build that future today.

However, changing the face of transportation is a costly business, one that typically requires corporate backing or a lot of venture funding to realize such an ambitious goal. A recent funding round, some $128 million raised in a Series A round by Shenzhen-based Roadstar.ai, got us at Crunchbase News asking a question: Just how many independent, well-funded autonomous vehicles startups are out there?

In short, not as many as you’d think. To investigate further, we took a look at the set of independent companies in Crunchbase’s “autonomous vehicle” category that have raised $50 million or more in venture funding. After a little bit of hand filtering, we found that the companies mostly shook out into two broad categories: those working on sensor technologies, which are integral to any self-driving system, and more “full-stack” hardware and software companies, which incorporate sensors, machine-learned software models and control mechanics into more integrated autonomous systems.''',
    type='PLAIN_TEXT',
    )

response = client.classify_text(document)



'''
...more...
https://cloud.google.com/natural-language/docs/classify-text-tutorial
'''




#ZEND

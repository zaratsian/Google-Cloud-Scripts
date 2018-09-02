

#############################################################################
#
#   Google Cloud Vision (Image Analysis)
#
#   Usage:  file.py <path_to_img>
#
#   Dependencies:
#       pip install --upgrade google-cloud-vision
#
#   References:
#       https://cloud.google.com/vision/docs/libraries
#       https://github.com/nficano/pytube
#
#############################################################################



import os,sys
import io
from google.cloud import vision
from google.cloud.vision import types



def image_label_detection(image_filepath):
    
    # Instantiates a client
    client = vision.ImageAnnotatorClient()
    
    # Loads the image into memory
    with io.open(image_filepath, 'rb') as image_file:
        content = image_file.read()
    
    image = types.Image(content=content)
    
    # Performs label detection on the image file
    response = client.label_detection(image=image)
    labels = response.label_annotations
        
    print('Labels:')
    for label in labels:
        print(label.description)



def image_tag_web_entities(image_filepath):
    """Detects web annotations given an image."""
    client = vision.ImageAnnotatorClient()
    
    with io.open(image_filepath, 'rb') as image_file:
        content = image_file.read()
    
    image = vision.types.Image(content=content)
    
    response = client.web_detection(image=image)
    annotations = response.web_detection
    
    if annotations.best_guess_labels:
        for label in annotations.best_guess_labels:
            print('\nBest guess label: {}'.format(label.label))
    
    if annotations.pages_with_matching_images:
        print('\n{} Pages with matching images found:'.format(
            len(annotations.pages_with_matching_images)))
        
        for page in annotations.pages_with_matching_images:
            print('\n\tPage url   : {}'.format(page.url))
            
            if page.full_matching_images:
                print('\t{} Full Matches found: '.format(
                       len(page.full_matching_images)))
                
                for image in page.full_matching_images:
                    print('\t\tImage url  : {}'.format(image.url))
            
            if page.partial_matching_images:
                print('\t{} Partial Matches found: '.format(
                       len(page.partial_matching_images)))
                
                for image in page.partial_matching_images:
                    print('\t\tImage url  : {}'.format(image.url))
    
    if annotations.web_entities:
        print('\n{} Web entities found: '.format(
            len(annotations.web_entities)))
        
        for entity in annotations.web_entities:
            print('\n\tScore      : {}'.format(entity.score))
            print(u'\tDescription: {}'.format(entity.description))
    
    if annotations.visually_similar_images:
        print('\n{} visually similar images found:\n'.format(
            len(annotations.visually_similar_images)))
        
        for image in annotations.visually_similar_images:
            print('\tImage url    : {}'.format(image.url))



if __name__ == "__main__":
    
    image_filepath = sys.argv[1]
    
    image_label_detection(image_filepath)
    
    image_tag_web_entities(image_filepath)



#ZEND

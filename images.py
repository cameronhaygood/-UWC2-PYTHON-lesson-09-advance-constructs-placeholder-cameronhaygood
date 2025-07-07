
from loguru import logger
from peewee import IntegrityError

from socialnetwork_model import insert_table, search_table, update_table, delete_table, Pictures

# Add Image to Pictures Table
image_insert = insert_table(Pictures)

def add_image(user_id, tags):
    '''Finds the last image ID in the Pictures table and increments it by 1'''
    image_id = find_next_image_id()
    image_data = {'picture_id':f"{image_id}", 'user_id': user_id, 'tags': tags}
    if image_insert(**image_data) is True:
        logger.info(f'Added {image_id} image to database')
        return True
    else:
        logger.error(f'Integrity Error adding image: {image_id}, {user_id}, {tags}')
        return False

def find_next_image_id():
    '''Cycles through Picture IDs to find next unique ID'''
    counter = 1
    while True:
        next_unique_id = str(counter).zfill(10)
        logger.debug(f'Testing if {next_unique_id} exists')
        if image_search(picture_id=next_unique_id) is None:
            logger.debug(f'Returning {next_unique_id}')
            return next_unique_id
        counter += 1

# Search Images
def search_image():
    '''Curries the search function to the Pictures table, then searches for picture_id in that table'''
    _image_search = search_table(Pictures)

    # All we want for this inner function is user_id and we can now search for it
    def search(picture_id):
        nonlocal _image_search
        return _image_search(picture_id=picture_id)

    return search
image_search = search_image()




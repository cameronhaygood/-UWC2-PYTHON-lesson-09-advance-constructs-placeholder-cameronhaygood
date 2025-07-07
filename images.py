
from loguru import logger
from peewee import IntegrityError

from socialnetwork_model import insert_table, search_table, update_table, delete_table, Pictures

# Add Image to Pictures Table
image_insert = insert_table(Pictures)

def add_image(user_id, tags):
    '''Finds the last image ID in the Pictures table and increments it by 1'''
    image_counter = 1
    image_data = {'picture_id':f"{image_counter:010d}", 'user_id': user_id, 'tags': tags}
    if image_insert(**image_data) is True:
        logger.info(f'Added {image_counter} image to database')
        image_counter += 1
        return True
    else:
        logger.error(f'Integrity Error adding image: {image_counter}, {user_id}, {tags}')
        return False



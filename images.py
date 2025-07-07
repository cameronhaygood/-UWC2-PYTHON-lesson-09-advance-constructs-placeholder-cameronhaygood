
from loguru import logger

from socialnetwork_model import insert_table, search_table, update_table, delete_table, Pictures

# Add Image to Pictures Table
image_insert = insert_table(Pictures)

def add_image():
    '''Finds the last image ID in the Pictures table and increments it by 1'''
    image_counter = 0



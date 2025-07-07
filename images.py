import os
from pathlib import Path

from loguru import logger
from peewee import IntegrityError

from socialnetwork_model import insert_table, search_table, update_table, delete_table, Pictures

PICTURE_DIR = "pictures/"
path = Path.cwd() / PICTURE_DIR

# Add Image to Pictures Table
image_insert = insert_table(Pictures)

def add_image(user_id, tags):
    '''Finds the last image ID in the Pictures table and increments it by 1'''
    image_id = find_next_image_id()
    output_dir = convert_tags_to_dir(tags, user_id)
    image_data = {'picture_id':f"{image_id}", 'user_id': user_id, 'tags': tags}
    os.makedirs(output_dir, exist_ok=True)
    filepath = os.path.join(output_dir, f"{image_id}.png")
    with open(filepath, 'w') as new_image:
        new_image.write(str(image_data))
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

def convert_tags_to_dir(tags, user_id):
    tags = tags.replace('#', '').split()
    logger.debug(tags)
    tags.sort()
    output_dir = PICTURE_DIR+f"{user_id}/"+"/".join(tags)
    logger.debug(output_dir)
    return output_dir

def list_user_images(_path):
    if _path.is_file():
        # Stop only at .png files
        if _path.suffix == '.png':
            final_path_data = _path.split('//')
            # path follows the format 'pictures/user_id/tags/file'
            # Second value is user_id, third-second to last is tags, last is image
            file_data = (final_path_data[1], final_path_data[2:-1], final_path_data[-1])
            logger.debug (f"Tuple generated for {final_path_data[1]}: {file_data}")
    elif 'venv' in str(_path.absolute()):
        # Skip the venv folders
        pass
    else:
        # Since it's a directory, let's recurse into them
        for i in _path.iterdir():
            list_user_images(i)

# Search Images
def search_image():
    '''Curries the search function to the Pictures table, then searches for picture_id in that table'''
    _image_search = search_table(Pictures)

    # All we want for this inner function is picture_id and we can now search for it
    def search(picture_id):
        nonlocal _image_search
        return _image_search(picture_id=picture_id)

    return search
image_search = search_image()




from app.common import file_io
import time


__frames = []
__count_time = ""

# http://stackoverflow.com/questions/26392336/importing-images-from-a-directory-python

def init_slideshow():
    print("init")
    global __frames
    __frames = file_io.get_images_as_byte_array("/resources/static/uploads/favorites", ".jpg")


def get_slideshow_frame(original_frame):
    if len(__frames) > 0:
        img = __frames[0]
        return img
    else:
        return original_frame

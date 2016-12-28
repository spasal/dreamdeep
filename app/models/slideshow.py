from app.common import file_io
import time


__frames = []
__count_time = ""

# http://stackoverflow.com/questions/26392336/importing-images-from-a-directory-python

def init_slideshow():
    print("init")
    ''''tmp_frames = file_io.get_exif_files("/resources/static/uploads/favorites")
    tmp_frame_paths = [x['path'] for x in tmp_frames]
    for path in tmp_frame_paths:
        print(path)
        tmp_img = open(path)
        __frames.append(tmp_img)

    print(__frames)
    __count_time = time.time()'''
    global __frames
    __frames = file_io.get_images_as_byte_array("/resources/static/uploads/favorites", ".jpg")


def get_slideshow_frame():
    if len(__frames) > 0:
        img = __frames[0]
        return img
    else:
        return None

from app.common import file_io
import time


__frames = []
__count_time = 4
__start_time = ""
__index = 0


def init_slideshow():
    print("init")
    global __frames
    __frames = file_io.get_images_as_byte_array("/resources/static/uploads/favorites", ".jpg")

def get_slideshow_frame(original_frame):
    global __start_time
    global __index

    if len(__frames) > 0:
        if __start_time is "":
            __start_time = time.time()

        elapsed = int(time.time() - __start_time)

        if elapsed > __count_time:
            __index += 1
            __start_time = time.time()
            if __index == len(__frames):
                __index = 0

        return __frames[__index]
    else:
        return original_frame

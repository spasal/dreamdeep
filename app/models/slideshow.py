from app.common import file_io
import time


__frames = []
__frames_content = []
__count_time = ""


def init_slideshow():
    print("init")
    tmp_frames = file_io.get_exif_files("/resources/static/uploads/favorites")
    tmp_frame_paths = [x['path'] for x in tmp_frames]
    for path in tmp_frame_paths:
        print(path)
        tmp_img = open(path)
        img = tmp_img.load()
        __frames.append(tmp_img)
        __frames_content.append(img)

    print(__frames)
    print(__frames_content)
    __count_time = time.time()


def get_slideshow_frame():
    print("getting da frame")
    # tmp_frame = __frames[0]

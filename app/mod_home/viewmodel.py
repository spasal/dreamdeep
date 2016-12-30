from app.models import init_slideshow, get_slideshow_frame
from app.models import VideoCamera, Dream, detect_faces
from app.common import file_io
from flask import Response
import datetime, time
import cv2
import os


class ViewModel(object):
    '''' PUBLIC VIDEOSTREAMER PARAMETER MANIPULATION '''
    def start_dream(self, data):
        if not self.__is_locked:
            self.__iterations, self.__layer = int(data['iteration']), str(data['layer'])
            self.__start_time = time.time()

            self.__is_locked, self.__show_count_down = True, True
            self.__show_general, self.__show_dream = False, False

    def reset_window(self):
        if not self.__is_locked:
            self.__show_general = True
            self.__show_dream, self.__show_count_down = False, False

    def get_default_control_values(self):
        return {
            "iteration": self.__iterations,
            "layers": self.__layers,
            "all_layers": self.__all_layers,
            "default_layer": self.__default_layer
        }


    '''' VIDEOSTREAM GENERATOR + FRAME MANIPULATION '''
    # HTTP VIDEO STREAM RESPONSE
    def video_feed(self):
        return Response(self.__gen(VideoCamera()), mimetype='multipart/x-mixed-replace; boundary=frame')

    # OUTPUT FRAME MANIPULATION
    def __gen(self, camera):
        dream_generator = Dream('resources/app_data/inception')
        self.__layers = dream_generator.get_featured_layers()
        self.__all_layers = dream_generator.get_all_layers()
        self.__default_layer = dream_generator.get_default_layer()
        init_slideshow()

        while True:
            frame = self.__get_frame(camera)

            # do various operations depending on what control is set
            if self.__show_general:
                frame = self.__determine_if_slideshow_and_return_frame(frame)

            if self.__show_dream:
                frame = self.__frame_dream

            if self.__start_dream:
                yield self.__get_jpeg_bytestream(camera.convert_to_jpeg, frame.copy())
                frame = dream_generator.render_deepdream(self.__layer, frame, self.__iterations)
                frame_jpg = camera.convert_to_jpeg(frame)
                self.__handle_dream(frame, frame_jpg)

            if self.__show_count_down:
                frame = self.__count_down(self.__start_time, self.__count, camera, frame)

            # output the result
            yield self.__get_jpeg_bytestream(camera.convert_to_jpeg, frame)


    '''' PRIVATE FRAME MANIPULATION HELPERS '''
    def __get_jpeg_bytestream(self, convert_to_jpeg, frame):
        if type(frame) is not bytearray:
                frame = convert_to_jpeg(frame)
        return (b'--frame\r\n'
                    b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

    def __get_frame(self, camera):
        return camera.get_frame(False)

    def __determine_if_slideshow_and_return_frame(self, frame):
        # todo; split functionality in detect_faces and is_slideshow
        is_slideshow, frame = detect_faces(frame)
        if is_slideshow:
            frame = get_slideshow_frame(frame)

        return frame

    def __handle_dream(self, frame_dream, frame_dream_jpg):
        self.__frame_dream = frame_dream
        self.__save_dream(frame_dream_jpg, self.__layer, self.__iterations)

        self.__start_dream, self.__is_locked = False, False
        self.__show_dream = True

    def __count_down(self, start_time, count, camera, frame):
        elapsed = int(time.time() - start_time)
        resting = count - elapsed
        cv2.putText(img=frame, text=str(resting), org=(300, 300), fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=4, thickness=4, color=(255, 255, 255))

        if resting <= 0:
            self.__show_count_down = False
            self.__start_dream = True
            frame = camera.get_frame(False)

        return frame


    '''' PRIVATE HELPER FUNCTIONS '''
    def __save_dream(self, frame_dream, layer, iterations):
        # get path and filename
        filename = str(time.time()) + ".jpg"
        path = os.path.join(os.getcwd(), "resources", "static", "uploads", "history", filename)

        # save image
        file_io.save_file(path, frame_dream)

        # save metadata to jpeg
        date = str(datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S"))
        timestamp = filename[:-4]
        userdata = {'id': filename, 'path': path, 'layer': layer, 'iterations': iterations, 'timestamp': timestamp, 'date_time': date, 'is_favorite': False}

        file_io.save_exif_file(userdata)

    def __init__(self):
        self.__show_general = True

        self.__show_dream = False
        self.__show_count_down = False
        self.__start_dream = False

        self.__is_locked = False

        self.__count = 3
        self.__duplicate_show = False

        self.__iterations = 10
        self.__layers = ""
        self.__all_layers = ""
        self.__default_layer = ""


vm = ViewModel()

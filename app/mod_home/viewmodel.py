from app.models import VideoCamera, Dream, detect_faces
from app.common import file_io
from flask import Response
import datetime
import time
import json
import cv2
import os


class ViewModel(object):
    def __init__(self):
        self.__show_general = True

        self.__show_dream = False
        self.__show_count_down = False
        self.__init_dream = False

        self.__is_locked = False

        self.__count = 3
        self.__iterations = 10
        self.__layers = ""
        self.__all_layers = ""


    # PUBLIC CONTROLLERS OF VIDEO STREAM
    def start_dream(self, data):
        if not self.__is_locked:
            self.__is_locked = True
            self.__show_count_down = True
            self.__start_time = time.time()

            self.__iterations = int(data['iteration'])

            self.__show_general = False
            self.__show_dream = False

    def reset_window(self):
        if not self.__is_locked:
            self.__show_general = True
            self.__start_time = time.time()

            self.__show_dream = False
            self.__show_count_down = False

    def get_default_control_values(self):
        data = {
            "iteration": self.__iterations,
            "layers": self.__layers,
            "all_layers": self.__all_layers,
            "default_layer": "test"
        }
        return json.dumps(data)


    # GET VIDEO STREAM
    def video_feed(self):
        return Response(self.__gen(VideoCamera()), mimetype='multipart/x-mixed-replace; boundary=frame')


    # CORE VM DREAM LOGIC
    def __gen(self, camera):
        dream_generator = Dream('resources/app_data/inception')
        self.__layers = dream_generator.get_featured_layers()
        self.__all_layers = dream_generator.get_all_layers()

        while True:
            # REGULAR STREAM
            if self.__show_general:
                ''''frame = camera.get_frame(False)
                is_slideshow, frame = detect_faces(frame)

                if not is_slideshow:
                    frame = camera.convert_to_jpeg(frame)
                    yield (b'--frame\r\n'
                        b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
                else:
                    # put logic to show slideshow
                    a = "a"'''
                frame = camera.get_frame()
                yield (b'--frame\r\n'
                        b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')


            # SHOW THE RESULT
            if self.__show_dream:
                yield (b'--frame\r\n'
                    b'Content-Type: image/jpeg\r\n\r\n' + self.__frame_dream + b'\r\n\r\n')


            # INIT DREAM
            if self.__init_dream:
                frame = camera.get_frame(True)
                yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

                frame = camera.get_frame(False)
                layer = dream_generator.get_layer()

                frame_dream = dream_generator.render_deepdream(layer, frame, self.__iterations)
                frame_dream = camera.convert_to_jpeg(frame_dream)

                yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + frame_dream + b'\r\n\r\n')

                self.__frame_dream = frame_dream
                self.__init_dream = False
                self.__show_dream = True
                self.__save_dream(self.__frame_dream, layer, self.__iterations)
                self.__is_locked = False


            # COUNT DOWN
            if self.__show_count_down:
                elapsed = int(time.time() - self.__start_time)
                resting = self.__count - elapsed

                frame_text = camera.get_frame(False)
                cv2.putText(img=frame_text, text=str(resting), org=(300, 300), fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=4, thickness=4, color=(255, 255, 255))
                frame_text = camera.convert_to_jpeg(frame_text)

                yield (b'--frame\r\n'
                    b'Content-Type: image/jpeg\r\n\r\n' + frame_text + b'\r\n\r\n')

                if resting <= 0:
                    self.__show_count_down = False
                    self.__init_dream = True
                    frame = camera.get_frame(True)
                    yield (b'--frame\r\n'
                        b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')


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


vm = ViewModel()

from app.models import init_slideshow, get_slideshow_frame
from app.models import VideoCamera, Dream, detect_faces
from app.common import file_io
from flask import Response
import datetime, time
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
        self.__default_layer = ""


    # PUBLIC CONTROLLERS OF VIDEO STREAM
    def start_dream(self, data):
        if not self.__is_locked:
            print("starting dream")
            self.__is_locked = True
            self.__show_count_down = True
            self.__start_time = time.time()

            self.__iterations = int(data['iteration'])
            self.__layer = str(data['layer'])

            self.__show_general = False
            self.__show_dream = False

    def reset_window(self):
        if not self.__is_locked:
            print("resetting window")
            self.__show_general = True
            self.__start_time = time.time()

            self.__show_dream = False
            self.__show_count_down = False

    def get_default_control_values(self):
        return {
            "iteration": self.__iterations,
            "layers": self.__layers,
            "all_layers": self.__all_layers,
            "default_layer": self.__default_layer
        }


    # GET VIDEO STREAM
    def video_feed(self):
        return Response(self.__gen(VideoCamera()), mimetype='multipart/x-mixed-replace; boundary=frame')


    # CORE VM DREAM LOGIC
    def __gen(self, camera):
        dream_generator = Dream('resources/app_data/inception')
        self.__layers = dream_generator.get_featured_layers()
        self.__all_layers = dream_generator.get_all_layers()
        self.__default_layer = dream_generator.get_default_layer()
        init_slideshow()

        while True:
            frame = camera.get_frame(False)

            # REGULAR STREAM
            if self.__show_general:
                # todo; split functionality in detect_faces and is_slideshow
                is_slideshow, frame = detect_faces(frame)
                if is_slideshow:
                    frame = get_slideshow_frame(frame)

            # SHOW THE RESULT
            if self.__show_dream:
                frame = self.__frame_dream


            # INIT DREAM
            if self.__init_dream:
                tmp_frame = camera.get_frame(True)
                yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + tmp_frame + b'\r\n\r\n')

                frame = dream_generator.render_deepdream(self.__layer, frame, self.__iterations)
                frame_save = camera.convert_to_jpeg(frame)

                self.__frame_dream = frame
                self.__init_dream = False
                self.__show_dream = True
                self.__save_dream(frame_save, self.__layer, self.__iterations)
                self.__is_locked = False


            # COUNT DOWN
            if self.__show_count_down:
                elapsed = int(time.time() - self.__start_time)
                resting = self.__count - elapsed
                cv2.putText(img=frame, text=str(resting), org=(300, 300), fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=4, thickness=4, color=(255, 255, 255))

                if resting <= 0:
                    self.__show_count_down = False
                    self.__init_dream = True
                    frame = camera.get_frame(False)


            frame = camera.convert_to_jpeg(frame)
            yield (b'--frame\r\n'
                        b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')


    def __save_dream(self, frame_dream, layer, iterations):
        # get path and filename
        filename = str(time.time()) + ".jpg"
        path = os.path.join(os.getcwd(), "resources", "static", "uploads", "history", filename)
        print("1a")

        # save image
        file_io.save_file(path, frame_dream)
        print("1b")

        # save metadata to jpeg
        date = str(datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S"))
        timestamp = filename[:-4]
        userdata = {'id': filename, 'path': path, 'layer': layer, 'iterations': iterations, 'timestamp': timestamp, 'date_time': date, 'is_favorite': False}
        print("1c")

        file_io.save_exif_file(userdata)
        print("1d")

print("INIT VM")
vm = ViewModel()

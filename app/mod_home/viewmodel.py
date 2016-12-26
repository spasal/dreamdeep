from app.models import VideoCamera, Dream
from flask import Response
import time, os, json
from PIL import Image
import piexif, datetime
import cv2



class ViewModel(object):
    def __init__(self):
        self.__show_general = True

        self.__show_dream = False
        self.__show_count_down = False
        self.__init_dream = False

        self.__is_locked = False

        self.__count = 3


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

            self.__show_dream = False
            self.__show_count_down = False

    def get_default_control_values(self):
        data = json.dumps({"iteration": "10"})
        return data


    # GET VIDEO STREAM
    def video_feed(self):
        return Response(self.__gen(VideoCamera()), mimetype = 'multipart/x-mixed-replace; boundary=frame')


    # CORE VM DREAM LOGIC
    def __gen(self, camera):
        dream_generator = Dream('resources/inception')

        while True:
            # REGULAR STREAM
            if self.__show_general:
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

                yield (b'--frame\r\n'
                         b'Content-Type: image/jpeg\r\n\r\n' + frame_dream + b'\r\n\r\n')

                self.__frame_dream = frame_dream
                self.__init_dream = False
                self.__show_dream = True
                self.__save_dream(self.__frame_dream, layer, self.__iterations)
                self.__is_locked = False
                print("done")


            # COUNT DOWN
            if self.__show_count_down:
                elapsed = int(time.time() - self.__start_time)
                resting = self.__count - elapsed

                frame_text = camera.get_frame(False)
                cv2.putText(img=frame_text, text=str(resting), org=(300,300),
                    fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=4, thickness=4, color=(255, 255, 255))
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
        fileName = str(time.time()) + ".jpg"
        path = os.path.join(os.getcwd(), "resources", "static","uploads", "history", fileName)

        # save image
        output = open(path, "wb")
        output.write(frame_dream)
        output.close()

        # write custom metadata
        date = str(datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S"))
        timestamp = fileName[:-4]
        userdata = json.dumps({'id': fileName, 'path': path, 'layer': layer, 'iterations': iterations, 'timestamp': timestamp, 'date_time': date, 'is_favorite': False})

        exif_ifd = {piexif.ExifIFD.UserComment : userdata}
        exif_dict = {"Exif": exif_ifd}
        exif_bytes = piexif.dump(exif_dict)

        im = Image.open(path)
        im.save(path, exif=exif_bytes)


vm = ViewModel()

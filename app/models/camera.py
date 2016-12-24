
import cv2


class VideoCamera(object):
    def __init__(self):
        self.video = cv2.VideoCapture(0)

        success = False
        while not success:
            success, image = self.video.read()
            ret, jpeg = cv2.imencode('.jpg', image)
            self.last_frame = jpeg.tobytes()

    def __del__(self):
        self.video.release()

    def get_frame(self, is_jpeg=True):
        success, image = self.video.read()
        # We are using Motion JPEG, but OpenCV defaults to capture raw images,
        # so we must encode it into JPEG in order to correctly display the
        # video stream.
        if is_jpeg:
            if success:
                ret, jpeg = cv2.imencode('.jpg', image)
                jpeg = jpeg.tobytes()
                self.last_frame = jpeg
                return jpeg
            else:
                return self.last_frame
        else:
            return image

    def convert_to_jpeg(self, image):
        ret, jpeg = cv2.imencode('.jpg', image)
        jpeg = jpeg.tobytes()
        self.last_frame = jpeg
        return jpeg

    def count_down(self):
        print()

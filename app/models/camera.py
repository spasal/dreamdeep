
import cv2


class VideoCamera(object):
    def __init__(self):
        print("---VIDEOCAMERA INITIALIZED")
        self.video = cv2.VideoCapture(0)

        success = False
        while not success:
            success, image = self.video.read()
            if success:
                ret, jpeg = cv2.imencode('.jpg', image)
                self.last_frame = jpeg.tobytes()

    def __del__(self):
        print("DELETING VIDEO")
        self.video.release()

    def get_frame(self, is_jpeg=True):
        # We are using Motion JPEG, but OpenCV defaults to capture raw images. we must encode it into JPEG in order to correctly display the video stream.
        success = False
        while not success:
            success, image = self.video.read()
            if success:
                image = cv2.flip(image, 1)
                if is_jpeg:
                    ret, jpeg = cv2.imencode('.jpg', image)
                    jpeg = jpeg.tobytes()
                    self.last_frame = jpeg
                    return jpeg
                else:
                    return image

    def convert_to_jpeg(self, image):
        ret, jpeg = cv2.imencode('.jpg', image)
        jpeg = jpeg.tobytes()
        self.last_frame = jpeg
        return jpeg

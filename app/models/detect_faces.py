import cv2
import copy
import os

__current_dir = os.path.dirname(__file__)

# face detection cascades
__relative_path = '../../data/cascades'
__full_path = os.path.join(__current_dir, __relative_path)

__face_cascade_path = os.path.join(__full_path, 'haarcascade_frontalface_default.xml')
__alt_face_cascade_path = os.path.join(__full_path, 'haarcascade_profileface.xml')
__face_cascade = cv2.CascadeClassifier(__face_cascade_path)
__alt_face_cascade = cv2.CascadeClassifier(__alt_face_cascade_path)


def __drawFaces(frame, faces, color):
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)


def __drawText(frame, text):
    cv2.putText(img=frame, text=text, org=(75, 400),
                fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=1, thickness=2, color=(255, 255, 255))


def detectFaces(frm):

    # Our operations on the frame come here
    frame = copy.deepcopy(frm)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces_front = __face_cascade.detectMultiScale(gray, 1.3, 5)
    faces_alt = __alt_face_cascade.detectMultiScale(gray, 1.3, 5)

    hasFace = False
    if(faces_front != () or faces_alt != ()):
            # drawFaces(frame, faces_front, (255, 0, 0))
            # drawFaces(frame, faces_alt, (0, 255, 0))
        __drawText(frame, 'Press space to start DREAMING')
        hasFace = True

    return hasFace, frame

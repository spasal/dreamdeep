import cv2
import copy
import os

# face detection cascades
__current_dir = os.path.dirname(__file__)

__relative_path = '../../resources/cascades'
__full_path = os.path.join(__current_dir, __relative_path)

__face_cascade_path = os.path.join(__full_path, 'haarcascade_frontalface_default.xml')
__alt_face_cascade_path = os.path.join(__full_path, 'haarcascade_profileface.xml')
__face_cascade = cv2.CascadeClassifier(__face_cascade_path)
__alt_face_cascade = cv2.CascadeClassifier(__alt_face_cascade_path)

__has_faces = []
__count = 60


def __drawFaces(frame, faces, color):
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)


def __drawText(frame, text):
    cv2.putText(img=frame, text=text, org=(75, 400),
                fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=1, thickness=2, color=(255, 255, 255))


def detect_faces(frame):

    # Our operations on the frame come here
    frm = copy.deepcopy(frame)
    gray = cv2.cvtColor(frm, cv2.COLOR_BGR2GRAY)

    faces_front = __face_cascade.detectMultiScale(gray, 1.3, 5)
    faces_alt = __alt_face_cascade.detectMultiScale(gray, 1.3, 5)

    hasFace = False
    if(faces_front != () or faces_alt != ()):
            # drawFaces(frame, faces_front, (255, 0, 0))
            # drawFaces(frame, faces_alt, (0, 255, 0))
        __drawText(frame, 'Deep dreams are made of you')
        hasFace = True

    __has_faces.append(hasFace)
    if len(__has_faces) > __count:
        __has_faces.pop(0)

    i_trues = __has_faces.count(True)
    i_false = __has_faces.count(False)

    hasFace = i_trues > i_false

    return hasFace, frame

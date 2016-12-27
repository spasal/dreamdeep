import cv2
import copy
import os
import time

# face detection cascades
__current_dir = os.path.dirname(__file__)
__relative_path = '../../resources/cascades'
__full_path = os.path.join(__current_dir, __relative_path)
__face_cascade_path = os.path.join(__full_path, 'haarcascade_frontalface_default.xml')
__alt_face_cascade_path = os.path.join(__full_path, 'haarcascade_profileface.xml')
__face_cascade = cv2.CascadeClassifier(__face_cascade_path)
__alt_face_cascade = cv2.CascadeClassifier(__alt_face_cascade_path)

__has_faces = []
__latest_has_faces = []
__count = 60
__count_time = time.time()


def __drawFaces(frame, faces, color):
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)


def __drawText(frame, text):
    cv2.putText(img=frame, text=text, org=(75, 400),
                fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=1, thickness=2, color=(255, 255, 255))


def __append_to_arr(arr, val, count):
    arr.append(val)
    if len(arr) > count:
        arr.pop(0)


def detect_faces(frame):
    # detect face
    frm = copy.deepcopy(frame)
    gray = cv2.cvtColor(frm, cv2.COLOR_BGR2GRAY)

    faces_front = __face_cascade.detectMultiScale(gray, 1.3, 5)
    faces_alt = __alt_face_cascade.detectMultiScale(gray, 1.3, 5)

    has_face = False
    if(faces_front != () or faces_alt != ()):
        has_face = True

    # running average of has_face
    __append_to_arr(__has_faces, has_face, __count)
    i_trues, i_false = __has_faces.count(True), __has_faces.count(False)
    has_face = i_trues > i_false
    if has_face:
        __drawText(frame, 'Deep dreams are made of you')

    # add result to has_face_avg
    __append_to_arr(__latest_has_faces, has_face, 2)

    # check if slideshow should start
    slideshow = False
    if not has_face:
        global __count_time
        index = len(__latest_has_faces) - 1
        last_has_face = __latest_has_faces[index - 1]

        # previous frame has face, start counting
        if last_has_face:
            __count_time = time.time()

        # check if value exceeds
        else:
            elapsed = int(time.time() - __count_time)
            if elapsed > 3:
                slideshow = True

    return slideshow, frame

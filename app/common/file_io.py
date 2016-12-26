from PIL import Image
import sys, os, json
import piexif
import shutil


def get_exif_files(path):
    upload_path = sys.path[0] + path

    # get all files
    files = []
    for (dirpath, dirnames, filenames) in os.walk(upload_path):
        files.extend(filenames)
        break

    # build history
    items = []
    for file in files:
        file_path = os.path.join(upload_path, file)
        exif_dict = piexif.load(file_path)

        usercomment = exif_dict["Exif"][37510].decode("utf-8")
        usercomment = json.loads(usercomment)

        items.append(usercomment)

    return items


def get_exif_file(path, file_name):
    upload_path = sys.path[0] + path
    file_path = os.path.join(upload_path, file_name)
    try:
        exif_dict = piexif.load(file_path)

        usercomment = exif_dict["Exif"][37510].decode("utf-8")
        usercomment = json.loads(usercomment)

        return usercomment
    except:
        return None


def save_exif_file(userdata):
    path = userdata["path"]
    userdata = json.dumps(userdata)
    exif_ifd = {piexif.ExifIFD.UserComment: userdata}
    exif_dict = {"Exif": exif_ifd}
    exif_bytes = piexif.dump(exif_dict)

    im = Image.open(path)
    im.save(path, exif=exif_bytes)


def remove_file(path, file_name=None, is_complete=True):
    if is_complete:
        os.remove(path)
    else:
        path = sys.path[0] + path
        path = os.path.join(path, file_name)
        os.remove(path)


def insert_or_delete_file(userdata, destination_path):
    file_name = userdata["id"]
    original_path = userdata["path"]
    upload_path = sys.path[0] + destination_path
    upload_path = os.path.join(upload_path, file_name)

    if os.path.isfile(upload_path):
        os.remove(upload_path)
    else:
        print(original_path)
        print(upload_path)
        shutil.copy2(original_path, upload_path)

from PIL import Image
import numpy
import sys, os, json
import glob
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
        shutil.copy2(original_path, upload_path)


def save_file(path, file):
    output = open(path, 'wb')
    output.write(file)
    output.close()


def get_images_as_byte_array(path, extension):
    download_path = sys.path[0] + path + "/*" + extension
    image_list = []
    for filename in glob.glob(download_path):
        with open(filename, "rb") as imageFile:
            f = imageFile.read()
            b = bytearray(f)
            image_list.append(b)

    return image_list


def get_image(path, resized=True):
    print("downloading file")
    pil_image = Image.open(path).convert('RGB')

    # resize image if needed
    if resized:
        w, h = pil_image.size[0], pil_image.size[1]
        if w > 640:
            pil_image = __resize_image_basewidth(pil_image, 640)
            h = pil_image.size[1]
        if h > 480:
            pil_image = __resize_image_baseheight(pil_image, 640)

    open_cv_image = numpy.array(pil_image)
    open_cv_image = open_cv_image[:, :, ::-1].copy()

    return open_cv_image


def __resize_image_basewidth(source, basewidth):
    wpercent = (basewidth / float(source.size[0]))
    hsize = int((float(source.size[1])*float(wpercent)))
    img = source.resize((basewidth, hsize), Image.ANTIALIAS)
    return img


def __resize_image_baseheight(source, baseheight):
    hpercent = (baseheight / float(source.size[1]))
    wsize = int((float(source.size[0])*float(hpercent)))
    img = source.resize((baseheight, wsize), Image.ANTIALIAS)
    return img


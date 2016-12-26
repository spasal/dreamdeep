from app.mod_history import history_blueprint as app
from flask import render_template, redirect, url_for
import os, sys, datetime
from PIL import Image
import piexif, json


def __get_items(path):
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
        print('getting files', file_path)

        usercomment = exif_dict["Exif"][37510].decode("utf-8")
        usercomment = json.loads(usercomment)

        items.append(usercomment)

    return items


def __get_item(path, id):
    upload_path = sys.path[0] + path
    file_path = os.path.join(upload_path, id)
    try:
        exif_dict = piexif.load(file_path)

        usercomment = exif_dict["Exif"][37510].decode("utf-8")
        usercomment = json.loads(usercomment)

        return usercomment
    except:
        return None

def __save_item(userdata):
    path = userdata["path"]
    userdata = json.dumps(userdata)
    exif_ifd = {piexif.ExifIFD.UserComment : userdata}
    exif_dict = {"Exif": exif_ifd}
    exif_bytes = piexif.dump(exif_dict)

    im = Image.open(path)
    im.save(path, exif=exif_bytes)


@app.route('/history')
def index():
    history = __get_items('/resources/static/uploads/history')
    history = sorted(history, key=lambda p: p['timestamp'], reverse=True)
    return render_template('history.html', history=history)


@app.route('/history/del/<id>')
def delete(id):
    item = __get_item('/resources/static/uploads/history', id)
    if item:
        os.remove(item["path"])

    return redirect(url_for('mod_history.index'))


@app.route('/history/fav/<id>')
def favorite(id):
    item = __get_item('/resources/static/uploads/history', id)
    if item:
        item["is_favorite"] = not item["is_favorite"]
        __save_item(item)

    return redirect(url_for('mod_history.index'))

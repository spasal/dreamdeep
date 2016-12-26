from app.mod_history import history_blueprint as app
from flask import render_template, redirect, url_for
import os, sys, datetime
import piexif, json


def __get_history_list():
    upload_path = sys.path[0] + '/resources/static/uploads/history'

    # get all files
    files = []
    for (dirpath, dirnames, filenames) in os.walk(upload_path):
        files.extend(filenames)
        break

    # build history
    history = []
    for file in files:
        filepath = os.path.join(upload_path, file)
        exif_dict = piexif.load(filepath)

        usercomment = exif_dict["Exif"][37510].decode("utf-8")
        usercomment = json.loads(usercomment)
        date_time = exif_dict["Exif"][36867].decode("utf-8")

        layer = usercomment["layer"]
        path = usercomment["path"]
        iterations = usercomment["iterations"]
        timestamp = usercomment["timestamp"]
        is_favorite = usercomment["is_favorite"]

        history.append(
            {'id': timestamp, 'image': file, 'time': date_time, 'layer': layer, 'iterations': iterations, 'path': path, 'is_favorite': is_favorite
            }
        )

    return history


@app.route('/history')
def index():
    history = __get_history_list()
    print(history)
    history = sorted(history, key=lambda p: p['time'], reverse=True)
    return render_template('history.html', history=history)


@app.route('/history/del/<id>')
def delete(id):
    print(id)
    print(redirect(url_for('mod_history.index')))
    return redirect(url_for('mod_history.index'))


@app.route('/history/fav/<id>')
def favorite(id):
    # re-write tag to know if is favorite
    print(id)
    print(redirect(url_for('mod_history.index')))
    return redirect(url_for('mod_history.index'))

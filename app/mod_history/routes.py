from app.mod_history import history_blueprint as app
from flask import render_template
import os, sys, datetime

@app.route('/history')
def index():
    print("defining history template")

    upload_path = sys.path[0] + '/resources/static/uploads/history'

    # get all files
    files = []
    for (dirpath, dirnames, filenames) in os.walk(upload_path):
        files.extend(filenames)
        break

    # build history
    history = []
    for file in files:
        timestamp = float(os.path.splitext(file)[0])
        time = datetime.datetime.fromtimestamp(timestamp)

        history.append({'image': file, 'time': time, 'id': timestamp})

    history = sorted(history, key=lambda p: p['time'], reverse=True)
    print(history)

    return render_template('history.html', history=history)

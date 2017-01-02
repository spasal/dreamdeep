from app.common import mail_handler
from app import create_app
from flask import request, redirect, url_for
import os
import time

app = create_app('PRODUCTION')
''''
app, mail = mail_handler.init_mail_handler(app)

APP_ROOT = os.path.dirname(os.path.abspath(__file__))

from app.mod_home.viewmodel import vm

@app.route("/upload", methods=["POST"])
def upload():
    target = os.path.join(APP_ROOT, "resources", "static", "uploads", "uploads")

    if not os.path.isdir(target):
        os.mkdir(target)

    if not vm.is_dreaming:
        for file in request.files.getlist("file"):
            print(file)
            filename = str(time.time()) + os.path.splitext(file.filename)[1]
            destination = os.path.join(target, filename)
            print(destination)

            file.save(destination)
            vm.show_image_upload(destination)

    return redirect(url_for('mod_home.index'))'''

@app.route("/upload", methods=["POST"])
def upload():
    target = os.path.join(APP_ROOT, "resources", "static", "uploads", "uploads")
    print(target)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, threaded=True)

from flask import render_template, redirect, url_for, request
from app.mod_home import home_blueprint as app
from app.mod_home.viewmodel import vm
from config import app_root
import os, time


@app.route('/')
def index():
    return render_template('home.html')


@app.route('/get_video_feed')
def get_video_feed():
    return vm.video_feed()


@app.route("/upload", methods=["POST"])
def upload():
    print("upload")
    target = os.path.join(app_root, "resources", "static", "uploads", "uploads")

    if not os.path.isdir(target):
        os.mkdir(target)

    if not vm.is_dreaming():
        for file in request.files.getlist("file"):
            print(file)
            filename = str(time.time()) + os.path.splitext(file.filename)[1]
            destination = os.path.join(target, filename)
            print(destination)

            file.save(destination)
            vm.show_image_upload(destination)

    return redirect(url_for('mod_home.index'))

from flask import render_template
from app.mod_home import home_blueprint as app
from app.mod_home.viewmodel import vm


@app.route('/')
def index():
    return render_template('home.html')


@app.route('/get_video_feed')
def get_video_feed():
    return vm.video_feed()

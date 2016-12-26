from app.mod_api_handler import api_handler__blueprint as app
from app.mod_home.viewmodel import vm
from flask import request
import json

# usefull resource      # , limit
''''
http://pycoder.net/bospy/presentation.html#bonus-material
http://codehandbook.org/python-flask-jquery-ajax-post/
'''


@app.route('/start_dream', methods=['POST'])
# @limit(requests=10, window=60, by="ip")
def handle_post():
    data = request.get_json(force=True)
    vm.start_dream(data)
    return json.dumps({'status': 'OK'})


@app.route('/reset_view')
def handle_reset():
    vm.reset_window()
    return json.dumps({'status': 'OK'})


@app.route('/default')
def handle_default():
    return vm.get_default_control_values()
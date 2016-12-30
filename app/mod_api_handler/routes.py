from app.mod_api_handler import api_handler__blueprint as app
from app.mod_home.viewmodel import vm
from flask import request
import json


@app.route('/start_dream', methods=['POST'])
# @limit(requests=10, window=60, by="ip")
def handle_dream():
    data = request.get_json(force=True)
    vm.start_dream(data)
    return json.dumps({"status": "OK"})


@app.route('/reset_view')
def handle_reset():
    vm.reset_window()
    return json.dumps({"status": "OK"})


@app.route('/default')
def handle_default():
    # get the data untill they are filled
    has_return_values = False
    while not has_return_values:
        res = vm.get_default_control_values()
        if res["layers"] != "" and res["all_layers"] != "" and res["default_layer"] != "":
            has_return_values = True
            return json.dumps(res)


@app.route('/is_dream')
def handle_is_dream():
    answer = vm.is_dreaming()
    return json.dumps({"is_dreaming": answer})

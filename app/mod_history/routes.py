from flask import render_template
from app.mod_history import history_blueprint as app


@app.route('/history')
def index():
    print("defining history template")
    return render_template('history.html')

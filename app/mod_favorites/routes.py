from flask import render_template
from app.mod_favorites import favorites_blueprint as app


@app.route('/favorites')
def index():
    print("defining favorites template")
    return render_template('favorites.html')

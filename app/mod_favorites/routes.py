from app.mod_favorites import favorites_blueprint as app
from flask import render_template, redirect, url_for
from app.common import file_io


@app.route('/favorites')
def index():
    favorites = file_io.get_exif_files('/resources/static/uploads/favorites')
    favorites = sorted(favorites, key=lambda p: p['timestamp'], reverse=True)
    return render_template('favorites.html', favorites=favorites)


@app.route('/favorites/del/<id>')
def delete(id):
    item = file_io.get_exif_file('/resources/static/uploads/favorites', id)
    if item:
        file_io.remove_file(item["path"])
        if item["is_favorite"]:
            file_io.remove_file('/resources/static/uploads/favorites', item["id"], False)

    return redirect(url_for('mod_favorites.index'))


@app.route('/favorites/fav/<id>')
def favorite(id):
    item = file_io.get_exif_file('/resources/static/uploads/favorites', id)
    if item:
        item["is_favorite"] = not item["is_favorite"]
        file_io.save_exif_file(item)
        file_io.insert_or_delete_file(item, '/resources/static/uploads/favorites')

    return redirect(url_for('mod_favorites.index'))
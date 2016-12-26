from app.mod_history import history_blueprint as app
from flask import render_template, redirect, url_for
from app.common import file_io


@app.route('/history')
def index():
    history = file_io.get_exif_files('/resources/static/uploads/history')
    history = sorted(history, key=lambda p: p['timestamp'], reverse=True)
    return render_template('history.html', history=history)


@app.route('/history/del/<id>')
def delete(id):
    item = file_io.get_exif_file('/resources/static/uploads/history', id)
    if item:
        file_io.remove_file(item["path"])
        if item["is_favorite"]:
            file_io.remove_file('/resources/static/uploads/favorites', item["id"], False)

    return redirect(url_for('mod_history.index'))


@app.route('/history/fav/<id>')
def favorite(id):
    item = file_io.get_exif_file('/resources/static/uploads/history', id)
    if item:
        item["is_favorite"] = not item["is_favorite"]
        file_io.save_exif_file(item)
        file_io.insert_or_delete_file(item, '/resources/static/uploads/favorites')

    return redirect(url_for('mod_history.index'))

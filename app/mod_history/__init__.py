from flask import Blueprint

history_blueprint = Blueprint('mod_history', __name__, template_folder='../../resources/templates/history')

from app.mod_history import routes
from flask import Blueprint

favorites_blueprint = Blueprint('mod_favorites', __name__, template_folder='../../resources/templates/favorites')

from app.mod_favorites import routes
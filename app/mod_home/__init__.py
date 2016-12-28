from flask import Blueprint

home_blueprint = Blueprint('mod_home', __name__, template_folder='../../resources/templates/home')

from app.mod_home import routes

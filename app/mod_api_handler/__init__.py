from flask import Blueprint

api_handler__blueprint = Blueprint('mod_api_handler', __name__)

from app.mod_api_handler import routes
from flask import Blueprint

bp = Blueprint('ditto', __name__, template_folder='templates', static_folder='static')

from app.ditto import ditto
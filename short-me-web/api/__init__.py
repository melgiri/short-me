from flask import Blueprint
api = Blueprint('api', __name__)

from . import auth
from . import manage
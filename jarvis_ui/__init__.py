from flask import Blueprint 
jarvis_ui = Blueprint('jarvis_ui', __name__) 
from . import routes 

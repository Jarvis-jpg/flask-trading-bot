from flask import render_template, Blueprint 
from . import jarvis_ui 
 
@jarvis_ui.route('/') 
def home(): 

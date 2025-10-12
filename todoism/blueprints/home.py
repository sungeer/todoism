from flask import render_template, Blueprint, current_app, make_response, jsonify
from flask_login import current_user

from todoism.extensions import db

home_bp = Blueprint('home', __name__)


@home_bp.route('/')
def index():
    return render_template('index.html')


@home_bp.route('/intro')
def intro():
    return render_template('_intro.html')

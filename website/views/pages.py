from flask import Blueprint, render_template

pages_bp = Blueprint('standalone_pages_bp', __name__)


@pages_bp.route('/')
def home():
    return render_template('index.html')

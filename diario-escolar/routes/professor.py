from flask import Blueprint, render_template

professor_bp = Blueprint('professor', __name__)


@professor_bp.route('/')
def dashboard():
    return render_template('professor/dashboard.html')
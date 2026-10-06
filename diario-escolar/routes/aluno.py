from flask import Blueprint, render_template

aluno_bp = Blueprint('aluno', __name__)


@aluno_bp.route('/')
def dashboard():
    return render_template('aluno/dashboard.html')
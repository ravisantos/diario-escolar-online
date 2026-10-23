from flask import Blueprint, flash, redirect, render_template, request, url_for
from extensions import db
from routes.decorators import login_obrigatorio

aluno_bp = Blueprint('aluno', __name__)


@aluno_bp.route('/')
def dashboard():
    return render_template('aluno/dashboard.html')

@aluno_bp.route('/boletim', methods=['GET'])
@login_obrigatorio('aluno')
def boletim():
    return render_template('aluno/boletim.html')



@aluno_bp.route('/frequencia', methods=['GET'])
@login_obrigatorio('aluno')
def frequencia():
    return render_template('aluno/frequencia.html')




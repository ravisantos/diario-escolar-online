from flask import Blueprint, flash, redirect, render_template, request, url_for

from extensions import db
from models.disciplina import Disciplina
from models.turma import Turma
from routes.decorators import login_obrigatorio

admin_bp = Blueprint('admin', __name__)

TURNOS = ('Manhã', 'Tarde', 'Noite')


@admin_bp.route('/')
@login_obrigatorio('admin')
def dashboard():
    return render_template(
        'admin/dashboard.html',
        total_turmas=Turma.query.count(),
        total_disciplinas=Disciplina.query.count(),
    )


# ------------------------------------------------ TURMAS

def _ler_turma_do_formulario():
    """Lê e valida o formulário. Devolve (nome, ano, turno, erro)."""


from flask import Blueprint, abort, render_template, request, session

from models.aluno import Aluno
from routes.decorators import login_obrigatorio
from services.frequencia import FREQUENCIA_MINIMA, frequencia
from services.notas import BIMESTRES, MEDIA_MINIMA, boletim

aluno_bp = Blueprint('aluno', __name__)


def _aluno_logado():
    aluno = Aluno.query.filter_by(usuario_id=session['usuario_id']).first()
    if aluno is None:
        abort(403)
    return aluno


def _matricula_escolhida(aluno):
    """Devolve (matrícula escolhida, todas as matrículas do aluno).

    O aluno só enxerga as próprias matrículas. Sem ?matricula=, mostra a ativa
    do ano letivo mais recente.
    """
    matriculas = sorted(aluno.matriculas,
                        key=lambda m: (m.status == 'ativa', m.turma.ano_letivo, m.id),
                        reverse=True)
    if not matriculas:
        return None, []

    escolhida_id = request.args.get('matricula', type=int)
    if escolhida_id is None:
        return matriculas[0], matriculas
    for matricula in matriculas:
        if matricula.id == escolhida_id:
            return matricula, matriculas
    abort(404)


@aluno_bp.route('/')
@login_obrigatorio('aluno')
def dashboard():
    aluno = _aluno_logado()
    matricula, _ = _matricula_escolhida(aluno)
    return render_template('aluno/dashboard.html', aluno=aluno, matricula=matricula)


@aluno_bp.route('/boletim')
@login_obrigatorio('aluno')
def boletim_rota():
    matricula, matriculas = _matricula_escolhida(_aluno_logado())
    disciplinas = boletim(matricula) if matricula else []
    return render_template('aluno/boletim.html', matricula=matricula, matriculas=matriculas,
                           disciplinas=disciplinas, bimestres=BIMESTRES,
                           media_minima=MEDIA_MINIMA)


@aluno_bp.route('/frequencia')
@login_obrigatorio('aluno')
def frequencia_rota():
    matricula, matriculas = _matricula_escolhida(_aluno_logado())
    disciplinas, registros, geral = frequencia(matricula) if matricula else ([], [], None)
    return render_template('aluno/frequencia.html', matricula=matricula, matriculas=matriculas,
                           disciplinas=disciplinas, registros=registros, geral=geral,
                           frequencia_minima=FREQUENCIA_MINIMA)

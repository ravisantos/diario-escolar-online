from datetime import date

from flask import Blueprint, abort, flash, redirect, render_template, request, session, url_for

from extensions import db
from models.alocacao import Alocacao
from models.aula import Aula
from models.avaliacao import Avaliacao
from models.professor import Professor
from routes.decorators import login_obrigatorio
from services.diario import (criar_aula, criar_avaliacao, excluir_aula,
                             excluir_avaliacao, matriculas_ativas,
                             salvar_chamada, salvar_notas)

professor_bp = Blueprint('professor', __name__)


def _professor_logado():
    professor = Professor.query.filter_by(usuario_id=session['usuario_id']).first()
    if professor is None:
        abort(403)
    return professor


def _minha_alocacao(alocacao_id):
    """Busca a alocação e garante que ela pertence ao professor logado."""
    alocacao = db.get_or_404(Alocacao, alocacao_id)
    if alocacao.professor_id != _professor_logado().id:
        abort(403)
    return alocacao


@professor_bp.route('/')
@login_obrigatorio('professor')
def dashboard():
    professor = _professor_logado()
    alocacoes = sorted(professor.alocacoes,
                       key=lambda a: (-a.turma.ano_letivo, a.turma.nome, a.disciplina.nome))
    return render_template('professor/dashboard.html', alocacoes=alocacoes,
                           total_alunos={a.id: len(matriculas_ativas(a.turma_id)) for a in alocacoes})


@professor_bp.route('/turma/<int:alocacao_id>')
@login_obrigatorio('professor')
def turma(alocacao_id):
    alocacao = _minha_alocacao(alocacao_id)
    avaliacoes = sorted(alocacao.avaliacoes, key=lambda a: (a.bimestre, a.data or date.min, a.id))
    aulas = sorted(alocacao.aulas, key=lambda a: (a.data, a.id), reverse=True)
    return render_template('professor/turma.html', alocacao=alocacao,
                           alunos=matriculas_ativas(alocacao.turma_id),
                           avaliacoes=avaliacoes, aulas=aulas,
                           hoje=date.today().isoformat())


# ---------- avaliações e notas ----------

@professor_bp.route('/turma/<int:alocacao_id>/avaliacoes/nova', methods=['GET', 'POST'])
@login_obrigatorio('professor')
def nova_avaliacao(alocacao_id):
    alocacao = _minha_alocacao(alocacao_id)
    if request.method == 'POST':
        try:
            avaliacao = criar_avaliacao(
                alocacao,
                request.form.get('titulo', ''),
                request.form.get('bimestre', ''),
                request.form.get('data', ''),
                request.form.get('valor_maximo', ''),
            )
        except ValueError as erro:
            flash(str(erro), 'erro')
        else:
            flash('Avaliação criada. Agora lance as notas.', 'sucesso')
            return redirect(url_for('professor.notas', avaliacao_id=avaliacao.id))
    return render_template('professor/avaliacao.html', alocacao=alocacao)


def _minha_avaliacao(avaliacao_id):
    avaliacao = db.get_or_404(Avaliacao, avaliacao_id)
    _minha_alocacao(avaliacao.alocacao_id)
    return avaliacao


@professor_bp.route('/avaliacao/<int:avaliacao_id>/notas', methods=['GET', 'POST'])
@login_obrigatorio('professor')
def notas(avaliacao_id):
    avaliacao = _minha_avaliacao(avaliacao_id)
    if request.method == 'POST':
        valores = {m.id: request.form.get(f'nota_{m.id}', '')
                   for m in matriculas_ativas(avaliacao.alocacao.turma_id)}
        try:
            salvar_notas(avaliacao, valores)
        except ValueError as erro:
            db.session.rollback()
            flash(str(erro), 'erro')
        else:
            flash('Notas salvas.', 'sucesso')
            return redirect(url_for('professor.turma', alocacao_id=avaliacao.alocacao_id))

    atuais = {n.matricula_id: n.valor for n in avaliacao.notas}
    return render_template('professor/notas.html', avaliacao=avaliacao,
                           matriculas=matriculas_ativas(avaliacao.alocacao.turma_id),
                           atuais=atuais)


@professor_bp.route('/avaliacao/<int:avaliacao_id>/excluir', methods=['POST'])
@login_obrigatorio('professor')
def excluir_avaliacao_rota(avaliacao_id):
    avaliacao = _minha_avaliacao(avaliacao_id)
    alocacao_id = avaliacao.alocacao_id
    try:
        excluir_avaliacao(avaliacao)
    except ValueError as erro:
        flash(str(erro), 'erro')
    else:
        flash('Avaliação excluída.', 'sucesso')
    return redirect(url_for('professor.turma', alocacao_id=alocacao_id))


# ---------- aulas e chamada ----------

@professor_bp.route('/turma/<int:alocacao_id>/aulas/nova', methods=['POST'])
@login_obrigatorio('professor')
def nova_aula(alocacao_id):
    alocacao = _minha_alocacao(alocacao_id)
    try:
        aula = criar_aula(alocacao, request.form.get('data', ''), request.form.get('conteudo', ''))
    except ValueError as erro:
        flash(str(erro), 'erro')
        return redirect(url_for('professor.turma', alocacao_id=alocacao.id))
    flash('Aula registrada. Faça a chamada.', 'sucesso')
    return redirect(url_for('professor.chamada', aula_id=aula.id))


def _minha_aula(aula_id):
    aula = db.get_or_404(Aula, aula_id)
    _minha_alocacao(aula.alocacao_id)
    return aula


@professor_bp.route('/aula/<int:aula_id>/chamada', methods=['GET', 'POST'])
@login_obrigatorio('professor')
def chamada(aula_id):
    aula = _minha_aula(aula_id)
    if request.method == 'POST':
        presentes = {int(i) for i in request.form.getlist('presente') if i.isdigit()}
        salvar_chamada(aula, presentes)
        flash('Chamada salva.', 'sucesso')
        return redirect(url_for('professor.turma', alocacao_id=aula.alocacao_id))

    registros = {f.matricula_id: f.presente for f in aula.frequencias}
    return render_template('professor/frequencia.html', aula=aula,
                           matriculas=matriculas_ativas(aula.alocacao.turma_id),
                           registros=registros)


@professor_bp.route('/aula/<int:aula_id>/excluir', methods=['POST'])
@login_obrigatorio('professor')
def excluir_aula_rota(aula_id):
    aula = _minha_aula(aula_id)
    alocacao_id = aula.alocacao_id
    try:
        excluir_aula(aula)
    except ValueError as erro:
        flash(str(erro), 'erro')
    else:
        flash('Aula excluída.', 'sucesso')
    return redirect(url_for('professor.turma', alocacao_id=alocacao_id))

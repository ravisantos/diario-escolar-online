from flask import Blueprint, flash, redirect, render_template, request, url_for

from extensions import db

from models.alocacao import Alocacao
from models.usuario import Usuario
from models.disciplina import Disciplina
from models.turma import Turma
from models.professor import Professor
from models.aluno import Aluno
from models.matricula import Matricula

from routes.decorators import login_obrigatorio

from services.usuarios import criar_professor, criar_aluno
from services.matricula import matricular

admin_bp = Blueprint('admin', __name__)

TURNOS = ('Manhã', 'Tarde', 'Noite', 'Integral')  # Lista de turnos

# Rotas para os templates do painel admin:

# Dashboard admin (inicio)

@admin_bp.route('/')
@login_obrigatorio('admin')
def dashboard():
    return render_template('admin/dashboard.html')

#Disciplinas

@admin_bp.route('/disciplinas', methods=['GET', 'POST'])
@login_obrigatorio('admin')
def disciplinas():
    if request.method == 'POST':
        nome = request.form.get('nome', '').strip()

        if not nome:
            flash('Informe o nome da disciplina.', 'erro')
        elif Disciplina.query.filter_by(nome=nome).first():
            flash('Já existe uma disciplina com esse nome.', 'erro')
        else:
            db.session.add(Disciplina(nome=nome))
            db.session.commit()
            flash(f'Disciplina {nome} criada.', 'sucesso')
            return redirect(url_for('admin.disciplinas'))
        
    editando = None
    editar_id = request.args.get('editar', type=int)
    if editar_id:
        editando = db.session.get(Disciplina, editar_id)

    lista = Disciplina.query.order_by(Disciplina.nome).all()
    return render_template('admin/disciplinas.html', disciplinas=lista, editando=editando)

@admin_bp.route('/disciplinas/<int:disciplina_id>/editar', methods=['POST'])
@login_obrigatorio('admin')
def editar_disciplina(disciplina_id):
    disciplina = db.get_or_404(Disciplina, disciplina_id)
    nome = request.form.get('nome', '').strip()
    outra = Disciplina.query.filter_by(nome=nome).first()

    if not nome:
        flash('Informe o nome da disciplina.', 'erro')
        return redirect(url_for('admin.disciplinas', editar=disciplina.id))
    if outra and outra.id != disciplina.id:
        flash('Já existe uma disciplina com esse nome.', 'erro')
        return redirect(url_for('admin.disciplinas', editar=disciplina.id))

    disciplina.nome = nome
    db.session.commit()
    flash('Disciplina atualizada.', 'sucesso')
    return redirect(url_for('admin.disciplinas'))

@admin_bp.route('/disciplinas/<int:disciplina_id>/excluir', methods=['POST'])
@login_obrigatorio('admin')
def excluir_disciplina(disciplina_id):
    disciplina = db.get_or_404(Disciplina, disciplina_id)

    if disciplina.alocacoes:
        flash('Não dá para excluir: a disciplina já está alocada a um professor em alguma turma.', 'erro')
    else:
        db.session.delete(disciplina)
        db.session.commit()
        flash('Disciplina excluída.', 'sucesso')
    return redirect(url_for('admin.disciplinas'))

# Alocações

@admin_bp.route('/alocacoes', methods=['GET', 'POST'])
@login_obrigatorio('admin')
def alocacoes():
    lista_turmas = Turma.query.order_by(Turma.ano_letivo.desc(), Turma.nome).all()
    lista_disciplinas = Disciplina.query.order_by(Disciplina.nome).all()
    lista_professores = Professor.query.join(Usuario).order_by(Usuario.nome).all()

    if request.method == 'POST':
        turma_id = request.form.get('turma_id', type=int)
        disciplina_id = request.form.get('disciplina_id', type=int)
        professor_id = request.form.get('professor_id', type=int)

        if not (turma_id and disciplina_id and professor_id):
            flash('Escolha a turma, a disciplina e o professor.', 'erro')
        elif not (db.session.get(Turma, turma_id)
                  and db.session.get(Disciplina, disciplina_id)
                  and db.session.get(Professor, professor_id)):
            flash('Turma, disciplina ou professor inválido.', 'erro')
        elif Alocacao.query.filter_by(turma_id=turma_id, disciplina_id=disciplina_id).first():
            flash('Essa disciplina já tem professor nessa turma.', 'erro')
        else:
            db.session.add(Alocacao(turma_id=turma_id,
                                    disciplina_id=disciplina_id,
                                    professor_id=professor_id))
            db.session.commit()
            flash('Alocação criada.', 'sucesso')
            return redirect(url_for('admin.alocacoes'))

    faltando = []
    if not lista_turmas:
        faltando.append('turmas')
    if not lista_disciplinas:
        faltando.append('disciplinas')
    if not lista_professores:
        faltando.append('professores')

    lista = (Alocacao.query
             .join(Turma).join(Disciplina)
             .order_by(Turma.ano_letivo.desc(), Turma.nome, Disciplina.nome)
             .all())

    return render_template('admin/alocacoes.html',
                           alocacoes=lista,
                           turmas=lista_turmas,
                           disciplinas=lista_disciplinas,
                           professores=lista_professores,
                           faltando=faltando)

# Professores

@admin_bp.route('/professores', methods=['GET', 'POST'])
@login_obrigatorio('admin')
def professores():
    if request.method == 'POST':
        nome = request.form.get('nome', '')
        email = request.form.get('email', '')
        senha = request.form.get('senha', '')

        try:
            criar_professor(
                request.form.get('nome', ''),
                request.form.get('email', ''),
                request.form.get('senha', '')
            )
        except ValueError as erro:
            flash(str(erro), 'erro')

        else:
            flash('Professor cadastrado', 'sucesso')
            return redirect(url_for('admin.professores'))

    lista = Professor.query.join(Usuario).order_by(Usuario.nome).all()
    return render_template('admin/professores.html', professores=lista)

# Turmas

@admin_bp.route('/turmas', methods=['GET', 'POST'])
@login_obrigatorio('admin')
def turmas():
    if request.method == 'POST':
        nome = request.form.get('nome', '').strip()
        ano = request.form.get('ano_letivo', type=int)
        turno = request.form.get('turno', '')

        if not nome:
            flash('Informe o nome da turma.', 'erro')
        elif ano is None or not 2000 <= ano <= 2100:
            flash('Informe um ano letivo entre 2000 e 2100.', 'erro')
        elif turno not in TURNOS:
            flash('Escolha um turno.', 'erro')
        elif Turma.query.filter_by(nome=nome, ano_letivo=ano).first():
            flash('Já existe uma turma com esse nome nesse ano letivo.', 'erro')
        else:
            db.session.add(Turma(nome=nome, ano_letivo=ano, turno=turno))
            db.session.commit()
            flash('Turma criada.', 'sucesso')
            return redirect(url_for('admin.turmas'))

    lista = Turma.query.order_by(Turma.ano_letivo.desc(), Turma.nome).all()
    return render_template('admin/turmas.html', turmas=lista, turnos=TURNOS)



# Matrículas

@admin_bp.route('/matriculas', methods=['GET', 'POST'])
@login_obrigatorio('admin')
def matriculas():
    if request.method == 'POST':
        try:
            matricular(
                request.form.get('aluno_id', type=int),
                request.form.get('turma_id', type=int),
            )
        except ValueError as erro:
            flash(str(erro), 'erro')
        else:
            flash('Matrícula realizada.', 'sucesso')
            return redirect(url_for('admin.matriculas'))

    lista_alunos = Aluno.query.join(Usuario).order_by(Usuario.nome).all()
    lista_turmas = Turma.query.order_by(Turma.ano_letivo.desc(), Turma.nome).all()

    faltando = []
    if not lista_alunos:
        faltando.append('alunos')
    if not lista_turmas:
        faltando.append('turmas')

    lista = (Matricula.query
             .join(Matricula.aluno).join(Aluno.usuario)
             .order_by(Usuario.nome)
             .all())

    return render_template('admin/matriculas.html',
                           matriculas=lista, alunos=lista_alunos,
                           turmas=lista_turmas, faltando=faltando)

# Alunos

@admin_bp.route('/alunos', methods=['GET', 'POST'])
@login_obrigatorio('admin')
def alunos():
    if request.method == 'POST':
        try:
            criar_aluno(
                request.form.get('nome', ''),
                request.form.get('email', ''),
                request.form.get('senha', ''),
                request.form.get('ra', ''),
                request.form.get('data_nascimento', ''),
            )
        except ValueError as erro:
            flash(str(erro), 'erro')
        else:
            flash('Aluno cadastrado.', 'sucesso')
            return redirect(url_for('admin.alunos'))

    lista = Aluno.query.join(Usuario).order_by(Usuario.nome).all()
    return render_template('admin/alunos.html', alunos=lista)



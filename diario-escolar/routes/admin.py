from flask import Blueprint, flash, redirect, render_template, request, url_for

from extensions import db

from models.usuario import Usuario
from models.disciplina import Disciplina
from models.turma import Turma
from models.professor import Professor

from routes.decorators import login_obrigatorio

from services.usuarios import criar_professor

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

    lista = Disciplina.query.order_by(Disciplina.nome).all()
    return render_template('admin/disciplinas.html', disciplinas=lista)

# Alocações

@admin_bp.route('/alocacoes', methods=['GET', 'POST'])
@login_obrigatorio('admin')
def alocacoes():
    return render_template('admin/alocacoes.html')

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
    return render_template('admin/matriculas.html')

# Alunos

@admin_bp.route('/alunos', methods=['GET', 'POST'])
@login_obrigatorio('admin')
def alunos():
    return render_template('admin/alunos.html')

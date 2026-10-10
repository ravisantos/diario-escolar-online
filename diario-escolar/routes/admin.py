from flask import Blueprint, flash, redirect, render_template, request, url_for

from extensions import db
from models.disciplina import Disciplina
from routes.decorators import login_obrigatorio

admin_bp = Blueprint('admin', __name__)

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
    return render_template('admin/professores.html')

# Turmas

@admin_bp.route('/turmas', methods=['GET', 'POST'])
@login_obrigatorio('admin')
def turmas():
    return render_template('admin/turmas.html')

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

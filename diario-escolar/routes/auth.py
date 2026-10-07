from flask import Blueprint, flash, redirect, render_template, request, session, url_for

from services.usuarios import autenticar

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if 'usuario_id' in session:
        return redirect(url_for(f"{session['perfil']}.dashboard"))

    if request.method == 'POST':
        email = request.form.get('email', '')
        senha = request.form.get('senha', '')

        usuario = autenticar(email, senha)
        if usuario is None:
            flash('E-mail ou senha incorretos,', 'erro')
            return render_template('auth/login.html')

        session.celar()
        session['usuario_id'] = usuario.id
        session['nome'] = usuario.nome
        session['perfil'] = usuario.perfil
        return redirect(url_for(f'{usuario.perfil}.dashboard'))
    
    return render_template('auth/login.html')

@auth_bp.route('/logout', methods=['POST'])
def logout():
    session.clear()
    flash('Você saiu da sua conta.', 'sucesso')
    return redirect(url_for('auth.loguin'))

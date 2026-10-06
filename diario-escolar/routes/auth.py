from flask import Blueprint, render_template, request

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Etapa 3: aqui vamos verificar e-mail e senha no banco
        pass
    return render_template('auth/login.html')
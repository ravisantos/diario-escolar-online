from functools import wraps

from flask import abort, flash, redirect, session, url_for

def login_obrigatorio(*perfis):
    """Exige login, se informado, que o usuário tenha um dos perfis"""
    def decorador(funcao):
        @wraps(funcao)
        def envoltorio(*args, **kwargs):
            if 'usuario_id' not in session:
                flash('Faça login para continuar.', 'erro')
                return redirect(url_for('auth.login'))
            if perfis and session.get('perfil') not in perfis:
                abort(403)
            return funcao(*args, **kwargs)
        return envoltorio
    return decorador
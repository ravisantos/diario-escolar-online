from extensions import db
from models.usuario import Usuario, PERFIS

def autenticar(email, senha):
    """Devolve o usurário se e-mail e senha estiverem certos; senão, none."""
    usuario  = Usuario.query.filter_by(email=email.strip().lower()).first()
    if usuario and usuario.ativo and usuario.verificar_senha(senha):
        return usuario
    return None

def criar_usuario(nome, email, senha, perfil):
    if perfil not in PERFIS:
        raise ValueError('Perfil inválido.')
    email = email.strip().lower()
    if Usuario.query.filter_by(email=email).first():
        raise ValueError('Já existe um usuário com esse e-mail.')
    if len(senha) < 6:
        raise ValueError('A senha precisa ter pelo menos 6 caracteres.')

    usuario = Usuario(nome=nome.strip(), email=email, perfil=perfil)
    usuario.definir_senha(senha)
    db.session.add(usuario)
    db.session.commit()

    return usuario
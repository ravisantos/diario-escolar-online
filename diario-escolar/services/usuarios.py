from extensions import db
from models.professor import Professor
from models.usuario import Usuario, PERFIS


def autenticar(email, senha):
    """Devolve o usuário se e-mail e senha estiverem certos; senão, None."""
    usuario = Usuario.query.filter_by(email=email.strip().lower()).first()
    if usuario and usuario.ativo and usuario.verificar_senha(senha):
        return usuario
    return None


def criar_usuario(nome, email, senha, perfil, salvar=True):
    nome = nome.strip()
    email = email.strip().lower()

    if not nome:
        raise ValueError('Informe o nome.')
    if '@' not in email:
        raise ValueError('Informe um e-mail válido.')
    if perfil not in PERFIS:
        raise ValueError('Perfil inválido.')
    if len(senha) < 6:
        raise ValueError('A senha precisa ter pelo menos 6 caracteres.')
    if Usuario.query.filter_by(email=email).first():
        raise ValueError('Já existe um usuário com esse e-mail.')

    usuario = Usuario(nome=nome, email=email, perfil=perfil)
    usuario.definir_senha(senha)
    db.session.add(usuario)
    if salvar:
        db.session.commit()
    return usuario


def criar_professor(nome, email, senha):
    """Cria o login e o cadastro do professor num único commit."""
    usuario = criar_usuario(nome, email, senha, 'professor', salvar=False)
    professor = Professor(usuario=usuario)
    db.session.add(professor)
    db.session.commit()
    return professor
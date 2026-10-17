from datetime import date

from extensions import db

from models.usuario import Usuario, PERFIS
from models.professor import Professor
from models.aluno import Aluno



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

def editar_usuario(usuario, nome, email, senha='', salvar=True):
    """Atualiza nome, e-mail e (opcionalmente) a senha. Senha vazia = mantém a atual."""
    nome = nome.strip()
    email = email.strip().lower()

    if not nome:
        raise ValueError('Informe o nome.')
    if '@' not in email:
        raise ValueError('Informe um e-mail válido.')

    outro = Usuario.query.filter_by(email=email).first()
    if outro and outro.id != usuario.id:
        raise ValueError('Já existe um usuário com esse e-mail.')

    if senha:
        if len(senha) < 6:
            raise ValueError('A senha precisa ter pelo menos 6 caracteres.')
        usuario.definir_senha(senha)

    usuario.nome = nome
    usuario.email = email
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

def criar_aluno(nome, email, senha, ra, data_nascimento=''):
    """Cria o login e o cadastro do aluno num único commit."""
    ra = ra.strip()
    if not ra:
        raise ValueError('Informe o RA do aluno.')
    if Aluno.query.filter_by(ra=ra).first():
        raise ValueError('Já existe um aluno com esse RA.')

    nascimento = None
    if data_nascimento.strip():
        try:
            nascimento = date.fromisoformat(data_nascimento.strip())
        except ValueError:
            raise ValueError('Data de nascimento inválida.')
        if nascimento > date.today():
            raise ValueError('A data de nascimento não pode ser no futuro.')

    usuario = criar_usuario(nome, email, senha, 'aluno', salvar=False)
    aluno = Aluno(usuario=usuario, ra=ra, data_nascimento=nascimento)
    db.session.add(aluno)
    db.session.commit()
    return aluno
from werkzeug.security import generate_password_hash, check_password_hash

from extensions import db

PERFIS = ('admin', 'professor', 'aluno')


class Usuario(db.Model):
    __tablename__ = 'usuarios'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    senha_hash = db.Column(db.String(255), nullable=False)
    perfil = db.Column(db.String(20), nullable=False)  # 'admin', 'professor' ou 'aluno'
    ativo = db.Column(db.Boolean, nullable=False, default=True)

    def definir_senha(self, senha):
        self.senha_hash = generate_password_hash(senha)

    def verificar_senha(self, senha):
        return check_password_hash(self.senha_hash, senha)

    def __repr__(self):
        return f'<Usuario {self.email} ({self.perfil})>'
from extensions import db
from datetime import date


class Aluno(db.Model):
    __tablename__ = 'alunos'

    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), unique=True, nullable=False)
    ra = db.Column(db.String(20), unique=True, nullable=False)  # número de registro do aluno
    data_nascimento = db.Column(db.Date)


    usuario = db.relationship('Usuario', backref=db.backref('aluno', uselist=False))
    matriculas = db.relationship('Matricula', back_populates='aluno')

    @property
    def idade(self): # (Calcula a idade do aluno)
        if not self.data_nascimento:
            return None
        hoje = date.today()
        anos = hoje.year - self.data_nascimento.year
        if (hoje.month, hoje.day) < (self.data_nascimento.month, self.data_nascimento.day):
            anos -= 1
        return anos

    def __repr__(self):
        return f'<Aluno {self.ra}>'
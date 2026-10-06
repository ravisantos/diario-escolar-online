from extensions import db


class Aluno(db.Model):
    __tablename__ = 'alunos'

    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), unique=True, nullable=False)
    ra = db.Column(db.String(20), unique=True, nullable=False)  # número de registro do aluno
    data_nascimento = db.Column(db.Date)

    usuario = db.relationship('Usuario', backref=db.backref('aluno', uselist=False))
    matriculas = db.relationship('Matricula', back_populates='aluno')

    def __repr__(self):
        return f'<Aluno {self.ra}>'
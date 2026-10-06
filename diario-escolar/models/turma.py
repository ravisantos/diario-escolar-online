from extensions import db


class Turma(db.Model):
    __tablename__ = 'turmas'
    __table_args__ = (db.UniqueConstraint('nome', 'ano_letivo'),)

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(50), nullable=False)  # ex.: '2º DS'
    ano_letivo = db.Column(db.Integer, nullable=False)  # ex.: 2026
    turno = db.Column(db.String(20))  # manhã, tarde ou noite

    matriculas = db.relationship('Matricula', back_populates='turma')
    alocacoes = db.relationship('Alocacao', back_populates='turma')

    def __repr__(self):
        return f'<Turma {self.nome}/{self.ano_letivo}>'
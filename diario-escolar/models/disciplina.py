from extensions import db


class Disciplina(db.Model):
    __tablename__ = 'disciplinas'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), unique=True, nullable=False)

    alocacoes = db.relationship('Alocacao', back_populates='disciplina')

    def __repr__(self):
        return f'<Disciplina {self.nome}>'
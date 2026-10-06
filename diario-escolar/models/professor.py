from extensions import db


class Professor(db.Model):
    __tablename__ = 'professores'

    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), unique=True, nullable=False)

    usuario = db.relationship('Usuario', backref=db.backref('professor', uselist=False))
    alocacoes = db.relationship('Alocacao', back_populates='professor')

    def __repr__(self):
        return f'<Professor {self.id}>'
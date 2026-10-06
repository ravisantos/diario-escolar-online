from extensions import db


class Nota(db.Model):
    """Nota de um aluno em uma avaliação."""
    __tablename__ = 'notas'
    __table_args__ = (db.UniqueConstraint('avaliacao_id', 'matricula_id'),)

    id = db.Column(db.Integer, primary_key=True)
    avaliacao_id = db.Column(db.Integer, db.ForeignKey('avaliacoes.id'), nullable=False)
    matricula_id = db.Column(db.Integer, db.ForeignKey('matriculas.id'), nullable=False)
    valor = db.Column(db.Float, nullable=False)

    avaliacao = db.relationship('Avaliacao', back_populates='notas')
    matricula = db.relationship('Matricula', back_populates='notas')
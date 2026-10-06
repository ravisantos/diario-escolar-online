from extensions import db


class Frequencia(db.Model):
    """Presença (ou falta) de um aluno em uma aula."""
    __tablename__ = 'frequencias'
    __table_args__ = (db.UniqueConstraint('aula_id', 'matricula_id'),)

    id = db.Column(db.Integer, primary_key=True)
    aula_id = db.Column(db.Integer, db.ForeignKey('aulas.id'), nullable=False)
    matricula_id = db.Column(db.Integer, db.ForeignKey('matriculas.id'), nullable=False)
    presente = db.Column(db.Boolean, nullable=False, default=True)

    aula = db.relationship('Aula', back_populates='frequencias')
    matricula = db.relationship('Matricula', back_populates='frequencias')
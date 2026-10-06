from extensions import db


class Aula(db.Model):
    """Uma aula dada pelo professor numa data (a chamada é feita em cima dela)."""
    __tablename__ = 'aulas'

    id = db.Column(db.Integer, primary_key=True)
    alocacao_id = db.Column(db.Integer, db.ForeignKey('alocacoes.id'), nullable=False)
    data = db.Column(db.Date, nullable=False)
    conteudo = db.Column(db.String(255))

    alocacao = db.relationship('Alocacao', back_populates='aulas')
    frequencias = db.relationship('Frequencia', back_populates='aula')
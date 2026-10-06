from extensions import db


class Avaliacao(db.Model):
    """Uma prova/trabalho de uma disciplina numa turma."""
    __tablename__ = 'avaliacoes'

    id = db.Column(db.Integer, primary_key=True)
    alocacao_id = db.Column(db.Integer, db.ForeignKey('alocacoes.id'), nullable=False)
    titulo = db.Column(db.String(120), nullable=False)
    bimestre = db.Column(db.Integer, nullable=False)  # 1 a 4
    data = db.Column(db.Date)
    valor_maximo = db.Column(db.Float, nullable=False, default=10.0)

    alocacao = db.relationship('Alocacao', back_populates='avaliacoes')
    notas = db.relationship('Nota', back_populates='avaliacao')
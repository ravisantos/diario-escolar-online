from extensions import db


class Alocacao(db.Model):
    """Diz qual professor dá qual disciplina em qual turma."""
    __tablename__ = 'alocacoes'
    __table_args__ = (db.UniqueConstraint('disciplina_id', 'turma_id'),)

    id = db.Column(db.Integer, primary_key=True)
    professor_id = db.Column(db.Integer, db.ForeignKey('professores.id'), nullable=False)
    disciplina_id = db.Column(db.Integer, db.ForeignKey('disciplinas.id'), nullable=False)
    turma_id = db.Column(db.Integer, db.ForeignKey('turmas.id'), nullable=False)

    professor = db.relationship('Professor', back_populates='alocacoes')
    disciplina = db.relationship('Disciplina', back_populates='alocacoes')
    turma = db.relationship('Turma', back_populates='alocacoes')
    avaliacoes = db.relationship('Avaliacao', back_populates='alocacao')
    aulas = db.relationship('Aula', back_populates='alocacao')
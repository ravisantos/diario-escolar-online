from extensions import db


class Matricula(db.Model):
    """Liga um aluno a uma turma."""
    __tablename__ = 'matriculas'
    __table_args__ = (db.UniqueConstraint('aluno_id', 'turma_id'),)

    id = db.Column(db.Integer, primary_key=True)
    aluno_id = db.Column(db.Integer, db.ForeignKey('alunos.id'), nullable=False)
    turma_id = db.Column(db.Integer, db.ForeignKey('turmas.id'), nullable=False)
    status = db.Column(db.String(20), nullable=False, default='ativa')  # ativa, transferida, cancelada

    aluno = db.relationship('Aluno', back_populates='matriculas')
    turma = db.relationship('Turma', back_populates='matriculas')
    notas = db.relationship('Nota', back_populates='matricula')
    frequencias = db.relationship('Frequencia', back_populates='matricula')
from extensions import db

from models.aluno import Aluno
from models.matricula import Matricula
from models.turma import Turma


def matricular(aluno_id, turma_id):
    """Matricula um aluno em uma turma (1 turma ativa por aluno em cada ano letivo)."""
    aluno = db.session.get(Aluno, aluno_id) if aluno_id else None
    turma = db.session.get(Turma, turma_id) if turma_id else None
    if aluno is None or turma is None:
        raise ValueError('Escolha um aluno e uma turma válidos.')

    if Matricula.query.filter_by(aluno_id=aluno.id, turma_id=turma.id).first():
        raise ValueError('Esse aluno já está matriculado nessa turma.')

    outra = (Matricula.query.join(Turma)
             .filter(Matricula.aluno_id == aluno.id,
                     Matricula.status == 'ativa',
                     Turma.ano_letivo == turma.ano_letivo)
             .first())
    if outra:
        raise ValueError(
            f'Esse aluno já está matriculado na turma {outra.turma.nome} em {turma.ano_letivo}.')

    matricula = Matricula(aluno_id=aluno.id, turma_id=turma.id, status='ativa')
    db.session.add(matricula)
    db.session.commit()
    return matricula
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
        raise ValueError('Esse aluno já tem matrícula nessa turma (se estiver cancelada, use Reativar).')

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


def cancelar_matricula(matricula):
    """Marca a matrícula como cancelada (o histórico de notas e faltas é mantido)."""
    if matricula.status != 'ativa':
        raise ValueError('Só dá para cancelar uma matrícula ativa.')
    matricula.status = 'cancelada'
    db.session.commit()


def reativar_matricula(matricula):
    """Volta uma matrícula cancelada para ativa (se o aluno não estiver em outra turma no ano)."""
    if matricula.status == 'ativa':
        raise ValueError('Essa matrícula já está ativa.')
    outra = (Matricula.query.join(Turma)
             .filter(Matricula.aluno_id == matricula.aluno_id,
                     Matricula.status == 'ativa',
                     Matricula.id != matricula.id,
                     Turma.ano_letivo == matricula.turma.ano_letivo)
             .first())
    if outra:
        raise ValueError(
            f'O aluno já tem matrícula ativa na turma {outra.turma.nome} em {matricula.turma.ano_letivo}.')
    matricula.status = 'ativa'
    db.session.commit()


def excluir_matricula(matricula):
    """Apaga a matrícula. Só é permitido se ela não tiver notas nem frequência."""
    if matricula.notas or matricula.frequencias:
        raise ValueError('Essa matrícula já tem notas ou frequência. Use "Cancelar" para manter o histórico.')
    db.session.delete(matricula)
    db.session.commit()

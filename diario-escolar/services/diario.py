from datetime import date

from extensions import db
from models.aula import Aula
from models.avaliacao import Avaliacao
from models.aluno import Aluno
from models.frequencia import Frequencia
from models.matricula import Matricula
from models.nota import Nota
from models.usuario import Usuario


def matriculas_ativas(turma_id):
    """Matrículas ativas de uma turma, em ordem alfabética pelo nome do aluno."""
    return (Matricula.query
            .join(Matricula.aluno).join(Aluno.usuario)
            .filter(Matricula.turma_id == turma_id, Matricula.status == 'ativa')
            .order_by(Usuario.nome)
            .all())


def _ler_data(texto, obrigatoria=False):
    texto = (texto or '').strip()
    if not texto:
        if obrigatoria:
            raise ValueError('Informe a data.')
        return None
    try:
        return date.fromisoformat(texto)
    except ValueError:
        raise ValueError('Data inválida.')


def _ler_numero(texto):
    """Aceita '7,5' ou '7.5'. Levanta ValueError se não for número."""
    return float(texto.strip().replace(',', '.'))


# ---------- avaliações e notas ----------

def criar_avaliacao(alocacao, titulo, bimestre, data, valor_maximo):
    titulo = (titulo or '').strip()
    if not titulo:
        raise ValueError('Informe o título da avaliação.')

    try:
        bimestre = int(bimestre)
    except (TypeError, ValueError):
        raise ValueError('Escolha o bimestre.')
    if bimestre not in (1, 2, 3, 4):
        raise ValueError('O bimestre deve ser de 1 a 4.')

    try:
        maximo = _ler_numero(valor_maximo or '10')
    except ValueError:
        raise ValueError('Valor máximo inválido.')
    if maximo <= 0:
        raise ValueError('O valor máximo deve ser maior que zero.')

    avaliacao = Avaliacao(alocacao_id=alocacao.id, titulo=titulo, bimestre=bimestre,
                          data=_ler_data(data), valor_maximo=maximo)
    db.session.add(avaliacao)
    db.session.commit()
    return avaliacao


def salvar_notas(avaliacao, valores):
    """valores: {matricula_id: texto}. Texto vazio = sem nota. Tudo ou nada."""
    existentes = {n.matricula_id: n for n in avaliacao.notas}
    novas = {}   # matricula_id -> float ou None (None = remover)

    for matricula in matriculas_ativas(avaliacao.alocacao.turma_id):
        texto = (valores.get(matricula.id) or '').strip()
        if not texto:
            novas[matricula.id] = None
            continue
        try:
            nota = _ler_numero(texto)
        except ValueError:
            raise ValueError(f'Nota inválida para {matricula.aluno.usuario.nome}.')
        if not 0 <= nota <= avaliacao.valor_maximo:
            raise ValueError(
                f'A nota de {matricula.aluno.usuario.nome} deve ficar entre 0 e {avaliacao.valor_maximo:g}.')
        novas[matricula.id] = nota

    for matricula_id, nota in novas.items():
        atual = existentes.get(matricula_id)
        if nota is None:
            if atual:
                db.session.delete(atual)
        elif atual:
            atual.valor = nota
        else:
            db.session.add(Nota(avaliacao_id=avaliacao.id, matricula_id=matricula_id, valor=nota))
    db.session.commit()


def excluir_avaliacao(avaliacao):
    if avaliacao.notas:
        raise ValueError('Essa avaliação já tem notas lançadas. Apague as notas (campos em branco) antes.')
    db.session.delete(avaliacao)
    db.session.commit()


# ---------- aulas e chamada ----------

def criar_aula(alocacao, data, conteudo):
    dia = _ler_data(data, obrigatoria=True)
    if dia > date.today():
        raise ValueError('A data da aula não pode ser no futuro.')
    aula = Aula(alocacao_id=alocacao.id, data=dia, conteudo=(conteudo or '').strip())
    db.session.add(aula)
    db.session.commit()
    return aula


def salvar_chamada(aula, presentes):
    """presentes: conjunto de ids de matrícula marcados como presentes."""
    existentes = {f.matricula_id: f for f in aula.frequencias}
    for matricula in matriculas_ativas(aula.alocacao.turma_id):
        presente = matricula.id in presentes
        registro = existentes.get(matricula.id)
        if registro:
            registro.presente = presente
        else:
            db.session.add(Frequencia(aula_id=aula.id, matricula_id=matricula.id, presente=presente))
    db.session.commit()


def excluir_aula(aula):
    if aula.frequencias:
        raise ValueError('Essa aula já tem chamada registrada e não pode ser excluída.')
    db.session.delete(aula)
    db.session.commit()

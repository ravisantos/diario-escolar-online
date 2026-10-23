from datetime import date

BIMESTRES = (1, 2, 3, 4)
MEDIA_MINIMA = 6.0   # abaixo disso a média aparece em vermelho no boletim


def boletim(matricula):
    """Monta o boletim de uma matrícula: uma entrada por disciplina da turma.

    Nota do bimestre = (soma das notas obtidas / soma dos valores máximos das
    avaliações já lançadas) x 10, assim avaliações com valor máximo diferente
    (ex.: prova de 10 e trabalho de 5) entram na proporção certa.
    Média final = média dos bimestres que já têm nota.
    """
    notas = {n.avaliacao_id: n.valor for n in matricula.notas}
    alocacoes = sorted(matricula.turma.alocacoes, key=lambda a: a.disciplina.nome)

    disciplinas = []
    for alocacao in alocacoes:
        avaliacoes = sorted(alocacao.avaliacoes,
                            key=lambda a: (a.bimestre, a.data or date.min, a.id))
        itens = []
        lancadas = {b: [] for b in BIMESTRES}   # bimestre -> [(nota, valor_maximo)]
        for avaliacao in avaliacoes:
            valor = notas.get(avaliacao.id)
            itens.append({'avaliacao': avaliacao, 'nota': valor})
            if valor is not None and avaliacao.bimestre in lancadas:
                lancadas[avaliacao.bimestre].append((valor, avaliacao.valor_maximo))

        medias = {}
        for bimestre, pares in lancadas.items():
            if pares:
                obtido = sum(v for v, _ in pares)
                maximo = sum(m for _, m in pares)
                medias[bimestre] = obtido / maximo * 10
            else:
                medias[bimestre] = None

        com_nota = [m for m in medias.values() if m is not None]
        disciplinas.append({
            'alocacao': alocacao,
            'itens': itens,
            'medias': medias,
            'media_final': sum(com_nota) / len(com_nota) if com_nota else None,
        })
    return disciplinas

FREQUENCIA_MINIMA = 75.0   # % mínimo de presença exigido


def frequencia(matricula):
    """Resumo de presenças/faltas de uma matrícula, por disciplina.

    Só entram aulas em que a chamada já foi feita para o aluno.
    Devolve (disciplinas, registros, geral).
    """
    registros = sorted(matricula.frequencias,
                       key=lambda f: (f.aula.data, f.id), reverse=True)

    por_alocacao = {}
    for registro in registros:
        por_alocacao.setdefault(registro.aula.alocacao_id, []).append(registro)

    disciplinas = []
    for alocacao in sorted(matricula.turma.alocacoes, key=lambda a: a.disciplina.nome):
        regs = por_alocacao.get(alocacao.id, [])
        disciplinas.append(_resumo(regs, alocacao=alocacao))

    return disciplinas, registros, _resumo(registros)


def _resumo(registros, **extra):
    total = len(registros)
    presencas = sum(1 for r in registros if r.presente)
    percentual = presencas / total * 100 if total else None
    return {
        'total': total,
        'presencas': presencas,
        'faltas': total - presencas,
        'percentual': percentual,
        'em_risco': percentual is not None and percentual < FREQUENCIA_MINIMA,
        **extra,
    }

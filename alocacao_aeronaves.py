import random

voos_diarios = {
    ("Sao Paulo (GRU)", "Rio de Janeiro (GIG)"): (1.0, 10),
    ("Sao Paulo (GRU)", "Brasilia (BSB)"): (2.0, 6),
    ("Sao Paulo (GRU)", "Belo Horizonte (CNF)"): (1.5, 8),
    ("Rio de Janeiro (GIG)", "Sao Paulo (GRU)"): (1.0, 10),
    ("Rio de Janeiro (GIG)", "Brasilia (BSB)"): (2.0, 5),
    ("Rio de Janeiro (GIG)", "Belo Horizonte (CNF)"): (1.5, 6),
    ("Brasilia (BSB)", "Sao Paulo (GRU)"): (2.0, 6),
    ("Brasilia (BSB)", "Rio de Janeiro (GIG)"): (2.0, 5),
    ("Brasilia (BSB)", "Belo Horizonte (CNF)"): (1.5, 7),
    ("Belo Horizonte (CNF)", "Sao Paulo (GRU)"): (1.5, 8),
    ("Belo Horizonte (CNF)", "Rio de Janeiro (GIG)"): (1.5, 6),
    ("Belo Horizonte (CNF)", "Brasilia (BSB)"): (1.5, 7)
}

def gerar_individuo():
    individuo = {}
    for rota, (duracao, num_voos_diarios) in voos_diarios.items():
        horarios = sorted(random.sample(range(6, 22), num_voos_diarios))
        individuo[rota] = horarios
    return individuo

def calcular_fitness(individuo):
    aviões = []  
    for rota, horarios in individuo.items():
        duracao_voo, _ = voos_diarios[rota]
        for horario in horarios:
            horario_inicio = horario - 1
            horario_fim = horario + duracao_voo + 0.5
            aviao_alocado = False
            for aviao in aviões:
                if all(horario_inicio >= f or horario_fim <= i for i, f in aviao):
                    aviao.append((horario_inicio, horario_fim))
                    aviao_alocado = True
                    break
            if not aviao_alocado:
                aviões.append([(horario_inicio, horario_fim)])
    return len(aviões)

def selecao_torneio(populacao, tamanho_torneio=5):
    torneio = random.sample(populacao, tamanho_torneio)
    melhor = min(torneio, key=calcular_fitness)
    return melhor

def crossover(pai1, pai2):
    filho = {}
    for rota in voos_diarios.keys():
        if random.random() < 0.5:
            filho[rota] = pai1[rota][:]
        else:
            filho[rota] = pai2[rota][:]
    return filho

def mutacao(individuo):
    rota = random.choice(list(voos_diarios.keys()))
    num_voos_diarios = voos_diarios[rota][1]
    if rota in individuo and individuo[rota]:
        index = random.randrange(len(individuo[rota]))
        novos_horarios = list(set(range(6, 22)) - set(individuo[rota]))
        if novos_horarios:
            individuo[rota][index] = random.choice(novos_horarios)
            individuo[rota] = sorted(individuo[rota])
    return individuo

def algoritmo_genetico(tamanho_populacao=50, geracoes=100, taxa_mutacao=0.1):
    populacao = [gerar_individuo() for _ in range(tamanho_populacao)]
    for _ in range(geracoes):
        nova_populacao = []
        while len(nova_populacao) < tamanho_populacao:
            pai1 = selecao_torneio(populacao)
            pai2 = selecao_torneio(populacao)
            filho = crossover(pai1, pai2)
            if random.random() < taxa_mutacao:
                filho = mutacao(filho)
            nova_populacao.append(filho)
        populacao = sorted(nova_populacao, key=calcular_fitness)[:tamanho_populacao]
    return min(populacao, key=calcular_fitness)

melhor_solucao = algoritmo_genetico()
print("Número mínimo de aviões necessários:", calcular_fitness(melhor_solucao))
for rota, horarios in melhor_solucao.items():
    print(f"Rota {rota}: {horarios}")

import random

# Dados dos voos diários
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
    for rota, (_, num_voos_diarios) in voos_diarios.items():
        horarios = sorted(random.sample(range(6, 22), num_voos_diarios)) # Gera horários de partida
        individuo[rota] = horarios
    return individuo

def calcular_fitness_e_avioes(individuo):
    aviões = []
    for rota, horarios in individuo.items():
        duracao_voo, _ = voos_diarios[rota]
        for horario in horarios:
            horario_inicio = horario - 1  # Tempo antes do embarque para manutenção
            horario_fim = horario + duracao_voo + 0.5  # Tempo após o desembarque para manutenção
            aviao_alocado = False
            for aviao in aviões:
                if all(horario_inicio >= f or horario_fim <= i for i, f in aviao):
                    aviao.append((horario_inicio, horario_fim))
                    aviao_alocado = True
                    break
            if not aviao_alocado:
                aviões.append([(horario_inicio, horario_fim)])
    # O inverso do número de aviões como fitness incentiva soluções com menos aviões
    fitness = 1 / len(aviões)
    return fitness, len(aviões)

def selecao_torneio(populacao, fitnesses, tamanho_torneio=5):
    indices_torneio = random.sample(range(len(populacao)), tamanho_torneio)
    torneio = [fitnesses[i] for i in indices_torneio]
    vencedor = indices_torneio[torneio.index(max(torneio))]
    return populacao[vencedor]

def crossover(pai1, pai2):
    filho = {}
    for rota in voos_diarios.keys():
        if random.random() < 0.5:
            filho[rota] = pai1[rota][:]
        else:
            filho[rota] = pai2[rota][:]
    return filho

def mutacao(individuo, taxa_mutacao=0.1):
    for rota, (_, num_voos_diarios) in voos_diarios.items():
        if random.random() < taxa_mutacao:
            horarios = sorted(random.sample(range(6, 22), num_voos_diarios))
            individuo[rota] = horarios
    return individuo

def algoritmo_genetico(tamanho_populacao=50, geracoes=100, taxa_mutacao=0.1):
    populacao = [gerar_individuo() for _ in range(tamanho_populacao)]
    fitnesses = [calcular_fitness_e_avioes(ind)[0] for ind in populacao]
    for _ in range(geracoes):
        nova_populacao = []
        nova_fitnesses = []
        while len(nova_populacao) < tamanho_populacao:
            pai1 = selecao_torneio(populacao, fitnesses)
            pai2 = selecao_torneio(populacao, fitnesses)
            filho = crossover(pai1, pai2)
            filho = mutacao(filho, taxa_mutacao)
            nova_populacao.append(filho)
            nova_fitnesses.append(calcular_fitness_e_avioes(filho)[0])
        populacao = [pop for _, pop in sorted(zip(nova_fitnesses, nova_populacao), key=lambda x: x[0], reverse=True)]
        fitnesses = sorted(nova_fitnesses, reverse=True)
    melhor_individuo = populacao[0]
    _, qtd_avioes = calcular_fitness_e_avioes(melhor_individuo)
    return melhor_individuo, qtd_avioes

# Para exibir as rotas e os horários da melhor solução encontrada pelo algoritmo genético,
# vamos formatar e imprimir essas informações de maneira legível.

def imprimir_rotas_e_horarios(melhor_solucao):
    for rota, horarios in melhor_solucao.items():
        origem, destino = rota
        print(f"Rota {origem} -> {destino}: Horários de partida -> {horarios}")



# Roda o algoritmo genético e imprime o melhor resultado encontrado, incluindo o número de aviões utilizados
melhor_solucao, qtd_avioes = algoritmo_genetico()
fitness_melhor_solucao, _ = calcular_fitness_e_avioes(melhor_solucao)
print(f"Fitness da melhor solução: {fitness_melhor_solucao}, Número de aviões utilizados: {qtd_avioes}")
imprimir_rotas_e_horarios(melhor_solucao)

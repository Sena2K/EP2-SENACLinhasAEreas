import random

# Definindo os dados do problema
rotas = [
    ("São Paulo (GRU)", "Rio de Janeiro (GIG)", 1.0),
    ("São Paulo (GRU)", "Brasília (BSB)", 2.0),
    ("São Paulo (GRU)", "Belo Horizonte (CNF)", 1.5),
    ("Rio de Janeiro (GIG)", "São Paulo (GRU)", 1.0),
    ("Rio de Janeiro (GIG)", "Brasília (BSB)", 2.0),
    ("Rio de Janeiro (GIG)", "Belo Horizonte (CNF)", 1.5),
    ("Brasília (BSB)", "São Paulo (GRU)", 2.0),
    ("Brasília (BSB)", "Rio de Janeiro (GIG)", 2.0),
    ("Brasília (BSB)", "Belo Horizonte (CNF)", 1.5),
    ("Belo Horizonte (CNF)", "São Paulo (GRU)", 1.5),
    ("Belo Horizonte (CNF)", "Rio de Janeiro (GIG)", 1.5),
    ("Belo Horizonte (CNF)", "Brasília (BSB)", 1.5)
]

voos_diarios = {
    ("São Paulo (GRU)", "Rio de Janeiro (GIG)"): 10,
    ("São Paulo (GRU)", "Brasília (BSB)"): 6,
    ("São Paulo (GRU)", "Belo Horizonte (CNF)"): 8,
    ("Rio de Janeiro (GIG)", "São Paulo (GRU)"): 10,
    ("Rio de Janeiro (GIG)", "Brasília (BSB)"): 5,
    ("Rio de Janeiro (GIG)", "Belo Horizonte (CNF)"): 6,
    ("Brasília (BSB)", "São Paulo (GRU)"): 6,
    ("Brasília (BSB)", "Rio de Janeiro (GIG)"): 5,
    ("Brasília (BSB)", "Belo Horizonte (CNF)"): 7,
    ("Belo Horizonte (CNF)", "São Paulo (GRU)"): 8,
    ("Belo Horizonte (CNF)", "Rio de Janeiro (GIG)"): 6,
    ("Belo Horizonte (CNF)", "Brasília (BSB)"): 7
}

def gerar_individuo():
    return {rota: random.randint(1, 10) for rota in rotas}

def calcular_fitness(individuo):
    avioes_usados = set()
    for aviao in individuo.values():
        avioes_usados.add(aviao)
    return len(avioes_usados)

# Função de seleção por tragedia
def selecao_tragedia(populacao, num_a_manter):
    populacao_ordenada = sorted(populacao, key=lambda ind: calcular_fitness(ind))
    return populacao_ordenada[:num_a_manter]

# Função de mutação de troca de genes
def mutacao(individuo):
    rota = random.choice(rotas)
    individuo[rota] = random.randint(1, 10)
    return individuo

def crossover(pai1, pai2):
    filho = {}
    for rota in rotas:
        if random.random() < 0.5:
            filho[rota] = pai1[rota]
        else:
            filho[rota] = pai2[rota]
    return filho

def algoritmo_genetico(tamanho_populacao, geracoes):
    populacao = [gerar_individuo() for _ in range(tamanho_populacao)]
    for _ in range(geracoes):
        populacao = selecao_tragedia(populacao, tamanho_populacao // 2)
        while len(populacao) < tamanho_populacao:
            pai1 = random.choice(populacao)
            pai2 = random.choice(populacao)
            filho = crossover(pai1, pai2)
            if random.random() < 0.1:  # Chance de mutação
                filho = mutacao(filho)
            populacao.append(filho)
    melhor_individuo = min(populacao, key=lambda ind: calcular_fitness(ind))
    return melhor_individuo

melhor_solucao = algoritmo_genetico(tamanho_populacao=50, geracoes=100)
print("Melhor alocação de aviões:")
for rota, num_avioes in melhor_solucao.items():
    print(f"{rota[0]} -> {rota[1]}: {num_avioes} aviões")
print("Fitness:", calcular_fitness(melhor_solucao))
import random

# Definição das rotas, tempos de voo e número de voos diários
rotas = [
    ("GRU", "GIG", 1.0, 10),
    ("GRU", "BSB", 2.0, 6),
    ("GRU", "CNF", 1.5, 8),
    ("GIG", "GRU", 1.0, 10),
    ("GIG", "BSB", 2.0, 5),
    ("GIG", "CNF", 1.5, 6),
    ("BSB", "GRU", 2.0, 6),
    ("BSB", "GIG", 2.0, 5),
    ("BSB", "CNF", 1.5, 7),
    ("CNF", "GRU", 1.5, 8),
    ("CNF", "GIG", 1.5, 6),
    ("CNF", "BSB", 1.5, 7)
]

# Função de fitness: calcula o número total de aeronaves usadas
def fitness(roteamento):
    aeronaves_utilizadas = set()
    for voo in roteamento:
        aeronaves_utilizadas.add(voo[0])
    return len(aeronaves_utilizadas)

# Função de seleção por torneio
def selecao_torneio(populacao, fitness_populacao, tamanho_torneio):
    torneio = random.sample(list(zip(populacao, fitness_populacao)), tamanho_torneio)
    vencedor = min(torneio, key=lambda x: x[1])[0]
    return vencedor

# Função de mutação de troca de genes
def mutacao_troca_genes(roteamento):
    i, j = random.sample(range(len(roteamento)), 2)
    roteamento[i], roteamento[j] = roteamento[j], roteamento[i]
    return roteamento

# Função de crossover de um ponto
def crossover_um_ponto(roteamento1, roteamento2):
    ponto_corte = random.randint(0, len(roteamento1) - 1)
    filho1 = roteamento1[:ponto_corte] + roteamento2[ponto_corte:]
    filho2 = roteamento2[:ponto_corte] + roteamento1[ponto_corte:]
    return filho1, filho2

# Algoritmo genético
def algoritmo_genetico(populacao, tamanho_populacao, num_geracoes, taxa_mutacao, taxa_crossover, tamanho_torneio):
    for _ in range(num_geracoes):
        nova_populacao = []
        fitness_populacao = [fitness(roteamento) for roteamento in populacao]

        for _ in range(tamanho_populacao // 2):
            pai1 = selecao_torneio(populacao, fitness_populacao, tamanho_torneio)
            pai2 = selecao_torneio(populacao, fitness_populacao, tamanho_torneio)

            if random.random() < taxa_crossover:
                filho1, filho2 = crossover_um_ponto(pai1, pai2)
            else:
                filho1, filho2 = pai1[:], pai2[:]

            if random.random() < taxa_mutacao:
                filho1 = mutacao_troca_genes(filho1)
            if random.random() < taxa_mutacao:
                filho2 = mutacao_troca_genes(filho2)

            nova_populacao.append(filho1)
            nova_populacao.append(filho2)

        populacao = nova_populacao

    melhor_roteamento = min(populacao, key=fitness)
    return melhor_roteamento, fitness(melhor_roteamento)

# Exemplo de uso
populacao_inicial = [random.sample(rotas, len(rotas)) for _ in range(50)]  # População inicial com alocações aleatórias
melhor_roteamento, num_aeronaves = algoritmo_genetico(populacao_inicial, 50, 1000, 0.01, 0.8, 3)
print("Melhor roteamento:", melhor_roteamento)
print("Número de aeronaves necessárias:", num_aeronaves)

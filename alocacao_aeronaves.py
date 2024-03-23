import random

import numpy as np
from matplotlib import pyplot as plt

# Definindo os dados do problema
# rotas = [
#     ("São Paulo (GRU)", "Rio de Janeiro (GIG)"),
#     ("São Paulo (GRU)", "Brasília (BSB)"),
#     ("São Paulo (GRU)", "Belo Horizonte (CNF)"),
#     ("Rio de Janeiro (GIG)", "São Paulo (GRU)"),
#     ("Rio de Janeiro (GIG)", "Brasília (BSB)"),
#     ("Rio de Janeiro (GIG)", "Belo Horizonte (CNF)"),
#     ("Brasília (BSB)", "São Paulo (GRU)"),
#     ("Brasília (BSB)", "Rio de Janeiro (GIG)"),
#     ("Brasília (BSB)", "Belo Horizonte (CNF)"),
#     ("Belo Horizonte (CNF)", "São Paulo (GRU)"),
#     ("Belo Horizonte (CNF)", "Rio de Janeiro (GIG)"),
#     ("Belo Horizonte (CNF)", "Brasília (BSB)")
# ]

voos_diarios = {
    ("São Paulo (GRU)", "Rio de Janeiro (GIG)"): (1.0, 10),
    ("São Paulo (GRU)", "Brasília (BSB)"): (2.0, 6),
    ("São Paulo (GRU)", "Belo Horizonte (CNF)"): (1.5, 8),
    ("Rio de Janeiro (GIG)", "São Paulo (GRU)"): (1.0, 10),
    ("Rio de Janeiro (GIG)", "Brasília (BSB)"): (2.0, 5),
    ("Rio de Janeiro (GIG)", "Belo Horizonte (CNF)"): (1.5, 6),
    ("Brasília (BSB)", "São Paulo (GRU)"): (2.0, 6),
    ("Brasília (BSB)", "Rio de Janeiro (GIG)"): (2.0, 5),
    ("Brasília (BSB)", "Belo Horizonte (CNF)"): (1.5, 7),
    ("Belo Horizonte (CNF)", "São Paulo (GRU)"): (1.5, 8),
    ("Belo Horizonte (CNF)", "Rio de Janeiro (GIG)"): (1.5, 6),
    ("Belo Horizonte (CNF)", "Brasília (BSB)"): (1.5, 7)
}

def gerar_individuo():
    individuo = {}
    for rota in voos_diarios:
        duracao_voo, num_voos_diarios = voos_diarios[rota]
        horarios = []
        for _ in range(num_voos_diarios):
            # gerando horarios aleatorios entre 6h e 22h, levando em consideraçao a duraçao do voo
            horario = random.randint(6, 22 - int(duracao_voo))
            horarios.append(horario)
        individuo[rota] = horarios
    return individuo

def calcular_fitness(individuo):
    avioes_ocupados = set()
    penalidade = 0
    for rota, horarios in individuo.items():
        duracao_voo, _ = voos_diarios[rota] # ignorando o segundo valor da dupla so isso, python god.
        for horario in horarios:
            for hora in range(horario, horario + int(duracao_voo) + 1):
                if hora >= 6 and hora <= 22:
                    avioes_ocupados.add(hora)
    for hora in range(6, 23):
        if hora not in avioes_ocupados:
            penalidade += 1
    return len(avioes_ocupados) + penalidade
def selecao_torneio(populacao, tamanho_torneio):
    torneio = random.sample(populacao, tamanho_torneio)
    melhor_individuo = min(torneio, key=lambda ind: calcular_fitness(ind))
    return melhor_individuo

def crossover(pai1, pai2):
    rotas_pai1 = list(pai1.keys())
    rotas_pai2 = list(pai2.keys())
    rota_comum = random.choice(list(set(rotas_pai1) & set(rotas_pai2)))  # Escolhe uma rota em comum
    horarios_pai1 = pai1[rota_comum]
    horarios_pai2 = pai2[rota_comum]
    filho = {}
    for rota in rotas_pai1 + rotas_pai2:
        if rota == rota_comum:
            horarios_filho = []
            for h1, h2 in zip(horarios_pai1, horarios_pai2):
                horarios_filho.append(random.choice([h1, h2]))
            filho[rota] = horarios_filho
        else:
            if rota in pai1:
                filho[rota] = pai1[rota]
            else:
                filho[rota] = pai2[rota]
    return filho

def mutacao(individuo):
    rota = random.choice(list(individuo.keys()))
    horarios = individuo[rota]
    duracao_voo, _ = voos_diarios[rota]
    horarios[random.randint(0, len(horarios) - 1)] = random.randint(6, 22 - int(duracao_voo))
    individuo[rota] = horarios
    return individuo

def algoritmo_genetico(tamanho_populacao, geracoes, tamanho_torneio):
    populacao = [gerar_individuo() for _ in range(tamanho_populacao)]
    for _ in range(geracoes):
        nova_populacao = []
        for _ in range(tamanho_populacao):
            pai1 = selecao_torneio(populacao, tamanho_torneio)
            pai2 = selecao_torneio(populacao, tamanho_torneio)
            filho = crossover(pai1, pai2)
            if random.random() < 0.1:  # Chance de mutaçao
                filho = mutacao(filho)
            nova_populacao.append(filho)
        populacao = nova_populacao
    melhor_individuo = min(populacao, key=lambda ind: calcular_fitness(ind))
    return melhor_individuo


melhor_solucao = algoritmo_genetico(tamanho_populacao=50, geracoes=100, tamanho_torneio=5)
print("Melhor alocação de aviões:")
for rota, horarios in melhor_solucao.items():
    print(f"{rota[0]} -> {rota[1]}: {horarios}")
print("Fitness:", calcular_fitness(melhor_solucao))


#Isso aqui foi uma ia que fez obviamente kkkkkk, dps eu tiro so qria ver
# def analisar_resultados(melhor_solucao):
#   """
#   Realiza uma análise detalhada da melhor solução do algoritmo genético.
#
#   Args:
#     melhor_solucao: Dicionário que representa a melhor solução.
#
#   Returns:
#     None.
#   """
#
#   # Distribuição dos horários dos voos
#   for rota, horarios in melhor_solucao.items():
#     # Gráfico de dispersão
#     plt.scatter(horarios, range(len(horarios)))
#     plt.xlabel("Horário de Partida")
#     plt.ylabel("Frequência")
#     plt.title(f"Distribuição dos horários - {rota}")
#     plt.show()
#
#     # Histograma
#     plt.hist(horarios)
#     plt.xlabel("Horário de Partida")
#     plt.ylabel("Frequência")
#     plt.title(f"Histograma dos horários - {rota}")
#     plt.show()
#
#   # Sobreposição de horários
#   matriz_sobreposicao = np.zeros((len(voos_diarios), len(voos_diarios)))
#   for rota1, horarios1 in melhor_solucao.items():
#     for rota2, horarios2 in melhor_solucao.items():
#       if rota1 != rota2:
#         for h1 in horarios1:
#           for h2 in horarios2:
#             if h1 == h2:
#               matriz_sobreposicao[voos_diarios.index((rota1, rota2))] += 1
#
#   # Imprimir matriz de sobreposição
#   print("Matriz de sobreposição:")
#   print(matriz_sobreposicao)
#
#   # Identificar rotas com maior sobreposição
#   rotas_sobrepostas = []
#   for i in range(len(matriz_sobreposicao)):
#     for j in range(len(matriz_sobreposicao[0])):
#       if matriz_sobreposicao[i][j] > 0:
#         rotas_sobrepostas.append((voos_diarios.keys()[i], voos_diarios.keys()[j]))
#
#   # Imprimir rotas com maior sobreposição
#   print("Rotas com maior sobreposição:")
#   print(rotas_sobrepostas)
#
#   # Utilização de cada aeronave
#   avioes_utilizados = {}
#   for rota, horarios in melhor_solucao.items():
#     duracao_voo, num_voos_diarios = voos_diarios[rota]
#     avioes_utilizados[rota] = num_voos_diarios * (int(duracao_voo) + 1)
#
#   # Gráfico de barras
#   plt.bar(avioes_utilizados.keys(), avioes_utilizados.values())
#   plt.xlabel("Rota")
#   plt.ylabel("Número de Voos")
#   plt.title("Utilização de cada aeronave")
#   plt.show()
#
# # Executar a função
# analisar_resultados(melhor_solucao)
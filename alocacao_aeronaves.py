from typing import Dict, List, Tuple
import random

Route = Tuple[str, str]
Schedule = Dict[Route, List[int]]
FitnessDetails = Tuple[float, int, Dict[int, List[Tuple[Route, int, float]]]]

voos_diarios: Dict[Route, Tuple[float, int]] = {
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

def gerar_individuo() -> Schedule:
    individuo: Schedule = {}
    for rota, (_, num_voos_diarios) in voos_diarios.items():
        horarios = sorted(random.sample(range(6, 22), num_voos_diarios))
        individuo[rota] = horarios
    return individuo

def calcular_penalidade_tempo_ocioso(avioes_detalhes, limite_tempo_ocioso):
    penalidade = 0
    for detalhes in avioes_detalhes.values():
        for i in range(1, len(detalhes)):
            tempo_ocioso = detalhes[i][1] - detalhes[i-1][2]  # Corrigido para o índice correto
            if tempo_ocioso > limite_tempo_ocioso:
                penalidade += tempo_ocioso - limite_tempo_ocioso
    return penalidade

def otimizar_alocacao_e_horarios(individuo: Schedule, limite_tempo_ocioso: int = 4) -> FitnessDetails:
    avioes_detalhes = {}
    avioes_horarios = {}
    aviao_id = 0

    todos_voos = [(rota, horario) for rota, horarios in individuo.items() for horario in horarios]
    todos_voos.sort(key=lambda x: x[1])

    for rota, horario_partida in todos_voos:
        origem, destino = rota
        duracao_voo, _ = voos_diarios[rota]
        horario_partida_real = horario_partida - 1
        horario_chegada = horario_partida + duracao_voo + 0.5

        aviao_alocado = None
        for aviao, (ult_destino, ult_horario_chegada) in avioes_horarios.items():
            if origem == ult_destino and (ult_horario_chegada + 1.5) <= horario_partida_real:
                aviao_alocado = aviao
                break

        if aviao_alocado is not None:
            avioes_detalhes[aviao_alocado].append((rota, horario_partida, horario_chegada))
            avioes_horarios[aviao_alocado] = (destino, horario_chegada)
        else:
            aviao_id += 1
            avioes_detalhes[aviao_id] = [(rota, horario_partida, horario_chegada)]
            avioes_horarios[aviao_id] = (destino, horario_chegada)

    num_avioes = len(avioes_detalhes)

    penalidade_tempo_ocioso = calcular_penalidade_tempo_ocioso(avioes_detalhes, limite_tempo_ocioso)
    fitness = 1 / (1 + penalidade_tempo_ocioso * 0.05 + num_avioes * 0.05)
    return fitness, num_avioes, avioes_detalhes


def selecao_por_torneio(populacao, fitness_populacao, tamanho_torneio, num_pais):
    pais_selecionados = []
    for _ in range(num_pais):
        indices_torneio = random.sample(range(len(populacao)), tamanho_torneio)
        melhor_fitness = float('-inf')
        melhor_individuo = None
        for indice in indices_torneio:
            if fitness_populacao[indice] > melhor_fitness:
                melhor_fitness = fitness_populacao[indice]
                melhor_individuo = populacao[indice]
        pais_selecionados.append(melhor_individuo)
    return pais_selecionados

def mutacao(individuo: Schedule, taxa_mutacao: float) -> Schedule:
    novo_individuo = individuo.copy()
    for aviao, horarios in novo_individuo.items():
        if len(horarios) < len(voos_diarios) / len(novo_individuo) and random.random() < taxa_mutacao:
            for rota in random.sample(list(voos_diarios.keys()), len(horarios)):
                if len(novo_individuo[rota]) > 1:
                    novo_horario = novo_individuo[rota].pop()
                    novo_individuo[rota].sort()
                    horarios.append(novo_horario)
                    horarios.sort()
    return novo_individuo

def crossover(pai1: Schedule, pai2: Schedule, taxa_crossover: float) -> Tuple[Schedule, Schedule]:
    if random.random() > taxa_crossover:
        return pai1, pai2
    filho1, filho2 = pai1.copy(), pai2.copy()
    ponto_corte = random.randint(1, len(pai1) - 2)
    for i, rota in enumerate(pai1):
        if i >= ponto_corte:
            filho1[rota], filho2[rota] = filho2[rota], filho1[rota]
    return filho1, filho2

def algoritmo_genetico(populacao_inicial, geracoes, taxa_mutacao, taxa_crossover, tamanho_torneio, num_pais):
    populacao = populacao_inicial
    historico_fitness = []
    for geracao in range(geracoes):
        fitness_populacao = [otimizar_alocacao_e_horarios(individuo)[0] for individuo in populacao]
        pais = selecao_por_torneio(populacao, fitness_populacao, tamanho_torneio, num_pais)
        nova_populacao = []
        while len(nova_populacao) < len(populacao):
            pai1, pai2 = random.sample(pais, 2)
            filho1, filho2 = crossover(pai1, pai2, taxa_crossover)
            filho1 = mutacao(filho1, taxa_mutacao)
            filho2 = mutacao(filho2, taxa_mutacao)
            nova_populacao.extend([filho1, filho2])
        populacao = nova_populacao[:len(populacao)]
        melhor_fitness = max(fitness_populacao)
        historico_fitness.append(melhor_fitness)
        print(f"Geração {geracao + 1}: Melhor Fitness = {melhor_fitness}")
    return populacao, historico_fitness

NUM_INDIVIDUOS = 50
GERACOES = 50
TAXA_MUTACAO = 0.1
TAXA_CROSSOVER = 0.7
TAMANHO_TORNEIO = 5
NUM_PAIS = 25

populacao_inicial = [gerar_individuo() for _ in range(NUM_INDIVIDUOS)]
populacao_final, historico_fitness = algoritmo_genetico(populacao_inicial, GERACOES, TAXA_MUTACAO, TAXA_CROSSOVER, TAMANHO_TORNEIO, NUM_PAIS)
print("\nHistórico de Fitness por Geração:")
for i, fitness in enumerate(historico_fitness, 1):
    print(f"Geração {i}: {fitness}")

melhor_individuo = max(populacao_final, key=lambda individuo: otimizar_alocacao_e_horarios(individuo)[0])
fitness, num_avioes, avioes_detalhes = otimizar_alocacao_e_horarios(melhor_individuo)
saida = f"Fitness: {fitness}, Número de aviões: {num_avioes}\n\n"
for aviao, voos in avioes_detalhes.items():
    saida += f"Avião {aviao}:\n"
    for rota, partida, chegada in voos:
        saida += f"  {rota[0]} -> {rota[1]} às {partida}h\n"
    saida += "\n"
print(saida.strip())

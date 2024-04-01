from typing import Dict, List, Tuple
import random
Rota = Tuple[str, str]
Schedule = Dict[Rota, List[int]]
Fitness = Tuple[float, int, Dict[int, List[Tuple[Rota, int]]]]

voos_diarios: Dict[Rota, Tuple[float, int]] = {
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
    return {rota: sorted(random.sample(range(6, 22), num_voos)) for rota, (_, num_voos) in voos_diarios.items()}

def calcular_tempo_ocioso_e_uso_de_avioes(individuo: Schedule) -> Tuple[int, int, float]:
    """Calcula o número total de aviões usados, o total de tempo ocioso e penalidades por uso ineficiente."""
    voos_organizados = [(rota, horario) for rota, horarios in individuo.items() for horario in horarios]
    voos_organizados.sort(key=lambda x: x[1]) 
    
    avioes_em_uso = {}
    tempo_ocioso_total = 0
    ultimo_horario_por_aviao = {}
    
    for rota, horario_partida in voos_organizados:
        duracao_voo = voos_diarios[rota][0]
        horario_chegada = horario_partida + duracao_voo
        aviao_alocado = None
        
        for aviao, (ultima_chegada, ultima_destino) in ultimo_horario_por_aviao.items():
            if ultima_destino == rota[0] and horario_partida >= ultima_chegada + 1.5: 
                aviao_alocado = aviao
                tempo_ocioso_total += horario_partida - ultima_chegada - 1.5
                break
                
        if not aviao_alocado:
            aviao_alocado = len(avioes_em_uso) + 1
            avioes_em_uso[aviao_alocado] = []
            
        avioes_em_uso[aviao_alocado].append((rota, horario_partida, horario_chegada))
        ultimo_horario_por_aviao[aviao_alocado] = (horario_chegada, rota[1])
    
    penalidade = len(avioes_em_uso) * 10 + tempo_ocioso_total
    
    return len(avioes_em_uso), tempo_ocioso_total, 1 / (1 + penalidade)  

def fitness(individuo: Schedule) -> float:
    _, _, fitness_value = calcular_tempo_ocioso_e_uso_de_avioes(individuo)
    return fitness_value

def selecao(populacao: List[Schedule], fitnesses: List[float]) -> List[Schedule]:
    selecionados = []
    for _ in range(len(populacao) // 2):
        i, j = random.sample(range(len(populacao)), 2)
        selecionados.append(populacao[i] if fitnesses[i] > fitnesses[j] else populacao[j])
    return selecionados

def mutacao(individuo: Schedule, taxa_mutacao: float = 0.1) -> Schedule:
    if random.random() < taxa_mutacao:
        rota = random.choice(list(individuo.keys()))
        individuo[rota] = sorted(random.sample(range(6, 22), len(individuo[rota])))
    return individuo

def crossover(pai1: Schedule, pai2: Schedule) -> Tuple[Schedule, Schedule]:
    filho1, filho2 = pai1.copy(), pai2.copy()
    for rota in filho1.keys():
        if random.random() > 0.5:
            filho1[rota], filho2[rota] = filho2[rota], filho1[rota]
    return filho1, filho2

def algoritmo_genetico(geracoes: int = 100, tamanho_populacao: int = 50) -> Tuple[Schedule, List[float]]:
    populacao = [gerar_individuo() for _ in range(tamanho_populacao)]
    historico_fitness = []

    for g in range(geracoes):
        fitnesses = [fitness(individuo) for individuo in populacao]
        melhor_fitness = max(fitnesses)
        historico_fitness.append(melhor_fitness)
        
        # Imprime o melhor fitness desta geração
        print(f"Geração {g + 1}: Melhor Fitness = {melhor_fitness}")
        
        nova_populacao = selecao(populacao, fitnesses)
        descendentes = []
        while len(descendentes) < tamanho_populacao:
            pai1, pai2 = random.sample(nova_populacao, 2)
            filho1, filho2 = crossover(pai1, pai2)
            descendentes.append(mutacao(filho1))
            descendentes.append(mutacao(filho2))
        populacao = descendentes[:tamanho_populacao]
    
    melhor_individuo = max(populacao, key=fitness)
    return melhor_individuo, historico_fitness

melhor_individuo, historico_fitness = algoritmo_genetico(geracoes=50, tamanho_populacao=100)

def formatar_e_imprimir_resultado(melhor_individuo: Schedule):
    voos_organizados = []
    for rota, horarios in melhor_individuo.items():
        for horario in horarios:
            voos_organizados.append((rota, horario))
    voos_organizados.sort(key=lambda x: x[1])

    alocacao_avioes = {}
    ultimo_destino = {}
    ultimo_horario_chegada = {}
    aviao_id = 1

    for rota, partida in voos_organizados:
        origem, destino = rota
        duracao_voo = voos_diarios[rota][0]
        horario_chegada = partida + duracao_voo

        aviao_alocado = None
        for aviao, dest in ultimo_destino.items():
            if dest == origem and ultimo_horario_chegada[aviao] <= partida:
                aviao_alocado = aviao
                break

        if aviao_alocado is None:
            aviao_alocado = aviao_id
            aviao_id += 1

        alocacao_avioes.setdefault(aviao_alocado, []).append((rota, partida))
        ultimo_destino[aviao_alocado] = destino
        ultimo_horario_chegada[aviao_alocado] = horario_chegada

    for aviao, voos in alocacao_avioes.items():
        print(f"Avião {aviao}:")
        for rota, horario in voos:
            print(f"  {rota[0]} -> {rota[1]} às {horario}h")
        print()

melhor_individuo, historico_fitness = algoritmo_genetico(geracoes=50, tamanho_populacao=50)

print("\nHistórico de Fitness por Geração:")
for i, fitness in enumerate(historico_fitness, 1):
    print(f"Geração {i}: {fitness}")

formatar_e_imprimir_resultado(melhor_individuo)




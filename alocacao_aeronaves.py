import random

# Definindo os dados do problema
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
    for rota in voos_diarios:
        duracao_voo, num_voos_diarios = voos_diarios[rota]
        horarios = []
        for _ in range(num_voos_diarios):
            embarque = 1.0
            desembarque = 0.5
            while True:
                horario = random.randint(6 + int(embarque), 24 - int(duracao_voo) - int(desembarque))
                if horario not in horarios:  # Verifica se o horário já foi utilizado
                    break
            horarios.append(horario)
        individuo[rota] = horarios
    return individuo

def calcular_fitness(individuo):
    avioes_ocupados = set()
    for rota, horarios in individuo.items():
        duracao_voo, _ = voos_diarios[rota]
        embarque = 1.0
        desembarque = 0.5
        for horario in horarios:
            for hora in range(horario - int(embarque), horario + int(duracao_voo) + int(desembarque) + 1):
                if 6 <= hora <= 24:
                    avioes_ocupados.add(hora)

    aeronaves_nao_utilizadas = set(range(6, 25)) - avioes_ocupados
    penalidade = len(aeronaves_nao_utilizadas)

    return len(avioes_ocupados) + penalidade

def validar_solucao(solucao):
    # Verificar cobertura de voos
    voos_cobertos = set()
    for rota, horarios in solucao.items():
        for horario in horarios:
            voos_cobertos.add((rota[0], rota[1]))

    todas_rotas = set(voos_diarios.keys())
    if voos_cobertos != todas_rotas:
        return False, "Alguns voos nao estao cobertos pela alocacao de avioes."

    return True, "Solucao valida."


def algoritmo_genetico(tamanho_populacao, geracoes, tamanho_torneio):
    populacao = [gerar_individuo() for _ in range(tamanho_populacao)]
    for _ in range(geracoes):
        nova_populacao = []
        for _ in range(tamanho_populacao):
            pai1 = selecao_torneio(populacao, tamanho_torneio)
            pai2 = selecao_torneio(populacao, tamanho_torneio)
            filho = crossover(pai1, pai2)
            if random.random() < 0.1:  # Chance de mutacao
                filho = mutacao_troca_voos(filho)
            nova_populacao.append(filho)
        populacao = nova_populacao
    melhor_solucao = min(populacao, key=lambda ind: calcular_fitness(ind))
    return melhor_solucao

def selecao_torneio(populacao, tamanho_torneio):
    torneio = random.sample(populacao, tamanho_torneio)
    melhor_individuo = min(torneio, key=lambda ind: calcular_fitness(ind))
    return melhor_individuo

def crossover(pai1, pai2):
    rotas_pai1 = list(pai1.keys())
    rotas_pai2 = list(pai2.keys())
    rota_comum = random.choice(list(set(rotas_pai1) & set(rotas_pai2)))
    horarios_pai1 = pai1[rota_comum]
    horarios_pai2 = pai2[rota_comum]
    filho = {}
    for rota in rotas_pai1 + rotas_pai2:
        if rota == rota_comum:
            horarios_filho = []
            for h1, h2 in zip(horarios_pai1, horarios_pai2):
                horarios_filho.append(random.choice([h1, h2]))
            # Verifica e ajusta possíveis horários duplicados
            horarios_filho = verificar_e_corrigir_horarios(horarios_filho)
            filho[rota] = horarios_filho
        else:
            if rota in pai1:
                filho[rota] = pai1[rota]
            else:
                filho[rota] = pai2[rota]

    return filho

def verificar_e_corrigir_horarios(horarios):
    horarios_corrigidos = []
    for horario in horarios:
        while horario in horarios_corrigidos:
            horario = gerar_novo_horario(horarios_corrigidos)
        horarios_corrigidos.append(horario)
    return horarios_corrigidos

def verificar_e_corrigir_horario_existente(voo, novo_horario):
    if novo_horario in voo:
        novo_horario = gerar_novo_horario(voo)
    return novo_horario

def gerar_novo_horario(voo):
    # Gera um novo horário aleatório para o voo
    novo_horario = random.choice(range(6, 25))
    while novo_horario in voo:
        novo_horario = random.choice(range(6, 25))
    return novo_horario

def mutacao_troca_voos(individuo):
    rotas = list(individuo.keys())
    rota1, rota2 = random.sample(rotas, 2)
    horarios1 = individuo[rota1]
    horarios2 = individuo[rota2]
    index1 = random.randint(0, len(horarios1) - 1)
    index2 = random.randint(0, len(horarios2) - 1)
    horarios1[index1], horarios2[index2] = horarios2[index2], horarios1[index1]

    # Verifica e ajusta possíveis horários duplicados
    horarios1 = verificar_e_corrigir_horarios(horarios1)
    horarios2 = verificar_e_corrigir_horarios(horarios2)

    individuo[rota1] = horarios1
    individuo[rota2] = horarios2
    return individuo

def verificar_e_ajustar_horario_voo(individuo, rota, novo_horario):
    horarios = individuo.get(rota, [])
    if novo_horario in horarios:
        novo_horario = gerar_novo_horario(horarios)
    return novo_horario

def gerar_novo_horario(horarios_existentes):
    novo_horario = random.choice(range(6, 25))  # Gerar um novo horário aleatório
    while novo_horario in horarios_existentes:
        novo_horario = random.choice(range(6, 25))
    return novo_horario
# Funcao para executar o algoritmo genetico e validar a solucao encontrada
def imprimir_detalhes_voos(solucao):
    print("Detalhes dos Voos:")
    for rota, horarios in solucao.items():
        origem, destino = rota
        for i, horario in enumerate(horarios):
            print(f"Voo {i+1}: {origem} -> {destino} -> Embarque: {horario - 1} - Horário de Partida: {horario}, Horário de Chegada: {horario + voos_diarios[rota][0]}")

# Função para executar o algoritmo genético e validar a solução encontrada
def executar_algoritmo_genetico():
    melhor_solucao = algoritmo_genetico(tamanho_populacao=50, geracoes=100, tamanho_torneio=5)
    print("Melhor alocacao de avioes:")
    for rota, horarios in melhor_solucao.items():
        print(f"{rota[0]} -> {rota[1]}: {horarios}")
    print("O número de aviões necessário é:", calcular_fitness(melhor_solucao))

    # Validar a solução encontrada
    solucao_valida, mensagem = validar_solucao(melhor_solucao)
    if solucao_valida:
        print("A solução encontrada é válida.")
        # Imprimir detalhes dos voos na solução
        imprimir_detalhes_voos(melhor_solucao)
    else:
        print("A solução encontrada é inválida:", mensagem)


# Executar o algoritmo genético
executar_algoritmo_genetico()

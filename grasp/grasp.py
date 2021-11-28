import copy
import random
from grasp import fitness
from grasp import constantes as const

### FUNCAO AUXILIAR DA "CALCULA_RCL" QUE DETERMINA O CUSTO DE SELEÇÃO DO
### PROXIMO PROFESSOR PARA A GRADE
### O CUSTO É BASEADO NA QUANTIDADE DE AULAS (HORARIOS) QUE UM PROFESSOR PRECISA
### MINISTRAR
### QUANTO MAIS AULAS -> MENOR O CUSTO PARA ESCOLHER ESSE PROFESSOR

def calcula_custos(candidatos):
    custos = []
    professores = []
    for i in range(0, len(candidatos)):
        if (candidatos[i][const.INDICE_PROFESSOR] != const.HORARIO_VAGO):
            professores.append(candidatos[i][const.INDICE_PROFESSOR])
    for i in range(0, len(candidatos)):
        # CUSTO = TOTAL DE HORARIOS NA GRADE - QUANTAS AULAS (HORARIOS) NA SEMANA UM PROFESSOR AINDA TEM
        custo = const.TOTAL_HORARIOS_GRADE - professores.count(candidatos[i][const.INDICE_PROFESSOR]) 
        custos.append(custo)
    return custos


### FUNCAO AUXILIAR DA "GRASP_CONSTRUCAO" QUE CONSTROI A LISTA RESTRITA DE
### CANDIDATOS - RCL (restricted candidate list) 
### A FUNCAO AVALIA OS CUSTOS DE CADA AULA CANDIDATA COM BASE NOS CUSTOS
### MÍNIMO E MÁXIMO ATUAIS E NO FATOR DE ALEATORIEDADE (ALFA_RCL)
### ALFA_RCL PRÓXIMO A ZERO -> BUSCA MAIS GULOSA
### ALFA_RCL PRÓXIMO A UM   -> BUSCA MAIS ALEATORIA 

def calcula_rcl(candidatos, custos, custo_min, custo_max, alfa_rcl = const.PADRAO_ALFA_RCL):
    rcl = []
    for i in range(0, len(candidatos)):
        if (custos[i] <= custo_min + alfa_rcl*(custo_max - custo_min)):
            rcl.append(candidatos[i])
    return rcl

### FUNCAO DE CONSTRUCAO DE UMA SOLUCAO [GRADE DE HORARIOS,FITNESS DA SOLUCAO] 
### UTILIZANDO A META-HEURÍSTICA GRASP 
### (GREEDY RANDOMIZED ADAPTIVE SEARCH PROCEDURE)
### COM BASE NO CONJUNTO DE AULAS NECESSARIAS (DISCIPLINA, PROFESSOR)
### E NO FATOR DE ALEATORIEDADE DA RCL (ALFA_RCL)
### ALFA_RCL PRÓXIMO A ZERO -> BUSCA MAIS GULOSA
### ALFA_RCL PRÓXIMO A UM   -> BUSCA MAIS ALEATORIA 

def grasp_construcao(aulas, alfa_rcl = const.PADRAO_ALFA_RCL):
    solucao = copy.deepcopy(const.PADRAO_SOLUCAO_INICIAL_VAZIA)
    candidatos = copy.deepcopy(aulas)
    custos = calcula_custos(candidatos)
    while (len(candidatos) > 0):
        custo_min = min(custos)
        custo_max = max(custos)
        rcl = calcula_rcl(candidatos, custos, custo_min, custo_max, alfa_rcl)
        # seleciona um elemento aleatório no vetor de candidatos (RCL)
        elemento = rcl[random.randrange(len(rcl))]
        solucao[const.INDICE_GRADE].append(elemento)
        candidatos.remove(elemento)
        calcula_custos(candidatos)
    solucao[const.INDICE_FITNESS] = fitness.funcao_objetivo(solucao[const.INDICE_GRADE])
    return solucao


### FUNCAO QUE, A PARTIR DE UMA SOLUCAO INICIAL, CALCULA UMA SOLUCAO VIZINHA
### O CALCULO É FEITO TROCANDO UMA ÚNICA POSICAO DA GRADE POR OUTRA DE FORMA 
### ALEATORIA (EX.: TROCA DO PRIMEIRO HORÁRIO DA SEGUNDA PELO ÚLTIMO DA SEXTA)

def calcula_vizinho(solucao_inicial):
    # Randomizacao apenas trocando as aulas no mesmo dia
    #horarios = random.sample(list(range(0,10)), 2)
    #sala = random.randrange(5)
    #trocas = [horarios[0]+10*sala, horarios[1]+10*sala]

    # Randomizacao trocando todas as posicoes na grade (seleciona duas posicoes aleatorias dentro da grade)
    trocas = random.sample(list(range(0,len(solucao_inicial[const.INDICE_GRADE]))), 2)
    solucao = copy.deepcopy(solucao_inicial)
    auxiliar = solucao[const.INDICE_GRADE][trocas[0]]
    solucao[const.INDICE_GRADE][trocas[0]] = solucao[const.INDICE_GRADE][trocas[1]]
    solucao[const.INDICE_GRADE][trocas[1]] = auxiliar
    solucao[const.INDICE_FITNESS] = fitness.funcao_objetivo(solucao[const.INDICE_GRADE])
    return solucao


### FUNCAO QUE A REALIZA UMA BUSCA LOCAL PELA MELHOR SOLUCAO 
### [GRADE DE HORARIOS,FITNESS DA SOLUCAO] A PARTIR DE UMA 
### SOLUCAO INICIAL. ESTA BUSCA LOCAL UTILIZA O ALGORITMO HILL CLIMBING.
### A QUANTIDADE PADRAO MÁXIMA DE SOLUCOES VIZINHAS CALCULADAS 
### PARA CADA NOVA MELHOR SOLUCAO ENCONTRADA É 1000 (MAX_ITERACOES)
### E O LIMITE PADRAO (THRESHOLD) PARA ENCERRAR A BUSCA LOCAL É ZERO

def busca_local(solucao_inicial, 
                max_iteracoes = const.PADRAO_MAX_ITERACOES_BUSCA_LOCAL, 
                limite = const.PADRAO_LIMITE_BUSCA_LOCAL):
    contador = 0
    melhor_solucao = solucao_inicial
    while (contador < max_iteracoes and melhor_solucao[const.INDICE_FITNESS]>limite):
        solucao = calcula_vizinho(melhor_solucao)
        if (solucao[const.INDICE_FITNESS] < melhor_solucao[const.INDICE_FITNESS]):
            contador = 0
            melhor_solucao = solucao
        else: 
            contador += 1 
    return melhor_solucao


### FUNCAO DE BUSCA DA MELHOR SOLUCAO GLOBAL [GRADE DE HORARIOS,FITNESS DA SOLUCAO] 
### UTILIZANDO A META-HEURÍSTICA GRASP 
### (GREEDY RANDOMIZED ADAPTIVE SEARCH PROCEDURE)
### COM BASE NO CONJUNTO DE AULAS NECESSARIAS (DISCIPLINA, PROFESSOR)
### NUMA SOLUCAO INICIAL (QUE PODE SER VAZIA)
### NUM NUMERO MÁXIMO DE ITERACOES DE BUSCA (MAX_ITERACOES - PADRAO = 5000)
### NO FATOR DE ALEATORIEDADE DA RCL (ALFA_RCL - PADRAO = 0.5) 
### ALFA_RCL PRÓXIMO A ZERO -> BUSCA MAIS GULOSA
### ALFA_RCL PRÓXIMO A UM   -> BUSCA MAIS ALEATORIA 
### E NO LIMITE (THRESHOLD) PARA ENCERRAR A BUSCA GLOBAL (LIMITE - PADRAO = 0)

def grasp_grade(aulas, 
                solucao_inicial = const.PADRAO_SOLUCAO_INICIAL_VAZIA, 
                max_iteracoes = const.PADRAO_MAX_ITERACOES_GRASP, 
                alfa_rcl = const.PADRAO_ALFA_RCL, 
                limite = const.PADRAO_LIMITE_GRASP,
                max_iteracoes_busca_local = const.PADRAO_MAX_ITERACOES_BUSCA_LOCAL,
                limite_busca_local = const.PADRAO_LIMITE_BUSCA_LOCAL):
    contador = 0
    melhor_solucao = solucao_inicial
    while (contador < max_iteracoes and melhor_solucao[const.INDICE_FITNESS]>limite):
        solucao = grasp_construcao(aulas, alfa_rcl)
        solucao = busca_local(solucao, max_iteracoes = max_iteracoes_busca_local, limite = limite_busca_local)
        if (solucao[const.INDICE_FITNESS] < melhor_solucao[const.INDICE_FITNESS]):
            melhor_solucao = solucao 
        contador += 1
        #print('\rIteracao =', contador, '-> Custo Solucao =', melhor_solucao[const.INDICE_FITNESS], end='')
        print('Iteracao =', contador, '-> Custo Solucao =', melhor_solucao[const.INDICE_FITNESS])
    return melhor_solucao

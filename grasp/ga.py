import random
import numpy as np
import pandas as pd
from pyeasyga import pyeasyga #pip install pyeasyga
# from pyeasyga.pyeasyga import pyeasyga #!git clone https://github.com/remiomosowon/pyeasyga.git

### CONSTANTES GLOBAIS ###

# SEPARADOR CSV
SEPARADOR_CSV = ';'

# INDICES DA SOLUCAO [ORDEM_GRADE, VALOR_FITNESS]
INDICE_GRADE = 0
INDICE_FITNESS = 1

# CONFIGURACAO DA GRADE ESCOLAR
TOTAL_DIAS = 5
TOTAL_SALAS = 5
TOTAL_HORARIOS_DIA = 2
TOTAL_AULAS_DIA = TOTAL_SALAS * TOTAL_HORARIOS_DIA
TOTAL_HORARIOS_GRADE = TOTAL_DIAS * TOTAL_SALAS * TOTAL_HORARIOS_DIA
DIAS_DA_SEMANA = ['Segunda','Terça','Quarta','Quinta','Sexta']

# REPRESENTACAO HORARIO VAGO NA GRADE
HORARIO_VAGO = 'VAGO'

# INDICES (POSICOES) DOS ELEMENTOS NOS VETORES 
# PROF_DISC_HORA [PROFESSOR, DISCIPLINA, HORARIOS, DISPONIBILIDADE] E 
# AULAS [PROFESSOR, DISCIPLINA]
INDICE_PROFESSOR = 0
INDICE_DISCIPLINA = 1
INDICE_HORARIOS = 2
INDICE_DISPONIBILIDADE = 3

# VALOR BINARIO QUE REPRESENTA SE O PROFESSOR DISPONIVEL/INDISPONIVEL
PROFESSOR_INDISPONIVEL = 0

# VALORES PADRAO PARA O GA
PADRAO_TAMANHO_POPULACAO=200
PADRAO_GERACOES=100
PADRAO_PROBABILIDADE_CROSSOVER=0.8
PADRAO_PROBABILIDADE_MUTACAO=0.5
PADRAO_ELITISMO=True
PADRAO_VERBOSE=True
PADRAO_MAXIMIZAR_FITNESS=False

### FIM CONSTANTES GLOBAIS

### VARIAVEIS GLOBAIS

aulas = [[[HORARIO_VAGO,HORARIO_VAGO] for _ in range(TOTAL_HORARIOS_GRADE)] ]
disponibilidade_professores = {}

### FIM VARIAVEIS GLOBAIS

# Carrega a configuracao da Grade a partir de um arquivo CSV
# Definição de:
# 1) Professores
# 2) Disciplinas
# 3) Aulas [Professor, Disciplina] 
# 4) Quantidade de horarios que uma aula deve ter por semana
# 5) Indisponibilidade de horarios dos professores  
# Retorna o conjunto de Aulas Totais = [Professor, Disciplina] 
# e a Disponibilidade dos Professores

def carrega_configuracao(url_config):
    prof_disc_hora = pd.read_csv(url_config, sep = SEPARADOR_CSV)
    prof_disc_hora = prof_disc_hora.values
    # preenche um vetor com 50 posicoes do tipo HORARIO_VAGO
    grade_completa = [[HORARIO_VAGO,HORARIO_VAGO] for _ in range(TOTAL_HORARIOS_GRADE)] 
    # Disponibilidades dos professores
    disponibilidades = {}
    # Se a quantidade de aulas < 50 a lista de aulas termina com valores VAGO
    contador = 0;
    for i in range(0, prof_disc_hora.shape[0]):
        aula = prof_disc_hora[i] 
        qtde_horarios_aula = aula[INDICE_HORARIOS]
        disponibilidade = aula[INDICE_DISPONIBILIDADE]
        professor = aula[INDICE_PROFESSOR]
        disciplina = aula[INDICE_DISCIPLINA]
        if professor not in disponibilidades:
            disp_binaria = list(map(int, list(bin(disponibilidade)[2:].zfill(10))))
            disp_binaria.reverse()
            disponibilidades[professor] = disp_binaria
        for j in range(0, qtde_horarios_aula):
          grade_completa[contador] = [professor, disciplina]
          contador += 1;
  
    return grade_completa, disponibilidades

# Define a funcao que cria uma representacao de uma solucao candidata
def cria_individuo(dados_iniciais):
    individuo = dados_iniciais[:]
    random.shuffle(individuo)
    return individuo

# Define a operacao de Crossover do GA
def crossover(pai_1, pai_2):
    crossover_indice = random.randrange(1, len(pai_1))
    filho_1a = pai_1[:crossover_indice]
    filho_1b = [i for i in pai_2 if i not in filho_1a]
    filho_1 = filho_1a + filho_1b

    filho_2a = pai_2[crossover_indice:]
    filho_2b = [i for i in pai_1 if i not in filho_2a]
    filho_2 = filho_2a + filho_2b

    return filho_1, filho_2

# Define a operacao de Mutacao do GA
def mutacao(individuo):
    mutacao_indice1 = random.randrange(len(individuo))
    mutacao_indice2 = random.randrange(len(individuo))
    individuo[mutacao_indice1], individuo[mutacao_indice2] = individuo[mutacao_indice2], individuo[mutacao_indice1]

# Define como aleatoria a operacao de Selecao do GA - PADRAO = TOURNAMENT
#def selecao(populacao):
#    return random.choice(populacao)

# Define a função de fitness
def fitness (individuo, dados_iniciais):
    posicoes_grade = individuo

    # PESO DAS VIOLACOES NA FUNCAO OBJETIVO (FITNESS)
    PESO_PROF_INDISPONIVEL = 1
    PESO_PROF_MESMO_HORARIO = 1
    PESO_DISC_MESMO_DIA_SALA_DIFER = 0.1
    PESO_DISC_MESMO_DIA_SALA_IGUAL = 0.05
    PESO_PRIMEIRO_HORARIO_VAGO = 0.1
    PESO_SEGUNDO_HORARIO_VAGO = 0.05
    
    violacoes = 0;
    
    # preencher todas as 50 posicoes com o mesmo valor HORARIO_VAGO
    grade = [[HORARIO_VAGO,HORARIO_VAGO] for _ in range(TOTAL_HORARIOS_GRADE)]  

    #Transforma as lista de posicoes em um grade com as aulas
    for i in range(len(posicoes_grade)):
        grade[i] = aulas[posicoes_grade[i]]
        # Verifica se o professor esta disponivel nesse horario
        professor_atual = grade[i][INDICE_PROFESSOR]
        if professor_atual != HORARIO_VAGO and disponibilidade_professores[professor_atual][i%TOTAL_SALAS] ==  PROFESSOR_INDISPONIVEL:
            violacoes += PESO_PROF_INDISPONIVEL
    
    
    # A mesma sala não poderá ter mais de uma aula ao mesmo tempo;
    # Essa restrição é atendida sempre devido a forma como a grade é montada

    # 1) A mesma aula não poderá acontecer simultaneamente em salas diferentes;
    # 2) Um professor não poderá dar 2 ou mais aulas ao mesmo tempo;
    # A premissa 2) já engloba a premissa 1) pois cada disciplina
    # tem sempre o mesmo professor
    
    for dia in range(TOTAL_DIAS):
        for horario in range(TOTAL_HORARIOS_DIA):
            for sala_atual in range(TOTAL_SALAS):
                evento_atual = dia*TOTAL_DIAS*TOTAL_HORARIOS_DIA+horario*TOTAL_SALAS+sala_atual 
                professor_atual = grade[evento_atual][INDICE_PROFESSOR]
                if (professor_atual != HORARIO_VAGO):
                    for proxima_sala in range(sala_atual+1,TOTAL_SALAS):
                        proximo_evento = dia*TOTAL_DIAS*TOTAL_HORARIOS_DIA+horario*TOTAL_SALAS+proxima_sala
                        proximo_professor = grade[proximo_evento][INDICE_PROFESSOR]
                        if (professor_atual == proximo_professor):
                            #return PESO_PROF_MESMO_HORARIO #Hard Constraint Professor no mesmo horario violada
                            violacoes += PESO_PROF_MESMO_HORARIO
                            # evita a recontagem quando o mesmo professor 
                            # aparece mais de 2 vezes no mesmo dia e horario
                            #break


    # Caso a carga horária de uma aula seja maior que um 1 horário por semana,
    # é desejável que as aulas não sejam na sequência imediata (mesmo dia);
    # Como é uma premissa desejável e não obrigatória o peso da violacao é 0.1

    for dia in range(TOTAL_DIAS):
        for sala_h1 in range(TOTAL_SALAS):
            evento_h1 = dia*TOTAL_DIAS*TOTAL_HORARIOS_DIA+sala_h1
            disciplina_h1 = grade[evento_h1][INDICE_DISCIPLINA]
            if (disciplina_h1 != HORARIO_VAGO):
                for sala_h2 in range(TOTAL_SALAS):
                    evento_h2 = dia*TOTAL_DIAS*TOTAL_HORARIOS_DIA+sala_h2+TOTAL_SALAS
                    disciplina_h2 = grade[evento_h2][INDICE_DISCIPLINA]
                    if (disciplina_h1 == disciplina_h2): # a mesma disciplina acontece no mesmo dia
                        if (sala_h1 == sala_h2): # se for na mesma sala a penalizacao reduz pela metade
                            violacoes+=PESO_DISC_MESMO_DIA_SALA_IGUAL
                        else:
                            violacoes+=PESO_DISC_MESMO_DIA_SALA_DIFER
                        # Quando as disciplinas sao iguais no horario 1 e 2
                        # Nao é necessario verificar outras salas no horario 2
                        # pois só vai haver a novamente a penalização se houver
                        # a mesma disciplina no mesmo horário em salas diferentes
                        # Mas isso a regra anterior já penalizou assim para 
                        # não penalizar novamente o laço é interrompido
                        break 
    

    # É desejável que não existam buracos (horários/salas sem aula)
    # na grade de horário
    # Considera-se o número total de posicoes da grade (salas*dias*horarios) = 50 
    # Como é uma premissa desejável e não obrigatória o peso da violacao é:
    # 0.1 Se o horário vago for o primeiro do dia
    # 0.05 Se o horario vago for o segundo do dia
    
    posicao_final = TOTAL_HORARIOS_GRADE - 1;
    while (posicao_final > -1 and grade[posicao_final][INDICE_PROFESSOR] == HORARIO_VAGO):
        posicao_final -= 1
    for i in range(0, posicao_final+1):
        if (grade[i][INDICE_PROFESSOR] == HORARIO_VAGO):
            if ((i // TOTAL_SALAS) % 2 == 0): # o horario sem aula é o primeiro do dia
               violacoes+=PESO_PRIMEIRO_HORARIO_VAGO
            else:
               violacoes+=PESO_SEGUNDO_HORARIO_VAGO # o horario sem aula é o segundo do dia (penalização menor)


    # OBS: Uma questao importante é saber se o peso da violacao 
    # de deixar um horario vago deve ser o mesmo que 
    # colocar a mesma disciplina em sequencia no dia

    # O fitness (funcao objetivo) será :
    # Melhor - quanto mais se aproximar de 0 (menos violacoes)
    # Pior - quanto mais se aproximar de 1 (mais violacoes)
    fitness = 1 - 1 / (violacoes + 1)
    return fitness

# Gera Grade a partir das Aulas e da Solucao (Posicoes) encontrada
def gera_grade(aulas, solucao):
    grade = [[] for _ in range(TOTAL_HORARIOS_GRADE)]
    for i in range(len(solucao)):
        grade[i] = aulas[solucao[i]]
    return grade

# Imprime a Solucao Encontrada [grade, valor fitness]
def imprime_solucao(solucao):
    grade = solucao[INDICE_GRADE]
    for i in range(0,len(grade)):
        dia = DIAS_DA_SEMANA[i // TOTAL_AULAS_DIA]
        if (i % TOTAL_AULAS_DIA == 0):
            print('\n\n',dia)
        if (i % TOTAL_SALAS == 0):
            print('\nHorario ', 1 + i % 2, '--------------------')
        # imprime um conjunto [PROFESSOR,DISCIPLINA]    
        print(grade[i], end = ' | ')
    print('\nFitness da Solucao = ',solucao[INDICE_FITNESS])    
    return


# Funcao Principal de Controle

def geleia_ga(url_config, 
              tamanho_populacao=PADRAO_TAMANHO_POPULACAO,
              geracoes=PADRAO_GERACOES,
              probabilidade_crossover=PADRAO_PROBABILIDADE_CROSSOVER,
              probabilidade_mutacao=PADRAO_PROBABILIDADE_MUTACAO,
              elitismo=PADRAO_ELITISMO,
            #   verbose=PADRAO_VERBOSE, #SOMENTE NA VERSAO DO GIT DA LIBRARY
              maximizar_fitness=PADRAO_MAXIMIZAR_FITNESS):

    # Carrega as variaveis globais a partir do arquivo de configuracao
    global aulas, disponibilidade_professores
    aulas, disponibilidade_professores = carrega_configuracao(url_config) 
    
    # Define os dados iniciais (lista com todas as posicoes da grade (0-49))
    dados_iniciais = list(range(0,TOTAL_HORARIOS_GRADE))

    # Inicializacao do GA
    ga = pyeasyga.GeneticAlgorithm(dados_iniciais,
                                    population_size=tamanho_populacao,
                                    generations=geracoes,
                                    crossover_probability=probabilidade_crossover,
                                    mutation_probability=probabilidade_mutacao,
                                    elitism=elitismo,
                                    # verbose=verbose, #SOMENTE NA VERSAO DO GIT
                                    maximise_fitness=maximizar_fitness)
    
    # Define a funcao que cria uma representacao de uma solucao candidata
    ga.create_individual = cria_individuo

    # Define a operacao de Crossover do GA
    ga.crossover_function = crossover

    # Define a operacao de Mutacao do GA
    ga.mutate_function = mutacao

    # Define a operacao de Selecao do GA - PADRAO = TOURNAMENT
    #ga.selection_function = selecao

    # Define a função de fitness
    ga.fitness_function = fitness      
    
    # Executa o GA
    ga.run()                            

    grade = gera_grade(aulas, ga.best_individual()[1])
    solucao = [grade, ga.best_individual()[0]]
    
    return solucao
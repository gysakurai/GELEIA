import copy
import random
import numpy  as np
import pandas as pd
from grasp import fitness
from grasp import grasp
from grasp import constantes as const

### GERA UMA SOLUCAO ALEATORIA [GRADE DE HORARIOS,FITNESS DA SOLUCAO] 
### COM BASE NO CONJUNTO DE AULAS NECESSARIAS 
### (DISCIPLINA, PROFESSOR)

def solucao_aleatoria(aulas):
    solucao = copy.deepcopy(const.PADRAO_SOLUCAO_INICIAL_VAZIA)
    solucao[const.INDICE_GRADE] = random.sample(aulas, len(aulas))
    solucao[const.INDICE_FITNESS] = fitness.funcao_objetivo(solucao[const.INDICE_GRADE])
    return solucao

### FUNCAO QUE TRANSFORMA A ESTRUTURA DO TIPO
### [DISCIPLINA, PROFESSOR, QUANTIDADE DE HORARIOS EXIGIDO PELA DISCIPLINA] 
### EM UMA ESTRUTURA (GRADE) DE AULAS NECESSARIAS DO TIPO [DISCIPLINA, PROFESSOR]
### ONDE É REPLICADO O VALOR [DISCIPLINA, PROFESSOR] DE ACORDO COM A QUANTIDADE
### DE HORARIOS DE CADA DISCIPLINA EXIGE, COMO A GRADE COMPORTA ATÉ 50 HORÁRIOS 
### (NUMERO DE DIAS X NUMERO DE HORARIOS NO DIA X NUMERO DE SALAS), 
### CASO QUANTIDADE DE AULAS NECESSARIAS SEJA MENOR QUE O TAMANHO DA GRADE (50)
### O RESTANTE DA GRADE É PREENCHIDO COM VALORES ['VAGO','VAGO']

def gera_aulas(prof_disc_hora):
    # dt = np.dtype([('disciplina', np.unicode_, 4), ('professor', np.unicode_, 4)])
    aulas = [] 
    for i in range(0, prof_disc_hora.shape[0]):
        aula = prof_disc_hora[i] 
        qtde_horarios_aula = aula[const.INDICE_HORARIOS]
        for j in range(0, qtde_horarios_aula):
          aulas.append((aula[const.INDICE_PROFESSOR],aula[const.INDICE_DISCIPLINA]))
    # Se a quantidade de aulas < 50 preenche a lista aulas com valores VAGO
    for i in range(len(aulas),const.TOTAL_HORARIOS_GRADE):
        aulas.append((const.HORARIO_VAGO, const.HORARIO_VAGO))
    return aulas #np.array(aulas,dt)

### FUNCAO QUE IMPRIME UMA SOLUCAO [GRADE DE HORARIOS, FITNESS DA SOLUCAO]
### DE FORMA AMIGÀVEL

def imprime_solucao(solucao):
    for i in range(0,len(solucao[const.INDICE_GRADE])):
        dia = const.DIAS_DA_SEMANA[i // const.TOTAL_AULAS_DIA]
        if (i % const.TOTAL_AULAS_DIA == 0):
            print('\n\n',dia)
        if (i % const.TOTAL_SALAS == 0):
            print('\nHorario ', 1 + i % 2, '--------------------')
        # imprime um conjunto [PROFESSOR,DISCIPLINA]    
        print(solucao[const.INDICE_GRADE][i], end = ' | ')
    print('\nFitness da Solucao = ',solucao[const.INDICE_FITNESS])    
    return

### METODO PRINCIPAL QUE RECEBE A URL DO CASO DE TESTE E RETORNA 
### A MELHOR SOLUCAO [GRADE DE HORARIOS, FITNESS DA SOLUCAO] ENCONTRADA
### 
def principal(url_caso_de_teste, 
              calcula_solucao_inicial = const.PADRAO_FLAG_CALCULA_SOLUCAO_INICIAL,
              max_iteracoes = const.PADRAO_MAX_ITERACOES_GRASP, 
              alfa_rcl = const.PADRAO_ALFA_RCL, 
              limite = const.PADRAO_LIMITE_GRASP,
              max_iteracoes_busca_local = const.PADRAO_MAX_ITERACOES_BUSCA_LOCAL,
              limite_busca_local = const.PADRAO_LIMITE_BUSCA_LOCAL):
    prof_disc_hora = pd.read_csv(url_caso_de_teste, sep = const.SEPARADOR_CSV)
    prof_disc_hora = prof_disc_hora.values
    aulas = gera_aulas(prof_disc_hora)
    solucao_inicial = const.PADRAO_SOLUCAO_INICIAL_VAZIA
    if (calcula_solucao_inicial):
        solucao_inicial = solucao_aleatoria(aulas)
    melhor_solucao = grasp.grasp_grade(aulas, 
                                       solucao_inicial = solucao_inicial, 
                                       max_iteracoes = max_iteracoes,                        
                                       alfa_rcl = alfa_rcl, 
                                       limite = limite,
                                       max_iteracoes_busca_local = max_iteracoes_busca_local,
                                       limite_busca_local = limite_busca_local)
    imprime_solucao(melhor_solucao)
    return(melhor_solucao)

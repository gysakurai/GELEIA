import copy
from grasp import constantes as const



### FUNCAO OBJETIVO (FITNESS)
### AS FORMAS DO CALCULO ESTAO DEFINIDAS NOS COMENTARIOS DENTRO DA FUNCAO
### É UMA FUNCAO DE MINIMIZACAO QUE RETORNA VALOR ENTRE 0 E 1 
def funcao_objetivo(grade):
    
### CONSTANTES UTILIZADAS PELA FUNCAO
### A CRIACAO DA REFERENCIA LOCAL SE MOSTROU MAIS PERFORMÁTICA (EM TORNO DE 20%) 

# CONFIGURACAO DA GRADE ESCOLAR
    TOTAL_DIAS = const.TOTAL_DIAS
    TOTAL_SALAS = const.TOTAL_SALAS
    TOTAL_HORARIOS_DIA = const.TOTAL_HORARIOS_DIA
    TOTAL_HORARIOS_GRADE = const.TOTAL_HORARIOS_GRADE

# INDICES (POSICOES) DOS ELEMENTOS NO VETOR AULAS [PROFESSOR, DISCIPLINA]
    INDICE_PROFESSOR = const.INDICE_PROFESSOR
    INDICE_DISCIPLINA = const.INDICE_DISCIPLINA

# REPRESENTACAO HORARIO VAGO NA GRADE
    HORARIO_VAGO = const.HORARIO_VAGO

# PESO DAS VIOLACOES NA FUNCAO OBJETIVO (FITNESS)
    PESO_PROF_MESMO_HORARIO = const.PESO_PROF_MESMO_HORARIO
    PESO_DISC_MESMO_DIA_SALA_DIFER = const.PESO_DISC_MESMO_DIA_SALA_DIFER
    PESO_DISC_MESMO_DIA_SALA_IGUAL = const.PESO_DISC_MESMO_DIA_SALA_IGUAL
    PESO_PRIMEIRO_HORARIO_VAGO = const.PESO_PRIMEIRO_HORARIO_VAGO
    PESO_SEGUNDO_HORARIO_VAGO = const.PESO_SEGUNDO_HORARIO_VAGO    
    
    violacoes = 0;
    
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
                            violacoes += PESO_PROF_MESMO_HORARIO
                            # evita a recontagem quando o mesmo professor 
                            # aparece mais de 2 vezes no mesmo dia e horario
                            break


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
                        # a regra anterior já penaliza a mesma disciplina no mesmo horário
                        # assim para não penalizar novamente o laço é interrompido
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
    fitness = 1 - 1 / (1 * violacoes + 1);
    return fitness

# GELEIA - Grade Escolar Livre Elaborada com Inteligência Artificial

Projeto para a construção de uma aplicação web, baseada em streamlit (https://streamlit.io/), de geração automática de grade escolar (timetable) utilizando um algoritmo de meta-heurística.

Versão V1: **06/12/2021**

    - O algoritmo de meta-heurística utilizado foi um Algoritmo Genético (AG ou GA - Genetic algorithm).

Realizado por alunos do programa de Mestrado do Curso de Ciência da Computação da Universidade Estadual de Londrina.

Disciplina: Inteligência Computacional

Alunos:

    - Marcus Vinicius Alencar Terra - marcus.vinicius.terra@uel.br
    - Vitor de Castro Silva - vitor.castro.silva@uel.br
    - Guilherme Yukio Sakurai - guilhermeyukio@uel.br
    - Julia Gil - jugilsantos@gmail.com

## Premissas da Grade de Horários

A Grade de horários escolares, elaborada através da aplicação proposta, baseia-se nas seguintes premissas:

    - A grade deverá representar o horário completo contendo todas as aulas definidas pelo usuário;
    - A grade será construída considerando uma semana de 5 dias (segunda a sexta) com 2 horários para aula
    por dia (08:00-10:00 e 10:30 - 12:30), assim a grade terá um total de 10 horários por semana;
    - O número de salas de aula disponíveis simultaneamente é 5, sendo que todas as salas são iguais e podem 
    ser usadas por todas as disciplinas;
    - O número máximo de disciplinas do curso será, portanto, igual a 50 
    (total de horários disponíveis na semana (10) X número de salas (5));
    - Uma aula é composta pelo conjunto: disciplina-professor-carga horária semanal;
    - Cada disciplina terá um professor único que será pré-definido pelo usuário;
    - Cada professor terá uma lista, pré-definida pelo usuário, dos horários que não estará disponível para aulas
    - A carga horária semanal de cada disciplina será pré-definida pelo usuário, sendo que cada aula deverá 
    ocorrer pelo menos 1 vez (1 horário) por semana;
    - O preenchimento da grade de horário deve começar no primeiro horário da segunda-feira e terminar no 
    último horário da sexta-feira.
    
## Restrições da Grade de Horários
    
    Restrições Rígidas (Hard Constraints)
    - A mesma aula não poderá acontecer simultaneamente em salas diferentes;
    - Um professor não poderá dar 2 ou mais aulas ao mesmo tempo;
    - A mesma sala não poderá ter mais de uma aula ao mesmo tempo;
    - Um professor não poderá dar aulas nos horários em que esteja indisponível;
    
    Restrições Leves (Soft Constraints)
    - Caso a carga horária de uma aula seja maior que um 1 horário por semana, é desejável que as aulas não 
    sejam na sequência imediata;
    - É desejável que não existam "buracos" (horários vagos sem aula) na grade de horário;
    
## Detalhamento Técnico
    

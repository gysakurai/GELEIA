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
    
    Restrições Rígidas (Hard Constraints) - Penalização Maior
    - A mesma aula não poderá acontecer simultaneamente em salas diferentes;
    - Um professor não poderá dar 2 ou mais aulas ao mesmo tempo;
    - A mesma sala não poderá ter mais de uma aula ao mesmo tempo;
    - Um professor não poderá dar aulas nos horários em que esteja indisponível;
    
    Restrições Leves (Soft Constraints) - Penalização Menor
    - Caso a carga horária de uma aula seja maior que um 1 horário por semana, é desejável que as aulas não 
    sejam na sequência imediata;
    - É desejável que não existam "buracos" (horários vagos sem aula) na grade de horário;
    
## Detalhamento Técnico
    
A construção da solução proposta dividiu-se em 3 partes principais:

    - Planilha para a definição dos dados de entrada (Configuração da Grade)
    - Algoritmo de meta-heurística para elaboração da Grade com base na configuração
    - Construção de ambiente no Streamlit para a operação do sistema e apresentação dos resultados
    
### Planilha para a definição dos dados de entrada (Configuração da Grade)

A aplicação utiliza-se de uma planilha do Google Sheets (https://docs.google.com/spreadsheets/d/1aW7UF_39EvxF_X4GnAKx1JOwjAPlNarZo3GAD4olM6A/edit?usp=sharing) para que o usuário realize a definição dos seguinte dados de entrada:

    - Professores
    - Disciplinas
    - Carga horária semanal de cada disciplina
    - Lista dos horários em que os professores estarão indisponíveis
    
A planilha possui ainda um conjunto de scripts que auxiliam o usuário na geração do arquivo de configuração da grade (formato csv). Este arquivo é necessário para a execução do algoritmo de meta-heurística (AG).

Obs.: a planilha é uma ferramenta suavizadora utilizada na geração do arquivo de configuração, dessa forma, ela pode ser dispensada por usuários mais experientes capazes de criar o arquivo .csv diretamente.

Exemplo de arquivo de configuração de grade de horário:

    "Professor";"Disciplina";"Horarios Semanais";"Disponibilidade"
    "Professor 1";"Disciplina 1";2;1020
    "Professor 2";"Disciplina 2";2;1011
    "Professor 3";"Disciplina 3";4;991
    "Professor 4";"Disciplina 4";4;767

### Algoritmo de meta-heurística para elaboração da Grade com base na configuração

Conforme mencionado anteriormente, o algoritmo selecionado para a implementação da meta-heurística foi o Algoritmo Genético (AG ou GA).

Por se tratar de um algoritmo amplamente conhecido e utilizado na Inteligência Computacional, optou-se por adotar a solução implementada pela biblioteca python pyeasyga (https://github.com/remiomosowon/pyeasyga).

Para que o AG pudesse resolver o problema proposto, foi preciso realizar a implementação/sobrescrita dos métodos de Criação de Indivíduo (create_individual), Crossover (crossover), Mutação (mutate) e Fitness (fitness). Nestes métodos foram incorporadas as heurísticas relativas à construção da Grade Escolar. 
  
#### Criação de Indivíduo

Para o AG, um indivíduo é uma sequência de aulas, ou mais especificamente, de posições das aulas dentro da grade escolar.

Assim, o método de criação de indivíduo gera um vetor dos números de 0 a 49 distribuídos aleatoriamente. Estes números representam a posição que cada uma das aulas pré-definidas ocupa na grade.

#### Crossover

Neste método são passados 2 pais como parâmetros e são gerados 2 novos filhos utilizando-se a seguinte abordagem:

    - Seleciona-se uma posição aleatória no vetor que representa o indivíduo (0 a 49)
    - Utilizando-se a posição selecionada separa-se uma parte do pai1 que vai para o filho1
    - A outra parte do filho1 será composta por todas as posições de aula do pai2 que não existem ainda no filho1
    - Utilizando-se a posição selecionada separa-se uma parte do pai2 que vai para o filho2
    - A outra parte do filho2 será composta por todas as posições de aula do pai1 que não existem ainda no filho2
    
Exemplo do algoritmo de crossover (5 posições)

    pai1 = [0,1,2,3,4]
    pai2 = [3,0,4,2,1]
    posicao_aleatoria = 2
    filho1 = [0,1] + [3,4,2] = [0,1,3,4,2]
    filho2 = [3,0] + [1,2,4] = [3,0,1,2,4]
    
#### Mutação

O método da mutação recebe um indivíduo como parâmetro e realiza as seguintes operações:

    - Selecionam-se duas posições aleatórias (A e B) no vetor que representa o indivíduo (0 a 49)
    - Troca-se a posição A pela posição B e vice-versa
 
Exemplo do algoritmo de Mutação (5 posições)

    indivíduo = [4,2,0,3,1]
    posicao_A = 1
    posicao_B = 4
    novo_individuo = [4,1,0,3,2]
    
#### Fitness

A função ou método de fitness irá calcular o quão adequada é solução encontrada pelo AG. O cálculo baseia-se na violação das restrições definidas anteriormente (rígidas e leves).

A função de fitness irá retornar um valor entre 0 e 1, e por se tratar de um problema de minimização das violações, quanto mais próximo de 0 melhor será a solução.

A fórmula básica para o cálculo da função de fitness é a seguinte:

    fitness = 1 - 1 / (violacoes + 1)

A aplicação utiliza os seguintes valores para os pesos das violações (valores definidos empiricamente):

    PESO_PROF_INDISPONIVEL = 1
    PESO_PROF_MESMO_HORARIO = 1
    PESO_DISC_MESMO_DIA_SALA_DIFER = 0.1
    PESO_DISC_MESMO_DIA_SALA_IGUAL = 0.05
    PESO_PRIMEIRO_HORARIO_VAGO = 0.1
    PESO_SEGUNDO_HORARIO_VAGO = 0.05

Para maiores detalhes sobre o método de fitness, consulte o código de sua implementação (https://github.com/gysakurai/GELEIA/blob/main/grasp/ga.py).

#### Método Principal (geleia_ga)

A busca meta-heurística utilizando-se AG inicia-se com chamada ao métdo geleia_ga. 

A assinatura do método geleia_ga com seus parâmetros é apresentada a seguir:

    geleia_ga(url_config, 
              tamanho_populacao=PADRAO_TAMANHO_POPULACAO,
              geracoes=PADRAO_GERACOES,
              probabilidade_crossover=PADRAO_PROBABILIDADE_CROSSOVER,
              probabilidade_mutacao=PADRAO_PROBABILIDADE_MUTACAO,
              elitismo=PADRAO_ELITISMO,
              maximizar_fitness=PADRAO_MAXIMIZAR_FITNESS)
    
    onde
    
    url_config: Caminho para o arquivo de configuração .csv (pode ser um arquivo na internet)
    tamanho_populacao: é o tamanho inicial da população utilizada pelo AG para a resolução
    probabilidade_crossover: é a probabilidade de ocorrer crossover na geração de um novo indivíduo
    probabilidade_mutacao: é a probabilidade de ocorrer mutacao na geração de um novo indivíduo
    elitismo: é a definição se o algoritmo utiliza elitismo nas gerações ou não
    maximizar_fitness: indica se o AG deve ser utilizado para maximizar ou minimizar a função de fitness
        
A seguir, apresenta-se os valores padrão utilizados pelo AG (hiperparâmetros):

    PADRAO_TAMANHO_POPULACAO=200
    PADRAO_GERACOES=100
    PADRAO_PROBABILIDADE_CROSSOVER=0.8
    PADRAO_PROBABILIDADE_MUTACAO=0.5
    PADRAO_ELITISMO=True
    PADRAO_MAXIMIZAR_FITNESS=False

Importante: Para a chamada do método geleia_ga apenas o parâmetro url_config é obrigatório

#### Métodos adicionais

Além dos métodos citados acima, a aplicação possui ainda 3 métodos auxiliares:

    carrega_configuracao(url_config): Carrega o arquivo .csv definindo as configurações iniciais da grade
    gera_grade(aulas, solucao): A partir das aulas que existem e da solução que apresenta as posições 
    que elas ocupam na grade, é gerado um vetor do tipo [[professor, disciplina],...]
    imprime_solucao(solucao): Imprime em modo texto a solução passada como parâmetro
    

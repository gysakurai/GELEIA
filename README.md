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
    - Julia Gil Santos - jugilsantos@gmail.com

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
    
O projeto Geleia tem o Python como linguagem principal de desenvolvimento e sua construção dividiu-se em 3 partes principais:

    - Planilha para a definição dos dados de entrada (Configuração da Grade)
    - Algoritmo de meta-heurística para elaboração da Grade com base na configuração
    - Construção de ambiente no Streamlit para a operação do sistema e apresentação dos resultados
    
Os participantes deste projeto exerceram os seguintes papéis ou atividades na construção da solução:

| Nome do Participante/Aluno | Papel Exercido |
|---|---|
|Julia Gil Santos|Construção dos Casos de Testes; Teste e Análise da Função de Fitness; Documentação|
|Marcus Vinicius Alencar Terra|Coordenação do Projeto; Construção da Planilha de Dados; Teste da Aplicação; Documentação|
|Vitor de Castro Silva|Análise, Implementação e Testes do Algoritmo de Meta-heurística (GA); Documentação|
|Guilherme Yukio Sakurai|Integração de Código; Construção de GUI no Streamlit; Deploy da Aplicação; Documentação|

### Planilha para a definição dos dados de entrada (Configuração da Grade)

A aplicação utiliza-se de uma planilha do Google Sheets (https://docs.google.com/spreadsheets/d/1aW7UF_39EvxF_X4GnAKx1JOwjAPlNarZo3GAD4olM6A/edit?usp=sharing) para que o usuário realize a definição dos seguinte dados de entrada:

    - Professores
    - Disciplinas
    - Carga horária semanal de cada disciplina
    - Lista dos horários em que os professores estarão indisponíveis
    
A planilha possui ainda um conjunto de scripts que auxiliam o usuário na geração do arquivo de configuração da grade (formato csv). Este arquivo é necessário para a execução do algoritmo de meta-heurística (AG).

Obs.: a planilha é uma ferramenta suavizadora utilizada na geração do arquivo de configuração, dessa forma, ela pode ser dispensada por usuários mais experientes capazes de criar o arquivo .csv diretamente.



A disponibilidade de cada professor é dada pela configuração, através da planilha, dos horários disponíveis de cada um deles, conforme demonstrado na figura abaixo:
![Gui Geleia](https://github.com/gysakurai/GELEIA/blob/main/telas/Planilha_Aba_Disponibilidades.png)

Na aba "Dados" da planilha, o usuário irá relacionar os professores inseridos na aba anterior "Disponibilidade" com as disciplinas que eles devem ministrar, indicando a quantidade de horários semanais que cada disciplina deve ter. 

A figura a seguir apresenta um exemplo de preenchimento da aba Dados:
![Gui Geleia](https://github.com/gysakurai/GELEIA/blob/main/telas/Planilha_Aba_Dados.png)

#### Cálculo da disponibilidade dos professores

Nota-se que na aba "Dados", a coluna "Disponibilidade" é uma representação decimal da disponibilidade de cada **professor**, esta é uma coluna somente para leitura e faz referência direta à coluna "Codificação" da Aba "Disponibilidades".

A coluna "Codificação", por sua vez, é calculada automaticamente pela planilha utilizando-se uma codificação de binário para decimal, conforme detalhamento a seguir:

1) Considerando que cada horário pode ter apenas 2 valores com relação à disponibilidade do professor:

    "Disponível" ou "Indisponível"

optou-se por representar essa disponibilidade como um valor binário: 

    0 = Indisponível
    1 = Disponível
    
2) Nas premissas propostas neste projeto, ficou definido que existem apenas 2 horários diários durante 5 dias na semana, ou seja, existem 10 horários possíveis de aulas para cada professor. 

Dessa forma, é possível entender que: 
 
    Existem 10 valores binários (0 ou 1), para cada professor, representando a disponibilidade em cada um dos horários

Isto é, a lista de disponibilidade de um professor é definida por um conjunto de dígitos binários
    
    Ex.: [0, 1, 0, 0, 1, 1, 1, 1, 1, 1] 
    
3) Com base nesta lista é realizada a codificação dos dígitos binários em um número decimal, conforme exemplo completo a seguir:

Supondo as seguintes disponibilidades para o "Professor X":


#### Exportação dos dados da planilha para a aplicação Geleia

O Geleia processa como entrada um arquivo .csv com os dados dos professores, disciplinas, quantidade de horários e disponibilidades. 

Para gerar este arquivo com as configurações/restrições da grade escolar, o usuário deve clicar em "Clique para exportar CSV" na aba "Dados" da planilha, neste momento um programa (script) irá gerar o arquivo de configuração com a extensão '.csv' no formato esperado pela aplicação Geleia.

A seguir, é apresentado um exemplo de arquivo de configuração de grade de horário:
```
"Professor";"Disciplina";"Horarios Semanais";"Disponibilidade"
"Professor 1";"Disciplina 1";2;1020
"Professor 2";"Disciplina 2";2;1011
"Professor 3";"Disciplina 3";4;991
"Professor 4";"Disciplina 4";4;767
"Professor 1";"Disciplina 5";4;1020
```
### Algoritmo de meta-heurística para elaboração da Grade com base na configuração

Conforme mencionado anteriormente, o algoritmo selecionado para a implementação da meta-heurística foi o Algoritmo Genético (AG ou GA).

Por se tratar de um algoritmo amplamente conhecido e utilizado na Inteligência Computacional, optou-se por adotar a solução implementada pela biblioteca python pyeasyga (https://github.com/remiomosowon/pyeasyga).

Para que o AG pudesse resolver o problema proposto, foi preciso realizar a implementação/sobrescrita dos métodos de Criação de Indivíduo (create_individual), Crossover (crossover), Mutação (mutate) e Fitness (fitness). Nestes métodos foram incorporadas as heurísticas relativas à construção da Grade Escolar. 

Para maiores detalhes sobre a implementação do AG, consulte o seu código-fonte em: (https://github.com/gysakurai/GELEIA/blob/main/grasp/ga.py).

#### Criação de Indivíduo

Para o AG, um indivíduo é uma sequência de aulas, ou mais especificamente, de posições das aulas dentro da grade escolar.

Assim, o método de criação de indivíduo gera uma lista dos números de 0 a 49 distribuídos aleatoriamente. Estes números representam a posição que cada uma das aulas pré-definidas irá ocupar na grade.

#### Crossover

Neste método são passados 2 pais como parâmetros e são gerados 2 novos filhos utilizando-se a seguinte abordagem:

    - Seleciona-se uma posição de corte aleatória entre 0 a 49 
      (todas as posições possíveis na lista que representa o indivíduo) 
    - Utilizando-se a posição selecionada separa-se uma parte do pai1 que vai para o filho1
    - A outra parte do filho1 será composta por todas as posições de aula do pai2 que ainda não existem no filho1
    - Utilizando-se novamente a posição selecionada separa-se uma parte do pai2 que vai para o filho2
    - A outra parte do filho2 será composta por todas as posições de aula do pai1 que ainda não existem no filho2
    
Exemplo do algoritmo de crossover (5 posições)
```    
pai1 = [0,2,3,4,1]
pai2 = [4,0,1,2,3]
posicao_de_corte_aleatoria = 2
filho1 = [0,2] + [4,1,3] = [0,2,4,1,3]
filho2 = [4,0] + [2,3,1] = [4,0,2,3,1]
```        
#### Mutação

O método da mutação recebe um indivíduo como parâmetro e realiza as seguintes operações:

    - Selecionam-se duas posições aleatórias (A e B) na lista que representa o indivíduo (entre 0 e 49)
    - Troca-se o valor que está na posição A pelo valor da que está na posição B e vice-versa
 
Exemplo do algoritmo de Mutação (5 posições)
```
indivíduo = [4,2,0,3,1]
posicao_A = 1
posicao_B = 4
novo_individuo = [4,1,0,3,2]
```        
#### Fitness

A função ou método de fitness irá calcular o quão adequada é solução encontrada pelo AG. O cálculo baseia-se na violação das restrições definidas anteriormente (rígidas e leves).

A função de fitness irá retornar um valor entre 0 e 1, e por se tratar de um problema de minimização das violações, quanto mais próximo de 0 melhor será a solução.

A fórmula básica para o cálculo da função de fitness é a seguinte:
```    
fitness = 1 - 1 / (violacoes + 1)
```    
A aplicação utiliza os seguintes valores para os pesos das violações (valores definidos empiricamente):
```    
PESO_PROF_INDISPONIVEL = 1
PESO_PROF_MESMO_HORARIO = 1
PESO_DISC_MESMO_DIA_SALA_DIFER = 0.1
PESO_DISC_MESMO_DIA_SALA_IGUAL = 0.05
PESO_PRIMEIRO_HORARIO_VAGO = 0.1
PESO_SEGUNDO_HORARIO_VAGO = 0.05
```    

#### Método Principal (geleia_ga)

A busca meta-heurística utilizando-se AG inicia-se com chamada ao método geleia_ga. 

A assinatura do método geleia_ga com seus parâmetros é apresentada a seguir:
```
geleia_ga(url_config, 
          tamanho_populacao=PADRAO_TAMANHO_POPULACAO,
          geracoes=PADRAO_GERACOES,
          probabilidade_crossover=PADRAO_PROBABILIDADE_CROSSOVER,
          probabilidade_mutacao=PADRAO_PROBABILIDADE_MUTACAO,
          elitismo=PADRAO_ELITISMO,
          maximizar_fitness=PADRAO_MAXIMIZAR_FITNESS)
```    
onde:
```        
url_config: Caminho (URL) para o arquivo de configuração .csv (pode ser um arquivo na internet) - Tipo: String 
tamanho_populacao: é o tamanho inicial da população utilizada pelo AG para a resolução do problema - Tipo: int
probabilidade_crossover: é a probabilidade de ocorrer crossover na geração de um novo indivíduo - Tipo: float
probabilidade_mutacao: é a probabilidade de ocorrer mutação na geração de um novo indivíduo - Tipo: float
elitismo: é a definição se o algoritmo utiliza elitismo nas gerações
         (define se mantém a melhor solução da geração anterior ou não) - Tipo: boolean
maximizar_fitness: indica se o AG deve ser utilizado para maximizar ou minimizar a função de fitness
                   (em tese, este valor sempre será 'False') - Tipo: boolean
```            
A seguir, apresenta-se os valores padrão utilizados pelo AG (hiperparâmetros):
```    
PADRAO_TAMANHO_POPULACAO=200
PADRAO_GERACOES=100
PADRAO_PROBABILIDADE_CROSSOVER=0.8
PADRAO_PROBABILIDADE_MUTACAO=0.5
PADRAO_ELITISMO=True
PADRAO_MAXIMIZAR_FITNESS=False
```    
Importante: Para a chamada do método geleia_ga apenas o parâmetro url_config é obrigatório

Exemplos de chamadas do método principal geleia_ga:

a) Arquivo local com os demais parâmetros no valor padrão
```
solucao = geleia_ga('<arquivo_local>.csv')

ou 

solucao = geleia_ga(url_config='<arquivo_local>.csv')
```
b) Arquivo remoto com o tamanho da populacao = 100
```
solucao = geleia_ga('http://<endereco_na_internet>/<arquivo_remoto>.csv', tamanho_populacao=100)
```
c) Arquivo local com o todos os parâmetros preenchidos
```
solucao = geleia_ga(url_config='<arquivo_local>.csv', 
                    tamanho_populacao=50,
                    probabilidade_crossover=0.9,
                    probabilidade_mutacao=0.3,
                    elitismo=False,
                    maximizar_fitness=False)
```

O tipo de retorno do método geleia_ga é um vetor, ou lista, de 2 posições, onde a primeira posição representa o vetor da solução encontrada (Grade Escolar Completa), com tuplas do tipo [Professor, Disciplina], e a segunda posição é o valor da função de fitness para esta solução (número real entre 0 e 1). 
```
[solucao_encontrada, fitness_da_solucao] 
```
Exemplo de retorno do método geleia_ga:
```
[ [ ['Professor1','Disciplina1'] , ['Professor2','Disciplina2'] , ... , ['Professor1','Disciplina7'] ] , 0.1 ]
```
#### Métodos adicionais

Além dos métodos citados acima, a aplicação possui ainda 3 métodos auxiliares:

    carrega_configuracao(url_config): Carrega o arquivo .csv definindo as configurações iniciais da grade
    gera_grade(aulas, solucao): A partir das aulas que existem e da solução que apresenta as posições 
    que elas ocupam na grade, é gerado um vetor do tipo [[professor, disciplina],...]
    imprime_solucao(solucao): Imprime em modo texto a solução passada como parâmetro
    
A implementação completa do AG encontra-se em: (https://github.com/gysakurai/GELEIA/blob/main/grasp/ga.py).
    
## Como utilizar o Geleia

Para executar a aplicação, deve-se seguir os seguintes passos:

1) Acessar o link da aplicação no Streamlit: https://bitly.com/GELEIA_MESTUEL
2) Acessar e preencher a planilha com as configurações da grade 
3) Gerar, a partir da planilha, o arquivo .csv e carregá-lo no local indicado
4) Aguardar o processamento
5) Verificar a Grade Escolar
6) Fazer o download da imagem da grade para cada uma das salas

A imagem, a seguir, representa a interface gráfica da aplicação no https://streamlit.io:

![Gui Geleia](https://github.com/gysakurai/GELEIA/blob/main/telas/Geleia.png)


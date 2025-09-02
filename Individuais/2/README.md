# Algoritmo MaxMin Select - Seleção Simultânea do Maior e Menor Elementos

Este projeto implementa o algoritmo MaxMin Select em Python utilizando a técnica de divisão e conquista para encontrar simultaneamente o maior e menor elementos de uma sequência de números.

## Como rodar o projeto

1. Certifique-se de ter o Python instalado (versão 3.x).
2. Navegue até o diretório `Individuais/2/`.
3. Execute o arquivo principal:

```bash
python main.py
```

O programa solicitará uma sequência de números separados por espaços e exibirá o maior e menor elementos encontrados, juntamente com o número de comparações realizadas.

## Lógica do Algoritmo MaxMin Select

O algoritmo MaxMin Select utiliza a técnica de divisão e conquista para encontrar simultaneamente o maior e menor elementos de uma sequência com eficiência otimizada. A estratégia funciona da seguinte forma:

### Casos Base:
1. **Lista com 1 elemento**: O único elemento é tanto o mínimo quanto o máximo.
2. **Lista com 2 elementos**: Uma comparação determina qual é o mínimo e qual é o máximo.

### Caso Recursivo:
1. **Divisão**: A lista é dividida ao meio (índice médio).
2. **Conquista**: Aplica-se recursivamente o algoritmo em cada metade.
3. **Combinação**: Compara os resultados das duas metades:
   - O mínimo final é o menor entre os mínimos das duas metades
   - O máximo final é o maior entre os máximos das duas metades

### Vantagens:
- Reduz o número de comparações de 2n-2 (abordagem ingênua) para aproximadamente 3n/2
- Complexidade temporal O(n) com constante otimizada
- Utiliza divisão e conquista de forma eficiente

## Modelo para main.py

Arquivo: main.py
Objetivo: Implementa o algoritmo MaxMin Select utilizando divisão e conquista.

### Classes e Responsabilidades:

- **MaxMinResult**
  Encapsula o resultado contendo o valor mínimo e máximo encontrados.
  Responsável por armazenar e apresentar os resultados de forma estruturada.

- **MaxMinSelector (ABC)**
  Interface abstrata que define o contrato para implementações do algoritmo.
  Segue o princípio da inversão de dependência (DIP).

- **DivideConquerMaxMinSelector**
  Implementa o algoritmo MaxMin Select usando divisão e conquista.
  Conta o número de comparações realizadas para análise de eficiência.
  Segue o princípio da responsabilidade única (SRP).

- **InputHandler**
  Responsável por capturar e validar a entrada do usuário.
  Trata erros de entrada e solicita nova entrada quando necessário.
  Segue o princípio da responsabilidade única (SRP).

- **OutputHandler**
  Responsável por formatar e exibir os resultados ao usuário.
  Encapsula a apresentação da saída de forma clara e organizada.

- **MaxMinApp**
  Orquestra a execução do programa coordenando entrada, processamento e saída.
  Utiliza injeção de dependência para o seletor, seguindo DIP.

### Estrutura do arquivo:
- Implementa classes separadas para cada responsabilidade
- Segue os princípios SOLID, especialmente SRP e DIP
- Utiliza abstrações para permitir diferentes implementações do algoritmo

## Relatório Técnico

### Análise da Complexidade Assintótica pelo Método de Contagem de Operações

#### Detalhamento das Comparações por Etapa:

**Casos Base:**
- **n = 1**: 0 comparações (elemento único é min e max)
- **n = 2**: 1 comparação (determina qual é min e qual é max)

**Caso Recursivo (n > 2):**
1. **Divisão**: O(1) - cálculo do índice médio
2. **Conquista**: 
   - Chamada recursiva na metade esquerda: T(⌊n/2⌋)
   - Chamada recursiva na metade direita: T(⌈n/2⌉)
3. **Combinação**: 2 comparações
   - 1 comparação para encontrar o mínimo entre as duas metades
   - 1 comparação para encontrar o máximo entre as duas metades

#### Recorrência para o Número de Comparações:

```
T(n) = {
    0,                           se n = 1
    1,                           se n = 2  
    T(⌊n/2⌋) + T(⌈n/2⌉) + 2,    se n > 2
}
```

#### Resolução da Recorrência:

Para simplificar, consideremos n = 2^k (potência de 2):

```
T(n) = 2T(n/2) + 2
```

Expandindo a recorrência:
- T(n) = 2T(n/2) + 2
- T(n) = 2[2T(n/4) + 2] + 2 = 4T(n/4) + 6
- T(n) = 4[2T(n/8) + 2] + 6 = 8T(n/8) + 14
- ...
- T(n) = 2^i × T(n/2^i) + 2(2^i - 1)

Quando n/2^i = 2, temos i = log₂(n) - 1:
- T(n) = 2^(log₂(n)-1) × T(2) + 2(2^(log₂(n)-1) - 1)
- T(n) = (n/2) × 1 + 2(n/2 - 1)
- T(n) = n/2 + n - 2
- T(n) = 3n/2 - 2

**Resultado:** T(n) = 3n/2 - 2 comparações

**Complexidade Assintótica:** O(n)

#### Verificação com Exemplos:
- n = 4: T(4) = 3(4)/2 - 2 = 4 comparações
- n = 8: T(8) = 3(8)/2 - 2 = 10 comparações
- n = 16: T(16) = 3(16)/2 - 2 = 22 comparações

### Análise da Complexidade Assintótica pela Aplicação do Teorema Mestre

#### Recorrência do MaxMin Select:
```
T(n) = 2T(n/2) + O(1)
```

#### Aplicação do Teorema Mestre:

O Teorema Mestre se aplica a recorrências da forma:
```
T(n) = aT(n/b) + f(n)
```

No nosso caso:
- a = 2 (duas chamadas recursivas)
- b = 2 (divisão pela metade)
- f(n) = O(1) (trabalho constante na combinação)

#### Parâmetros:
- log_b(a) = log₂(2) = 1
- f(n) = O(1) = O(n⁰)

#### Comparação:
- f(n) = O(n⁰) e log_b(a) = 1
- Como 0 < 1, temos f(n) = O(n^(log_b(a)-ε)) onde ε = 1

#### Aplicação do Caso 1 do Teorema Mestre:
Se f(n) = O(n^(log_b(a)-ε)) para algum ε > 0, então:
```
T(n) = Θ(n^(log_b(a))) = Θ(n¹) = Θ(n)
```

**Conclusão:** A complexidade temporal é Θ(n), confirmando nossa análise anterior.

### Análise Completa de Complexidade:

- **Complexidade temporal**: O(n) com aproximadamente 3n/2 comparações
- **Complexidade espacial**: O(log n) devido à profundidade da recursão
- **Casos**:
  - **Melhor caso**: O(n) - não há melhor caso, sempre precisa examinar todos os elementos
  - **Caso médio**: O(n) - comportamento consistente independente da disposição dos dados  
  - **Pior caso**: O(n) - mesmo comportamento para qualquer entrada

### Comparação com Abordagem Ingênua:
- **Abordagem ingênua**: 2n-2 comparações (uma passada para min, outra para max)
- **MaxMin Select**: 3n/2-2 comparações (aproximadamente 25% menos comparações)

## Saída da Execução

Exemplo de saídas na execução:

```
MaxMin Select Algorithm - Divide and Conquer
==================================================
Enter numbers separated by spaces: 3 7 1 9 4 2 8
Result: Min: 1, Max: 9
Number of comparisons: 8
```

```
MaxMin Select Algorithm - Divide and Conquer
==================================================
Enter numbers separated by spaces: 5
Result: Min: 5, Max: 5
Number of comparisons: 0
```

## Documentação e links úteis

- [Introduction to Algorithms - CLRS](https://mitpress.mit.edu/books/introduction-algorithms-third-edition)
- [Divide and Conquer Algorithms](https://www.geeksforgeeks.org/divide-and-conquer/)
- [Master Theorem](https://en.wikipedia.org/wiki/Master_theorem_(analysis_of_algorithms))

## Licença

Este projeto está licenciado sob a Licença MIT.

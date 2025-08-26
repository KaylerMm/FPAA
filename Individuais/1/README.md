# Algoritmo de Karatsuba para Multiplicação de Inteiros

Este projeto implementa o algoritmo de Karatsuba em Python para multiplicação eficiente de dois números inteiros.

## Como rodar o projeto

1. Certifique-se de ter o Python instalado (versão 3.x).
2. Navegue até o diretório `Individuais/1/`.
3. Execute o arquivo principal:

```bash
python main.py
```

O programa solicitará dois números inteiros e exibirá o resultado da multiplicação usando o algoritmo de Karatsuba.

## Lógica do Algoritmo de Karatsuba

O algoritmo de Karatsuba é uma técnica eficiente para multiplicar dois números grandes, reduzindo o número de multiplicações necessárias em relação ao método tradicional. Ele utiliza a seguinte abordagem:

1. Divide cada número em duas partes (alta e baixa).
2. Calcula três multiplicações recursivas:
   - z0: multiplicação das partes baixas
   - z1: multiplicação da soma das partes (alta + baixa)
   - z2: multiplicação das partes altas
3. Combina os resultados usando a fórmula:
   - resultado = (z2 * 10^(2*m)) + ((z1 - z2 - z0) * 10^m) + z0
   - Onde m é metade do número de dígitos do maior número

Essa abordagem reduz a complexidade de multiplicação de O(n^2) para aproximadamente O(n^1.585), tornando o algoritmo mais eficiente para números grandes.

## Relatório Técnico

### Análise da Complexidade Ciclomática

#### Fluxo de Controle da Função `multiply`

- Início
- Verifica se `x < 10` ou `y < 10`
  - Se verdadeiro: retorna multiplicação direta
  - Se falso: executa divisão dos números, chamadas recursivas e retorna resultado combinado

#### Grafo de Fluxo

- Nós:
  1. Início
  2. Condição (`x < 10 or y < 10`)
  3. Retorno direto
  4. Divisão dos números
  5. Chamada recursiva z0
  6. Chamada recursiva z1
  7. Chamada recursiva z2
  8. Retorno combinado

- Arestas:
  - Início → Condição
  - Condição → Retorno direto
  - Condição → Divisão dos números
  - Divisão dos números → z0
  - z0 → z1
  - z1 → z2
  - z2 → Retorno combinado

- Cálculo:
  - E (arestas) = 7
  - N (nós) = 8
  - P (componentes conexos) = 1

  **Complexidade ciclomática:**  
  M = E − N + 2P = 7 − 8 + 2×1 = 1

  (Obs: Para cada chamada recursiva, o grafo se repete, mas a função principal tem 1 caminho de decisão.)

---

### Análise da Complexidade Assintótica

- **Complexidade temporal:**  
  O(n^log2(3)) ≈ O(n^1.585)  
  (n = número de dígitos dos inteiros)

- **Complexidade espacial:**  
  O(n), devido à profundidade da recursão e armazenamento temporário das variáveis.

- **Casos:**
  - Melhor caso: Quando um dos números tem apenas 1 dígito (multiplicação direta, O(1))
  - Caso médio: Números de tamanho semelhante, O(n^1.585)
  - Pior caso: Números grandes, O(n^1.585) (a recursão é sempre dividida pela metade)

## Saída da Execução
Exemplo de saídas na execução:
```python
Enter the first integer: 3
Enter the second integer: 4
Result: 12
```

## Documentação e links úteis
https://pt.wikipedia.org/wiki/Algoritmo_de_Karatsuba
https://www.youtube.com/watch?v=LCY4dnm88oI

## Licença
Este projeto está licenciado sob a Licença MIT.

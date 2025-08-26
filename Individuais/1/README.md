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

## SRP (Single Responsibility Principle)

O código foi estruturado seguindo o princípio da responsabilidade única, separando funções para entrada, processamento e saída.

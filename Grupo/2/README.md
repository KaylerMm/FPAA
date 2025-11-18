# FloodFill - Sistema de Mapeamento de Regiões de Terreno

## Contribuidores
- [André Augusto](https://github.com/AndreAugusto0908)
- [Gabriel Matos](https://github.com/gabrielmatosmartins)
- [Italo Lelis](https://github.com/italohdc)
- [Kayler Moura](https://github.com/KaylerMm)
- [Pedro Couto](https://github.com/PedroPCouto)

## Como Executar o Projeto

### Pré-requisitos

1. **Python 3.6 ou superior**
2. **Biblioteca tkinter** (para interface gráfica)

### Instalação do tkinter

O tkinter geralmente vem incluído com o Python, mas em alguns sistemas Linux pode precisar ser instalado separadamente:

```bash
# Ubuntu/Debian
sudo apt-get update
sudo apt-get install python3-tk

# CentOS/RHEL/Fedora
sudo yum install tkinter
# ou
sudo dnf install python3-tkinter

# Arch Linux
sudo pacman -S tk

# macOS e Windows
# tkinter já incluído com Python
```

### Execução

1. **Navegue até o diretório do projeto:**
```bash
cd Grupo/2/
```

2. **Execute a aplicação:**
```bash
python3 main.py
```

3. **Escolha uma das opções:**
   - **1**: Demonstração com exemplo predefinido
   - **2**: Entrada interativa para grades personalizadas
   - **3**: Demonstração com grades aleatórias
   - **4**: Interface gráfica visual (requer tkinter)

### Solução de Problemas

Se encontrar erro "ModuleNotFoundError: No module named 'tkinter'":
- Instale o tkinter usando os comandos acima
- A aplicação funcionará em modo terminal (opções 1-3) mesmo sem tkinter

## Descrição do Projeto

Este projeto implementa um sistema inteligente de mapeamento de terrenos usando o algoritmo FloodFill para robôs autônomos. O sistema identifica e colore regiões conectadas em um terreno de grade 2D, ajudando robôs a visualizar e planejar operações em ambientes desconhecidos.

## Visão Geral do Problema

O sistema de mapeamento de terrenos aborda o desafio de identificar e classificar automaticamente regiões em uma grade bidimensional onde cada célula pode ser:

- **0**: Terreno navegável (branco - pode ser preenchido)
- **1**: Obstáculo (preto - não navegável, ignorado pelo preenchimento)  
- **2, 3, 4, ...**: Regiões já coloridas (vermelho, laranja, amarelo, etc.)

## Implementação do Algoritmo FloodFill

O algoritmo FloodFill funciona através de:

1. **Ponto Inicial**: Começando a partir de uma coordenada de célula inicial (x, y)
2. **Detecção de Região**: Identificando todas as células conectadas ao ponto inicial com valor 0
3. **Processo de Preenchimento**: Substituindo o valor 0 das células conectadas por um valor de cor específico
4. **Respeito aos Limites**: Respeitando obstáculos (valor 1) e regiões previamente coloridas
5. **Continuação Automática**: Encontrando a próxima célula navegável e repetindo o processo com uma nova cor
6. **Mapeamento Completo**: Continuando até que todo o terreno navegável seja mapeado e colorido

### Características do Algoritmo

- **Conectividade**: Apenas células adjacentes ortogonalmente (cima, baixo, esquerda, direita) são consideradas conectadas
- **Evitar Obstáculos**: Não pode atravessar células com valor 1 (obstáculos)
- **Preservação de Região**: Mantém a integridade das regiões previamente coloridas
- **Descoberta Automática**: Localiza e preenche automaticamente todas as regiões navegáveis desconectadas
- **Progressão de Cores**: Usa valores de cor incrementais (2, 3, 4, ...) para diferentes regiões

## Estrutura do Projeto

```
Grupo/2/
├── main.py              # Arquivo principal de implementação
├── README.md            # Documentação do projeto
├── requirements.txt     # Dependências do sistema
└── gui_test.py         # Teste de funcionalidade da GUI
```

## Exemplos de Uso

### Exemplo 1: Mapeamento Básico de Regiões

**Entrada:**
```
Dimensões da grade: 4x5
Grade inicial:
0 0 1 0 0
0 1 1 0 0
0 0 1 1 1
1 1 0 0 0

Coordenadas iniciais: (0, 0)
```

**Saída:**
```
Grade final:
2 2 1 3 3
2 1 1 3 3
2 2 1 1 1
1 1 4 4 4
```

**Explicação:**
- Região 2 (vermelho): Área conectada começando de (0,0)
- Região 3 (laranja): Área separada no canto superior direito
- Região 4 (amarelo): Região desconectada no canto inferior direito

### Exemplo 2: Terreno Complexo

**Entrada:**
```
Dimensões da grade: 4x5
Grade inicial:
0 1 0 0 1
0 1 0 0 1
0 1 1 1 1
0 0 0 1 0

Coordenadas iniciais: (0, 2)
```

**Saída:**
```
Grade final:
3 1 2 2 1
3 1 2 2 1
3 1 1 1 1
3 3 3 1 4
```

**Explicação:**
- Região 2 (vermelho): Área conectada no meio superior
- Região 3 (laranja): Conexão da coluna esquerda e linha inferior
- Região 4 (amarelo): Célula isolada no canto inferior direito

## Representação Visual

### Legenda de Cores:
- **0** → Branco (Terreno navegável)
- **1** → Preto (Obstáculo)
- **2** → Vermelho (Primeira região preenchida)
- **3** → Laranja (Segunda região preenchida)  
- **4** → Amarelo (Terceira região preenchida)
- **5+** → Cores adicionais para mais regiões

## Implementação Técnica Detalhada

### Classes Principais

- **Grid**: Gerencia a representação e operações do terreno 2D
- **FloodFillStrategy**: Padrão de estratégia abstrata para diferentes algoritmos de preenchimento
- **RecursiveFloodFill**: Implementação recursiva do algoritmo flood fill
- **IterativeFloodFill**: Implementação iterativa baseada em pilha (padrão)
- **TerrainMapper**: Orquestra o processo de mapeamento de regiões
- **GridInputHandler**: Trata validação e análise de entrada do usuário
- **FloodFillApp**: Controlador principal da aplicação

### Complexidade do Algoritmo

- **Complexidade de Tempo**: O(n × m) onde n e m são as dimensões da grade
- **Complexidade de Espaço**: O(n × m) no pior caso para a pilha de recursão ou iteração

### Padrões de Design Utilizados

- **Padrão Strategy**: Para diferentes implementações de flood fill
- **Princípio de Responsabilidade Única**: Cada classe tem uma responsabilidade focada
- **Validação de Entrada**: Tratamento robusto de erros para entradas do usuário

## Características Interativas

A aplicação fornece quatro modos de execução:

1. **Demonstração de Exemplo**: Executa exemplos predefinidos para mostrar o algoritmo
2. **Modo Interativo**: Permite entrada de grade personalizada e coordenadas iniciais  
3. **Demonstração de Grade Aleatória**: Gera terrenos aleatórios com obstáculos configuráveis
4. **Interface Gráfica**: Animação visual em tempo real do flood fill com controles GUI

### Geração de Grade Aleatória

A aplicação inclui geração automática de terrenos aleatórios com:

- **Dimensões Configuráveis**: Defina tamanho de grade personalizado (linhas × colunas)
- **Controle de Densidade de Obstáculos**: Especifique porcentagem de obstáculos (0-100%)
- **Visualização Animada**: Assista o processo de preenchimento passo a passo
- **Múltiplos Cenários**: Gere diferentes tipos de terreno para teste

### Validação de Entrada

- Dimensões da grade devem ser inteiros positivos
- Valores da grade devem ser válidos (0 para navegável, 1 para obstáculos)
- Coordenadas iniciais devem estar dentro dos limites da grade
- Porcentagens de obstáculos dentro da faixa válida (0-100%)
- Recuperação automática de erros com nova solicitação e valores padrão

## Recursos Especiais

### **Modos de Operação**
- **Modo Terminal**: Interface de linha de comando completa
- **Modo Gráfico**: Visualização em tempo real com animação
- **Modo Batch**: Processamento automático de múltiplas grades
- **Modo Interativo**: Entrada personalizada pelo usuário

### **Funcionalidades Técnicas**
- **Algoritmo Otimizado**: Implementação eficiente baseada em pilha
- **Detecção Automática**: Encontra todas as regiões desconectadas
- **Animação Suave**: Visualização passo-a-passo configurável
- **Tratamento de Erros**: Validação robusta de entrada
- **Multi-threading**: Interface não bloqueante durante processamento

## Características da Interface Gráfica

### **Animação Visual do Flood Fill**
- **Visualização em tempo real**: Assista o algoritmo flood fill executar passo a passo
- **Regiões codificadas por cor**: Cada região preenchida exibe uma cor diferente
- **Seleção interativa de células**: Clique em qualquer célula navegável para iniciar o preenchimento
- **Atualizações dinâmicas da grade**: Veja as células mudarem de cor conforme são processadas

### **Geração de Grade Aleatória**
- **Parâmetros configuráveis**: Defina dimensões da grade (linhas × colunas)
- **Densidade de obstáculos**: Controle a porcentagem de obstáculos (0-100%)
- **Geração instantânea**: Crie novos terrenos aleatórios com um clique
- **Grades de exemplo**: Carregue exemplos predefinidos para teste

### **Interface de Controle**
- **Controles Iniciar/Parar**: Inicie o processo de flood fill da posição selecionada
- **Funcionalidade de reset**: Restaure a grade ao estado navegável original
- **Limpar seleção**: Remova a seleção atual de célula
- **Atualizações de status**: Feedback em tempo real sobre a operação atual

### **Elementos Visuais**
- **Legenda de cores**: Mapeamento claro de valores para cores
- **Coordenadas da grade**: Feedback visual para posições selecionadas
- **Destaque de célula**: Borda azul indica célula inicial selecionada
- **Multi-threading**: Interface não bloqueante durante execução do algoritmo

## Mapeamento de Cores

| Valor | Cor | Descrição |
|-------|--------|-----------|
| 0 | Branco | Terreno navegável |
| 1 | Preto | Obstáculo |
| 2 | Vermelho | Primeira região preenchida |
| 3 | Laranja | Segunda região preenchida |
| 4 | Amarelo | Terceira região preenchida |
| 5+ | Verde/Azul/Roxo | Regiões adicionais |

## Instruções de Uso

### Modo GUI
1. **Iniciar**: Selecione a opção 4 ao executar a aplicação
2. **Gerar Grade**: Use "Generate Random Grid" ou "Load Sample Grid"
3. **Selecionar Ponto Inicial**: Clique em qualquer célula branca (valor 0)
4. **Iniciar Animação**: Clique em "Start FloodFill" para começar a visualização
5. **Reset/Repetir**: Use "Reset" para restaurar o estado original

### Características Avançadas

- **Processamento Multi-região**: Encontra e preenche automaticamente todas as regiões desconectadas
- **Velocidade de Animação**: Atraso otimizado para visualização clara
- **Tratamento de Erros**: Previne seleções e operações inválidas
- **Segurança de Thread**: Animação concorrente sem travamento da interface

## Executando Testes

A aplicação inclui casos de exemplo integrados que demonstram a funcionalidade do algoritmo. Execute o modo de exemplo para verificar se a implementação funciona corretamente com os exemplos fornecidos.

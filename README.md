# Mython 🐍 — A linguagem mais simples do mundo baseada em lógica e inglês A2

**Mython** é uma linguagem de programação super simplificada, inspirada em Python, escrita em inglês básico (nível A2), focada em:

- ✅ **lógica clara**
- ✅ **frases naturais**
- ✅ **baixa dificuldade**
- ✅ **alta legibilidade**
- ✅ **zero complexidade sintática**
- ✅ **conversão automática para Python real**

> **⚠️ IMPORTANTE**: Mython **NÃO executa código diretamente**.  
> **É OBRIGATÓRIO transformar em Python normal antes de rodar.**  
> 
> Fluxo: **Mython (.logic)** → **Transpiler** → **Python (.py)** → **Execução**

## 🎯 A Missão do Mython

> **"Mython permite programar TUDO que Python consegue, mas exigindo apenas lógica básica. Simples quando possível, Python quando necessário."**

📖 **Veja [MYTHON_BASIC.md](MYTHON_BASIC.md) para entender exatamente o que você precisa saber**  
📚 **Veja [GRAMMAR_A2.md](GRAMMAR_A2.md) para a gramática oficial A2/B1**  
🔥 **Veja [PYTHON_COMPLETE.md](PYTHON_COMPLETE.md) para ver como fazer tudo do Python de forma simples**

## 🎯 O Objetivo da Linguagem

Mython existe para:

- ✅ **escrever lógica de computador de forma simples**
- ✅ **apenas lógica básica, nada complicado**
- ✅ **remover sintaxe difícil**
- ✅ **ensinar lógica de forma natural**
- ✅ **deixar código mais parecido com linguagem humana**
- ✅ **ajudar iniciantes a entender lógica**
- ✅ **permitir escrever lógica sem esforço**
- ✅ **evitar erros de indentação, parênteses, tipos, etc**
- ✅ **gerar Python limpo e funcional**

> **Foco**: Apenas lógica simples. Condicionais, loops, listas, funções básicas. Nada mais.

### Ela é perfeita para:

- 👶 **iniciantes** que querem aprender lógica
- 🎓 **jovens** aprendendo programação
- 👥 **pessoas que não sabem programar** mas querem escrever lógica
- ⚡ **quem quer escrever lógica simples** rapidamente
- 🧠 **quem quer pensar logicamente** sem se preocupar com sintaxe
- 🏫 **ensino em escolas** de lógica básica
- 📝 **quem precisa escrever algoritmos simples**

> **Não é para**: Programação complexa, sistemas avançados, arquiteturas complicadas. Use Python puro para isso.

## 🔥 Como Mython Funciona Internamente

Mython possui **3 etapas internas**:

### 🧩 1. Você escreve lógica natural

Exemplo:

```logic
ask number age "your age"

if age is over 17:
    say "adult"
else:
    say "minor"
```

Esse é o código Mython.

Você está literalmente escrevendo:
- pergunte a idade
- se idade for maior que 17
- fale "adulto"
- senão fale "menor"

**Não há:**
- ❌ parênteses
- ❌ tipos
- ❌ sintaxe rígida
- ❌ símbolos estranhos

**É lógica pura.**

### 🧩 2. O Transpiler (Mython engine) converte para Python

Mython transforma o código acima em:

```python
age = int(input("your age"))

if age > 17:
    print("adult")
else:
    print("minor")
```

Ou seja: interpreta frases naturais e as transforma em comandos Python reais.

### 🧩 3. Você executa o Python gerado

O arquivo `.py` é criado e pode ser rodado normalmente:

```bash
python seu_programa.py
```

Você tem o poder total do Python.

## 🧠 O que Mython Entende? (Conceito Central)

Mython entende comandos naturais em inglês, como:

### ✔ Entrada (inputs)

```logic
ask name "your name"
ask number age "your age"
ask word item "favorite item"
```

### ✔ Saída (print)

```logic
say "Hello"
say name
say "age: " + age
```

### ✔ Condições naturais

```logic
if age is 18:
if age is over 18:
if age is under 10:
if age is at least 5:
if age is at most 20:
if name is not "bob":
```

Mython transforma tudo isso em operadores Python automaticamente.

### ✔ Repetições

```logic
repeat 5 times:
    say "hello"
```

→ vira:

```python
for _ in range(5):
    print("hello")
```

### ✔ Listas

```logic
list names = ["ana", "bob"]
add "carlos" to names
remove "ana" from names

for each name in names:
    say name
```

Tudo vira código Python de lista.

### ✔ Funções simples

```logic
define greet(person):
    say "Hello " + person
```

→ vira:

```python
def greet(person):
    print("Hello " + person)
```

### ✔ Funções pré-definidas (macros)

Mython inclui comandos intuitivos como:

```logic
wait 3 seconds
random number from 1 to 10
save text "hello" to file "a.txt"
read file "a.txt" as data
```

Esses comandos usam:
- `random`
- `time`
- `open()`
- conversões automáticas

**Você não precisa saber Python, só Mython.**

## 🌍 Por que a Linguagem usa Inglês A2?

Porque inglês A2 é:

- ✅ **universal**
- ✅ **extremamente simples**
- ✅ **fácil de memorizar**
- ✅ **quase sem gramática difícil**
- ✅ **usado em ensino básico**
- ✅ **perfeito para iniciantes**
- ✅ **curto, direto**
- ✅ **claro para lógica**

### Mython não usa:

- ❌ palavras difíceis
- ❌ frases longas
- ❌ estruturas avançadas
- ❌ preposições complexas
- ❌ funções com muitos parâmetros
- ❌ sintaxe técnica

### Ela usa frases como:

- `ask` (perguntar)
- `say` (dizer)
- `if` (se)
- `repeat` (repetir)
- `list` (lista)
- `add` (adicionar)
- `remove` (remover)

E comparações como:

- `is` (é)
- `is over` (é maior que)
- `is under` (é menor que)
- `is not` (não é)
- `at least` (pelo menos)
- `at most` (no máximo)

## 🧩 O Estilo da Linguagem

Mython é:

- ✅ a versão mínima de Python
- ✅ mais simples até que pseudocódigo
- ✅ lógico
- ✅ natural
- ✅ legível por crianças
- ✅ poderoso por dentro
- ✅ sintaxe inspirada em diálogo

**É como conversar com o computador.**

## ⚙️ O que Mython NÃO faz (de propósito)

Mython **NÃO**:

- ❌ substitui Python
- ❌ tem execução direta
- ❌ é low-level
- ❌ usa símbolos difíceis
- ❌ exige tipagem
- ❌ exige conhecimento técnico
- ❌ perde tempo com sintaxe rígida

**Ela é linguagem humana → Python.**

## 🧬 Filosofia da Linguagem

> **"A lógica deve ser fácil de escrever. A máquina cuida do resto."**

Mython é sobre **pensamento, não sintaxe**.

Ela existe para permitir:

- ✅ **clareza**
- ✅ **acessibilidade**
- ✅ **ensino**
- ✅ **prototipação rápida**
- ✅ **scripts naturais**
- ✅ **automação simples**

E no futuro:

- 🤖 **agentes LLM escritos em Mython**
- 🤖 **automações de IA**
- 🧠 **lógica natural + inteligência artificial**
- ⚡ **geração automática de código**

---

## 📦 Instalação

```bash
pip install -e .
```

> 🚀 **Novo?** Veja [START_HERE.md](START_HERE.md) para começar rapidamente!

## 🚀 Uso Básico

### Transpilar um arquivo

```bash
mython program.logic
```

Isso gera um arquivo `program.py` com o código Python equivalente.

### Transpilar e executar

```bash
mython program.logic --run
```

**O que acontece:**
1. Transpila `program.logic` → `program.py` (Python normal)
2. Executa `python program.py` automaticamente

**⚠️ Lembre-se**: O código Mython **sempre** vira Python normal antes de rodar.

### Especificar arquivo de saída

```bash
mython program.logic -o output.py
```

## 📝 Sintaxe da Linguagem

Mython é **focado em lógica simples**. Aqui está o que você precisa:

### 🟩 Lógica Básica (Foco Principal)

#### Comentários
```logic
# Este é um comentário
```

#### Saída (Print)
```logic
say "Hello, World!"
say name
say "age: " + str(age)
```

#### Entrada (Input)
```logic
ask name "Digite seu nome: "
ask number age "Digite sua idade: "
```

#### Condições
```logic
if age is over 17:
    say "Maior de idade"
else:
    say "Menor de idade"
```

**Operadores de comparação:**
- `is` → `==`
- `is not` → `!=`
- `is over` → `>`
- `is under` → `<`
- `is at least` → `>=`
- `is at most` → `<=`

#### Repetição
```logic
repeat 5 times:
    say "Olá!"

for each name in names:
    say name

while condition:
    say "running"
```

#### Listas
```logic
list names = ["ana", "bob", "carlos"]
add "diana" to names
remove "bob" from names
```

#### Funções
```logic
define greet(name):
    say "Olá, " + name + "!"

greet("Maria")
```

#### Arquivos
```logic
read file "arquivo.txt" as data
save text "conteúdo" to file "arquivo.txt"

open "file.txt" as f:
    set lines = f.readlines()
```

#### Utilitários
```logic
wait 3 seconds
set number = random number from 1 to 100
```

### 🟦 Funcionalidades Adicionais (Opcional)

Se precisar de algo mais avançado, você pode usar Python puro diretamente no código Mython, ou usar estas funcionalidades (mas o foco é manter simples):

#### Classes (se necessário)
```logic
class Person:
    init(name):
        set self.name = name
    
    task greet():
        say "Hello, I am " + self.name
```

#### Exceções (se necessário)
```logic
attempt:
    risky_operation()
catch ValueError as error:
    say "Error: " + str(error)
```

#### Imports
```logic
use math
use json as j
```

> **Lembre-se**: O foco do Mython é **lógica simples**. Use Python puro se precisar de algo complicado.

### Python Puro (Escape) - Poder Completo

**Mython permite usar Python puro diretamente para qualquer coisa:**

```logic
# Lógica simples em Mython
say "Processando..."

# Python puro para qualquer coisa
import math
import numpy as np
import requests
from sklearn.linear_model import LinearRegression

# Volta para Mython
say "Pronto!"
```

**O transpiler copia Python puro exatamente como está. Você pode fazer TUDO que Python faz.**

> 🔥 **Veja [PYTHON_COMPLETE.md](PYTHON_COMPLETE.md) para exemplos completos de como fazer tudo do Python de forma simples**

📖 **Veja [MYTHON_BASIC.md](MYTHON_BASIC.md) - O que você precisa saber (ESSENCIAL)**  
📚 **Veja [GRAMMAR_A2.md](GRAMMAR_A2.md) - Gramática oficial A2/B1**  
🔥 **Veja [PYTHON_COMPLETE.md](PYTHON_COMPLETE.md) - Como fazer tudo do Python de forma simples**  
⚙️ **Veja [HOW_IT_WORKS.md](HOW_IT_WORKS.md) - Como funciona (transpilação obrigatória)**  
🔄 **Veja [ADVANCED_TRANSLATION.md](ADVANCED_TRANSLATION.md) - Como traduz coisas avançadas para Python**  
📐 **Veja [MYTHON_SPECIFICATION.md](MYTHON_SPECIFICATION.md) - Especificação oficial completa**  
🏗️ **Veja [TRANSPILER_DESIGN.md](TRANSPILER_DESIGN.md) - Design do transpiler**  
🚀 **Veja [MAXIMUM_LEVEL.md](MAXIMUM_LEVEL.md) - Nível máximo de pseudocódigo possível**  
📈 **Veja [PROGRESSIVE_GUIDE.md](PROGRESSIVE_GUIDE.md) - Guia progressivo do básico ao avançado**  
📚 **Veja [OFFICIAL_PATTERN_DICTIONARY.md](OFFICIAL_PATTERN_DICTIONARY.md) - Dicionário oficial baseado em fontes reais**  
📚 **Veja [PATTERN_DICTIONARY.md](PATTERN_DICTIONARY.md) - Dicionário completo de padrões**  
🧩 **Veja [BLOCKLY_INTEGRATION.md](BLOCKLY_INTEGRATION.md) - Integração Blockly (blocos visuais)**  
📋 **Veja [QUICK_REFERENCE.md](QUICK_REFERENCE.md) - Referência rápida**  
📖 **Veja [SYNTAX.md](SYNTAX.md) - Documentação completa**

## 📚 Exemplos

### Básicos
- `hello.logic` - Hello World básico
- `age.logic` - Verificação de idade
- `list.logic` - Trabalhando com listas
- `calculator.logic` - Calculadora simples
- `loop.logic` - Loops e repetições
- `function.logic` - Definindo e usando funções
- `random_example.logic` - Números aleatórios
- `wait_example.logic` - Aguardar com wait
- `philosophy.logic` - Demonstração da filosofia

### Avançados
- `class_example.logic` - Classes e OOP
- `async_example.logic` - Programação assíncrona
- `exception_example.logic` - Tratamento de exceções
- `decorator_example.logic` - Decorators
- `ai_example.logic` - IA com transformers (conceitual)
- `agent_example.logic` - Agentes autônomos (estrutura)

## 🏗️ Estrutura do Projeto

```
mython/
├── mython/
│   ├── __init__.py      # Módulo principal
│   ├── transpiler.py    # Motor de transpilação
│   ├── runtime.py       # Funções auxiliares
│   └── cli.py           # Interface de linha de comando
├── examples/            # Exemplos de programas
├── pyproject.toml       # Configuração do projeto
└── README.md            # Este arquivo
```

## 🔧 Como Funciona (Técnico)

**⚠️ OBRIGATÓRIO: Mython sempre transpila para Python antes de executar**

1. **Você escreve** código Mython em arquivo `.logic`
2. **Transpiler converte** para Python (arquivo `.py`)
3. **Python executa** o código gerado

**Processo detalhado:**
1. **Leitura**: O transpiler lê o arquivo `.logic` linha por linha
2. **Análise**: Cada linha é analisada e classificada (say, ask, if, etc.)
3. **Normalização**: Expressões naturais são convertidas para operadores Python
4. **Tradução**: Cada comando é traduzido para Python equivalente
5. **Geração**: O código Python é gerado e salvo em um arquivo `.py`
6. **Execução**: O Python executa o arquivo `.py` gerado

**Você NUNCA executa Mython diretamente. Sempre vira Python primeiro.**

## 🚧 Roadmap

### ✅ Implementado (v1.0)
- [x] Comandos básicos (say, ask, if, else)
- [x] Loops (repeat, for each, while)
- [x] Listas e operações
- [x] Funções
- [x] Operadores de comparação naturais
- [x] Wait e random
- [x] Classes e OOP
- [x] Async/Await
- [x] Exceções (try/except/finally)
- [x] Decorators
- [x] Imports (`use`, `from import`)
- [x] Macros de IA (load model, agent)
- [x] Context managers (open)
- [x] Lambda expressions
- [x] Documentação completa

### 🔄 Em Desenvolvimento
- [ ] Melhor tratamento de erros
- [ ] Mais built-ins (log, error, debug, warn)
- [ ] Suporte completo a agentes IA
- [ ] Integração com LangChain/AutoGen
- [ ] Documentação interativa
- [ ] Extensões para editores (VS Code, etc.)
- [ ] Sistema de módulos Mython

## 📄 Licença

MIT License

## 🤝 Contribuindo

Contribuições são bem-vindas! Veja `CONTRIBUTING.md` para mais detalhes.

---

**Mython** - A linguagem mais simples do mundo. Programação em inglês simples, Python por baixo dos panos. 🎉

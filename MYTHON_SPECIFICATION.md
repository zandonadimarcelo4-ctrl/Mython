# Especificação Oficial Mython 1.0

## ⭐ Princípio Fundamental

**O usuário escreve lógica simples. O sistema gera Python avançado.**

- ✅ Usuário escreve: pseudocódigo em inglês básico (A2/B1)
- ✅ Sistema gera: Python completo e avançado
- ✅ Usuário não precisa saber: Python, sintaxe técnica, conceitos avançados
- ✅ Usuário só precisa saber: **LÓGICA**

---

## 🟩 Nível A2 - Lógica Básica (90% dos casos)

### 1. Valores e Variáveis

```logic
set x = 10
set name = "Alice"
set price = 5.50
```

**Tradução Python:**
```python
x = 10
name = "Alice"
price = 5.50
```

### 2. Entrada e Saída

```logic
say "Hello, World!"
say name
say "Age: " + str(age)

ask name "What is your name? "
ask number age "What is your age? "
```

**Tradução Python:**
```python
print("Hello, World!")
print(name)
print("Age: " + str(age))

name = input("What is your name? ")
age = int(input("What is your age? "))
```

### 3. Condições

```logic
if age is over 18:
    say "Adult"
else:
    say "Minor"

if name is "Alice":
    say "Hello Alice"
elif name is "Bob":
    say "Hello Bob"
else:
    say "Hello stranger"
```

**Tradução Python:**
```python
if age > 18:
    print("Adult")
else:
    print("Minor")

if name == "Alice":
    print("Hello Alice")
elif name == "Bob":
    print("Hello Bob")
else:
    print("Hello stranger")
```

### 4. Repetições

```logic
repeat 5 times:
    say "Hello"

for each item in items:
    say item

while condition:
    say "Running"
```

**Tradução Python:**
```python
for _ in range(5):
    print("Hello")

for item in items:
    print(item)

while condition:
    print("Running")
```

### 5. Listas

```logic
list names = ["Alice", "Bob"]
add "Charlie" to names
remove "Bob" from names

for each name in names:
    say name
```

**Tradução Python:**
```python
names = ["Alice", "Bob"]
names.append("Charlie")
names.remove("Bob")

for name in names:
    print(name)
```

### 6. Funções Simples

```logic
define greet(name):
    say "Hello, " + name

greet("Alice")
```

**Tradução Python:**
```python
def greet(name):
    print("Hello, " + name)

greet("Alice")
```

---

## 🟦 Nível B1 - Conceitos Avançados Simplificados (10% dos casos)

### 1. Classes (Simplificadas)

**Mython (simples):**
```logic
class Person:
    init(name, age):
        set self.name = name
        set self.age = age
    
    task greet():
        say "Hello, I am " + self.name
    
    task get_age():
        return self.age
```

**Python Gerado (avançado):**
```python
class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age
    
    def greet(self):
        print("Hello, I am " + self.name)
    
    def get_age(self):
        return self.age
```

**O usuário não precisa saber:**
- `def __init__`
- `self` como primeiro parâmetro
- Sintaxe de métodos

**O usuário só precisa saber:**
- Lógica: "criar uma classe com nome e idade"
- Lógica: "método que cumprimenta"

### 2. Decorators (Simplificados)

**Mython (simples):**
```logic
retry 3 times:
    task fetch_data(url):
        set response = request(url)
        return response
```

**Python Gerado (avançado):**
```python
def retry(times):
    def decorator(func):
        def wrapper(*args, **kwargs):
            for _ in range(times):
                try:
                    return func(*args, **kwargs)
                except Exception:
                    if _ == times - 1:
                        raise
            return None
        return wrapper
    return decorator

@retry(3)
def fetch_data(url):
    response = request(url)
    return response
```

**O usuário não precisa saber:**
- Sintaxe de decorators
- `@` símbolo
- Funções aninhadas
- `*args, **kwargs`

**O usuário só precisa saber:**
- Lógica: "tentar 3 vezes se falhar"

### 3. Async/Await (Simplificado)

**Mython (simples):**
```logic
async task fetch(url):
    set data = await request(url)
    return data

async task main():
    set result = await fetch("http://example.com")
    say result
```

**Python Gerado (avançado):**
```python
import asyncio
import aiohttp

async def fetch(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            data = await response.text()
            return data

async def main():
    result = await fetch("http://example.com")
    print(result)

asyncio.run(main())
```

**O usuário não precisa saber:**
- `async def`
- `aiohttp`
- Context managers async
- `asyncio.run()`

**O usuário só precisa saber:**
- Lógica: "fazer algo de forma assíncrona"
- Lógica: "aguardar resultado"

### 4. Exceções (Simplificadas)

**Mython (simples):**
```logic
attempt:
    set result = 10 / 0
catch error:
    say "Error: " + str(error)
finally:
    say "Done"
```

**Python Gerado (avançado):**
```python
try:
    result = 10 / 0
except Exception as error:
    print("Error: " + str(error))
finally:
    print("Done")
```

**O usuário não precisa saber:**
- `try/except/finally`
- Tipos de exceção
- Hierarquia de exceções

**O usuário só precisa saber:**
- Lógica: "tentar fazer algo"
- Lógica: "se der erro, fazer outra coisa"

### 5. Context Managers (Simplificados)

**Mython (simples):**
```logic
open "file.txt" as file:
    set content = file.read()
    say content
```

**Python Gerado (avançado):**
```python
with open("file.txt", "r", encoding="utf-8") as file:
    content = file.read()
    print(content)
```

**O usuário não precisa saber:**
- `with` statement
- Context managers
- Encoding
- Modos de arquivo

**O usuário só precisa saber:**
- Lógica: "abrir arquivo e ler"

### 6. IA Avançada (EXTREMAMENTE Simplificada)

**Mython (super simples):**
```logic
use model "gpt2" as ai

ask question "Enter your question: "
set answer = ai.reply(question)
say answer
```

**Python Gerado (muito avançado):**
```python
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

model = AutoModelForCausalLM.from_pretrained("gpt2")
tokenizer = AutoTokenizer.from_pretrained("gpt2")

question = input("Enter your question: ")
inputs = tokenizer(question, return_tensors="pt")
outputs = model.generate(**inputs, max_length=100)
answer = tokenizer.decode(outputs[0], skip_special_tokens=True)
print(answer)
```

**O usuário não precisa saber:**
- Transformers
- Tokenizers
- Tensors
- PyTorch
- Encoding/decoding
- Modelos de linguagem

**O usuário só precisa saber:**
- Lógica: "usar modelo de IA"
- Lógica: "fazer pergunta e obter resposta"

### 7. List Comprehensions (Simplificadas)

**Mython (simples):**
```logic
for each number in data:
    add number * 2 to result
```

**Python Gerado (pode ser otimizado):**
```python
# Versão expandida
result = []
for number in data:
    result.append(number * 2)

# OU versão otimizada (se configurado)
result = [number * 2 for number in data]
```

**O usuário não precisa saber:**
- List comprehensions
- Sintaxe `[x for x in ...]`

**O usuário só precisa saber:**
- Lógica: "para cada número, multiplicar por 2 e adicionar"

### 8. Agentes Autônomos (Simplificados)

**Mython (super simples):**
```logic
agent Jarvis:
    goal "Help the user"
    tool browser
    tool python
    
    task think(question):
        say "Thinking about: " + question
        return "I can help"
    
    task execute(action):
        say "Executing: " + action
        return "Done"
```

**Python Gerado (muito avançado):**
```python
from langchain.agents import initialize_agent, Tool
from langchain.llms import OpenAI
from langchain.tools import Browser, PythonREPLTool

class Jarvis:
    def __init__(self):
        self.goal = "Help the user"
        self.tools = [
            Tool(name="browser", func=Browser().run),
            Tool(name="python", func=PythonREPLTool().run)
        ]
        self.llm = OpenAI()
        self.agent = initialize_agent(
            self.tools, 
            self.llm, 
            agent="zero-shot-react-description"
        )
    
    def think(self, question):
        print("Thinking about: " + question)
        return "I can help"
    
    def execute(self, action):
        print("Executing: " + action)
        return self.agent.run(action)
```

**O usuário não precisa saber:**
- LangChain
- Agents
- Tools
- LLMs
- Zero-shot prompting

**O usuário só precisa saber:**
- Lógica: "criar agente com objetivo"
- Lógica: "dar ferramentas ao agente"

---

## 🟧 Padrões de Reconhecimento do Transpiler

### 1. Detecção de Padrões Simples

O transpiler reconhece padrões e traduz:

| Padrão Mython | Detecta | Traduz Para |
|---------------|---------|-------------|
| `say X` | Comando de saída | `print(X)` |
| `ask X "text"` | Comando de entrada | `X = input("text")` |
| `if X is over Y` | Comparação natural | `if X > Y:` |
| `repeat N times` | Loop fixo | `for _ in range(N):` |
| `for each X in Y` | Loop em iterável | `for X in Y:` |

### 2. Detecção de Padrões Avançados

| Padrão Mython | Detecta | Traduz Para |
|---------------|---------|-------------|
| `class X:` | Definição de classe | `class X:` |
| `init(...):` | Construtor | `def __init__(self, ...):` |
| `task X(...):` | Método | `def X(self, ...):` |
| `async task X` | Função async | `async def X` |
| `await X` | Await | `await X` |
| `attempt:` | Try | `try:` |
| `catch error:` | Except | `except Exception as error:` |
| `retry N times:` | Decorator retry | `@retry(N)` |
| `use model "X" as Y` | Carregar modelo IA | `Y = AutoModel.from_pretrained("X")` |

### 3. Detecção de Dependências

O transpiler detecta automaticamente e adiciona imports:

| Uso Detectado | Import Adicionado |
|---------------|-------------------|
| `wait N seconds` | `import time` |
| `random number from A to B` | `import random` |
| `async task` ou `await` | `import asyncio` |
| `use model` | `from transformers import ...` |
| `agent X:` | `from langchain.agents import ...` |

---

## 🟨 Arquitetura do Sistema

### 1. Camadas

```
┌─────────────────────────────────────┐
│   Usuário (Lógica Simples A2/B1)   │
└──────────────┬──────────────────────┘
               │
               ▼
┌─────────────────────────────────────┐
│   Transpiler (Reconhecimento)      │
│   - Detecta padrões                 │
│   - Identifica tipo de comando      │
│   - Resolve dependências            │
└──────────────┬──────────────────────┘
               │
               ▼
┌─────────────────────────────────────┐
│   Gerador Python (Tradução)        │
│   - Traduz para Python              │
│   - Adiciona imports                │
│   - Estrutura código                │
└──────────────┬──────────────────────┘
               │
               ▼
┌─────────────────────────────────────┐
│   Python Avançado (.py)            │
│   - Código completo                 │
│   - Bibliotecas                     │
│   - Funcional                       │
└─────────────────────────────────────┘
```

### 2. Fluxo de Processamento

1. **Análise Lexical**: Identifica tokens (say, ask, if, etc.)
2. **Análise Sintática**: Reconhece estruturas (condições, loops, classes)
3. **Análise Semântica**: Detecta dependências e imports necessários
4. **Geração de Código**: Traduz para Python equivalente
5. **Otimização**: Adiciona imports, estrutura código

---

## 🟩 Regras de Tradução

### 1. Tradução Direta (1:1)

Comandos simples traduzem diretamente:

```logic
say "Hello"  →  print("Hello")
```

### 2. Tradução Expandida (1:N)

Comandos simples geram múltiplas linhas Python:

```logic
read file "a.txt" as data
```

```python
with open("a.txt", "r", encoding="utf-8") as f:
    data = f.read()
```

### 3. Tradução com Dependências

Comandos que requerem bibliotecas:

```logic
use model "gpt2" as ai
```

```python
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

ai = AutoModelForCausalLM.from_pretrained("gpt2")
```

### 4. Tradução de Padrões Complexos

Padrões que geram estruturas complexas:

```logic
retry 3 times:
    task fetch(url):
        return request(url)
```

```python
def retry(times):
    def decorator(func):
        def wrapper(*args, **kwargs):
            for _ in range(times):
                try:
                    return func(*args, **kwargs)
                except Exception:
                    if _ == times - 1:
                        raise
            return None
        return wrapper
    return decorator

@retry(3)
def fetch(url):
    return request(url)
```

---

## 🟦 Exemplos Completos

### Exemplo 1: IA Simples

**Mython:**
```logic
use model "gpt2" as ai

ask question "Your question: "
set answer = ai.reply(question)
say answer
```

**Python Gerado:**
```python
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

model = AutoModelForCausalLM.from_pretrained("gpt2")
tokenizer = AutoTokenizer.from_pretrained("gpt2")

question = input("Your question: ")
inputs = tokenizer(question, return_tensors="pt")
outputs = model.generate(**inputs, max_length=100)
answer = tokenizer.decode(outputs[0], skip_special_tokens=True)
print(answer)
```

### Exemplo 2: Agente Autônomo

**Mython:**
```logic
agent Helper:
    goal "Answer questions"
    tool browser
    
    task answer(question):
        set result = search(question)
        return result
```

**Python Gerado:**
```python
from langchain.agents import initialize_agent, Tool
from langchain.llms import OpenAI
from langchain.tools import Browser

class Helper:
    def __init__(self):
        self.goal = "Answer questions"
        self.tools = [Tool(name="browser", func=Browser().run)]
        self.llm = OpenAI()
        self.agent = initialize_agent(
            self.tools, 
            self.llm, 
            agent="zero-shot-react-description"
        )
    
    def answer(self, question):
        result = self.agent.run(question)
        return result
```

---

## 🟥 Garantias

### ✅ O Sistema Garante:

1. **Tradução Correta**: Sempre gera Python válido
2. **Funcionalidade Completa**: Todas as funcionalidades Python disponíveis
3. **Dependências Resolvidas**: Imports adicionados automaticamente
4. **Código Limpo**: Python bem estruturado e legível
5. **Compatibilidade**: Funciona com qualquer biblioteca Python

### ✅ O Usuário Só Precisa:

1. **Lógica Básica**: Valores, condições, loops, listas
2. **Inglês A2/B1**: Palavras simples
3. **Estruturar Passos**: Sequência lógica de ações

### ✅ O Usuário NÃO Precisa:

- ❌ Conhecer Python
- ❌ Conhecer sintaxe técnica
- ❌ Conhecer bibliotecas
- ❌ Conhecer conceitos avançados
- ❌ Configurar dependências
- ❌ Entender implementação

---

## 🎯 Resumo Final

**Mython = Lógica Simples → Python Avançado**

- ✅ Usuário escreve: pseudocódigo em inglês básico
- ✅ Sistema gera: Python completo e avançado
- ✅ Usuário não precisa saber: programação técnica
- ✅ Usuário só precisa saber: **LÓGICA**

**100% POSSÍVEL. 100% FUNCIONAL.**

---

**Mython 1.0** - Especificação Oficial 🐍✨


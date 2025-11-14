# Mython - Tudo que Python Faz, de Forma Simples

## ⭐ Princípio Fundamental

**Mython permite programar TUDO que Python consegue, mas exigindo apenas lógica básica.**

Se Python pode fazer, Mython também pode fazer - de forma mais simples.

---

## 🟩 Como Mython Faz Tudo do Python

### 1. Macros Simples para Funcionalidades Comuns

Mython fornece comandos simples para as coisas mais usadas:

| O que você quer fazer | Mython (Simples) | Python (Complexo) |
|----------------------|------------------|-------------------|
| Mostrar texto | `say "hello"` | `print("hello")` |
| Pedir entrada | `ask name "name?"` | `name = input("name?")` |
| Repetir N vezes | `repeat 5 times:` | `for _ in range(5):` |
| Loop em lista | `for each item in list:` | `for item in list:` |
| Adicionar à lista | `add item to list` | `list.append(item)` |
| Ler arquivo | `read file "a.txt" as data` | `with open("a.txt") as f: data = f.read()` |
| Aguardar | `wait 3 seconds` | `time.sleep(3)` |
| Número aleatório | `random number from 1 to 10` | `random.randint(1, 10)` |

### 2. Python Puro Direto (Escape)

**Se Mython não tem um comando simples, você pode usar Python puro diretamente:**

```logic
# Lógica simples em Mython
say "Processando..."

# Python puro para qualquer coisa
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression

# Volta para Mython
say "Pronto!"
```

**O transpiler copia Python puro exatamente como está.**

### 3. Misturando Mython e Python

Você pode misturar livremente:

```logic
# Mython simples
ask number n "Quantos números? "
list numbers = []

# Python puro
for i in range(n):
    numbers.append(i * 2)

# Volta para Mython
for each num in numbers:
    say num
```

---

## 🟦 Funcionalidades Python Completas

### ✅ Tudo que Python Faz, Mython Também Faz

#### 1. Estruturas de Dados
```logic
# Listas (Mython simples)
list items = [1, 2, 3]

# Dicionários (Python puro)
set data = {"name": "Alice", "age": 25}

# Tuplas (Python puro)
set point = (10, 20)

# Sets (Python puro)
set unique = {1, 2, 3, 3}
```

#### 2. Operações Matemáticas
```logic
# Mython simples
set x = 10
set y = 5
set result = x + y

# Python puro para matemática avançada
import math
set sqrt_result = math.sqrt(16)
set sin_value = math.sin(math.pi / 2)
```

#### 3. Manipulação de Strings
```logic
# Mython simples
set name = "Alice"
say "Hello " + name

# Python puro para strings avançadas
set upper = name.upper()
set split = "a,b,c".split(",")
set formatted = f"Name: {name}, Age: {25}"
```

#### 4. List Comprehensions
```logic
# Python puro (Mython não precisa simplificar isso)
set squares = [x**2 for x in range(10)]
set evens = [x for x in range(20) if x % 2 == 0]
```

#### 5. Funções Avançadas
```logic
# Mython simples
define greet(name):
    say "Hello " + name

# Python puro para funções avançadas
def complex_function(x, y=10, *args, **kwargs):
    return x + y + sum(args) + sum(kwargs.values())
```

#### 6. Classes e OOP
```logic
# Mython simples
class Person:
    init(name):
        set self.name = name
    
    task greet():
        say "Hello, I am " + self.name

# Python puro para OOP avançado
class AdvancedClass:
    def __init__(self):
        self._private = "secret"
    
    @property
    def value(self):
        return self._private
    
    @staticmethod
    def static_method():
        return "static"
```

#### 7. Decorators
```logic
# Mython simples
decorator cache:
    task expensive(x):
        return x * 2

# Python puro para decorators avançados
def advanced_decorator(func):
    def wrapper(*args, **kwargs):
        print("Before")
        result = func(*args, **kwargs)
        print("After")
        return result
    return wrapper
```

#### 8. Async/Await
```logic
# Mython simples
async task fetch(url):
    await asyncio.sleep(1)
    return "data"

# Python puro para async avançado
async def advanced_async():
    async with aiohttp.ClientSession() as session:
        async with session.get('http://example.com') as response:
            return await response.text()
```

#### 9. Exceções
```logic
# Mython simples
attempt:
    risky()
catch ValueError as error:
    say "Error: " + str(error)

# Python puro para exceções avançadas
try:
    risky()
except (ValueError, TypeError) as e:
    logger.error(f"Error: {e}")
    raise CustomException("Custom error") from e
finally:
    cleanup()
```

#### 10. Context Managers
```logic
# Mython simples
open "file.txt" as f:
    set data = f.read()

# Python puro para context managers avançados
from contextlib import contextmanager

@contextmanager
def custom_context():
    setup()
    try:
        yield resource
    finally:
        teardown()
```

#### 11. Generators
```logic
# Python puro (Mython não precisa simplificar)
def fibonacci():
    a, b = 0, 1
    while True:
        yield a
        a, b = b, a + b
```

#### 12. Metaclasses
```logic
# Python puro (casos muito avançados)
class Meta(type):
    def __new__(cls, name, bases, dct):
        # lógica complexa
        return super().__new__(cls, name, bases, dct)
```

#### 13. Bibliotecas Python
```logic
# Qualquer biblioteca Python funciona
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import requests
import flask
import django
import tensorflow as tf
import torch
import sklearn

# Tudo funciona normalmente
```

#### 14. APIs e Web
```logic
# Python puro para web
import requests
set response = requests.get("https://api.example.com/data")
set data = response.json()

# Flask/Django (Python puro)
from flask import Flask
app = Flask(__name__)

@app.route('/')
def home():
    return "Hello World"
```

#### 15. IA e Machine Learning
```logic
# Mython simples para IA básica
load model "gpt2" as model

# Python puro para IA avançada
import tensorflow as tf
from transformers import AutoModel
import torch.nn as nn

# Tudo funciona
```

#### 16. Processamento de Dados
```logic
# Python puro (pandas, numpy, etc.)
import pandas as pd
import numpy as np

set df = pd.read_csv("data.csv")
set result = df.groupby("category").mean()
```

#### 17. Multithreading/Multiprocessing
```logic
# Python puro
import threading
import multiprocessing

def worker():
    # trabalho
    pass

thread = threading.Thread(target=worker)
thread.start()
```

---

## 🟨 Estratégia: Simples Quando Possível, Python Quando Necessário

### Regra de Ouro

1. **Use Mython simples** para lógica básica (90% dos casos)
2. **Use Python puro** para coisas avançadas (10% dos casos)
3. **Misture livremente** - funciona perfeitamente

### Exemplo Completo

```logic
# 1. Lógica simples em Mython
say "Bem-vindo ao sistema"
ask name "Seu nome? "

# 2. Python puro para biblioteca
import requests
set response = requests.get(f"https://api.example.com/user/{name}")
set user_data = response.json()

# 3. Volta para Mython
if user_data["age"] is over 18:
    say "Você é maior de idade"
else:
    say "Você é menor de idade"

# 4. Python puro para processamento
set processed = [x * 2 for x in user_data["scores"]]

# 5. Mython para mostrar resultado
say "Scores processados:"
for each score in processed:
    say score
```

---

## 🟥 Garantias

### ✅ Mython Garante:

1. **100% Compatibilidade Python**: Qualquer código Python funciona
2. **Simplicidade para Lógica**: Comandos simples para 90% dos casos
3. **Poder Completo**: Acesso total a tudo do Python
4. **Sem Limitações**: Não há nada que Python faz que Mython não possa fazer
5. **Mistura Perfeita**: Mython e Python podem ser usados juntos

### ✅ Você Pode:

- ✅ Usar qualquer biblioteca Python
- ✅ Fazer qualquer operação Python
- ✅ Criar qualquer estrutura Python
- ✅ Usar qualquer padrão Python
- ✅ Integrar com qualquer sistema Python
- ✅ Fazer IA, web, dados, automação, tudo

### ✅ Mas Você Só Precisa Saber:

- ✅ Lógica básica (valores, condições, loops, listas)
- ✅ Inglês A2/B1 (palavras simples)
- ✅ Como estruturar passos

**NADA mais.**

---

## 🎯 Resumo

**Mython = Simplicidade para Lógica + Poder Completo do Python**

- Use comandos simples quando possível
- Use Python puro quando necessário
- Misture livremente
- Faça tudo que Python faz
- Mas de forma mais fácil

---

**Mython** - Tudo que Python faz, exigindo apenas lógica básica. 🐍✨


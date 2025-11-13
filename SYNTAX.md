# Sintaxe Oficial Mython 1.0

## 📚 Índice

1. [Camada A2 - Básica](#camada-a2---básica)
2. [Camada A2-Advanced - Avançada](#camada-a2-advanced---avançada)
3. [Macros de IA](#macros-de-ia)
4. [Operadores e Expressões](#operadores-e-expressões)

---

## 🟩 Camada A2 - Básica

### Entrada e Saída

```logic
# Saída
say "Hello, World!"
say variable
say "Value: " + str(number)

# Entrada
ask name "What is your name? "
ask number age "What is your age? "
```

### Condições

```logic
if condition:
    say "true"
else:
    say "false"

if age is over 18:
    say "adult"
elif age is over 12:
    say "teen"
else:
    say "child"
```

### Loops

```logic
# Repetição fixa
repeat 5 times:
    say "Hello"

# Loop sobre lista
for each item in items:
    say item

# Loop condicional
while condition:
    say "running"
```

### Listas

```logic
list names = ["Alice", "Bob"]
add "Charlie" to names
remove "Bob" from names

for each name in names:
    say name
```

### Funções

```logic
define greet(name):
    say "Hello, " + name

greet("Alice")
```

### Arquivos

```logic
# Ler arquivo
read file "data.txt" as content
say content

# Escrever arquivo
save text "Hello" to file "output.txt"

# Context manager
open "file.txt" as f:
    set lines = f.readlines()
```

### Utilitários

```logic
# Aguardar
wait 3 seconds

# Número aleatório
set number = random number from 1 to 100
```

---

## 🟦 Camada A2-Advanced - Avançada

### Classes

```logic
class Person:
    init(name, age):
        set self.name = name
        set self.age = age
    
    task greet():
        say "Hello, I am " + self.name
    
    task get_age():
        return self.age

# Uso
set person = Person("Alice", 25)
person.greet()
```

### Async/Await

```logic
use asyncio

async task fetch(url):
    await asyncio.sleep(1)
    return "Data from " + url

async task main():
    set data = await fetch("http://example.com")
    say data

asyncio.run(main())
```

### Exceções

```logic
attempt:
    set result = risky_operation()
catch ValueError as error:
    say "Error: " + str(error)
finally:
    say "Cleanup"
```

### Decorators

```logic
decorator cache:
    task cached_func(func):
        # Implementação do decorator
        return func

@cache
define expensive_function(x):
    return x * 2
```

### Imports

```logic
# Import simples
use math
use json as j

# Import específico
from math import sqrt
from transformers import AutoModel
```

### Expressões Lambda

```logic
set double = x => x * 2
set numbers = [1, 2, 3, 4]
set doubled = [double(n) for n in numbers]
```

### Controle de Fluxo

```logic
# Break e Continue
for each item in items:
    if item is "stop":
        break
    if item is "skip":
        continue
    say item

# Pass (placeholder)
if condition:
    pass
else:
    say "not condition"

# Assert
assert age is over 0
```

### Raise

```logic
define divide(a, b):
    if b is 0:
        raise ValueError("Division by zero")
    return a / b
```

---

## 🤖 Macros de IA

### Carregar Modelo

```logic
load model "gpt2" as model
load tokenizer "gpt2" as tokenizer
```

### Agentes

```logic
agent Jarvis:
    goal "Help the user"
    tool browser
    tool python
    tool calculator
```

---

## 🔧 Operadores e Expressões

### Comparações Naturais

| Mython | Python |
|--------|--------|
| `is` | `==` |
| `is not` | `!=` |
| `is over` | `>` |
| `is under` | `<` |
| `is at least` | `>=` |
| `is at most` | `<=` |

### Operadores Python

Todos os operadores Python funcionam normalmente:
- `+`, `-`, `*`, `/`, `//`, `%`
- `and`, `or`, `not`
- `in`, `not in`

### Atribuições

```logic
set x = 10
set name = "Alice"
set items = [1, 2, 3]
```

---

## 📝 Comentários

```logic
# Comentário de linha única

# Comentários podem estar em qualquer lugar
say "Hello"  # Comentário inline
```

---

## 🎯 Python Puro (Escape)

Qualquer linha que não seja reconhecida como comando Mython é copiada como Python puro:

```logic
import numpy as np
set array = np.array([1, 2, 3])
say array
```

---

## 🔄 Conversões Automáticas

O transpiler adiciona automaticamente:

- `import time` quando usa `wait`
- `import random` quando usa `random number from`
- `import asyncio` quando usa `async`/`await`
- `from transformers import ...` quando usa `load model`

---

## 💡 Dicas

1. **Indentação**: Use 4 espaços (como Python)
2. **Aspas**: Use `"` ou `'` para strings
3. **Case Sensitive**: Mython é case-sensitive
4. **Nomes**: Use nomes descritivos em inglês A2
5. **Simplicidade**: Prefira comandos Mython sobre Python puro quando possível

---

**Mython 1.0** - A linguagem mais simples do mundo. 🐍✨


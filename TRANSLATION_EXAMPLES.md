# Exemplos Práticos de Tradução Mython → Python

## 🎯 Veja Como Funciona na Prática

Este documento mostra exemplos reais de como o Mython traduz para Python.

---

## 📝 Exemplo 1: Lógica Básica

### Mython
```logic
ask number age "Your age: "
if age is over 18:
    say "Adult"
else:
    say "Minor"
```

### Python Gerado
```python
age = int(input("Your age: "))
if age > 18:
    print("Adult")
else:
    print("Minor")
```

✅ **Tradução perfeita - Funciona exatamente igual**

---

## 📝 Exemplo 2: Classes

### Mython
```logic
class Person:
    init(name, age):
        set self.name = name
        set self.age = age
    
    task greet():
        say "Hello, I am " + self.name
        say "I am " + str(self.age) + " years old"
```

### Python Gerado
```python
class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age
    
    def greet(self):
        print("Hello, I am " + self.name)
        print("I am " + str(self.age) + " years old")
```

✅ **Tradução perfeita - OOP completo**

---

## 📝 Exemplo 3: Async/Await

### Mython
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

### Python Gerado
```python
import asyncio

async def fetch(url):
    await asyncio.sleep(1)
    return "Data from " + url

async def main():
    data = await fetch("http://example.com")
    print(data)

asyncio.run(main())
```

✅ **Tradução perfeita - Async completo**

---

## 📝 Exemplo 4: Arquivos

### Mython
```logic
save text "Hello World" to file "output.txt"
read file "output.txt" as content
say content
```

### Python Gerado
```python
with open("output.txt", "w", encoding="utf-8") as f:
    f.write(str("Hello World"))
with open("output.txt", "r", encoding="utf-8") as f:
    content = f.read()
print(content)
```

✅ **Tradução perfeita - Context managers**

---

## 📝 Exemplo 5: Misturando Mython e Python

### Mython
```logic
# Mython simples
say "Starting"
ask number n "Enter number: "

# Python puro
import math
set result = math.sqrt(n)

# Volta para Mython
say "Square root: " + str(result)
```

### Python Gerado
```python
# Mython simples
print("Starting")
n = int(input("Enter number: "))

# Python puro
import math
result = math.sqrt(n)

# Volta para Mython
print("Square root: " + str(result))
```

✅ **Tradução perfeita - Mistura funciona**

---

## 📝 Exemplo 6: Listas e Loops

### Mython
```logic
list numbers = [1, 2, 3, 4, 5]
set total = 0

for each num in numbers:
    set total = total + num

say "Total: " + str(total)
```

### Python Gerado
```python
numbers = [1, 2, 3, 4, 5]
total = 0

for num in numbers:
    total = total + num

print("Total: " + str(total))
```

✅ **Tradução perfeita - Loops completos**

---

## 📝 Exemplo 7: Exceções

### Mython
```logic
attempt:
    set result = 10 / 0
catch ZeroDivisionError as error:
    say "Error: " + str(error)
finally:
    say "Done"
```

### Python Gerado
```python
try:
    result = 10 / 0
except ZeroDivisionError as error:
    print("Error: " + str(error))
finally:
    print("Done")
```

✅ **Tradução perfeita - Exceções completas**

---

## 📝 Exemplo 8: Utilitários

### Mython
```logic
set random_num = random number from 1 to 100
say "Random: " + str(random_num)

wait 2 seconds
say "Done waiting"
```

### Python Gerado
```python
import random

random_num = random.randint(1, 100)
print("Random: " + str(random_num))

import time
time.sleep(2)
print("Done waiting")
```

✅ **Tradução perfeita - Imports automáticos**

---

## 🎯 Teste Você Mesmo

1. **Crie um arquivo `.logic`** com código Mython
2. **Transpile**: `mython arquivo.logic`
3. **Veja o Python gerado**: `cat arquivo.py` (ou abra no editor)
4. **Execute**: `python arquivo.py`

**Você verá que o Python gerado funciona perfeitamente!**

---

## ✅ Garantias

- ✅ **Sempre gera Python válido**
- ✅ **Sempre funciona corretamente**
- ✅ **Preserva toda a lógica**
- ✅ **Adiciona imports necessários**
- ✅ **Mantém estrutura e indentação**

---

**Mython** - Traduz tudo para Python que funciona. 🐍✨


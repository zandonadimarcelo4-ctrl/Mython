# Guia Progressivo: Do Básico ao Avançado em Mython

## 🎯 Aprenda Progressivamente - Do Simples ao Complexo

Este guia mostra como ir do básico ao avançado de forma **muito simples de programar**.

---

## 📚 Nível 1: Básico Absoluto (Primeiros Passos)

### O que você aprende:
- Mostrar texto
- Pedir informações
- Guardar valores
- Decisões simples

### Exemplo 1: Hello World
```logic
say "Hello, World!"
```

**Python gerado:**
```python
print("Hello, World!")
```

### Exemplo 2: Perguntar e Responder
```logic
ask name "What is your name? "
say "Hello, " + name
```

**Python gerado:**
```python
name = input("What is your name? ")
print("Hello, " + name)
```

### Exemplo 3: Decisão Simples
```logic
ask number age "How old are you? "
if age is over 18:
    say "You are an adult"
else:
    say "You are a minor"
```

**Python gerado:**
```python
age = int(input("How old are you? "))
if age > 18:
    print("You are an adult")
else:
    print("You are a minor")
```

**✅ Você já pode fazer:** Programas simples de interação

---

## 📚 Nível 2: Loops e Listas (Repetir e Organizar)

### O que você aprende:
- Repetir ações
- Trabalhar com listas
- Processar múltiplos itens

### Exemplo 1: Repetir
```logic
say "Counting to 5:"
repeat 5 times:
    say "Hello"
```

**Python gerado:**
```python
print("Counting to 5:")
for _ in range(5):
    print("Hello")
```

### Exemplo 2: Lista Simples
```logic
list names = ["Alice", "Bob", "Charlie"]
for each name in names:
    say "Hello, " + name
```

**Python gerado:**
```python
names = ["Alice", "Bob", "Charlie"]
for name in names:
    print("Hello, " + name)
```

### Exemplo 3: Adicionar e Remover
```logic
list items = []
add "apple" to items
add "banana" to items
add "orange" to items

say "Items:"
for each item in items:
    say item

remove "banana" from items
say "After removing banana:"
for each item in items:
    say item
```

**Python gerado:**
```python
items = []
items.append("apple")
items.append("banana")
items.append("orange")

print("Items:")
for item in items:
    print(item)

items.remove("banana")
print("After removing banana:")
for item in items:
    print(item)
```

**✅ Você já pode fazer:** Processar dados, listas, loops

---

## 📚 Nível 3: Funções (Organizar Código)

### O que você aprende:
- Criar funções reutilizáveis
- Organizar código
- Retornar valores

### Exemplo 1: Função Simples
```logic
define greet(name):
    say "Hello, " + name

greet("Alice")
greet("Bob")
```

**Python gerado:**
```python
def greet(name):
    print("Hello, " + name)

greet("Alice")
greet("Bob")
```

### Exemplo 2: Função com Retorno
```logic
define add(a, b):
    set result = a + b
    return result

set sum = add(5, 3)
say "Sum: " + str(sum)
```

**Python gerado:**
```python
def add(a, b):
    result = a + b
    return result

sum = add(5, 3)
print("Sum: " + str(sum))
```

### Exemplo 3: Função com Lógica
```logic
define check_age(age):
    if age is over 18:
        return "adult"
    else:
        return "minor"

ask number age "Your age: "
set status = check_age(age)
say "You are an " + status
```

**Python gerado:**
```python
def check_age(age):
    if age > 18:
        return "adult"
    else:
        return "minor"

age = int(input("Your age: "))
status = check_age(age)
print("You are an " + status)
```

**✅ Você já pode fazer:** Código organizado e reutilizável

---

## 📚 Nível 4: Arquivos (Salvar e Ler Dados)

### O que você aprende:
- Ler arquivos
- Escrever arquivos
- Trabalhar com dados persistentes

### Exemplo 1: Escrever Arquivo
```logic
save text "Hello from Mython!" to file "output.txt"
say "File saved!"
```

**Python gerado:**
```python
with open("output.txt", "w", encoding="utf-8") as f:
    f.write(str("Hello from Mython!"))
print("File saved!")
```

### Exemplo 2: Ler Arquivo
```logic
read file "output.txt" as content
say "File content: " + content
```

**Python gerado:**
```python
with open("output.txt", "r", encoding="utf-8") as f:
    content = f.read()
print("File content: " + content)
```

### Exemplo 3: Processar Arquivo
```logic
read file "data.txt" as data
set lines = data.split("\n")
say "Number of lines: " + str(len(lines))
for each line in lines:
    say "Line: " + line
```

**Python gerado:**
```python
with open("data.txt", "r", encoding="utf-8") as f:
    data = f.read()
lines = data.split("\n")
print("Number of lines: " + str(len(lines)))
for line in lines:
    print("Line: " + line)
```

**✅ Você já pode fazer:** Trabalhar com arquivos e dados

---

## 📚 Nível 5: Classes (Organização Avançada)

### O que você aprende:
- Criar objetos
- Organizar dados e ações
- Reutilizar código

### Exemplo 1: Classe Simples
```logic
class Person:
    init(name):
        set self.name = name
    
    task greet():
        say "Hello, I am " + self.name

set person = Person("Alice")
person.greet()
```

**Python gerado:**
```python
class Person:
    def __init__(self, name):
        self.name = name
    
    def greet(self):
        print("Hello, I am " + self.name)

person = Person("Alice")
person.greet()
```

### Exemplo 2: Classe com Múltiplos Atributos
```logic
class Student:
    init(name, age, grade):
        set self.name = name
        set self.age = age
        set self.grade = grade
    
    task get_info():
        say "Name: " + self.name
        say "Age: " + str(self.age)
        say "Grade: " + str(self.grade)
    
    task update_grade(new_grade):
        set self.grade = new_grade
        say "Grade updated to " + str(new_grade)

set student = Student("Bob", 20, 85)
student.get_info()
student.update_grade(90)
student.get_info()
```

**Python gerado:**
```python
class Student:
    def __init__(self, name, age, grade):
        self.name = name
        self.age = age
        self.grade = grade
    
    def get_info(self):
        print("Name: " + self.name)
        print("Age: " + str(self.age))
        print("Grade: " + str(self.grade))
    
    def update_grade(self, new_grade):
        self.grade = new_grade
        print("Grade updated to " + str(new_grade))

student = Student("Bob", 20, 85)
student.get_info()
student.update_grade(90)
student.get_info()
```

**✅ Você já pode fazer:** Programação orientada a objetos

---

## 📚 Nível 6: Tratamento de Erros (Robustez)

### O que você aprende:
- Lidar com erros
- Tornar código mais robusto
- Prevenir falhas

### Exemplo 1: Tentar e Capturar
```logic
attempt:
    set result = 10 / 0
    say "Result: " + str(result)
catch error:
    say "Error occurred: " + str(error)
```

**Python gerado:**
```python
try:
    result = 10 / 0
    print("Result: " + str(result))
except Exception as error:
    print("Error occurred: " + str(error))
```

### Exemplo 2: Tentar até Funcionar
```logic
set success = false
repeat until success:
    attempt:
        read file "data.txt" as content
        say "File read successfully!"
        set success = true
    catch error:
        say "Error reading file, retrying..."
        wait 1 seconds
```

**Python gerado:**
```python
import time

success = False
while not success:
    try:
        with open("data.txt", "r", encoding="utf-8") as f:
            content = f.read()
        print("File read successfully!")
        success = True
    except Exception as error:
        print("Error reading file, retrying...")
        time.sleep(1)
```

**✅ Você já pode fazer:** Código robusto e confiável

---

## 📚 Nível 7: Programação Assíncrona (Eficiência)

### O que você aprende:
- Fazer múltiplas coisas ao mesmo tempo
- Melhorar performance
- Trabalhar com operações demoradas

### Exemplo 1: Async Simples
```logic
use asyncio

async task fetch_data(url):
    say "Fetching " + url
    await asyncio.sleep(1)
    return "Data from " + url

async task main():
    set data = await fetch_data("http://example.com")
    say data

asyncio.run(main())
```

**Python gerado:**
```python
import asyncio

async def fetch_data(url):
    print("Fetching " + url)
    await asyncio.sleep(1)
    return "Data from " + url

async def main():
    data = await fetch_data("http://example.com")
    print(data)

asyncio.run(main())
```

### Exemplo 2: Múltiplas Tarefas
```logic
use asyncio

async task process_item(item):
    say "Processing " + item
    await asyncio.sleep(0.5)
    return "Processed " + item

async task main():
    list items = ["item1", "item2", "item3"]
    list results = []
    
    for each item in items:
        set result = await process_item(item)
        add result to results
    
    say "All done!"
    for each result in results:
        say result

asyncio.run(main())
```

**Python gerado:**
```python
import asyncio

async def process_item(item):
    print("Processing " + item)
    await asyncio.sleep(0.5)
    return "Processed " + item

async def main():
    items = ["item1", "item2", "item3"]
    results = []
    
    for item in items:
        result = await process_item(item)
        results.append(result)
    
    print("All done!")
    for result in results:
        print(result)

asyncio.run(main())
```

**✅ Você já pode fazer:** Programas eficientes e rápidos

---

## 📚 Nível 8: IA e Machine Learning (Avançado)

### O que você aprende:
- Usar modelos de IA
- Processar texto com IA
- Criar sistemas inteligentes

### Exemplo 1: Chatbot Simples
```logic
use model "gpt2" as bot

ask question "Your question: "
set answer = bot.reply(question)
say "Bot: " + answer
```

**Python gerado:**
```python
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

model = AutoModelForCausalLM.from_pretrained("gpt2")
tokenizer = AutoTokenizer.from_pretrained("gpt2")

question = input("Your question: ")
inputs = tokenizer(question, return_tensors="pt")
outputs = model.generate(**inputs, max_length=100)
answer = tokenizer.decode(outputs[0], skip_special_tokens=True)
print("Bot: " + answer)
```

### Exemplo 2: Análise de Sentimento
```logic
use sentiment model as analyzer

ask text "Enter text to analyze: "
set result = analyzer.analyze(text)
say "Sentiment: " + result
```

**Python gerado:**
```python
from transformers import pipeline

analyzer = pipeline("sentiment-analysis")

text = input("Enter text to analyze: ")
result = analyzer(text)[0]
print("Sentiment: " + result['label'])
```

**✅ Você já pode fazer:** Sistemas com IA

---

## 📚 Nível 9: Agentes Autônomos (Máximo)

### O que você aprende:
- Criar agentes inteligentes
- Dar objetivos e ferramentas
- Sistemas autônomos

### Exemplo: Agente Assistente
```logic
agent Assistant:
    goal "Help the user with tasks"
    tool calculator
    tool search
    tool browser
    
    task help(question):
        say "I'm thinking about: " + question
        set answer = search(question)
        return answer
    
    task calculate(expression):
        set result = calculator.evaluate(expression)
        return result
```

**Python gerado:**
```python
from langchain.agents import initialize_agent, Tool
from langchain.llms import OpenAI
from langchain.tools import Calculator, DuckDuckGoSearchRun, Browser

class Assistant:
    def __init__(self):
        self.goal = "Help the user with tasks"
        self.tools = [
            Tool(name="calculator", func=Calculator().run),
            Tool(name="search", func=DuckDuckGoSearchRun().run),
            Tool(name="browser", func=Browser().run)
        ]
        self.llm = OpenAI()
        self.agent = initialize_agent(
            self.tools,
            self.llm,
            agent="zero-shot-react-description"
        )
    
    def help(self, question):
        print("I'm thinking about: " + question)
        answer = self.agent.run(question)
        return answer
    
    def calculate(self, expression):
        result = Calculator().run(expression)
        return result
```

**✅ Você já pode fazer:** Sistemas autônomos complexos

---

## 🎯 Progressão de Aprendizado

```
Nível 1: Básico        → Programas simples
Nível 2: Loops         → Processar dados
Nível 3: Funções       → Código organizado
Nível 4: Arquivos      → Dados persistentes
Nível 5: Classes       → OOP
Nível 6: Erros         → Código robusto
Nível 7: Async         → Performance
Nível 8: IA            → Inteligência
Nível 9: Agentes       → Autonomia
```

---

## 💡 Dicas de Aprendizado

1. **Comece simples**: Domine cada nível antes de avançar
2. **Pratique**: Escreva código em cada nível
3. **Experimente**: Modifique os exemplos
4. **Combine**: Use conceitos de níveis anteriores
5. **Crie projetos**: Aplique o que aprendeu

---

## 🚀 Próximos Passos

1. Pratique cada nível
2. Crie seus próprios exemplos
3. Combine conceitos
4. Construa projetos reais
5. Explore funcionalidades avançadas

---

**Mython** - Do básico ao avançado, sempre simples. 🐍✨


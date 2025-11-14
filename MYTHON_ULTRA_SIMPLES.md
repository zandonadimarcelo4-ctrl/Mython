# 🎯 Mython Ultra Simples - Mais Simples que Moonscript

## 🌍 Tradução Automática

**IMPORTANTE:** O Mython traduz automaticamente qualquer código para inglês antes de executar!

Você pode escrever em **qualquer idioma** e o sistema detecta e traduz automaticamente:
- 🇧🇷 Português: `perguntar`, `dizer`, `se`, `senão`
- 🇪🇸 Espanhol: `preguntar`, `decir`, `si`, `sino`
- 🇺🇸 Inglês: `ask`, `say`, `if`, `else`

---

## 🎯 Objetivo

Criar a linguagem mais simples possível, capaz de fazer coisas avançadas de forma extremamente intuitiva.

**Filosofia:**
- ✅ **Mínimas palavras-chave**
- ✅ **Máxima clareza**
- ✅ **Sintaxe natural como conversa**
- ✅ **Zero complexidade desnecessária**
- ✅ **Tradução automática para qualquer idioma**

---

## 💎 Princípios Fundamentais

### 1. **Uma Palavra = Uma Ação**

Em vez de múltiplas palavras para a mesma coisa, usar apenas UMA:

```python
# ❌ Complexo (não queremos):
say, print, show, display, tell  # 5 palavras para mesma coisa

# ✅ Ultra Simples:
say  # Apenas UMA palavra
```

### 2. **Ordem Natural**

Falar como falaria com alguém:

```python
# ❌ Não natural:
ask for number age

# ✅ Natural:
ask age number  # "Pergunta idade, número"
```

### 3. **Opcional = Não Precisa**

Se algo é opcional, deixar claro que pode omitir:

```python
# Prompt opcional:
ask name  # Sem prompt = ok
ask name "Your name?"  # Com prompt = ok
```

### 4. **Padrão Inteligente**

Inferir o que o usuário quer automaticamente:

```python
# Auto-detecta tipo:
ask age  # Se usar em comparação numérica = número automaticamente
```

---

## 🚀 Sintaxe Ultra Simplificada

### **Comandos Básicos (Máximo 3 palavras-chave)**

#### 1. **Dizer/Imprimir**
```python
say "Hello"  # Única forma
say name     # Diz variável
say "Hello " + name  # Diz expressão
```

#### 2. **Perguntar**
```python
ask name                      # Pergunta texto
ask number age                # Pergunta número
ask name "Your name?"         # Com prompt (opcional)
ask number age "Your age?"    # Número com prompt
```

**Tradução Automática:**
```python
# Português (traduzido automaticamente):
perguntar nome                          # ask name
perguntar numero idade                  # ask number age
perguntar numero idade "Sua idade?"     # ask number age "Your age?"
```

#### 3. **Fazer/Alterar**
```python
name = "John"         # Atribuição simples
age = 25              # Número
items = [1, 2, 3]     # Lista
person = {name: "John", age: 30}  # Dict (sem aspas nas chaves)
```

**Zero palavras-chave!** Usa apenas `=`

---

### **Controle de Fluxo (Máximo 2 palavras-chave)**

#### 1. **Se**
```python
# Forma natural (normalizada automaticamente):
if age is over 18:      # Normaliza para: if age > 18:
    say "Adult"
else:
    say "Minor"

# Forma Python direta (também funciona):
if age > 18:
    say "Adult"
else:
    say "Minor"
```

**Apenas:** `if` e `else` (sem `elif`, usar `else if`)

**Operadores Suportados:**
- `is over` / `is greater than` → `>`
- `is under` / `is less than` → `<`
- `is at least` → `>=`
- `is at most` → `<=`
- `equals` / `is equal to` → `==`
- `is not` → `!=`

#### 2. **Repetir**
```python
# Forma 1: N vezes
repeat 10:
    say "Hello"

# Forma 2: Para cada
for item in items:
    say item

# Forma 3: Enquanto
while age < 18:
    ask age number
```

**Apenas:** `repeat`, `for`, `while`

---

### **Funções (Apenas 1 palavra-chave)**

```python
def add(x, y):
    x + y  # Retorna automaticamente

def greet(name):
    say "Hello " + name
```

**Apenas:** `def` (sem `return` explícito na maioria dos casos)

---

### **Classes (Apenas 1 palavra-chave)**

```python
class Person:
    def __init__(name, age):
        self.name = name
        self.age = age
    
    def greet():
        say "Hello, I'm " + self.name
```

**Apenas:** `class` e `def` (mesmas palavras-chave)

---

## 📊 Comparação: Moonscript vs Mython Ultra Simples

| Feature | Moonscript | Mython Ultra Simples |
|---------|-----------|---------------------|
| **Palavras-chave** | ~30+ | **~10** |
| **Formas de print** | 1 | **1** (`say`) |
| **Formas de input** | 1 | **1** (`ask`) |
| **Operadores naturais** | Não | **Sim** (`is`, `is over`, etc.) |
| **Syntax sugar** | Sim | **Sim** (mais simples) |
| **Curva de aprendizado** | Média | **Mínima** |

---

## 💡 Exemplos Práticos

### Exemplo 1: Programa Básico
```python
ask name "What's your name? "
say "Hello " + name

ask age number "How old are you? "
if age > 18:
    say "You're an adult!"
else:
    say "You're a minor."
```

### Exemplo 2: Lista e Loop
```python
items = [1, 2, 3, 4, 5]

for item in items:
    say item * 2
```

### Exemplo 3: Função
```python
def double(x):
    x * 2

result = double(10)
say result  # Diz 20
```

### Exemplo 4: Classe
```python
class Person:
    def __init__(name):
        self.name = name
    
    def greet():
        say "Hello, I'm " + self.name

john = Person("John")
john.greet()
```

---

## 🎯 Regras de Simplificação

### 1. **Eliminar Redundância**
- ❌ `say`, `print`, `show`, `display`, `tell` → ✅ Apenas `say`
- ❌ `ask`, `get`, `read`, `prompt` → ✅ Apenas `ask`
- ❌ `if`, `when`, `whenever` → ✅ Apenas `if`

### 2. **Inferir Automaticamente**
- `ask age number` → Auto-converte para `int(input())`
- Última linha de função → Auto-return
- `{name: "John"}` → Auto-converte para `{"name": "John"}`

### 3. **Padrões Inteligentes**
- Se usar `age > 18`, `ask age` automaticamente vira número
- Se usar `name + "test"`, `ask name` automaticamente vira texto

### 4. **Zero Configuração**
- Não precisa declarar tipos
- Não precisa `return` explícito na maioria dos casos
- Não precisa `import` básico (auto-adiciona quando necessário)

---

## 🚀 Features Avançadas Simplificadas

### 1. **List Comprehensions**
```python
squares = [x * x for x in range(10)]
```

### 2. **Dict Literals**
```python
person = {name: "John", age: 30}
```

### 3. **Lambda (Simplificado)**
```python
double = x => x * 2
```

### 4. **Try/Except (Simplificado)**
```python
try:
    result = 10 / 0
except:
    say "Error happened"
```

---

## 📋 Palavras-Chave Finais

**Total: ~10 palavras-chave essenciais**

1. `say` - Dizer/Imprimir
2. `ask` - Perguntar
3. `if` - Se
4. `else` - Senão
5. `for` - Para cada
6. `while` - Enquanto
7. `repeat` - Repetir
8. `def` - Definir função
9. `class` - Classe
10. `try`/`except` - Tratamento de erro

**Operadores naturais** (não são palavras-chave, são operadores):
- `is`, `is not`, `is over`, `is under`, etc.

---

## 🎯 Objetivo Final

**Linguagem tão simples que:**
- ✅ Uma criança pode aprender em 10 minutos
- ✅ Qualquer pessoa que fala português/inglês entende
- ✅ Código parece conversa natural
- ✅ Zero barreiras de entrada

**Mas capaz de:**
- ✅ Fazer tudo que Python faz
- ✅ Programação orientada a objetos
- ✅ Programação funcional
- ✅ Programação assíncrona
- ✅ Todas as bibliotecas Python

---

## 💎 Resumo

**Mython Ultra Simples =**
- **Mínimo de palavras-chave** (~10)
- **Máxima clareza** (código = conversa)
- **Máxima simplicidade** (zero complexidade desnecessária)
- **Máximo poder** (faz tudo que Python faz)

**Mais simples que Moonscript?** ✅ **SIM!**

- Moonscript: ~30 palavras-chave
- Mython: ~10 palavras-chave
- Mython: Operadores naturais
- Mython: Auto-inferência
- Mython: Syntax sugar mais simples


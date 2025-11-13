# Dicionário de Padrões Mython

## 🎯 Baseado em Fontes Reais

Este dicionário é baseado em padrões reais de:
1. **Pseudocódigo Estruturado Clássico** (usado em universidades)
2. **Portugol** (faculdades brasileiras)
3. **VisualG** (editor de pseudocódigo)
4. **AppleScript** (DSL da Apple)
5. **Gherkin** (BDD)
6. **Blockly** (programação visual)

> 📖 **Veja [OFFICIAL_PATTERN_DICTIONARY.md](OFFICIAL_PATTERN_DICTIONARY.md) para o dicionário completo baseado em fontes reais**

---

## 🥇 Fonte 1: Pseudocódigo Estruturado Clássico

### Padrões Fundamentais

#### 1. Atribuição (SET)
**Pseudocódigo Clássico:**
```
SET x TO 10
SET name TO "Alice"
```

**Mython:**
```logic
set x = 10
set name = "Alice"
```

**Python:**
```python
x = 10
name = "Alice"
```

#### 2. Condição (IF/THEN/ELSE)
**Pseudocódigo Clássico:**
```
IF x > 10 THEN
    PRINT "big"
ELSE
    PRINT "small"
END IF
```

**Mython:**
```logic
if x is over 10:
    say "big"
else:
    say "small"
```

**Python:**
```python
if x > 10:
    print("big")
else:
    print("small")
```

#### 3. Loop FOR EACH
**Pseudocódigo Clássico:**
```
FOR EACH item IN list
    PRINT item
END FOR
```

**Mython:**
```logic
for each item in list:
    say item
```

**Python:**
```python
for item in list:
    print(item)
```

#### 4. Loop REPEAT
**Pseudocódigo Clássico:**
```
REPEAT 5 TIMES
    PRINT "hello"
END REPEAT
```

**Mython:**
```logic
repeat 5 times:
    say "hello"
```

**Python:**
```python
for _ in range(5):
    print("hello")
```

#### 5. Loop WHILE
**Pseudocódigo Clássico:**
```
WHILE condition DO
    PRINT "running"
END WHILE
```

**Mython:**
```logic
while condition:
    say "running"
```

**Python:**
```python
while condition:
    print("running")
```

#### 6. Função (FUNCTION/RETURN)
**Pseudocódigo Clássico:**
```
FUNCTION add(a, b)
    SET result TO a + b
    RETURN result
END FUNCTION
```

**Mython:**
```logic
define add(a, b):
    set result = a + b
    return result
```

**Python:**
```python
def add(a, b):
    result = a + b
    return result
```

#### 7. Entrada/Saída (INPUT/OUTPUT)
**Pseudocódigo Clássico:**
```
INPUT name
OUTPUT "Hello " + name
```

**Mython:**
```logic
ask name "Enter name: "
say "Hello " + name
```

**Python:**
```python
name = input("Enter name: ")
print("Hello " + name)
```

---

## 🥈 Fonte 2: DSLs de Ação

### Padrões do AppleScript

#### 1. Comandos de Ação
**AppleScript:**
```
say "hello"
open the file "notes.txt"
```

**Mython:**
```logic
say "hello"
open "notes.txt" as file
```

**Python:**
```python
print("hello")
with open("notes.txt", "r") as file:
    pass
```

#### 2. Repetição Natural
**AppleScript:**
```
repeat 5 times
    say "hello"
end repeat
```

**Mython:**
```logic
repeat 5 times:
    say "hello"
```

**Python:**
```python
for _ in range(5):
    print("hello")
```

#### 3. Condições Naturais
**AppleScript:**
```
if x is greater than 10 then
    say "big"
end if
```

**Mython:**
```logic
if x is over 10:
    say "big"
```

**Python:**
```python
if x > 10:
    print("big")
```

### Padrões do Gherkin (BDD)

#### 1. Estrutura Given/When/Then
**Gherkin:**
```
Given user is logged in
When he clicks the button
Then show the menu
```

**Mython:**
```logic
given user is logged in:
    set logged = true

when user clicks button:
    if logged:
        show menu()

then show menu:
    say "Menu displayed"
```

**Python:**
```python
# Given
logged = True

# When
if logged:
    show_menu()

# Then
def show_menu():
    print("Menu displayed")
```

#### 2. Cenários de Teste
**Gherkin:**
```
Scenario: User login
    Given user exists
    When user enters password
    Then user is authenticated
```

**Mython:**
```logic
scenario "User login":
    given user exists:
        set user = create_user()
    
    when user enters password:
        set authenticated = check_password(user, password)
    
    then user is authenticated:
        if authenticated:
            say "Login successful"
```

**Python:**
```python
def scenario_user_login():
    # Given
    user = create_user()
    
    # When
    authenticated = check_password(user, password)
    
    # Then
    if authenticated:
        print("Login successful")
```

### Padrões do Blockly Textual

#### 1. Blocos de Ação
**Blockly:**
```
print "hello"
set x to 10
```

**Mython:**
```logic
say "hello"
set x = 10
```

**Python:**
```python
print("hello")
x = 10
```

#### 2. Loops Condicionais
**Blockly:**
```
repeat until condition
    do something
```

**Mython:**
```logic
repeat until condition:
    do something
```

**Python:**
```python
while not condition:
    do_something()
```

#### 3. Estruturas de Controle
**Blockly:**
```
if condition then
    do this
else
    do that
```

**Mython:**
```logic
if condition:
    do this
else:
    do that
```

**Python:**
```python
if condition:
    do_this()
else:
    do_that()
```

---

## 📚 Dicionário Completo de Padrões

### Ações Básicas

| Padrão Mython | Origem | Python |
|---------------|--------|--------|
| `say X` | AppleScript | `print(X)` |
| `ask X "text"` | Pseudocódigo | `X = input("text")` |
| `ask number X "text"` | Pseudocódigo | `X = int(input("text"))` |
| `set X = Y` | Pseudocódigo | `X = Y` |

### Condições

| Padrão Mython | Origem | Python |
|---------------|--------|--------|
| `if X is Y` | Pseudocódigo | `if X == Y:` |
| `if X is not Y` | Pseudocódigo | `if X != Y:` |
| `if X is over Y` | Pseudocódigo | `if X > Y:` |
| `if X is under Y` | Pseudocódigo | `if X < Y:` |
| `if X is at least Y` | Pseudocódigo | `if X >= Y:` |
| `if X is at most Y` | Pseudocódigo | `if X <= Y:` |
| `else` | Pseudocódigo | `else:` |
| `elif X` | Pseudocódigo | `elif X:` |

### Loops

| Padrão Mython | Origem | Python |
|---------------|--------|--------|
| `repeat N times:` | Pseudocódigo/AppleScript | `for _ in range(N):` |
| `for each X in Y:` | Pseudocódigo | `for X in Y:` |
| `while condition:` | Pseudocódigo | `while condition:` |
| `repeat until condition:` | Blockly | `while not condition:` |

### Listas

| Padrão Mython | Origem | Python |
|---------------|--------|--------|
| `list X = [...]` | Pseudocódigo | `X = [...]` |
| `add Y to X` | AppleScript | `X.append(Y)` |
| `remove Y from X` | AppleScript | `X.remove(Y)` |

### Funções

| Padrão Mython | Origem | Python |
|---------------|--------|--------|
| `define func(args):` | Pseudocódigo | `def func(args):` |
| `return X` | Pseudocódigo | `return X` |
| `task method(args):` | Pseudocódigo | `def method(self, args):` |

### Classes

| Padrão Mython | Origem | Python |
|---------------|--------|--------|
| `class Name:` | Pseudocódigo | `class Name:` |
| `init(args):` | Pseudocódigo | `def __init__(self, args):` |
| `set self.X = Y` | Pseudocódigo | `self.X = Y` |

### Arquivos

| Padrão Mython | Origem | Python |
|---------------|--------|--------|
| `read file "path" as X` | AppleScript | `with open("path") as f: X = f.read()` |
| `save text X to file "path"` | AppleScript | `with open("path", "w") as f: f.write(str(X))` |
| `open "path" as X:` | AppleScript | `with open("path") as X:` |

### Exceções

| Padrão Mython | Origem | Python |
|---------------|--------|--------|
| `attempt:` | Pseudocódigo | `try:` |
| `catch error:` | Pseudocódigo | `except Exception as error:` |
| `finally:` | Pseudocódigo | `finally:` |
| `raise X` | Pseudocódigo | `raise X` |

### Async

| Padrão Mython | Origem | Python |
|---------------|--------|--------|
| `async task func(args):` | Pseudocódigo | `async def func(args):` |
| `await X` | Pseudocódigo | `await X` |

### Decorators

| Padrão Mython | Origem | Python |
|---------------|--------|--------|
| `decorator name:` | Pseudocódigo | `@name` |
| `retry N times:` | Gherkin | `@retry(N)` |

### Utilitários

| Padrão Mython | Origem | Python |
|---------------|--------|--------|
| `wait N seconds` | AppleScript | `time.sleep(N)` |
| `random number from A to B` | Pseudocódigo | `random.randint(A, B)` |

### Imports

| Padrão Mython | Origem | Python |
|---------------|--------|--------|
| `use module` | Pseudocódigo | `import module` |
| `use module as alias` | Pseudocódigo | `import module as alias` |
| `from module import item` | Pseudocódigo | `from module import item` |

### Controle de Fluxo

| Padrão Mython | Origem | Python |
|---------------|--------|--------|
| `break` | Pseudocódigo | `break` |
| `continue` | Pseudocódigo | `continue` |
| `pass` | Pseudocódigo | `pass` |
| `assert condition` | Pseudocódigo | `assert condition` |

### IA e Agentes

| Padrão Mython | Origem | Python |
|---------------|--------|--------|
| `load model "name" as X` | DSL Custom | `X = AutoModel.from_pretrained("name")` |
| `agent Name:` | Gherkin | `class Name:` (com setup de agente) |
| `goal "text"` | Gherkin | `# Goal: text` |
| `tool name` | Gherkin | `# Tool: name` |

### Expressões

| Padrão Mython | Origem | Python |
|---------------|--------|--------|
| `X => Y` | Lambda | `lambda X: Y` |

---

## 🎯 Padrões Combinados

### Estruturas Complexas

#### 1. Loop com Condição
**Mython:**
```logic
for each item in items:
    if item is over 10:
        say item
```

**Python:**
```python
for item in items:
    if item > 10:
        print(item)
```

#### 2. Função com Múltiplas Condições
**Mython:**
```logic
define process(age):
    if age is over 18:
        return "adult"
    elif age is over 12:
        return "teen"
    else:
        return "child"
```

**Python:**
```python
def process(age):
    if age > 18:
        return "adult"
    elif age > 12:
        return "teen"
    else:
        return "child"
```

#### 3. Classe com Múltiplos Métodos
**Mython:**
```logic
class Calculator:
    init():
        set self.result = 0
    
    task add(x):
        set self.result = self.result + x
        return self.result
    
    task reset():
        set self.result = 0
```

**Python:**
```python
class Calculator:
    def __init__(self):
        self.result = 0
    
    def add(self, x):
        self.result = self.result + x
        return self.result
    
    def reset(self):
        self.result = 0
```

---

## 📖 Referências

### Pseudocódigo Estruturado Clássico
- Baseado em padrões universitários
- Linguagem neutra e lógica
- Estrutura clara e direta

### DSLs de Ação
- **AppleScript**: Comandos naturais
- **Gherkin**: Estrutura Given/When/Then
- **Blockly Textual**: Blocos de código

---

## 🎯 Princípios de Design

1. **Simplicidade**: Padrões fáceis de entender
2. **Naturalidade**: Frases que parecem conversa
3. **Lógica**: Estrutura clara e direta
4. **Consistência**: Padrões seguem regras claras
5. **Extensibilidade**: Fácil adicionar novos padrões

---

**Mython** - Dicionário de Padrões Completo 🐍✨


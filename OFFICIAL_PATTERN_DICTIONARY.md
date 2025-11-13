# Dicionário Oficial de Padrões Mython

## 🎯 Baseado em Fontes Reais (Inglês)

Este dicionário é baseado em padrões reais em **inglês**:
1. **Pseudocódigo Estruturado Clássico** (usado em universidades - inglês)
2. **AppleScript** (DSL da Apple - inglês)
3. **Gherkin** (BDD - inglês)
4. **Blockly Textual** (programação visual - inglês)

---

## 📚 FONTE 1: Pseudocódigo Estruturado Clássico (Universidades)

### Padrões Fundamentais

#### 1. Atribuição
**Padrão Clássico:**
```
SET variável TO valor
```

**Mython:**
```logic
set variável = valor
```

**Python:**
```python
variável = valor
```

#### 2. Entrada de Dados
**Padrão Clássico:**
```
INPUT variável
READ variável
```

**Mython:**
```logic
ask variável "prompt"
ask number variável "prompt"
```

**Python:**
```python
variável = input("prompt")
variável = int(input("prompt"))
```

#### 3. Saída de Dados
**Padrão Clássico:**
```
OUTPUT valor
PRINT valor
WRITE valor
DISPLAY valor
```

**Mython:**
```logic
say valor
```

**Python:**
```python
print(valor)
```

#### 4. Estrutura Condicional
**Padrão Clássico:**
```
IF condição THEN
    instruções
ELSE
    instruções
END IF
```

**Mython:**
```logic
if condição:
    instruções
else:
    instruções
```

**Python:**
```python
if condição:
    instruções
else:
    instruções
```

#### 5. Estrutura de Repetição - FOR
**Padrão Clássico:**
```
FOR contador FROM início TO fim DO
    instruções
END FOR

FOR EACH item IN lista DO
    instruções
END FOR
```

**Mython:**
```logic
repeat N times:
    instruções

for each item in lista:
    instruções
```

**Python:**
```python
for _ in range(N):
    instruções

for item in lista:
    instruções
```

#### 6. Estrutura de Repetição - WHILE
**Padrão Clássico:**
```
WHILE condição DO
    instruções
END WHILE

REPEAT
    instruções
UNTIL condição
```

**Mython:**
```logic
while condição:
    instruções

repeat until condição:
    instruções
```

**Python:**
```python
while condição:
    instruções

while not condição:
    instruções
```

#### 7. Função/Procedimento
**Padrão Clássico:**
```
FUNCTION nome(parâmetros)
    instruções
    RETURN valor
END FUNCTION

PROCEDURE nome(parâmetros)
    instruções
END PROCEDURE
```

**Mython:**
```logic
define nome(parâmetros):
    instruções
    return valor
```

**Python:**
```python
def nome(parâmetros):
    instruções
    return valor
```

#### 8. Operadores de Comparação
**Padrão Clássico:**
```
= (igual)
≠ (diferente)
> (maior)
< (menor)
≥ (maior ou igual)
≤ (menor ou igual)
```

**Mython:**
```logic
is (igual)
is not (diferente)
is over (maior)
is under (menor)
is at least (maior ou igual)
is at most (menor ou igual)
```

**Python:**
```python
==
!=
>
<
>=
<=
```

---

## 📚 FONTE 2: AppleScript (DSL de Ação)

### Padrões AppleScript

#### 1. Comandos Naturais
**AppleScript:**
```
say "hello"
open file "notes.txt"
repeat 5 times
    say "hi"
end repeat
```

**Mython:**
```logic
say "hello"
open "notes.txt" as file
repeat 5 times:
    say "hi"
```

**Python:**
```python
print("hello")
with open("notes.txt") as file:
    pass
for _ in range(5):
    print("hi")
```

#### 2. Estruturas Naturais
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

---

## 📚 FONTE 3: Gherkin (BDD - Behavior Driven Development)

### Padrões Gherkin

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

#### 2. Cenários
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

---

## 📚 FONTE 4: Blockly Textual

### Padrões Blockly

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

#### 2. Estruturas de Controle
**Blockly:**
```
if condition then
    do this
else
    do that

repeat until condition
    do something
```

**Mython:**
```logic
if condition:
    do this
else:
    do that

repeat until condition:
    do something
```

**Python:**
```python
if condition:
    do_this()
else:
    do_that()

while not condition:
    do_something()
```

---

## 📋 Dicionário Completo de Padrões

### Ações Básicas

| Padrão Clássico | AppleScript | Mython | Python |
|-----------------|-------------|--------|--------|
| `OUTPUT x` | `say x` | `say x` | `print(x)` |
| `INPUT x` | `get x` | `ask x "prompt"` | `x = input("prompt")` |
| `SET x TO y` | `set x to y` | `set x = y` | `x = y` |

### Condições

| Padrão Clássico | AppleScript | Mython | Python |
|-----------------|-------------|--------|--------|
| `IF x THEN` | `if x then` | `if x:` | `if x:` |
| `ELSE` | `else` | `else:` | `else:` |
| `x = y` | `x is y` | `x is y` | `x == y` |
| `x ≠ y` | `x is not y` | `x is not y` | `x != y` |
| `x > y` | `x is greater than y` | `x is over y` | `x > y` |
| `x < y` | `x is less than y` | `x is under y` | `x < y` |
| `x ≥ y` | `x is greater than or equal to y` | `x is at least y` | `x >= y` |
| `x ≤ y` | `x is less than or equal to y` | `x is at most y` | `x <= y` |

### Repetições

| Padrão Clássico | AppleScript | Blockly | Mython | Python |
|-----------------|-------------|---------|--------|--------|
| `FOR i FROM 1 TO N` | `repeat N times` | `repeat N times` | `repeat N times:` | `for _ in range(N):` |
| `FOR EACH x IN list` | `repeat with x in list` | `for each x in list` | `for each x in list:` | `for x in list:` |
| `WHILE cond DO` | `repeat while cond` | `while cond` | `while cond:` | `while cond:` |
| `REPEAT ... UNTIL cond` | `repeat until cond` | `repeat until cond` | `repeat until cond:` | `while not cond:` |

### Funções

| Padrão Clássico | Blockly | Mython | Python |
|-----------------|---------|--------|--------|
| `FUNCTION nome()` | `function nome()` | `define nome():` | `def nome():` |
| `RETURN x` | `return x` | `return x` | `return x` |

### Listas

| Padrão Clássico | AppleScript | Mython | Python |
|-----------------|-------------|--------|--------|
| `list[1..N]` | `list {1, 2, 3}` | `list x = [...]` | `x = [...]` |
| `ADD x TO list` | `set end of list to x` | `add x to list` | `list.append(x)` |
| `REMOVE x FROM list` | `remove x from list` | `remove x from list` | `list.remove(x)` |

---

## 🎯 Padrões Combinados (Exemplos Reais)

### Exemplo 1: Algoritmo Clássico

**Pseudocódigo Estruturado:**
```
ALGORITMO Media
VAR
    n1, n2, media: REAL
INÍCIO
    ESCREVA("Digite a primeira nota: ")
    LEIA(n1)
    ESCREVA("Digite a segunda nota: ")
    LEIA(n2)
    media <- (n1 + n2) / 2
    ESCREVA("A média é: ", media)
FIM
```

**Mython:**
```logic
ask number n1 "Digite a primeira nota: "
ask number n2 "Digite a segunda nota: "
set media = (n1 + n2) / 2
say "A média é: " + str(media)
```

**Python:**
```python
n1 = int(input("Digite a primeira nota: "))
n2 = int(input("Digite a segunda nota: "))
media = (n1 + n2) / 2
print("A média é: " + str(media))
```

### Exemplo 2: Loop com Condição

**Pseudocódigo Estruturado:**
```
PARA i DE 1 ATÉ 10 FAÇA
    SE i MOD 2 = 0 ENTÃO
        ESCREVA(i)
    FIMSE
FIMPARA
```

**Mython:**
```logic
repeat 10 times:
    set i = i + 1
    if i % 2 is 0:
        say i
```

**Python:**
```python
for i in range(1, 11):
    if i % 2 == 0:
        print(i)
```

---

## 📖 Referências Oficiais

### Pseudocódigo Estruturado
- Padrões clássicos de universidades (inglês)
- Baseado em livros de algoritmos
- Sintaxe neutra e lógica

### AppleScript
- DSL da Apple
- Comandos naturais
- Automação de tarefas

### Gherkin
- BDD (Behavior Driven Development)
- Estrutura Given/When/Then
- Testes e especificações

### Blockly
- Programação visual
- Blocos de código
- Educação

---

## 🎯 Resumo

**Mython combina os melhores padrões em inglês de:**
- ✅ Pseudocódigo Estruturado Clássico (universidades)
- ✅ AppleScript (DSL da Apple)
- ✅ Gherkin (BDD)
- ✅ Blockly Textual (programação visual)

**Resultado:** Linguagem simples, natural e poderosa - **100% em inglês A2/B1**.

---

**Mython** - Dicionário Oficial de Padrões 🐍✨


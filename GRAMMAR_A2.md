# Gramática Mython A2/B1 - Oficial

## 🎯 Princípio

Toda sintaxe do Mython usa **inglês A2/B1** - o nível mais básico de inglês.

---

## 📝 Estruturas Básicas

### 1. Ações (Verbos Simples)

| Mython | Significado | Python |
|--------|-------------|--------|
| `say X` | Dizer/Mostrar | `print(X)` |
| `ask X "text"` | Perguntar | `X = input("text")` |
| `ask number X "text"` | Perguntar número | `X = int(input("text"))` |
| `set X = Y` | Guardar/Definir | `X = Y` |

### 2. Condições (Palavras Simples)

| Mython | Significado | Python |
|--------|-------------|--------|
| `if X is Y` | Se X é igual a Y | `if X == Y:` |
| `if X is not Y` | Se X não é Y | `if X != Y:` |
| `if X is over Y` | Se X é maior que Y | `if X > Y:` |
| `if X is under Y` | Se X é menor que Y | `if X < Y:` |
| `if X is at least Y` | Se X é pelo menos Y | `if X >= Y:` |
| `if X is at most Y` | Se X é no máximo Y | `if X <= Y:` |
| `else` | Senão | `else:` |

### 3. Repetições (Palavras Simples)

| Mython | Significado | Python |
|--------|-------------|--------|
| `repeat N times:` | Repetir N vezes | `for _ in range(N):` |
| `for each X in Y:` | Para cada X em Y | `for X in Y:` |
| `while X:` | Enquanto X | `while X:` |

### 4. Listas (Palavras Simples)

| Mython | Significado | Python |
|--------|-------------|--------|
| `list X = [...]` | Lista X com itens | `X = [...]` |
| `add Y to X` | Adicionar Y a X | `X.append(Y)` |
| `remove Y from X` | Remover Y de X | `X.remove(Y)` |

### 5. Funções (Palavras Simples)

| Mython | Significado | Python |
|--------|-------------|--------|
| `define name(args):` | Definir função | `def name(args):` |
| `return X` | Retornar X | `return X` |

### 6. Arquivos (Frases Simples)

| Mython | Significado | Python |
|--------|-------------|--------|
| `read file "path" as X` | Ler arquivo como X | `with open("path") as f: X = f.read()` |
| `save text X to file "path"` | Salvar texto X em arquivo | `with open("path", "w") as f: f.write(str(X))` |
| `open "path" as X:` | Abrir arquivo como X | `with open("path") as X:` |

### 7. Utilitários (Frases Simples)

| Mython | Significado | Python |
|--------|-------------|--------|
| `wait N seconds` | Aguardar N segundos | `time.sleep(N)` |
| `random number from A to B` | Número aleatório de A a B | `random.randint(A, B)` |

---

## 🎨 Regras de Gramática A2/B1

### 1. Palavras Comuns

Use apenas palavras que uma pessoa com inglês básico conhece:

- ✅ `say` (dizer)
- ✅ `ask` (perguntar)
- ✅ `if` (se)
- ✅ `else` (senão)
- ✅ `repeat` (repetir)
- ✅ `for each` (para cada)
- ✅ `add` (adicionar)
- ✅ `remove` (remover)
- ✅ `list` (lista)
- ✅ `set` (definir/guardar)
- ✅ `read` (ler)
- ✅ `save` (salvar)
- ✅ `open` (abrir)
- ✅ `wait` (aguardar)

### 2. Frases Simples

Construa frases como se estivesse falando:

- ✅ `say "hello"` (diga "olá")
- ✅ `ask name "your name"` (pergunte nome "seu nome")
- ✅ `if age is over 18` (se idade é maior que 18)
- ✅ `add "item" to list` (adicione "item" à lista)
- ✅ `read file "a.txt" as data` (leia arquivo "a.txt" como dados)

### 3. Sem Símbolos Técnicos

Evite símbolos que não são palavras:

- ❌ `()` (use palavras)
- ❌ `{}` (use palavras)
- ❌ `[]` (use palavras quando possível)
- ❌ `;` (não precisa)
- ❌ `@` (use palavras)
- ❌ `#` (ok para comentários)

### 4. Ordem Natural

A ordem das palavras deve ser natural:

- ✅ `say "hello"` (verbo + objeto)
- ✅ `ask name "question"` (verbo + variável + pergunta)
- ✅ `if age is over 18` (se + condição)
- ✅ `add item to list` (verbo + objeto + preposição + destino)

---

## 📚 Vocabulário A2/B1 Permitido

### Verbos (Ações)
- say, ask, set, add, remove, read, save, open, wait, repeat, return

### Substantivos (Coisas)
- file, text, number, list, name, age, item, data, result

### Adjetivos (Descrições)
- over, under, at least, at most, random

### Conjunções (Ligações)
- if, else, and, or, not

### Preposições (Relações)
- to, from, in, as, with

### Palavras Especiais
- each, times, seconds

---

## 🚫 O que NÃO Usar

### Palavras Técnicas
- ❌ `def`, `class`, `import`, `try`, `except`, `async`, `await`
- ❌ `function`, `method`, `variable`, `parameter`
- ❌ `iterator`, `generator`, `decorator`

### Símbolos Complexos
- ❌ `@`, `*`, `**`, `//`, `%`
- ❌ `lambda`, `yield`, `raise`

### Conceitos Avançados
- ❌ Herança, polimorfismo, encapsulamento
- ❌ Threading, multiprocessing
- ❌ Metaclasses, descriptors

---

## ✅ Exemplos de Gramática Correta

### ✅ BOM (A2/B1)
```logic
say "Hello"
ask name "What is your name?"
if age is over 18:
    say "adult"
else:
    say "minor"
```

### ❌ EVITAR (Muito Técnico)
```logic
def greet():
    print("Hello")
    
class Person:
    def __init__(self):
        pass
```

---

## 🎯 Resumo

**Gramática Mython = Inglês A2/B1 + Lógica Básica**

- Use palavras simples
- Use frases naturais
- Evite símbolos técnicos
- Evite conceitos avançados
- Mantenha simples

---

**Mython** - Gramática simples, poder completo. 🐍✨


# 📘 Mython Grammar Specification v1.0

**Status:** ✅ **ESTÁVEL** - Conflitos Reduce/Reduce resolvidos  
**Data:** 2025-01-27  
**Parser:** Lark LALR com Python-style indentation

---

## 📋 Índice

1. [Estrutura Geral](#estrutura-geral)
2. [Regras Base](#regras-base)
3. [Statements](#statements)
4. [Expressões](#expressões)
5. [Literais](#literais)
6. [Terminais](#terminais)
7. [Indentação](#indentação)
8. [Precedência de Operadores](#precedência-de-operadores)

---

## 1. Estrutura Geral

### 1.1 Ponto de Entrada

```lark
?start: statement+
```

O programa Mython é uma sequência de um ou mais `statement`.

**Importante:** O último `statement` pode não ter `_NEWLINE` final.

---

## 2. Regras Base

### 2.1 Statement

```lark
?statement: simple_stmt _NEWLINE?
         | compound_stmt
```

**Definição:**
- `simple_stmt`: Statement simples que não abre blocos
- `compound_stmt`: Statement composto que abre blocos indentados
- `_NEWLINE?`: Opcional - permite último statement sem newline final

**Regra Crítica:** `_NEWLINE` está no nível de `statement`, NÃO no nível de `simple_stmt`. Isso permite que blocos INDENT/DEDENT funcionem corretamente com o indenter.

---

### 2.2 Block Statement

```lark
?block_stmt: simple_stmt _NEWLINE?
           | compound_stmt
```

**Uso:** Usado DENTRO de blocos indentados (if, while, for, etc.).

**Importante:** `_NEWLINE` é opcional porque o último statement pode ser seguido diretamente por `DEDENT`.

---

## 3. Statements

### 3.1 Simple Statements

#### 3.1.1 Saída

```lark
say_stmt: SAY expr
```

**Exemplo:**
```mython
say "Hello, World!"
say nome
say idade + 1
```

**Python gerado:**
```python
print("Hello, World!")
print(nome)
print(idade + 1)
```

---

#### 3.1.2 Entrada

```lark
ask_stmt: ASK ask_type NAME STRING?
        | ASK ask_type NAME
        | ASK NAME STRING?
        | ASK NAME

ask_type: NUMBER_TYPE -> number
        | TEXT_TYPE -> text
```

**Exemplo:**
```mython
ask number idade "Digite sua idade: "
ask nome "Digite seu nome: "
```

**Python gerado:**
```python
idade = int(input("Digite sua idade: "))
nome = input("Digite seu nome: ")
```

---

#### 3.1.3 Atribuições

```lark
assign_stmt: NAME "=" expr
set_assign_stmt: SET NAME "=" expr
augmented_assignment_stmt: NAME ("+=" | "-=" | "*=" | "/=" | "//=" | "%=" | "**=") expr
```

**Exemplo:**
```mython
idade = 25
set nome = "Marcelo"
contador += 1
```

**Python gerado:**
```python
idade = 25
nome = "Marcelo"
contador += 1
```

**Importante:** `set_assign_stmt` usa terminal `SET` (não literal `"set"`) para garantir precedência sobre `NAME`.

---

#### 3.1.4 Estruturas de Dados

```lark
list_stmt: ("list" | "create" "list" | "make" "list") NAME "=" list_literal
dict_stmt: ("dict" | "dictionary" | "create" "dict" | "make" "dict") NAME "=" dict_literal
tuple_stmt: ("tuple" | "create" "tuple" | "make" "tuple") NAME "=" tuple_literal
set_stmt: ("create" "set" | "make" "set") NAME "=" set_literal
```

**Exemplo:**
```mython
list items = [1, 2, 3]
dict data = {"name": "Mython", "age": 25}
tuple coords = (10, 20)
make set numbers = {1, 2, 3}
```

---

#### 3.1.5 Chamada de Função

```lark
call_stmt: (NAME | attribute_access) "(" args? ")"
```

**Exemplo:**
```mython
requests.post("https://api.example.com", data={"key": "value"})
```

**Importante:** Usa `NAME` ou `attribute_access` diretamente para evitar conflito com `function_call` em `atom`.

---

#### 3.1.6 Imports

```lark
use_stmt: ("use" | "import" | "load" | "require" | "include") NAME ("as" NAME)?
from_import_stmt: "from" NAME ("import" | "load" | "require") NAME ("as" NAME)?
```

**Exemplo:**
```mython
use requests
use json as j
from math import pi
```

---

### 3.2 Compound Statements

#### 3.2.1 Condicionais

```lark
if_stmt: IF condition ":" _NEWLINE INDENT block_stmt+ DEDENT else_block?
else_block: _NEWLINE* ELSE ":" _NEWLINE INDENT block_stmt+ DEDENT
```

**Exemplo:**
```mython
if idade > 18:
    say "Adulto"
else:
    say "Menor"
```

**Importante:** `else_block` aceita `_NEWLINE*` antes de `ELSE` porque o indenter SEMPRE injeta `_NEWLINE` após `DEDENT`.

---

#### 3.2.2 Loops

```lark
while_stmt: WHILE condition ":" _NEWLINE INDENT block_stmt+ DEDENT
for_each_stmt: FOR NAME IN expr ":" _NEWLINE INDENT block_stmt+ DEDENT
repeat_stmt: REPEAT NUMBER ":" _NEWLINE INDENT block_stmt+ DEDENT
```

**Exemplo:**
```mython
while idade < 18:
    say idade
    idade = idade + 1

for item in lista:
    say item

repeat 5:
    say "Hello"
```

---

#### 3.2.3 Funções

```lark
function_def: (DEF | FUNC) NAME "(" params? ")" ":" _NEWLINE INDENT block_stmt+ DEDENT
async_function_def: "async" DEF NAME "(" params? ")" ":" _NEWLINE INDENT block_stmt+ DEDENT
return_stmt: RETURN expr?
```

**Exemplo:**
```mython
func soma(a, b):
    return a + b

async def buscar_dados():
    return await fetch()
```

---

#### 3.2.4 Classes

```lark
class_def: ("class" | "create" "class" | "make" "class" | "define" "class") NAME ("(" inheritance ")")? ":" _NEWLINE INDENT block_stmt+ DEDENT
```

---

## 4. Expressões

### 4.1 Hierarquia de Expressões

```lark
?expr: sum
     | dict_literal

?sum: product
    | sum "+" product  -> add
    | sum "-" product  -> sub

?product: atom
        | product "*" atom  -> mul
        | product "/" atom  -> div
        | product "//" atom -> floordiv
        | product "%" atom  -> mod
        | product "**" atom -> pow
```

**Precedência (da mais baixa para a mais alta):**
1. `+`, `-` (adição, subtração)
2. `*`, `/`, `//`, `%`, `**` (multiplicação, divisão, floor div, módulo, potência)
3. `atom` (átomos: NAME, NUMBER, STRING, literais, etc.)

**Importante:** `dict_literal` está diretamente em `expr` para resolver ambiguidades e permitir uso em argumentos de função.

---

### 4.2 Condições

```lark
?condition: logical_or

?logical_or: logical_and
           | logical_or OR logical_and -> or_expr

?logical_and: logical_not
            | logical_and AND logical_not -> and_expr

?logical_not: comparison
           | atom
           | NOT comparison -> not_expr
           | NOT atom -> not_expr

comparison: atom comparison_op atom
```

**Precedência lógica (da mais baixa para a mais alta):**
1. `or`
2. `and`
3. `not`
4. Comparações (`>`, `<`, `>=`, `<=`, `==`, `!=`)

---

### 4.3 Átomo

```lark
?atom: NAME | NUMBER | STRING
     | "(" expr ")"  -> paren_expr
     | function_call
     | attribute_access
     | subscription
     | list_literal
```

**Importante:** 
- `dict_literal` NÃO está em `atom` - está diretamente em `expr` para evitar conflitos
- `set_literal` NÃO está em `atom` - causa conflito com `set_stmt`
- `tuple_literal` NÃO está em `atom` - conflito resolvido pela regra `tuple_literal` com vírgula final

---

## 5. Literais

### 5.1 Lista

```lark
list_literal: "[" (expr ("," expr)*)? "]"
```

**Exemplo:**
```mython
[1, 2, 3]
["a", "b", "c"]
[]
```

---

### 5.2 Dicionário

```lark
dict_literal: "{" [pair ("," pair)*] "}"
pair: STRING ":" expr
```

**Exemplo:**
```mython
{"name": "Mython", "age": 25}
{}
```

**Resolução de Ambiguidade:** `dict_literal` usa `pair (STRING ":" expr)`, então SEMPRE tem `:`. Isso distingue de `set_literal` que NUNCA tem `:`.

---

### 5.3 Tupla

```lark
tuple_literal: "(" [expr ("," expr)* ","] ")"
```

**Exemplo:**
```mython
(10, 20)
(10,)
()
```

**Resolução de Ambiguidade:** `tuple_literal` SEMPRE termina com vírgula ou tem múltiplos itens. `paren_expr` é `(expr)` SEM vírgula. Isso resolve completamente a ambiguidade:
- `(x)` = expressão com parênteses
- `(x,)` = tupla com 1 elemento

---

### 5.4 Set

```lark
set_literal: "{" expr ("," expr)* "}"
```

**Exemplo:**
```mython
{1, 2, 3}
{1}
```

**Importante:** 
- Requer pelo menos 1 item (sem vírgula final)
- `{}` vazio não é `set_literal` - é `dict_literal` vazio (padrão Python)
- NÃO está em `atom` para evitar conflito com `set_stmt`

---

## 6. Terminais

### 6.1 Ordem de Precedência

**CRÍTICO:** A ordem dos terminais importa MUITO no Lark. Palavras-chave específicas DEVEM estar ANTES de `NAME`.

**Ordem correta:**
1. Tipos específicos (`NUMBER_TYPE`, `TEXT_TYPE`)
2. Palavras-chave principais (`ASK`, `SAY`, `IF`, `ELSE`, etc.)
3. Operadores (`AND`, `OR`, `NOT`, etc.)
4. `NAME` (captura o que sobrou)

---

### 6.2 Palavras-chave

```lark
NUMBER_TYPE: "number"
TEXT_TYPE: "text"
ASK: "ask"
SAY: "say"
IF: "if"
ELSE: "else"
WHILE: "while"
FOR: "for"
IN: "in"
DEF: "def"
FUNC: "func"
CLASS: "class"
RETURN: "return"
BREAK: "break"
CONTINUE: "continue"
PASS: "pass"
REPEAT: "repeat"
UNTIL: "until"
AND: "and"
OR: "or"
NOT: "not"
SET: "set"
```

---

### 6.3 Tipos Básicos

```lark
NAME: /[a-zA-Z_][a-zA-Z0-9_]*/
NUMBER: /\d+(\.\d+)?/
STRING: /"[^"]*"|'[^']*'/
FSTRING: /f"[^"]*"|f'[^']*'/
RSTRING: /r"[^"]*"|r'[^']*'/
BSTRING: /b"[^"]*"|b'[^']*'/
```

---

## 7. Indentação

### 7.1 Sistema de Indentação

Mython usa **indentação estilo Python** com `INDENT` e `DEDENT` tokens gerados pelo `MythonIndenter`.

```lark
_NEWLINE: /(\r?\n[ \t]*)+/
%ignore /[ \t]+/
```

**Importante:** Espaços/tabs são ignorados, mas `_NEWLINE` captura newline + espaços/tabs seguintes (indentação).

---

### 7.2 Blocos Indentados

Todos os blocos indentados seguem o mesmo padrão:

```lark
stmt: KEYWORD ":" _NEWLINE INDENT block_stmt+ DEDENT
```

**Fluxo:**
1. Palavra-chave (`if`, `while`, `for`, etc.)
2. `:` seguido de `_NEWLINE`
3. `INDENT` (gerado pelo indenter)
4. Um ou mais `block_stmt`
5. `DEDENT` (gerado pelo indenter)
6. `_NEWLINE` opcional (sempre injetado pelo indenter após `DEDENT`)

---

## 8. Precedência de Operadores

### 8.1 Aritméticos (da mais baixa para a mais alta)

1. `+`, `-` (adição, subtração)
2. `*`, `/`, `//`, `%` (multiplicação, divisão, floor div, módulo)
3. `**` (potência)

---

### 8.2 Comparação

Todos os operadores de comparação têm a mesma precedência:

```lark
comparison_op: GREATER | LESS | GREATER_EQUAL | LESS_EQUAL | EQUALS | NOT_EQUAL
```

---

### 8.3 Lógicos (da mais baixa para a mais alta)

1. `or`
2. `and`
3. `not`

---

## 9. Resolução de Conflitos

### 9.1 Conflitos Resolvidos

1. **`dict_literal` vs `set_literal`**: `dict_literal` usa `pair (STRING ":" expr)` - sempre tem `:`. `set_literal` nunca tem `:`.

2. **`tuple_literal` vs `paren_expr`**: `tuple_literal` sempre termina com vírgula ou tem múltiplos itens. `paren_expr` é `(expr)` sem vírgula.

3. **`set_stmt` vs `set_literal` em `atom`**: `set_literal` não está em `atom` para evitar conflito.

4. **`_NEWLINE` obrigatório vs opcional**: `_NEWLINE` opcional em `statement` permite último statement sem newline final.

---

## 10. Notas de Implementação

### 10.1 Parser

- **Tipo:** LALR (Lark)
- **Indenter:** `MythonIndenter` (baseado em `lark.indenter.Indenter`)
- **Tab length:** 4 espaços

---

### 10.2 Transformações

- Todas as transformações são feitas pelo `MythonTransformer`
- O transformer converte AST Mython → código Python
- `Tree` objects são recursivamente transformados em strings

---

## 11. Exemplos Completos

### 11.1 Programa Simples

```mython
ask number idade "Digite sua idade: "

if idade > 18:
    say "Você é adulto"
else:
    say "Você é menor"

say "Fim do programa"
```

**Python gerado:**
```python
idade = int(input("Digite sua idade: "))

if idade > 18:
    print("Você é adulto")
else:
    print("Você é menor")

print("Fim do programa")
```

---

### 11.2 Programa com Funções

```mython
func soma(a, b):
    return a + b

resultado = soma(2, 3)
say resultado
```

**Python gerado:**
```python
def soma(a, b):
    return a + b

resultado = soma(2, 3)
print(resultado)
```

---

### 11.3 Programa com Estruturas de Dados

```mython
list items = [1, 2, 3]
dict data = {"name": "Mython", "age": 25}

for item in items:
    say item

say data["name"]
```

**Python gerado:**
```python
items = [1, 2, 3]
data = {"name": "Mython", "age": 25}

for item in items:
    print(item)

print(data["name"])
```

---

## 12. Referências

- **Lark Documentation:** https://lark-parser.readthedocs.io/
- **Python Grammar:** https://docs.python.org/3/reference/grammar.html
- **Mython Indenter:** `mython/indenter.py`

---

**Última atualização:** 2025-01-27  
**Versão:** 1.0  
**Status:** ✅ Estável - Pronto para expansão


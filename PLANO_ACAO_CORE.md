# 🎯 Plano de Ação - Mython Core (1-2 semanas)

## 📊 Status Atual Detalhado

### ✅ O que JÁ FUNCIONA (40%)

#### Estrutura e Parsing
- ✅ Sistema de indentação (INDENT/DEDENT) funcionando
- ✅ `_NEWLINE` processado corretamente
- ✅ Blocos indentados funcionando
- ✅ `else_block` funcionando corretamente
- ✅ Parser Lark configurado corretamente
- ✅ Transformer básico funcionando

#### Statements Implementados
- ✅ `ask_stmt` - Entrada de dados
- ✅ `say_stmt` - Saída de dados
- ✅ `if_stmt` - Condicionais
- ✅ `else_block` - Bloco else
- ✅ `elif_stmt` - Estrutura criada (gramática)

#### Expressões Implementadas
- ✅ Expressões simples (atom)
- ✅ Comparações básicas (`>`, `<`, `==`, `>=`, `<=`, `!=`)
- ✅ Nomes de variáveis (NAME)
- ✅ Números (NUMBER)
- ✅ Strings (STRING)

---

## ⬜ O que FALTA Implementar (60%)

### 🔥 Prioridade CRÍTICA (Fazer PRIMEIRO)

#### 1. Atribuição (`assign_stmt`)
**Status:** Gramática existe, transformer precisa implementar

**Gramática atual:**
```lark
assign_stmt: "set" NAME "=" expr
           | NAME "=" expr
```

**Tarefas:**
- [ ] Implementar `assign_stmt` no transformer
- [ ] Testar atribuição simples: `set x = 10`
- [ ] Testar atribuição direta: `x = 10`
- [ ] Testar atribuição múltipla: `set a, b = 1, 2`
- [ ] Testar atribuição aumentada: `set x += 1`

**Tempo estimado:** 2-4 horas

#### 2. Operadores Aritméticos
**Status:** Gramática existe parcialmente, transformer precisa implementar

**Gramática atual:**
```lark
?expr: atom
     | function_call
     | attribute_access
     | subscription
```

**Tarefas:**
- [ ] Expandir gramática para incluir operadores aritméticos
- [ ] Implementar precedência de operadores
- [ ] Implementar no transformer
- [ ] Testar: `x = 1 + 2 * 3`
- [ ] Testar: `x = (1 + 2) * 3`

**Tempo estimado:** 4-6 horas

#### 3. Operadores Booleanos
**Status:** Gramática existe parcialmente, transformer precisa implementar

**Gramática atual:**
```lark
?condition: comparison
          | atom
```

**Tarefas:**
- [ ] Expandir gramática para incluir operadores booleanos
- [ ] Implementar precedência de operadores booleanos
- [ ] Implementar no transformer
- [ ] Testar: `if x > 5 and y < 10:`
- [ ] Testar: `if x > 5 or y < 10:`
- [ ] Testar: `if not x > 5:`

**Tempo estimado:** 2-4 horas

#### 4. Loops (`while_stmt` e `for_each_stmt`)
**Status:** Gramática existe, transformer precisa implementar

**Gramática atual:**
```lark
while_stmt: "while" condition ":" _NEWLINE INDENT block_stmt+ DEDENT
for_each_stmt: "for" NAME "in" expr ":" _NEWLINE INDENT block_stmt+ DEDENT
```

**Tarefas:**
- [ ] Implementar `while_stmt` no transformer
- [ ] Implementar `for_each_stmt` no transformer
- [ ] Implementar `break_stmt` e `continue_stmt`
- [ ] Testar loops simples
- [ ] Testar loops aninhados
- [ ] Testar `break` e `continue`

**Tempo estimado:** 4-6 horas

#### 5. Chamadas de Função
**Status:** Gramática existe, transformer precisa implementar

**Gramática atual:**
```lark
function_call: NAME "(" args? ")"
args: expr ("," expr)*
```

**Tarefas:**
- [ ] Implementar `function_call` no transformer
- [ ] Implementar `args` no transformer
- [ ] Testar chamadas simples: `say("hello")`
- [ ] Testar chamadas com múltiplos argumentos: `f(x, y, z)`
- [ ] Testar chamadas aninhadas: `f(g(x))`

**Tempo estimado:** 2-4 horas

---

### ⚡ Prioridade ALTA (Fazer DEPOIS dos críticos)

#### 6. Funções (`function_def`)
**Status:** Gramática existe, transformer precisa implementar

**Gramática atual:**
```lark
function_def: "def" NAME "(" params? ")" ":" _NEWLINE INDENT block_stmt+ DEDENT
params: NAME ("," NAME)*
```

**Tarefas:**
- [ ] Implementar `function_def` no transformer
- [ ] Implementar `params` no transformer
- [ ] Implementar `return_stmt` no transformer
- [ ] Testar funções simples
- [ ] Testar funções com parâmetros
- [ ] Testar funções com return
- [ ] Testar funções aninhadas

**Tempo estimado:** 4-6 horas

#### 7. Listas e Dicionários
**Status:** Gramática existe, transformer precisa implementar

**Gramática atual:**
```lark
list_stmt: ("list" | "create" "list" | "make" "list") NAME "=" list_literal
dict_stmt: ("dict" | "dictionary" | "create" "dict" | "make" "dict") NAME "=" dict_literal
list_literal: "[" (expr ("," expr)*)? "]"
dict_literal: "{" (expr ":" expr ("," expr ":" expr)*)? "}"
```

**Tarefas:**
- [ ] Implementar `list_stmt` no transformer
- [ ] Implementar `dict_stmt` no transformer
- [ ] Implementar acesso por índice: `lista[0]`
- [ ] Implementar acesso por chave: `dict["key"]`
- [ ] Testar listas e dicionários
- [ ] Testar métodos básicos (`append`, `remove`, etc.)

**Tempo estimado:** 4-6 horas

#### 8. Imports
**Status:** Gramática existe, transformer precisa implementar

**Gramática atual:**
```lark
use_stmt: ("use" | "import" | "load" | "require" | "include") NAME ("as" NAME)?
from_import_stmt: "from" NAME ("import" | "load" | "require") NAME ("as" NAME)?
```

**Tarefas:**
- [ ] Implementar `use_stmt` no transformer
- [ ] Implementar `from_import_stmt` no transformer
- [ ] Testar imports simples: `use math`
- [ ] Testar imports com alias: `use math as m`
- [ ] Testar from imports: `from math import sqrt`

**Tempo estimado:** 2-4 horas

#### 9. Strings Completas
**Status:** Gramática existe, transformer precisa melhorar

**Gramática atual:**
```lark
STRING: /"[^"]*"|'[^']*'/
FSTRING: /f"[^"]*"|f'[^']*'/
```

**Tarefas:**
- [ ] Implementar escapes em strings (`\n`, `\t`, `\"`, etc.)
- [ ] Implementar strings multilinha
- [ ] Implementar f-strings básicas
- [ ] Testar strings com escapes
- [ ] Testar strings multilinha
- [ ] Testar f-strings

**Tempo estimado:** 2-4 horas

---

### 📝 Prioridade MÉDIA (Fazer DEPOIS dos altos)

#### 10. Blocos Aninhados
**Status:** Funciona basicamente, precisa testar casos extremos

**Tarefas:**
- [ ] Testar `if` dentro de `if`
- [ ] Testar `if` dentro de `while`
- [ ] Testar `if` dentro de `for`
- [ ] Testar `while` dentro de `if`
- [ ] Testar `for` dentro de `if`
- [ ] Testar aninhamento profundo (3+ níveis)

**Tempo estimado:** 2-4 horas

---

## 🚀 Plano de Execução - Semana 1

### Dia 1: Atribuição e Operadores (8 horas)

#### Manhã (4 horas)
- [ ] Implementar `assign_stmt` no transformer
- [ ] Testar atribuição simples
- [ ] Testar atribuição múltipla
- [ ] Testar atribuição aumentada

#### Tarde (4 horas)
- [ ] Expandir gramática para operadores aritméticos
- [ ] Implementar precedência de operadores
- [ ] Implementar no transformer
- [ ] Testar operadores aritméticos

### Dia 2: Operadores Booleanos e Chamadas de Função (8 horas)

#### Manhã (4 horas)
- [ ] Expandir gramática para operadores booleanos
- [ ] Implementar precedência de operadores booleanos
- [ ] Implementar no transformer
- [ ] Testar operadores booleanos

#### Tarde (4 horas)
- [ ] Implementar `function_call` no transformer
- [ ] Implementar `args` no transformer
- [ ] Testar chamadas de função
- [ ] Testar chamadas aninhadas

### Dia 3-4: Loops (16 horas)

#### Dia 3 (8 horas)
- [ ] Implementar `while_stmt` no transformer
- [ ] Implementar `break_stmt` e `continue_stmt`
- [ ] Testar loops `while` simples
- [ ] Testar loops `while` aninhados
- [ ] Testar `break` e `continue`

#### Dia 4 (8 horas)
- [ ] Implementar `for_each_stmt` no transformer
- [ ] Testar loops `for` simples
- [ ] Testar loops `for` aninhados
- [ ] Testar `break` e `continue` em loops `for`

### Dia 5: Estruturas de Dados (8 horas)

#### Manhã (4 horas)
- [ ] Implementar `list_stmt` no transformer
- [ ] Implementar acesso por índice
- [ ] Testar listas

#### Tarde (4 horas)
- [ ] Implementar `dict_stmt` no transformer
- [ ] Implementar acesso por chave
- [ ] Testar dicionários

---

## 🚀 Plano de Execução - Semana 2

### Dia 6-7: Funções (16 horas)

#### Dia 6 (8 horas)
- [ ] Implementar `function_def` no transformer
- [ ] Implementar `params` no transformer
- [ ] Testar funções simples
- [ ] Testar funções com parâmetros

#### Dia 7 (8 horas)
- [ ] Implementar `return_stmt` no transformer
- [ ] Testar funções com return
- [ ] Testar funções aninhadas
- [ ] Testar chamadas de função

### Dia 8: Imports (8 horas)

#### Manhã (4 horas)
- [ ] Implementar `use_stmt` no transformer
- [ ] Testar imports simples

#### Tarde (4 horas)
- [ ] Implementar `from_import_stmt` no transformer
- [ ] Testar from imports
- [ ] Testar imports com alias

### Dia 9-10: Strings e Testes Finais (16 horas)

#### Dia 9 (8 horas)
- [ ] Implementar escapes em strings
- [ ] Implementar strings multilinha
- [ ] Implementar f-strings básicas
- [ ] Testar strings completas

#### Dia 10 (8 horas)
- [ ] Testar blocos aninhados
- [ ] Testar casos extremos
- [ ] Documentação completa
- [ ] Testes finais

---

## 📊 Métricas de Progresso

### Semana 1
- **Dia 1:** Atribuição e operadores aritméticos (20%)
- **Dia 2:** Operadores booleanos e chamadas de função (30%)
- **Dia 3:** Loops `while` (40%)
- **Dia 4:** Loops `for` (50%)
- **Dia 5:** Estruturas de dados (60%)

### Semana 2
- **Dia 6:** Funções básicas (70%)
- **Dia 7:** Funções avançadas (80%)
- **Dia 8:** Imports (90%)
- **Dia 9:** Strings (95%)
- **Dia 10:** Testes finais (100%)

---

## 🎯 Objetivos Finais

### Mython Core 100% Funcional
- ✅ Atribuição completa
- ✅ Operadores aritméticos e booleanos
- ✅ Loops (`while` e `for`)
- ✅ Chamadas de função
- ✅ Funções (`def`)
- ✅ Listas e dicionários
- ✅ Imports básicos
- ✅ Strings completas
- ✅ Blocos aninhados

### Testes Completos
- ✅ Testes unitários para cada feature
- ✅ Testes de integração
- ✅ Testes de casos extremos
- ✅ Testes de performance

### Documentação Completa
- ✅ Documentação de cada feature
- ✅ Exemplos de uso
- ✅ Guia de referência rápida
- ✅ Tutorial completo

---

## 🚀 Próximos Passos Imediatos

1. **Implementar `assign_stmt` no transformer** (2-4 horas)
2. **Expandir gramática para operadores aritméticos** (4-6 horas)
3. **Implementar operadores booleanos** (2-4 horas)
4. **Implementar loops** (4-6 horas)
5. **Implementar chamadas de função** (2-4 horas)

**Tempo total estimado:** 16-26 horas (2-3 dias úteis)

---

**Mython Core - 100% funcional em 1-2 semanas!** 🐍✨


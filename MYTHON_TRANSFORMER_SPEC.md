# 📘 Mython Transformer Specification v1.0

**Status:** ✅ **ESTÁVEL** - Fluxo de transformação estabelecido  
**Data:** 2025-01-27  
**Transformer:** `MythonTransformer` (Lark)

---

## 📋 Índice

1. [Visão Geral](#visão-geral)
2. [Arquitetura](#arquitetura)
3. [Fluxo de Transformação](#fluxo-de-transformação)
4. [Métodos Principais](#métodos-principais)
5. [Propagação de Valores](#propagação-de-valores)
6. [Indentação](#indentação)
7. [Imports Automáticos](#imports-automáticos)
8. [Exemplos](#exemplos)

---

## 1. Visão Geral

O `MythonTransformer` é responsável por converter a AST (Abstract Syntax Tree) gerada pelo Lark em código Python executável.

**Princípio Fundamental:** O Transformer **não chama `self.transform()` dentro dos métodos**. O Lark já fez a transformação recursiva dos filhos antes de chamar o método.

---

## 2. Arquitetura

### 2.1 Estrutura da Classe

```python
class MythonTransformer(Transformer):
    def __init__(self, source_code: str = None):
        super().__init__()
        self.indent_level = 0
        self.in_class = False
        self.source_code = source_code
        self.needs_imports = {
            'time': False,
            'random': False,
            'asyncio': False,
            'os': False,
            'datetime': False,
            'sys': False,
        }
```

**Estado Interno:**
- `indent_level`: Nível de indentação atual (0 = raiz)
- `in_class`: Flag indicando se está dentro de uma classe
- `source_code`: Código fonte original (opcional, para debug)
- `needs_imports`: Dicionário de imports necessários (adicionados automaticamente)

---

### 2.2 Método `indent()`

```python
def indent(self) -> str:
    """Retorna a indentação atual (4 espaços por nível)."""
    return "    " * self.indent_level
```

**Uso:** Todos os métodos que geram código indentado usam `self.indent()`.

---

## 3. Fluxo de Transformação

### 3.1 Processo Completo

```
Código Mython → Lark Parser → AST → Transformer → Código Python
```

### 3.2 Ordem de Transformação

1. **Lark processa a árvore recursivamente** de baixo para cima
2. **Cada nó é transformado** antes de passar para o pai
3. **O Transformer recebe filhos já transformados** (strings ou Tree)
4. **O método do Transformer junta os filhos** em código Python

**Regra Crítica:** NUNCA chame `self.transform()` dentro dos métodos do Transformer. O Lark já fez isso.

---

## 4. Métodos Principais

### 4.1 Entry Point: `start()`

```python
def start(self, statements: List[Any]) -> str:
    """
    start: statement+
    
    Junta todos os statements em código Python completo.
    Adiciona imports necessários no topo.
    """
```

**Comportamento:**
1. Verifica `needs_imports` e adiciona imports no topo
2. Processa cada statement (já transformado em string)
3. Junta tudo com quebras de linha
4. Retorna código Python completo

**Exemplo:**
```python
# Input AST:
Tree('start', [Tree('statement', [...]), Tree('statement', [...])])

# Output Python:
"""
import time

idade = 25
print(idade)
"""
```

---

### 4.2 Simple Statements: `simple_stmt()`

```python
def simple_stmt(self, children: List[Any]) -> str:
    """
    simple_stmt: say_stmt | ask_stmt | assign_stmt | ...
    
    Apenas retorna o resultado do filho (já transformado).
    Filtra tokens _NEWLINE se presentes.
    """
```

**Comportamento:**
1. Filtra tokens `_NEWLINE` (se presentes)
2. Retorna o primeiro child (já transformado em string)
3. Não chama `self.transform()` - o Lark já fez

**Exemplo:**
```python
# Input: Tree('simple_stmt', ['idade = 25', Token('_NEWLINE', '\n')])
# Output: 'idade = 25'
```

---

### 4.3 Compound Statements: `if_stmt()`

```python
def if_stmt(self, children: List[Any]) -> str:
    """
    if_stmt: IF condition ":" _NEWLINE INDENT block_stmt+ DEDENT else_block?
    
    Monta estrutura if/else completa com indentação correta.
    """
```

**Comportamento:**
1. Extrai `condition` (já transformado)
2. Extrai `block_stmt+` (lista de statements já transformados)
3. Extrai `else_block?` (opcional, já transformado)
4. Monta código Python com indentação correta

**Exemplo:**
```python
# Input AST:
Tree('if_stmt', [
    'idade > 18',  # condition
    'print("Adulto")',  # block_stmt[0]
    Token('INDENT'),
    Token('DEDENT'),
    'else:\n    print("Menor")'  # else_block
])

# Output Python:
"""
if idade > 18:
    print("Adulto")
else:
    print("Menor")
"""
```

---

### 4.4 Block Statements: `block_stmt()`

```python
def block_stmt(self, children: List[Any]) -> str:
    """
    block_stmt: simple_stmt _NEWLINE? | compound_stmt
    
    Indenta o conteúdo do bloco com 4 espaços.
    """
```

**Comportamento:**
1. Recebe statement já transformado (string)
2. Aplica indentação de 4 espaços a cada linha
3. Retorna código indentado

**Exemplo:**
```python
# Input: 'print("Hello")'
# Output (dentro de if): '    print("Hello")'
```

---

### 4.5 Expressões: `_expr()`

```python
def _expr(self, node: Any) -> str:
    """
    Helper para processar expressões (recursivamente se necessário).
    """
```

**Comportamento:**
1. Se é string, retorna como está
2. Se é Tree, transforma recursivamente (apenas neste caso específico)
3. Se é Token, retorna o valor

**Uso:** Métodos auxiliares que precisam processar expressões podem usar `_expr()`.

---

## 5. Propagação de Valores

### 5.1 Princípio

**Valores são propagados de baixo para cima na árvore:**

1. Tokens (`Token`) → Strings
2. Átomos (`atom`) → Strings
3. Expressões (`expr`) → Strings
4. Statements (`statement`) → Strings
5. Root (`start`) → Código Python completo

---

### 5.2 Exemplo Completo

```
Tree('start', [
    Tree('statement', [
        Tree('simple_stmt', [
            Tree('assign_stmt', [
                Token('NAME', 'idade'),
                Token('EQUAL', '='),
                Token('NUMBER', '25')
            ]),
            Token('_NEWLINE', '\n')
        ])
    ])
])
```

**Transformação passo a passo:**

1. `assign_stmt(['idade', '=', '25'])` → `'idade = 25'`
2. `simple_stmt(['idade = 25', '\n'])` → `'idade = 25'`
3. `statement(['idade = 25'])` → `'idade = 25'`
4. `start(['idade = 25'])` → `'idade = 25\n'`

---

## 6. Indentação

### 6.1 Sistema de Indentação

**Regra:** Cada nível de bloco adiciona 4 espaços.

**Métodos que gerenciam indentação:**

1. `block_stmt()`: Aplica indentação ao conteúdo do bloco
2. `if_stmt()`: Não aplica indentação (usa `block_stmt` para isso)
3. `else_block()`: Retorna `'else:'` sem indentação (o conteúdo usa `block_stmt`)

---

### 6.2 Exemplo de Indentação

```python
# Mython:
if idade > 18:
    say "Adulto"
    if idade > 21:
        say "Pode beber"

# Transformação:
# 1. if_stmt: monta estrutura, não indenta
# 2. block_stmt[0]: '    print("Adulto")'
# 3. block_stmt[1]: if_stmt aninhado
#    - block_stmt: '        print("Pode beber")'
```

---

## 7. Imports Automáticos

### 7.1 Sistema de Imports

O Transformer detecta automaticamente quando imports são necessários:

```python
self.needs_imports = {
    'time': False,
    'random': False,
    'asyncio': False,
    'os': False,
    'datetime': False,
    'sys': False,
}
```

**Exemplos:**

- `wait_stmt`: Ativa `needs_imports['time'] = True`
- `random_stmt`: Ativa `needs_imports['random'] = True`
- `async_function_def`: Ativa `needs_imports['asyncio'] = True`

---

### 7.2 Adição de Imports

Imports são adicionados no método `start()`:

```python
imports = []
if self.needs_imports['time']:
    imports.append("import time")
# ...

if imports:
    lines.extend(imports)
    lines.append("")
```

---

## 8. Exemplos

### 8.1 Exemplo Simples

**Mython:**
```mython
idade = 25
say idade
```

**Transformação:**
1. `assign_stmt(['idade', '=', '25'])` → `'idade = 25'`
2. `say_stmt(['idade'])` → `'print(idade)'`
3. `start(['idade = 25', 'print(idade)'])` → `'idade = 25\nprint(idade)\n'`

---

### 8.2 Exemplo com If/Else

**Mython:**
```mython
if idade > 18:
    say "Adulto"
else:
    say "Menor"
```

**Transformação:**
1. `condition` → `'idade > 18'`
2. `block_stmt(['print("Adulto")'])` → `'    print("Adulto")'`
3. `else_block(['print("Menor")'])` → `'else:\n    print("Menor")'`
4. `if_stmt(...)` → Monta estrutura completa

---

### 8.3 Exemplo com Função

**Mython:**
```mython
func soma(a, b):
    return a + b
```

**Transformação:**
1. `params(['a', 'b'])` → `'a, b'`
2. `return_stmt(['a + b'])` → `'return a + b'`
3. `block_stmt(['return a + b'])` → `'    return a + b'`
4. `function_def(...)` → Monta função completa

---

## 9. Métodos por Categoria

### 9.1 Statements Simples

- `say_stmt()`: `say expr` → `print(expr)`
- `ask_stmt()`: `ask number name` → `name = int(input())`
- `assign_stmt()`: `name = expr` → `name = expr`
- `set_assign_stmt()`: `set name = expr` → `name = expr`
- `call_stmt()`: `func(args)` → `func(args)`
- `use_stmt()`: `use module` → `import module`

---

### 9.2 Statements Compostos

- `if_stmt()`: `if condition: ... else: ...` → `if condition: ... else: ...`
- `while_stmt()`: `while condition: ...` → `while condition: ...`
- `for_each_stmt()`: `for item in expr: ...` → `for item in expr: ...`
- `function_def()`: `func name(params): ...` → `def name(params): ...`
- `class_def()`: `class Name: ...` → `class Name: ...`

---

### 9.3 Expressões

- `add()`: `a + b` → `a + b`
- `sub()`: `a - b` → `a - b`
- `mul()`: `a * b` → `a * b`
- `div()`: `a / b` → `a / b`
- `comparison()`: `a > b` → `a > b`
- `or_expr()`: `a or b` → `a or b`
- `and_expr()`: `a and b` → `a and b`
- `not_expr()`: `not a` → `not a`

---

### 9.4 Literais

- `list_literal()`: `[1, 2, 3]` → `[1, 2, 3]`
- `dict_literal()`: `{"key": value}` → `{"key": value}`
- `tuple_literal()`: `(1, 2)` → `(1, 2,)` (com vírgula final)
- `set_literal()`: `{1, 2, 3}` → `{1, 2, 3}`

---

## 10. Tratamento de Erros

### 10.1 Tokens Ignorados

Alguns tokens são filtrados automaticamente:

- `_NEWLINE`: Filtrado em `simple_stmt()` e outros métodos
- `INDENT`, `DEDENT`: Processados mas não geram código
- Tokens vazios: Ignorados

---

### 10.2 Fallbacks

Se um método não encontra o padrão esperado:

1. Tenta converter para string
2. Retorna string vazia se falhar
3. Loga aviso (em desenvolvimento)

---

## 11. Boas Práticas

### 11.1 ❌ NÃO FAZER

```python
def assign_stmt(self, children):
    # ERRADO: Chamar self.transform() dentro do método
    result = self.transform(children[0])
    return f"{result} = {children[1]}"
```

---

### 11.2 ✅ FAZER

```python
def assign_stmt(self, children):
    # CORRETO: children já estão transformados
    name = str(children[0])
    value = self._expr(children[1])  # Helper para expressões
    return f"{name} = {value}"
```

---

## 12. Referências

- **Lark Transformer:** https://lark-parser.readthedocs.io/en/latest/classes.html#lark.Transformer
- **Mython Grammar:** `MYTHON_GRAMMAR_SPEC.md`
- **Transformer Code:** `mython/transformer_lark.py`

---

**Última atualização:** 2025-01-27  
**Versão:** 1.0  
**Status:** ✅ Estável - Pronto para expansão


# 🚀 Tarefas Imediatas - Mython Core

## 📊 Status Atual Detalhado

### ✅ Gramática JÁ TEM (mas transformer precisa implementar)

1. **`assign_stmt`** ✅ Gramática existe
   - `assign_stmt: NAME "=" expr`
   - ⬜ Transformer não implementado

2. **`augmented_assignment_stmt`** ✅ Gramática existe
   - `augmented_assignment_stmt: NAME ("+=" | "-=" | "*=" | "/=" | "//=" | "%=" | "**=") expr`
   - ⬜ Transformer não implementado

3. **`while_stmt`** ✅ Gramática existe
   - `while_stmt: "while" condition ":" _NEWLINE INDENT block_stmt+ DEDENT`
   - ⬜ Transformer não implementado

4. **`for_each_stmt`** ✅ Gramática existe
   - `for_each_stmt: "for" NAME "in" expr ":" _NEWLINE INDENT block_stmt+ DEDENT`
   - ⬜ Transformer não implementado

5. **`function_def`** ✅ Gramática existe
   - `function_def: "def" NAME "(" params? ")" ":" _NEWLINE INDENT block_stmt+ DEDENT`
   - ⬜ Transformer não implementado

6. **`return_stmt`** ✅ Gramática existe
   - `return_stmt: "return" expr?`
   - ⬜ Transformer não implementado

7. **`break_stmt`** ✅ Gramática existe
   - `break_stmt: "break"`
   - ⬜ Transformer não implementado

8. **`continue_stmt`** ✅ Gramática existe
   - `continue_stmt: "continue"`
   - ⬜ Transformer não implementado

9. **`pass_stmt`** ✅ Gramática existe
   - `pass_stmt: "pass"`
   - ⬜ Transformer não implementado

10. **`list_stmt`** ✅ Gramática existe
    - `list_stmt: ("list" | "create" "list" | "make" "list") NAME "=" list_literal`
    - ⬜ Transformer não implementado

11. **`dict_stmt`** ✅ Gramática existe
    - `dict_stmt: ("dict" | "dictionary" | "create" "dict" | "make" "dict") NAME "=" dict_literal`
    - ⬜ Transformer não implementado

12. **`use_stmt`** ✅ Gramática existe
    - `use_stmt: ("use" | "import" | "load" | "require" | "include") NAME ("as" NAME)?`
    - ⬜ Transformer não implementado

13. **`from_import_stmt`** ✅ Gramática existe
    - `from_import_stmt: "from" NAME ("import" | "load" | "require") NAME ("as" NAME)?`
    - ⬜ Transformer não implementado

---

## 🔥 Tarefas Críticas (Implementar AGORA)

### 1. Implementar `assign_stmt` no transformer

**Gramática:**
```lark
assign_stmt: NAME "=" expr
```

**Transformer necessário:**
```python
def assign_stmt(self, args: List[Any]) -> str:
    """name = value"""
    var_name = args[0].value if isinstance(args[0], Token) else str(args[0])
    value = self._expr(args[2])
    return self.indent() + f"{var_name} = {value}"
```

**Teste:**
```mython
set x = 10
x = 20
```

**Tempo estimado:** 1-2 horas

---

### 2. Implementar `augmented_assignment_stmt` no transformer

**Gramática:**
```lark
augmented_assignment_stmt: NAME ("+=" | "-=" | "*=" | "/=" | "//=" | "%=" | "**=") expr
```

**Transformer necessário:**
```python
def augmented_assignment_stmt(self, args: List[Any]) -> str:
    """name += value"""
    var_name = args[0].value if isinstance(args[0], Token) else str(args[0])
    op = args[1].value if isinstance(args[1], Token) else str(args[1])
    value = self._expr(args[2])
    return self.indent() + f"{var_name} {op} {value}"
```

**Teste:**
```mython
set x = 10
x += 5
```

**Tempo estimado:** 1 hora

---

### 3. Implementar `while_stmt` no transformer

**Gramática:**
```lark
while_stmt: "while" condition ":" _NEWLINE INDENT block_stmt+ DEDENT
```

**Transformer necessário:**
```python
def while_stmt(self, args: List[Any]) -> str:
    """while condition:"""
    # Similar a if_stmt
    condition = self._expr(args[0])
    
    # Processar blocos (args[1:] contém _NEWLINE, INDENT, block_stmt+, DEDENT)
    statements = []
    for arg in args[1:]:
        if hasattr(arg, 'type') and arg.type == 'INDENT':
            self.indent_level += 1
        elif hasattr(arg, 'type') and arg.type == 'DEDENT':
            self.indent_level -= 1
        elif hasattr(arg, 'type') and arg.type in ['_NEWLINE']:
            continue
        elif isinstance(arg, Tree):
            transformed = self.transform(arg)
            if transformed and isinstance(transformed, str):
                statements.append(transformed)
    
    block = self.block(statements) if statements else ""
    result = self.indent() + f"while {condition}:"
    if block:
        result += "\n" + block
    
    return result
```

**Teste:**
```mython
set x = 0
while x < 10:
    say x
    set x += 1
```

**Tempo estimado:** 2-3 horas

---

### 4. Implementar `for_each_stmt` no transformer

**Gramática:**
```lark
for_each_stmt: "for" NAME "in" expr ":" _NEWLINE INDENT block_stmt+ DEDENT
```

**Transformer necessário:**
```python
def for_each_stmt(self, args: List[Any]) -> str:
    """for name in expr:"""
    # Similar a while_stmt
    var_name = args[0].value if isinstance(args[0], Token) else str(args[0])
    iterable = self._expr(args[2])
    
    # Processar blocos (args[3:] contém _NEWLINE, INDENT, block_stmt+, DEDENT)
    statements = []
    for arg in args[3:]:
        if hasattr(arg, 'type') and arg.type == 'INDENT':
            self.indent_level += 1
        elif hasattr(arg, 'type') and arg.type == 'DEDENT':
            self.indent_level -= 1
        elif hasattr(arg, 'type') and arg.type in ['_NEWLINE']:
            continue
        elif isinstance(arg, Tree):
            transformed = self.transform(arg)
            if transformed and isinstance(transformed, str):
                statements.append(transformed)
    
    block = self.block(statements) if statements else ""
    result = self.indent() + f"for {var_name} in {iterable}:"
    if block:
        result += "\n" + block
    
    return result
```

**Teste:**
```mython
for x in [1, 2, 3]:
    say x
```

**Tempo estimado:** 2-3 horas

---

### 5. Implementar `break_stmt`, `continue_stmt`, `pass_stmt` no transformer

**Gramática:**
```lark
break_stmt: "break"
continue_stmt: "continue"
pass_stmt: "pass"
```

**Transformer necessário:**
```python
def break_stmt(self, args: List[Any]) -> str:
    """break"""
    return self.indent() + "break"

def continue_stmt(self, args: List[Any]) -> str:
    """continue"""
    return self.indent() + "continue"

def pass_stmt(self, args: List[Any]) -> str:
    """pass"""
    return self.indent() + "pass"
```

**Teste:**
```mython
while True:
    break
    continue
    pass
```

**Tempo estimado:** 30 minutos

---

### 6. Implementar `return_stmt` no transformer

**Gramática:**
```lark
return_stmt: "return" expr?
```

**Transformer necessário:**
```python
def return_stmt(self, args: List[Any]) -> str:
    """return expr?"""
    if not args:
        return self.indent() + "return"
    value = self._expr(args[0])
    return self.indent() + f"return {value}"
```

**Teste:**
```mython
def func():
    return 10
    return
```

**Tempo estimado:** 30 minutos

---

### 7. Expandir gramática para operadores aritméticos

**Gramática atual (simplificada):**
```lark
?expr: atom
     | function_call
     | attribute_access
     | subscription
```

**Gramática necessária:**
```lark
?expr: term (("+" | "-") term)*
?term: factor (("*" | "/" | "//" | "%" | "**") factor)*
?factor: atom | "(" expr ")" | function_call | attribute_access | subscription
```

**Transformer necessário:**
```python
def expr(self, args: List[Any]) -> str:
    """Processa expressões com operadores aritméticos"""
    # Implementar precedência
    if len(args) == 1:
        return self._expr(args[0])
    
    # Processar termos e operadores
    result = self._expr(args[0])
    i = 1
    while i < len(args):
        if isinstance(args[i], Token):
            op = args[i].value
            if i + 1 < len(args):
                right = self._expr(args[i + 1])
                result = f"({result} {op} {right})"
                i += 2
            else:
                i += 1
        else:
            i += 1
    
    return result
```

**Teste:**
```mython
set x = 1 + 2 * 3
set y = (1 + 2) * 3
```

**Tempo estimado:** 4-6 horas

---

### 8. Expandir gramática para operadores booleanos

**Gramática atual (simplificada):**
```lark
?condition: comparison
          | atom
```

**Gramática necessária:**
```lark
?condition: comparison (("and" | "or") comparison)*
          | "not" comparison
          | comparison
          | atom
```

**Transformer necessário:**
```python
def condition(self, args: List[Any]) -> str:
    """Processa condições com operadores booleanos"""
    # Similar a expr, mas com and/or/not
    pass
```

**Teste:**
```mython
if x > 5 and y < 10:
    say "ok"
```

**Tempo estimado:** 2-4 horas

---

### 9. Implementar `function_call` no transformer

**Gramática:**
```lark
function_call: NAME "(" args? ")"
args: expr ("," expr)*
```

**Transformer necessário:**
```python
def function_call(self, args: List[Any]) -> str:
    """name(args)"""
    func_name = args[0].value if isinstance(args[0], Token) else str(args[0])
    if len(args) > 1:
        # Processar argumentos
        arg_list = []
        for arg in args[1:]:
            if isinstance(arg, Tree) and arg.data == 'args':
                arg_list.extend([self._expr(a) for a in arg.children])
            else:
                arg_list.append(self._expr(arg))
        return f"{func_name}({', '.join(arg_list)})"
    return f"{func_name}()"
```

**Teste:**
```mython
say "hello"
set x = len([1, 2, 3])
```

**Tempo estimado:** 2-4 horas

---

### 10. Implementar `function_def` no transformer

**Gramática:**
```lark
function_def: "def" NAME "(" params? ")" ":" _NEWLINE INDENT block_stmt+ DEDENT
params: NAME ("," NAME)*
```

**Transformer necessário:**
```python
def function_def(self, args: List[Any]) -> str:
    """def name(params):"""
    func_name = args[0].value if isinstance(args[0], Token) else str(args[0])
    
    # Processar parâmetros (args[1] = params?)
    params_str = ""
    if len(args) > 1 and isinstance(args[1], Tree) and args[1].data == 'params':
        params = [p.value if isinstance(p, Token) else str(p) for p in args[1].children]
        params_str = ", ".join(params)
    
    # Processar blocos (args[2:] contém ":", _NEWLINE, INDENT, block_stmt+, DEDENT)
    statements = []
    for arg in args[2:]:
        if hasattr(arg, 'type') and arg.type == 'INDENT':
            self.indent_level += 1
        elif hasattr(arg, 'type') and arg.type == 'DEDENT':
            self.indent_level -= 1
        elif hasattr(arg, 'type') and arg.type in ['_NEWLINE']:
            continue
        elif isinstance(arg, Tree):
            transformed = self.transform(arg)
            if transformed and isinstance(transformed, str):
                statements.append(transformed)
    
    block = self.block(statements) if statements else ""
    result = self.indent() + f"def {func_name}({params_str}):"
    if block:
        result += "\n" + block
    
    return result
```

**Teste:**
```mython
def func():
    say "hello"

def func2(x, y):
    return x + y
```

**Tempo estimado:** 3-4 horas

---

## 📊 Resumo das Tarefas

### Tarefas Críticas (16-26 horas)
1. `assign_stmt` - 1-2 horas
2. `augmented_assignment_stmt` - 1 hora
3. `while_stmt` - 2-3 horas
4. `for_each_stmt` - 2-3 horas
5. `break_stmt`, `continue_stmt`, `pass_stmt` - 30 minutos
6. `return_stmt` - 30 minutos
7. Operadores aritméticos - 4-6 horas
8. Operadores booleanos - 2-4 horas
9. `function_call` - 2-4 horas
10. `function_def` - 3-4 horas

### Tarefas Secundárias (10-16 horas)
11. `list_stmt` - 2-3 horas
12. `dict_stmt` - 2-3 horas
13. `use_stmt` - 1-2 horas
14. `from_import_stmt` - 1-2 horas
15. Strings completas - 2-4 horas
16. Blocos aninhados - 2-4 horas

**Tempo total estimado:** 26-42 horas (3-5 dias úteis)

---

## 🎯 Plano de Execução

### Dia 1: Atribuição e Operadores (8 horas)
- [ ] Implementar `assign_stmt`
- [ ] Implementar `augmented_assignment_stmt`
- [ ] Expandir gramática para operadores aritméticos
- [ ] Implementar operadores aritméticos no transformer
- [ ] Expandir gramática para operadores booleanos
- [ ] Implementar operadores booleanos no transformer

### Dia 2: Loops (8 horas)
- [ ] Implementar `while_stmt`
- [ ] Implementar `for_each_stmt`
- [ ] Implementar `break_stmt`, `continue_stmt`, `pass_stmt`
- [ ] Testar loops simples e aninhados

### Dia 3: Funções (8 horas)
- [ ] Implementar `function_call`
- [ ] Implementar `function_def`
- [ ] Implementar `return_stmt`
- [ ] Testar funções simples e aninhadas

### Dia 4: Estruturas de Dados (8 horas)
- [ ] Implementar `list_stmt`
- [ ] Implementar `dict_stmt`
- [ ] Testar listas e dicionários

### Dia 5: Imports e Strings (8 horas)
- [ ] Implementar `use_stmt`
- [ ] Implementar `from_import_stmt`
- [ ] Implementar strings completas
- [ ] Testes finais

---

**Mython Core - 100% funcional em 5 dias!** 🐍✨


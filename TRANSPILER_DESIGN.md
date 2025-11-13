# Design do Transpiler Mython

## 🎯 Objetivo

Traduzir código Mython (lógica simples) para Python (código avançado).

---

## 🏗️ Arquitetura

### Componentes Principais

1. **Lexer** - Análise lexical (identifica tokens)
2. **Parser** - Análise sintática (reconhece estruturas)
3. **Semantic Analyzer** - Análise semântica (dependências)
4. **Code Generator** - Geração de código Python
5. **Optimizer** - Otimizações e imports

---

## 📋 Padrões de Reconhecimento

### 1. Padrões Simples (A2)

| Padrão | Regex/Detecção | Ação |
|--------|----------------|------|
| `say X` | `^say\s+(.+)$` | `print(X)` |
| `ask X "text"` | `^ask\s+(\w+)\s+"(.+)"$` | `X = input("text")` |
| `ask number X "text"` | `^ask number\s+(\w+)\s+"(.+)"$` | `X = int(input("text"))` |
| `if X is over Y` | `if\s+(.+)\s+is over\s+(.+):` | `if X > Y:` |
| `repeat N times:` | `^repeat\s+(\d+)\s+times:$` | `for _ in range(N):` |
| `for each X in Y:` | `^for each\s+(\w+)\s+in\s+(.+):$` | `for X in Y:` |
| `add X to Y` | `^add\s+(.+)\s+to\s+(\w+)$` | `Y.append(X)` |
| `remove X from Y` | `^remove\s+(.+)\s+from\s+(\w+)$` | `Y.remove(X)` |

### 2. Padrões Avançados (B1)

| Padrão | Detecção | Ação |
|--------|----------|------|
| `class X:` | `^class\s+(\w+):$` | `class X:` |
| `init(...):` | `^init\((.+)\):$` | `def __init__(self, ...):` |
| `task X(...):` | `^task\s+(\w+)\((.+)\):$` | `def X(self, ...):` |
| `async task X` | `^async task\s+(.+)$` | `async def X` |
| `await X` | `^await\s+(.+)$` | `await X` |
| `attempt:` | `^attempt:$` | `try:` |
| `catch X:` | `^catch\s+(.+):$` | `except X:` |
| `retry N times:` | `^retry\s+(\d+)\s+times:$` | Gera decorator `@retry(N)` |
| `use model "X" as Y` | `^use model\s+"(.+)"\s+as\s+(\w+)$` | Carrega modelo IA |

---

## 🔄 Fluxo de Processamento

### Passo 1: Análise Lexical

```
Input: "say 'Hello'"
Tokens: [COMMAND: say, STRING: 'Hello']
```

### Passo 2: Análise Sintática

```
Tokens → AST (Abstract Syntax Tree)
say 'Hello' → PrintStatement(value='Hello')
```

### Passo 3: Análise Semântica

```
Detecta dependências:
- Usa "say" → precisa de print (built-in)
- Usa "wait" → precisa de import time
- Usa "async" → precisa de import asyncio
```

### Passo 4: Geração de Código

```
AST → Python Code
PrintStatement('Hello') → print('Hello')
```

### Passo 5: Otimização

```
- Adiciona imports necessários
- Remove código redundante
- Otimiza estruturas quando possível
```

---

## 🧩 Exemplos de Tradução

### Exemplo 1: Comando Simples

**Input:**
```logic
say "Hello"
```

**Processamento:**
1. Lexer: `[COMMAND: say, STRING: "Hello"]`
2. Parser: `PrintStatement(value="Hello")`
3. Generator: `print("Hello")`

**Output:**
```python
print("Hello")
```

### Exemplo 2: Comando com Dependência

**Input:**
```logic
wait 3 seconds
```

**Processamento:**
1. Lexer: `[COMMAND: wait, NUMBER: 3, KEYWORD: seconds]`
2. Parser: `WaitStatement(seconds=3)`
3. Semantic: Detecta necessidade de `import time`
4. Generator: `time.sleep(3)`

**Output:**
```python
import time

time.sleep(3)
```

### Exemplo 3: Estrutura Complexa

**Input:**
```logic
class Person:
    init(name):
        set self.name = name
```

**Processamento:**
1. Lexer: `[CLASS: Person, INIT: init(name), SET: self.name = name]`
2. Parser: `ClassDefinition(name="Person", methods=[__init__(name), ...])`
3. Generator: Gera classe Python completa

**Output:**
```python
class Person:
    def __init__(self, name):
        self.name = name
```

---

## 🔧 Implementação

### Estrutura de Dados

```python
class ASTNode:
    """Nó da árvore sintática"""
    pass

class PrintStatement(ASTNode):
    value: str

class IfStatement(ASTNode):
    condition: Expression
    then_block: List[ASTNode]
    else_block: List[ASTNode]

class ClassDefinition(ASTNode):
    name: str
    methods: List[MethodDefinition]
```

### Algoritmo Principal

```python
def transpile(source_code: str) -> str:
    # 1. Análise lexical
    tokens = lexer.tokenize(source_code)
    
    # 2. Análise sintática
    ast = parser.parse(tokens)
    
    # 3. Análise semântica
    dependencies = semantic_analyzer.analyze(ast)
    
    # 4. Geração de código
    python_code = code_generator.generate(ast)
    
    # 5. Adicionar imports
    imports = dependency_resolver.resolve(dependencies)
    final_code = imports + "\n" + python_code
    
    return final_code
```

---

## 🎯 Otimizações

### 1. Detecção de Imports

```python
def detect_imports(ast):
    imports = []
    if uses_time(ast):
        imports.append("import time")
    if uses_random(ast):
        imports.append("import random")
    if uses_async(ast):
        imports.append("import asyncio")
    return imports
```

### 2. Otimização de Loops

```python
# Mython
for each x in data:
    add x * 2 to result

# Pode gerar (se configurado)
result = [x * 2 for x in data]
```

### 3. Simplificação de Expressões

```python
# Normaliza condições
"age is over 18" → "age > 18"
"name is not 'test'" → "name != 'test'"
```

---

## 🟥 Casos Especiais

### 1. Python Puro (Escape)

Se o transpiler não reconhece um padrão, copia como Python puro:

```logic
import numpy as np  # Não reconhecido → copiado exatamente
```

### 2. Mistura Mython + Python

```logic
say "Hello"  # Mython → traduzido
import math  # Python → copiado
say math.pi  # Mython → traduzido
```

### 3. Context Managers

```logic
open "file.txt" as f:
    set data = f.read()
```

Gera:
```python
with open("file.txt", "r", encoding="utf-8") as f:
    data = f.read()
```

---

## 🎯 Resumo

**Transpiler = Reconhece Padrões → Traduz → Gera Python**

- ✅ Reconhece padrões simples e avançados
- ✅ Traduz para Python equivalente
- ✅ Adiciona dependências automaticamente
- ✅ Gera código válido e funcional

---

**Mython Transpiler** - Design Completo 🐍✨


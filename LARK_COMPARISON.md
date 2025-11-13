# 🔄 O Que Mudaria com Lark

## Comparação Prática: Atual vs Lark

---

## 📊 Estrutura Atual (Regex/Substituição)

### Como Funciona Agora:
```python
def translate_line(line: str) -> str:
    stripped = line.strip()
    
    # Múltiplos if/elif para cada comando
    if stripped.startswith("say "):
        content = stripped[len("say "):]
        return f"print({content})"
    
    if stripped.startswith("ask "):
        parts = stripped.split(" ", 2)
        var_name = parts[1]
        question = parts[2]
        return f'{var_name} = input({question})'
    
    # ... 1000+ linhas de if/elif
```

**Características:**
- ✅ Processamento linha por linha
- ✅ Múltiplos `if/elif` para cada padrão
- ✅ Regex e substituições simples
- ✅ ~1000+ linhas de código
- ⚠️ Difícil de manter
- ⚠️ Erros genéricos

---

## 🎯 Estrutura com Lark (Parser Formal)

### Como Funcionaria:

#### 1. **Gramática EBNF** (`mython_grammar.lark`):
```lark
start: statement+

statement: say_stmt
         | ask_stmt
         | if_stmt
         | loop_stmt
         | function_def
         | class_def
         | assignment
         | python_escape

say_stmt: "say" expression
        | "print" expression
        | "show" expression
        | "display" expression
        | "tell" expression

ask_stmt: "ask" VAR prompt
        | "ask" "for" VAR prompt
        | "get" VAR prompt
        | "read" VAR prompt
        | "prompt" VAR prompt
        | "ask" "number" VAR prompt
        | "ask" "for" "number" VAR prompt

if_stmt: ("if" | "when" | "whenever") condition ":" block
       | "if" condition ":" block ("else" | "otherwise") ":" block
       | "if" condition ":" block ("elif" | "else" "if" | "or" "if") condition ":" block

loop_stmt: ("repeat" | "do" | "loop") NUMBER ("times" | "time") ":" block
         | ("for" "each" | "for" "every" | "loop" "through" | "iterate" "over") VAR "in" expression ":" block
         | ("while" | "as" "long" "as") condition ":"

function_def: ("define" | "function" | "to" | "create" "function") VAR "(" params? ")" ":"
            | "return" expression
            | "give" "back" expression
            | "send" "back" expression

class_def: ("class" | "create" "class" | "make" "class" | "define" "class") VAR ("(" inheritance ")")? ":"
         | ("init" | "constructor" | "initialize" | "create" | "setup") "(" params? ")" ":"
         | ("task" | "method" | "function" | "do" | "perform" | "execute") VAR "(" params? ")" ":"

assignment: ("set" | "assign" | "let" | "make" | "put" | "store" | "save" | "create" | "initialize") VAR "=" expression

condition: expression comparison expression
         | expression ("is" | "equals" | "equal" "to") expression
         | expression ("is" "not" | "not" "equal" "to") expression
         | expression ("is" "over" | "is" "greater" "than" | "is" "above" | "greater" "than") expression
         | expression ("is" "under" | "is" "less" "than" | "is" "below" | "less" "than") expression
         | expression ("is" "at" "least" | "is" "greater" "than" "or" "equal" "to") expression
         | expression ("is" "at" "most" | "is" "less" "than" "or" "equal" "to") expression

comparison: ">" | "<" | ">=" | "<=" | "==" | "!="

expression: term (("+" | "-") term)*
term: factor (("*" | "/" | "//" | "%") factor)*
factor: NUMBER | STRING | VAR | "(" expression ")" | function_call

function_call: VAR "(" args? ")"
args: expression ("," expression)*

block: statement+

prompt: STRING | expression

inheritance: VAR ("," VAR)*

params: VAR ("," VAR)*

python_escape: /.*/  // Qualquer coisa que não seja reconhecida

%import common.NUMBER
%import common.STRING
%import common.WS
%ignore WS
```

#### 2. **Transformer** (`mython_transformer.py`):
```python
from lark import Transformer, Token

class MythonTransformer(Transformer):
    def say_stmt(self, args):
        expr = args[0]
        return f"print({expr})"
    
    def ask_stmt(self, args):
        var_name = args[0].value
        prompt = args[1]
        return f'{var_name} = input({prompt})'
    
    def if_stmt(self, args):
        condition = args[0]
        block = args[1]
        return f"if {condition}:\n{block}"
    
    def condition(self, args):
        left = args[0]
        op = args[1]
        right = args[2]
        # Normalizar operadores
        op_map = {
            "is": "==",
            "is not": "!=",
            "is over": ">",
            "is under": "<",
            # ...
        }
        return f"{left} {op_map.get(op, op)} {right}"
    
    # ... métodos para cada regra
```

#### 3. **Transpiler Principal** (`transpiler_lark.py`):
```python
from lark import Lark
from mython_transformer import MythonTransformer

def transpile_file(input_path: str, output_path: str = None) -> str:
    # Carregar gramática
    with open("mython_grammar.lark") as f:
        grammar = f.read()
    
    # Criar parser
    parser = Lark(grammar, start='start', parser='lalr')
    
    # Ler arquivo
    with open(input_path) as f:
        code = f.read()
    
    # Parsear
    tree = parser.parse(code)
    
    # Transformar
    transformer = MythonTransformer()
    python_code = transformer.transform(tree)
    
    # Salvar
    if output_path:
        with open(output_path, 'w') as f:
            f.write(python_code)
    
    return python_code
```

---

## 🔄 Mudanças Práticas

### 1. **Estrutura de Arquivos**

**Atual:**
```
mython/
  ├── transpiler.py (1000+ linhas)
  ├── cli.py
  └── __init__.py
```

**Com Lark:**
```
mython/
  ├── grammar/
  │   └── mython_grammar.lark (gramática EBNF)
  ├── transformer.py (transformações)
  ├── transpiler.py (orquestração)
  ├── cli.py
  └── __init__.py
```

### 2. **Tamanho do Código**

**Atual:**
- `transpiler.py`: ~1090 linhas
- Tudo em um arquivo
- Muitos `if/elif`

**Com Lark:**
- `grammar.lark`: ~100-200 linhas (gramática)
- `transformer.py`: ~300-500 linhas (transformações)
- `transpiler.py`: ~50-100 linhas (orquestração)
- **Total: ~450-800 linhas** (mais organizado)

### 3. **Tratamento de Erros**

**Atual:**
```python
# Erro genérico
if not stripped.startswith("say "):
    # ... tenta outros padrões
    # Se não encontrar, copia como Python puro
    return indent + stripped  # Pode gerar erro de sintaxe
```

**Com Lark:**
```python
# Erro preciso
try:
    tree = parser.parse(code)
except UnexpectedToken as e:
    # Erro: linha 5, coluna 10
    # Esperado: "say", "ask", "if", ...
    # Encontrado: "sai"
    # Sugestão: Você quis dizer "say"?
    raise SyntaxError(f"Linha {e.line}, coluna {e.column}: {e.message}")
```

### 4. **Manutenibilidade**

**Atual:**
```python
# Adicionar novo comando = adicionar mais if/elif
if stripped.startswith("new_command "):
    # ... lógica
```

**Com Lark:**
```lark
# Adicionar novo comando = adicionar regra na gramática
new_command_stmt: "new_command" expression
```

### 5. **Testes**

**Atual:**
```python
# Testar cada padrão manualmente
def test_say():
    assert translate_line("say 'hello'") == "print('hello')"
```

**Com Lark:**
```python
# Testar gramática automaticamente
def test_grammar():
    parser = Lark(grammar)
    tree = parser.parse("say 'hello'")
    assert tree.data == 'say_stmt'
```

---

## 📊 Comparação de Exemplo

### Código Mython:
```logic
say "Hello, World!"
ask name "What is your name? "
if name is "Alice":
    say "Hello, Alice!"
else:
    say "Hello, " + name
```

### Processamento Atual:
```python
# Linha 1: say "Hello, World!"
if stripped.startswith("say "):
    content = stripped[len("say "):]  # "Hello, World!"
    return "print(Hello, World!)"  # ✅

# Linha 2: ask name "What is your name? "
if stripped.startswith("ask "):
    parts = stripped.split(" ", 2)  # ["ask", "name", '"What is your name? "']
    var_name = parts[1]  # "name"
    question = parts[2]  # '"What is your name? "'
    return 'name = input("What is your name? ")'  # ✅

# Linha 3: if name is "Alice":
if stripped.startswith("if ") and stripped.endswith(":"):
    condition = stripped[len("if "):-1]  # 'name is "Alice"'
    condition_py = normalize_condition(condition)  # 'name == "Alice"'
    return 'if name == "Alice":'  # ✅
```

### Processamento com Lark:
```python
# Parse completo do arquivo
tree = parser.parse(code)

# Árvore gerada:
# start
#   ├── say_stmt: "Hello, World!"
#   ├── ask_stmt: name, "What is your name? "
#   └── if_stmt
#       ├── condition: name == "Alice"
#       ├── block
#       │   └── say_stmt: "Hello, Alice!"
#       └── else_block
#           └── say_stmt: "Hello, " + name

# Transformação automática
python_code = transformer.transform(tree)
# Gera código Python completo e estruturado
```

---

## ✅ Vantagens Práticas do Lark

1. **Erros Precisos**
   ```
   Erro na linha 5, coluna 12:
   Esperado: "say", "ask", "if"
   Encontrado: "sai"
   Sugestão: Você quis dizer "say"?
   ```

2. **Gramática Visível**
   - Gramática em arquivo separado
   - Fácil de entender e modificar
   - Documentação automática

3. **AST Estruturada**
   - Árvore de parse clara
   - Fácil análise estática
   - Melhor para IDEs

4. **Testes Automáticos**
   - Testar gramática
   - Testar transformações
   - Cobertura completa

---

## ⚠️ Desvantagens Práticas

1. **Curva de Aprendizado**
   - Aprender EBNF
   - Entender Lark
   - Debugging de gramática

2. **Migração Completa**
   - Reescrever tudo
   - Testar tudo novamente
   - Possíveis regressões

3. **Complexidade Inicial**
   - Mais arquivos
   - Mais conceitos
   - Mais abstrações

---

## 🎯 Conclusão

### O Que Mudaria:

1. **Estrutura**: De 1 arquivo para 3-4 arquivos organizados
2. **Código**: De ~1090 linhas para ~450-800 linhas mais organizadas
3. **Erros**: De genéricos para precisos com linha/coluna
4. **Manutenção**: De difícil para fácil (gramática declarativa)
5. **Testes**: De manuais para automáticos
6. **Performance**: Similar ou melhor
7. **Dependências**: Adiciona Lark (mas é puro Python)

### Recomendação:

**Para o estado atual do Mython**: Manter o atual funciona bem.

**Para o futuro**: Lark seria uma evolução natural quando:
- Projeto crescer
- Precisar de recursos complexos
- Quiser melhor tratamento de erros
- Quiser gramática formal

---

**Resumo: Lark mudaria a estrutura, mas melhoraria robustez e manutenibilidade!** 🚀


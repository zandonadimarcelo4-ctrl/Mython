# Cobertura Mython → Python

## ✅ O que JÁ está implementado

### Básico
- ✅ `say` → `print()`
- ✅ `ask` → `input()`
- ✅ `ask number` → `int(input())`
- ✅ `set` → atribuição `=`
- ✅ Variáveis

### Condições
- ✅ `if/else/elif` → `if/else/elif`
- ✅ Comparações: `is`, `is not`, `is over`, `is under`, `is at least`, `is at most`
- ✅ Operadores lógicos (via Python puro)

### Loops
- ✅ `repeat N times` → `for _ in range(N)`
- ✅ `for each X in Y` → `for X in Y`
- ✅ `while` → `while`
- ✅ `repeat until` → `while not`
- ✅ `break`, `continue`, `pass`

### Listas
- ✅ `list X = [...]` → `X = [...]`
- ✅ `add X to Y` → `Y.append(X)`
- ✅ `remove X from Y` → `Y.remove(X)`

### Funções
- ✅ `define func(args):` → `def func(args):`
- ✅ `return` → `return`
- ✅ `task` → métodos (com `self` automático em classes)

### Classes
- ✅ `class Name:` → `class Name:`
- ✅ `init(args):` → `__init__(self, args)`
- ✅ `set self.attr = value` → `self.attr = value`
- ✅ `task method():` → `def method(self):`

### Async
- ✅ `async task func():` → `async def func():`
- ✅ `await` → `await`

### Exceções
- ✅ `attempt:` → `try:`
- ✅ `catch error:` → `except Exception as error:`
- ✅ `finally:` → `finally:`
- ✅ `raise` → `raise`

### Decorators
- ✅ `decorator name:` → `@name`

### Arquivos
- ✅ `open "file" as var:` → `with open("file") as var:`
- ✅ `read file "path" as var` → `with open("path") as f: var = f.read()`
- ✅ `save text X to file "path"` → `with open("path", "w") as f: f.write(str(X))`

### Utilitários
- ✅ `wait N seconds` → `time.sleep(N)`
- ✅ `random number from A to B` → `random.randint(A, B)`

### Imports
- ✅ `use module` → `import module`
- ✅ `use module as alias` → `import module as alias`
- ✅ `from module import item` → `from module import item`

### Expressões
- ✅ `X => Y` → `lambda X: Y`
- ✅ `assert` → `assert`

### IA/Agentes (Macros)
- ✅ `load model "name" as var` → `AutoModel.from_pretrained("name")`
- ✅ `agent Name:` → comentário/placeholder
- ✅ `goal "text"` → comentário
- ✅ `tool name` → comentário

### Python Puro
- ✅ Qualquer código Python é copiado como está (escape completo)

---

## ❌ O que AINDA NÃO está implementado

### Estruturas de Dados
- ❌ Dicionários (`dict X = {...}`)
- ❌ Tuplas (`tuple X = (...)`)
- ❌ Sets (`set X = {...}`)
- ❌ Comprehensions (list, dict, set)

### Operações Avançadas
- ❌ Operadores: `+=`, `-=`, `*=`, `/=`, `//=`, `%=`, `**=`
- ❌ Operador `in` / `not in` (para strings, listas)
- ❌ Slicing (`list[1:5]`, `list[:3]`, `list[2:]`)
- ❌ Operador `**` (potência)
- ❌ Operador `//` (divisão inteira)
- ❌ Operador `%` (módulo) - funciona via Python puro

### Strings
- ❌ Métodos de string (`upper()`, `lower()`, `split()`, etc.) - funciona via Python puro
- ❌ F-strings / formatação avançada
- ❌ Multiplicação de strings (`"a" * 3`)

### Listas Avançadas
- ❌ `insert`, `pop`, `index`, `count`, `sort`, `reverse`
- ❌ Acesso por índice (`list[0]`)
- ❌ Slicing de listas

### Funções Avançadas
- ❌ Argumentos padrão (`define func(x=10):`)
- ❌ `*args`, `**kwargs`
- ❌ Funções aninhadas
- ❌ Closures
- ❌ Generators (`yield`)

### Classes Avançadas
- ❌ Herança (`class Child(Parent):`)
- ❌ Métodos estáticos (`@staticmethod`)
- ❌ Métodos de classe (`@classmethod`)
- ❌ Propriedades (`@property`)
- ❌ Métodos especiais (`__str__`, `__repr__`, `__len__`, etc.)
- ❌ Múltipla herança
- ❌ Mixins

### Módulos e Pacotes
- ❌ `__init__.py` (funciona via Python puro)
- ❌ Import relativo (`from .module import`)
- ❌ `import *` (funciona via Python puro)

### Context Managers Customizados
- ❌ `with` customizado (funciona via Python puro)

### Decorators Avançados
- ❌ Decorators com argumentos (`@decorator(arg)`)
- ❌ Decorators aninhados

### Async Avançado
- ❌ `asyncio.gather()`, `asyncio.create_task()`
- ❌ Context managers async (`async with`)

### Type Hints
- ❌ Anotações de tipo (`def func(x: int) -> str:`)

### Match/Case (Python 3.10+)
- ❌ `match` / `case` statements

### Walrus Operator (Python 3.8+)
- ❌ `:=` (atribuição em expressão)

### Dataclasses
- ❌ `@dataclass`

### Enums
- ❌ `Enum`

### Exceções Específicas
- ❌ Tipos específicos de exceção (funciona via Python puro)

### Metaclasses
- ❌ Metaclasses customizadas

### Descriptors
- ❌ Descriptors

### Abstract Base Classes
- ❌ `ABC`, `@abstractmethod`

---

## 🎯 Resumo

### ✅ Implementado: ~40 comandos básicos e intermediários
### ❌ Não implementado: ~30+ recursos avançados

### 💡 Solução Atual

**Para recursos não implementados, use Python puro:**

```logic
# Você pode escrever Python direto no Mython
import json
data = {"name": "test"}
result = json.dumps(data)

# Ou usar operadores Python
x += 1
y = [i*2 for i in range(10)]
```

**O transpiler copia Python puro como está!**

---

## 🚀 Próximos Passos (Opcional)

1. Adicionar dicionários: `dict X = {"key": "value"}`
2. Adicionar operadores: `+=`, `-=`, etc.
3. Adicionar slicing: `list[1:5]`
4. Adicionar herança: `class Child(Parent):`
5. Adicionar `yield` para generators
6. Adicionar `match/case` (Python 3.10+)

---

**Mython cobre ~70% do Python básico/intermediário.**
**Para o resto, use Python puro diretamente!**


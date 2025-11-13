# Mython 1.0 - Especificação Completa

## 🎯 Visão Geral

**Mython 1.0** é uma linguagem de programação que transpila para Python, focada em:

- ✅ **Simplicidade extrema** (inglês A2/B1)
- ✅ **Equivalência total ao Python**
- ✅ **Suporte a IA avançada**
- ✅ **Zero complexidade sintática**
- ✅ **Lógica humana, não código**

## 🏗️ Arquitetura

### Duas Camadas

1. **Camada A2 (Básica)**: 95% dos casos de uso
   - Comandos simples e naturais
   - Lógica básica
   - Ideal para iniciantes

2. **Camada A2-Advanced**: Funcionalidades avançadas
   - Classes e OOP
   - Async/Await
   - IA e agentes
   - Tudo que Python faz

### Fluxo de Transpilação

```
Mython (.logic) → Transpiler → Python (.py) → Execução
```

## 📋 Especificação Técnica

### Comandos Suportados

#### Entrada/Saída
- `say` → `print()`
- `ask` → `input()`
- `ask number` → `int(input())`

#### Controle de Fluxo
- `if/else/elif` → `if/else/elif`
- `while` → `while`
- `repeat N times` → `for _ in range(N)`
- `for each X in Y` → `for X in Y`
- `break`, `continue`, `pass`

#### Estruturas de Dados
- `list X = [...]` → `X = [...]`
- `add X to Y` → `Y.append(X)`
- `remove X from Y` → `Y.remove(X)`

#### Funções
- `define func(args):` → `def func(args):`
- `task method(args):` → `def method(args):`
- `return X` → `return X`

#### Classes
- `class Name:` → `class Name:`
- `init(args):` → `def __init__(self, args):`
- `set self.x = y` → `self.x = y`
- `task method(args):` → `def method(self, args):`

#### Async
- `async task func(args):` → `async def func(args):`
- `await expr` → `await expr`

#### Exceções
- `attempt:` → `try:`
- `catch Exception as e:` → `except Exception as e:`
- `finally:` → `finally:`
- `raise Exception("msg")` → `raise Exception("msg")`

#### Decorators
- `decorator name:` → `@name`
- `@decorator` → `@decorator`

#### Imports
- `use module` → `import module`
- `use module as alias` → `import module as alias`
- `from module import item` → `from module import item`

#### Arquivos
- `read file "path" as var` → `with open("path") as f: var = f.read()`
- `save text X to file "path"` → `with open("path", "w") as f: f.write(str(X))`
- `open "path" as var:` → `with open("path") as var:`

#### Utilitários
- `wait N seconds` → `time.sleep(N)`
- `random number from A to B` → `random.randint(A, B)`

#### Macros de IA
- `load model "name" as var` → `var = AutoModelForCausalLM.from_pretrained("name")`
- `agent Name:` → `# Agent: Name`
- `goal "text"` → `# Goal: text`
- `tool name` → `# Tool: name`

#### Expressões
- `X => Y` → `lambda X: Y`
- `assert condition` → `assert condition`

### Operadores de Comparação

| Mython | Python |
|--------|--------|
| `is` | `==` |
| `is not` | `!=` |
| `is over` | `>` |
| `is under` | `<` |
| `is at least` | `>=` |
| `is at most` | `<=` |

### Detecção Automática de Imports

O transpiler detecta automaticamente e adiciona:

- `import time` → quando usa `wait`
- `import random` → quando usa `random number from`
- `import asyncio` → quando usa `async`/`await`
- `from transformers import ...` → quando usa `load model`
- `import torch` → quando usa modelos de IA

## 🎨 Princípios de Design

1. **Simplicidade sobre Complexidade**: Sempre prefira o mais simples
2. **Natural sobre Técnico**: Frases naturais, não símbolos
3. **Lógica sobre Sintaxe**: Foco no pensamento, não na digitação
4. **Acessibilidade sobre Poder**: Fácil de usar, poderoso por dentro

## 📊 Estatísticas

- **Comandos suportados**: ~40 comandos principais
- **Operadores naturais**: 6 operadores de comparação
- **Camadas**: 2 (Básica e Avançada)
- **Equivalência Python**: 100% (via transpilação)

## 🔮 Futuro

Mython 1.0 é a base. Próximas versões incluirão:

- Sistema de módulos Mython
- Integração completa com frameworks de IA
- Agentes autônomos funcionais
- Extensões para editores
- Comunidade e ecossistema

---

**Mython 1.0** - A linguagem mais simples do mundo. 🐍✨


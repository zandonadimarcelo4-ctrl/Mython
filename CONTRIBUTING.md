# Guia de Contribuição - Mython

Este documento explica como adicionar novas funcionalidades, macros e comandos ao Mython.

## 🧩 Como Adicionar Novas Macros

### Passo 1: Definir a Sintaxe

Primeiro, defina como a macro será escrita em `.logic`. Por exemplo:

```logic
log "mensagem importante"
```

### Passo 2: Adicionar ao `translate_line`

Abra `mython/transpiler.py` e adicione um novo caso na função `translate_line`:

```python
# log
if stripped.startswith("log "):
    content = stripped[len("log "):]
    return indent + f'print(f"[LOG] {content}")'
```

### Passo 3: Testar

Crie um exemplo em `examples/` e teste:

```logic
log "teste de log"
```

Execute:
```bash
mython examples/test.logic --run
```

## 📋 Tabela de Macros Existentes

| Comando Mython | Python Gerado |
|----------------|---------------|
| `say X` | `print(X)` |
| `ask name "text"` | `name = input("text")` |
| `ask number age "text"` | `age = int(input("text"))` |
| `if COND:` | `if COND:` (com normalização) |
| `else:` | `else:` |
| `elif COND:` | `elif COND:` (com normalização) |
| `repeat N times:` | `for _ in range(N):` |
| `list names = [...]` | `names = [...]` |
| `add X to names` | `names.append(X)` |
| `remove X from names` | `names.remove(X)` |
| `for each item in items:` | `for item in items:` |
| `define func(args):` | `def func(args):` |
| `return X` | `return X` |
| `wait N seconds` | `time.sleep(N)` |
| `random number from A to B` | `random.randint(A, B)` |
| `save text X to file "path"` | `with open("path", "w") as f: f.write(str(X))` |
| `read file "path" as var` | `with open("path", "r") as f: var = f.read()` |

## 🔧 Operadores de Comparação

A função `normalize_condition` converte expressões naturais:

| Expressão | Operador Python |
|-----------|----------------|
| `is` | `==` |
| `is not` | `!=` |
| `is over` | `>` |
| `is under` | `<` |
| `is at least` | `>=` |
| `is at most` | `<=` |

## 🎯 Exemplo Completo: Adicionar `error`

### 1. Adicionar ao `translate_line`:

```python
# error
if stripped.startswith("error "):
    content = stripped[len("error "):]
    return indent + f'print(f"[ERROR] {content}", file=sys.stderr)'
```

### 2. Detectar uso de `sys`:

Na função `transpile_file`, adicione:

```python
needs_sys = False

# No loop:
if "error " in stripped:
    needs_sys = True

# No header:
if needs_sys:
    header.append("import sys")
```

### 3. Testar:

```logic
error "algo deu errado!"
```

## 🚀 Ideias para Novas Macros

- `log X` → `print(f"[LOG] {X}")`
- `debug X` → `print(f"[DEBUG] {X}")`
- `warn X` → `print(f"[WARN] {X}")`
- `stop` → `sys.exit(0)`
- `stop with code N` → `sys.exit(N)`
- `length of list` → `len(list)`
- `join list with "sep"` → `"sep".join(list)`
- `split text by "sep"` → `text.split("sep")`
- `convert X to number` → `int(X)`
- `convert X to text` → `str(X)`

## 📝 Boas Práticas

1. **Ordem importa**: Coloque comandos mais específicos antes dos genéricos
2. **Preserve indentação**: Sempre mantenha a indentação original
3. **Trate casos especiais**: Considere valores com aspas, variáveis, etc.
4. **Adicione exemplos**: Crie exemplos em `examples/` para cada nova macro
5. **Documente**: Atualize este arquivo e o README.md

## 🧪 Testando

Sempre teste suas mudanças:

```bash
# Transpilar
mython examples/seu_exemplo.logic

# Verificar o Python gerado
cat examples/seu_exemplo.py

# Executar
mython examples/seu_exemplo.logic --run
```

---

**Dúvidas?** Abra uma issue no repositório!


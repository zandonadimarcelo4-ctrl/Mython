# Como o Mython Funciona

## ⚠️ REGRA FUNDAMENTAL

**Mython NÃO executa código diretamente.**

**É OBRIGATÓRIO transformar em Python normal antes de rodar.**

---

## 🔄 Fluxo Completo

```
1. Você escreve Mython (.logic)
        ↓
2. Transpiler converte para Python (.py)
        ↓
3. Python executa o código (.py)
```

---

## 📝 Passo a Passo

### 1. Você Escreve Código Mython

Crie um arquivo `program.logic`:

```logic
say "Hello, World!"
ask name "What is your name? "
say "Hello, " + name
```

### 2. Transpiler Converte para Python

Execute:

```bash
mython program.logic
```

**O que acontece:**
- O transpiler lê `program.logic`
- Converte cada linha para Python
- Gera `program.py` (Python normal)

**Arquivo gerado (`program.py`):**
```python
print("Hello, World!")
name = input("What is your name? ")
print("Hello, " + name)
```

### 3. Python Executa

**Opção 1: Executar automaticamente**
```bash
mython program.logic --run
```

**Opção 2: Executar manualmente**
```bash
python program.py
```

---

## 🎯 Por Que Isso é Importante?

### ✅ Vantagens

1. **100% Compatível com Python**: O código gerado é Python puro
2. **Pode usar qualquer biblioteca Python**: Funciona tudo
3. **Debugging fácil**: Você pode ver e editar o Python gerado
4. **Performance nativa**: Executa como Python normal
5. **Ferramentas Python**: Pode usar todas as ferramentas Python

### ⚠️ Limitações

1. **Sempre precisa transpilar**: Não executa diretamente
2. **Gera arquivo Python**: Cria um arquivo `.py` intermediário
3. **Depende do Python**: Precisa ter Python instalado

---

## 🔍 O Que Acontece Internamente

### Exemplo Completo

**Mython (`example.logic`):**
```logic
ask number age "Your age: "
if age is over 18:
    say "Adult"
else:
    say "Minor"
```

**Transpiler processa:**
1. Lê linha: `ask number age "Your age: "`
   - Detecta: comando `ask number`
   - Traduz: `age = int(input("Your age: "))`

2. Lê linha: `if age is over 18:`
   - Detecta: condição `if` com `is over`
   - Normaliza: `age > 18`
   - Traduz: `if age > 18:`

3. Lê linha: `say "Adult"`
   - Detecta: comando `say`
   - Traduz: `print("Adult")`

**Python gerado (`example.py`):**
```python
age = int(input("Your age: "))
if age > 18:
    print("Adult")
else:
    print("Minor")
```

**Python executa:**
- Pede idade ao usuário
- Verifica se é maior que 18
- Mostra "Adult" ou "Minor"

---

## 🛠️ Comandos Disponíveis

### Transpilar apenas
```bash
mython program.logic
```
Gera `program.py` mas não executa.

### Transpilar e executar
```bash
mython program.logic --run
```
Gera `program.py` e executa automaticamente.

### Especificar arquivo de saída
```bash
mython program.logic -o output.py
```
Gera `output.py` ao invés de `program.py`.

---

## 💡 Dicas

### 1. Ver o Python Gerado

Sempre transpile primeiro para ver o Python:

```bash
mython program.logic
cat program.py  # ou type program.py no Windows
```

### 2. Editar o Python Gerado

Você pode editar o Python gerado diretamente se precisar:

```bash
mython program.logic
# Edite program.py manualmente
python program.py
```

### 3. Debugging

Se algo não funcionar:

1. Transpile: `mython program.logic`
2. Veja o Python: `cat program.py`
3. Execute: `python program.py`
4. Veja os erros do Python

---

## 🎯 Resumo

**Mython = Linguagem Simples → Transpiler → Python Normal → Execução**

- ✅ Você escreve em Mython (simples)
- ✅ Transpiler converte para Python (automático)
- ✅ Python executa (normal)

**Sempre transforma em Python antes de rodar. Sempre.**

---

**Mython** - Simples de escrever, Python de executar. 🐍✨


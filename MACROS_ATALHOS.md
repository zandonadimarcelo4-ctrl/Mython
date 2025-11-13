# 🎯 Mython - Macros e Atalhos Comuns

## ✅ Status: Macros Implementadas!

**Mython agora tem macros e atalhos para operações comuns, usando palavras simples e intuitivas!**

---

## 📊 Macros Disponíveis

### ➕ Operações Matemáticas

**Adição:**
- ✅ `add x and y` → `(x + y)`
- ✅ `sum x and y` → `(x + y)`
- ✅ `plus x and y` → `(x + y)`

**Subtração:**
- ✅ `subtract x from y` → `(y - x)`
- ✅ `minus x from y` → `(y - x)`

**Multiplicação:**
- ✅ `multiply x by y` → `(x * y)`
- ✅ `times x by y` → `(x * y)`

**Divisão:**
- ✅ `divide x by y` → `(x / y)`

**Exemplo:**
```logic
set x = 10
set y = 5
set result = add x and y
set product = multiply x by y
```

---

### 📝 Operações de String

**Join (Unir):**
- ✅ `join list with "separator"` → `"separator".join(list)`
- ✅ `combine list with "separator"` → `"separator".join(list)`

**Split (Separar):**
- ✅ `split string by "separator"` → `string.split("separator")`
- ✅ `separate string by "separator"` → `string.split("separator")`

**Case Conversion:**
- ✅ `uppercase string` → `string.upper()`
- ✅ `to uppercase string` → `string.upper()`
- ✅ `lowercase string` → `string.lower()`
- ✅ `to lowercase string` → `string.lower()`

**Exemplo:**
```logic
list words = ["hello", "world"]
set joined = join words with " "
set text = "hello,world"
set parts = split text by ","
set upper = uppercase "hello"
```

---

### 📋 Operações de Lista

**Tamanho:**
- ✅ `length of list` → `len(list)`
- ✅ `size of list` → `len(list)`
- ✅ `count items in list` → `len(list)`

**Primeiro/Último:**
- ✅ `first item in list` → `list[0]`
- ✅ `last item in list` → `list[-1]`

**Reverter:**
- ✅ `reverse list` → `list(reversed(list))`
- ✅ `flip list` → `list(reversed(list))`

**Ordenar:**
- ✅ `sort list` → `sorted(list)`
- ✅ `order list` → `sorted(list)`

**Exemplo:**
```logic
list numbers = [3, 1, 4, 1, 5]
set len = length of numbers
set first = first item in numbers
set last = last item in numbers
set reversed = reverse numbers
set sorted = sort numbers
```

---

### 📁 Operações de Arquivo

**Verificar Existência:**
- ✅ `exists file "path"` → `os.path.exists("path")`
- ✅ `file exists "path"` → `os.path.exists("path")`

**Deletar:**
- ✅ `delete file "path"` → `os.remove("path")`
- ✅ `remove file "path"` → `os.remove("path")`

**Exemplo:**
```logic
if exists file "data.txt":
    say "File exists!"
    delete file "data.txt"
```

---

### 📅 Operações de Data/Hora

**Data/Hora Atual:**
- ✅ `current time` → `datetime.datetime.now()`
- ✅ `now` → `datetime.datetime.now()`
- ✅ `current date` → `datetime.datetime.now()`
- ✅ `today` → `datetime.date.today()`

**Exemplo:**
```logic
set now = current time
set today = today
say "Current time: " + str(now)
```

---

### 🖥️ Operações de Sistema

**Sair do Programa:**
- ✅ `exit program` → `sys.exit()`
- ✅ `quit program` → `sys.exit()`
- ✅ `stop program` → `sys.exit()`

**Exemplo:**
```logic
say "Goodbye!"
exit program
```

---

## 🎯 Vantagens

### ✅ Simplicidade
- Palavras simples e intuitivas
- Sem sintaxe técnica
- Fácil de lembrar

### ✅ Naturalidade
- Soa como linguagem natural
- Expressões comuns do dia a dia
- Fácil de entender

### ✅ Produtividade
- Menos código para escrever
- Operações comuns prontas
- Menos erros

---

## 📚 Exemplo Completo

Veja `examples/macros_atalhos.logic` para exemplos de TODAS as macros!

```bash
mython examples/macros_atalhos.logic
python examples/macros_atalhos.py
```

---

## ✅ Resumo

**Macros Implementadas:**
- ✅ **Matemáticas**: 8 macros
- ✅ **Strings**: 8 macros
- ✅ **Listas**: 10 macros
- ✅ **Arquivos**: 4 macros
- ✅ **Data/Hora**: 4 macros
- ✅ **Sistema**: 3 macros

**Total: 37+ macros e atalhos!**

---

**Mython = Macros Simples + Operações Comuns** 🎯✨


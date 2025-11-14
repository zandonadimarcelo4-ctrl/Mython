# 🚀 Análise: Macros e Abstrações para Mython
## Como Tornar Mython Mais Poderoso e Fácil que Python

Este documento consolida as análises e sugestões para transformar o Mython em um **Transpiler de Abstração de Alto Nível**, posicionando-o como uma alternativa mais poderosa e fácil que Python através de macros e padrões.

---

## 📊 Visão Geral

### Objetivo
Transformar Mython de um **transpiler de sintaxe** para um **Transpiler de Abstração de Alto Nível**, onde comandos simples em Mython se expandem para blocos de código Python complexos e otimizados.

### Vantagem Competitiva
O Mython se torna mais viável que Python puro porque o usuário gasta **zero tempo** com:
- Sintaxe complexa de bibliotecas avançadas
- Boilerplate repetitivo
- Configurações detalhadas
- Aprendizado de APIs complexas

Focando apenas na **lógica de alto nível**.

---

## 🎯 1. Programação Assíncrona

### Problema Atual
Código Python assíncrono é complexo:
```python
async with httpx.AsyncClient() as client:
    response = await client.get("https://api.example.com")
    data = response.json()
```

### Solução: Macro HTTP Simplificada

**Sintaxe Mython:**
```mython
get data from "https://api.example.com" as json
post data to "https://api.example.com" with {"key": "value"} as response
```

**Python Gerado:**
```python
import httpx
import asyncio

async def _async_get():
    async with httpx.AsyncClient() as client:
        response = await client.get("https://api.example.com")
        return response.json()

data = asyncio.run(_async_get())
```

### Implementação

#### Gramática (`grammar.lark`):
```lark
// Macros HTTP
http_get_stmt: ("get" | "fetch" | "download") expr ("from" | "from url") STRING ("as" ("json" | "text" | "binary"))?
http_post_stmt: ("post" | "send") expr? ("to" | "to url") STRING ("with" expr)? ("as" ("json" | "text" | "binary"))?
```

#### Transformer (`transformer_lark.py`):
```python
def http_get_stmt(self, children: List[Any]) -> str:
    """
    http_get_stmt: get data from "url" as json
    """
    self.needs_imports['httpx'] = True
    self.needs_imports['asyncio'] = True
    
    # Extrair URL e formato
    url = self._expr(children[1])  # STRING
    format_type = "json" if "json" in str(children).lower() else "text"
    
    # Gerar código assíncrono
    return f"""
async def _async_get():
    async with httpx.AsyncClient() as client:
        response = await client.get({url})
        return response.{format_type}()

data = asyncio.run(_async_get())
""".strip()
```

---

## 📊 2. Manipulação de Dados (Pandas/Numpy)

### Problema Atual
Código Python para manipulação de dados é verboso:
```python
import pandas as pd
data = pd.read_csv("file.csv")
filtered = data[data["age"] > 18]
```

### Solução: Macros de Data Science

**Sintaxe Mython:**
```mython
load "file.csv" into data
filter data where column "age" is over 18
group data by "category"
sum data by "category"
```

**Python Gerado:**
```python
import pandas as pd

data = pd.read_csv("file.csv")
filtered = data[data["age"] > 18]
grouped = data.groupby("category")
summed = data.groupby("category").sum()
```

### Implementação

#### Gramática:
```lark
// Macros Data Science
load_data_stmt: ("load" | "read" | "import") STRING ("into" | "as") NAME
filter_data_stmt: "filter" NAME "where" "column" STRING comparison_op expr
group_data_stmt: "group" NAME "by" STRING
sum_data_stmt: "sum" NAME "by" STRING
```

#### Transformer:
```python
def load_data_stmt(self, children: List[Any]) -> str:
    """
    load_data_stmt: load "file.csv" into data
    """
    self.needs_imports['pandas'] = True
    
    file_path = self._expr(children[0])  # STRING
    var_name = children[1].value if isinstance(children[1], Token) else str(children[1])
    
    # Detectar extensão do arquivo
    if file_path.endswith('.csv'):
        return f"{var_name} = pd.read_csv({file_path})"
    elif file_path.endswith('.json'):
        return f"{var_name} = pd.read_json({file_path})"
    elif file_path.endswith('.xlsx'):
        return f"{var_name} = pd.read_excel({file_path})"
    else:
        return f"{var_name} = pd.read_csv({file_path})"  # Padrão
```

---

## 🖼️ 3. Interfaces Gráficas (GUI)

### Problema Atual
Criar interfaces gráficas é complexo:
```python
import streamlit as st
st.title("My App")
st.button("Click Me", on_click=my_function)
```

### Solução: Sintaxe Declarativa Simplificada

**Sintaxe Mython:**
```mython
create app with title "My App"
add button "Click Me" that runs function on_click
add text input "Enter name" saved to name
show data as table
```

**Python Gerado:**
```python
import streamlit as st

st.title("My App")
if st.button("Click Me"):
    on_click()
name = st.text_input("Enter name")
st.table(data)
```

### Implementação

#### Gramática:
```lark
// Macros GUI
create_app_stmt: "create" "app" "with" "title" STRING
add_button_stmt: "add" "button" STRING ("that" "runs" "function" NAME)?
add_input_stmt: "add" ("text" | "number") "input" STRING "saved" "to" NAME
show_data_stmt: "show" NAME ("as" ("table" | "chart" | "graph"))?
```

#### Transformer:
```python
def create_app_stmt(self, children: List[Any]) -> str:
    """
    create_app_stmt: create app with title "My App"
    """
    self.needs_imports['streamlit'] = True
    
    title = self._expr(children[0])  # STRING
    return f'st.title({title})'
```

---

## 🤖 4. Inteligência Artificial (LLMs)

### Problema Atual
Chamar APIs de LLMs é verboso:
```python
from openai import OpenAI
client = OpenAI()
response = client.chat.completions.create(
    model="gpt-4",
    messages=[{"role": "user", "content": "Hello"}]
)
```

### Solução: Comandos Naturais de IA

**Sintaxe Mython:**
```mython
ask model "gpt-4" "summarize this text" and save result to summary
load model "qwen2.5-mini" as local_model
generate image "a cat playing piano" saved to image.png
```

**Python Gerado:**
```python
from openai import OpenAI

client = OpenAI()
response = client.chat.completions.create(
    model="gpt-4",
    messages=[{"role": "user", "content": "summarize this text"}]
)
summary = response.choices[0].message.content
```

### Implementação

#### Gramática:
```lark
// Macros IA
ask_model_stmt: "ask" "model" STRING STRING ("and" "save" "result" "to" NAME)?
load_model_stmt: "load" "model" STRING ("as" NAME)?
generate_image_stmt: "generate" "image" STRING ("saved" "to" STRING)?
```

---

## 🌍 5. Internacionalização Avançada (I18N)

### Problema Atual
O sistema de i18n traduz apenas keywords, não frases completas.

### Solução: Tradução de Padrões Completos

**Sintaxe em Português:**
```mython
se idade for maior que 18:
    dizer "Você é maior de idade"
para cada item na lista:
    mostrar item
```

**Tradução Interna (A2):**
```mython
if age is over 18:
    say "Você é maior de idade"
for each item in list:
    show item
```

**Python Gerado:**
```python
if age > 18:
    print("Você é maior de idade")
for item in list:
    print(item)
```

### Implementação

Expandir o sistema de tradução para incluir:
1. **Dicionário de Padrões** (mapear frases completas)
2. **Normalização** (converter para sintaxe A2)
3. **Cache** (armazenar traduções frequentes)

---

## 📋 6. Sistema de Tipagem Opcional

### Problema Atual
Type hints são complexos para iniciantes.

### Solução: Sintaxe Natural para Tipos

**Sintaxe Mython:**
```mython
func calculate takes number a and number b returns number:
    return a + b
```

**Python Gerado:**
```python
def calculate(a: int, b: int) -> int:
    return a + b
```

### Implementação

#### Gramática:
```lark
// Type hints naturais
function_with_types: "func" NAME "takes" (type_spec NAME "and")* type_spec NAME "returns" type_spec ":"
type_spec: ("number" | "text" | "list" | "dict" | "bool")
```

---

## 🔧 7. Gerenciamento de Dependências

### Problema Atual
Gerenciar dependências requer conhecimento de `pip` e `requirements.txt`.

### Solução: Comando Simplificado

**Sintaxe Mython:**
```mython
use library "pandas"
use library "requests" as req
```

**Ação Automática:**
1. Gera `import pandas`
2. Adiciona `pandas` ao `requirements.txt`
3. (Opcional) Executa `pip install pandas`

### Implementação

Modificar `use_stmt` para:
1. Detectar se é biblioteca externa
2. Adicionar ao `requirements.txt`
3. Gerar import correto

---

## 🎯 Priorização de Implementação

### 🔴 Alta Prioridade (Esta Semana)
1. ✅ Macros HTTP básicas (`get data from "url"`)
2. ✅ Macros Data Science básicas (`load "file.csv" into data`)
3. ✅ Melhorar i18n para padrões completos

### 🟡 Média Prioridade (Próximas 2 Semanas)
4. ⏳ Macros GUI (`create app`, `add button`)
5. ⏳ Macros IA (`ask model`, `load model`)
6. ⏳ Tipagem opcional

### 🟢 Baixa Prioridade (Próximo Mês)
7. ⏳ Gerenciamento de dependências automatizado
8. ⏳ Macros avançadas (Web Scraping, Database, etc.)

---

## 💡 Princípios de Design para Macros

### 1. Natural > Técnico
Prefira comandos que soam como linguagem natural:
- ✅ `get data from "url"`
- ❌ `async_get_request("url")`

### 2. Simples > Complexo
Macros devem abstrair complexidade:
- ✅ `load "file.csv" into data`
- ❌ `data = pd.read_csv("file.csv", encoding="utf-8", sep=",", header=0)`

### 3. Consistente
Padrões similares devem funcionar de forma similar:
- `load "file.csv" into data`
- `load "file.json" into data`
- `load "file.xlsx" into data`

### 4. Extensível
Fácil adicionar novas macros seguindo o padrão estabelecido.

---

## 📈 Métricas de Sucesso

### Fase 1 (Macros Básicas)
- ✅ 10+ macros HTTP implementadas
- ✅ 10+ macros Data Science implementadas
- ✅ Redução de 50%+ no código necessário vs Python

### Fase 2 (Macros Avançadas)
- ✅ 20+ macros GUI implementadas
- ✅ 10+ macros IA implementadas
- ✅ Redução de 70%+ no código necessário vs Python

### Fase 3 (Ecosistema Completo)
- ✅ 50+ macros implementadas
- ✅ Documentação completa
- ✅ Exemplos práticos para cada macro

---

## 🚀 Próximos Passos

1. **Implementar macros HTTP básicas** (2-3 dias)
2. **Implementar macros Data Science básicas** (2-3 dias)
3. **Expandir i18n para padrões completos** (1 semana)
4. **Testar e documentar** (1 semana)

---

**Última atualização:** 2025-01-27
**Status:** Análise completa, pronto para implementação


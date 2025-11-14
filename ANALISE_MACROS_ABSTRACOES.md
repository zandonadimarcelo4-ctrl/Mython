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

### Implementação Detalhada

#### Gramática (`grammar.lark`):
```lark
// Macros HTTP - Ordem importa: mais específicos primeiro
http_get_stmt: ("get" | "fetch" | "download") NAME? ("from" | "from url") STRING ("as" ("json" | "text" | "binary" | "html"))?
http_post_stmt: ("post" | "send") expr? ("to" | "to url") STRING ("with" expr)? ("headers" expr)? ("as" ("json" | "text" | "binary"))?
http_put_stmt: ("put" | "update") expr ("to" | "to url") STRING ("with" expr)? ("as" ("json" | "text"))?
http_delete_stmt: ("delete" | "remove") ("from" | "from url") STRING ("as" ("json" | "text"))?
```

#### Transformer (`transformer_lark.py`):
```python
def http_get_stmt(self, children: List[Any]) -> str:
    """
    http_get_stmt: get data from "url" as json
    http_get_stmt: fetch result from "https://api.example.com" as json
    """
    self.needs_imports['httpx'] = True
    self.needs_imports['asyncio'] = True
    
    # Parsear children: [("get"|"fetch"), NAME?, ("from"|"from url"), STRING, ("as", format)?]
    var_name = None
    url = None
    format_type = "json"  # Padrão
    
    i = 0
    while i < len(children):
        child = children[i]
        
        # Verificar se é nome de variável (NAME antes de "from")
        if isinstance(child, Token) and child.type == 'NAME' and var_name is None:
            var_name = child.value
            i += 1
            continue
        
        # Verificar se é URL (STRING)
        if isinstance(child, Token) and child.type == 'STRING':
            url = child.value
            i += 1
            continue
        
        # Verificar se é formato ("as", "json"|"text"|"binary")
        if isinstance(child, str) and child.lower() == 'as':
            if i + 1 < len(children):
                format_token = children[i + 1]
                if isinstance(format_token, Token):
                    format_type = format_token.value.lower()
                    i += 2
                    continue
        
        i += 1
    
    # Validação
    if not url:
        raise SyntaxError("URL não especificada em http_get_stmt")
    
    if not url.startswith(('"', "'")) or not url.endswith(('"', "'")):
        raise SyntaxError(f"URL deve ser uma string: {url}")
    
    # Nome padrão da variável
    if not var_name:
        var_name = "data" if format_type == "json" else "response"
    
    # Mapear format_type para método httpx
    format_map = {
        "json": "response.json()",
        "text": "response.text",
        "binary": "response.content",
        "html": "response.text",  # HTML é texto
    }
    response_method = format_map.get(format_type, "response.json()")
    
    # Gerar código assíncrono
    indent = self.indent()
    return f"""
{indent}async def _async_get_{var_name}():
{indent}    async with httpx.AsyncClient() as client:
{indent}        response = await client.get({url})
{indent}        return {response_method}

{indent}{var_name} = asyncio.run(_async_get_{var_name}())
""".strip()
```

#### Exemplos de Uso:

**Exemplo 1: GET básico**
```mython
get data from "https://api.example.com/data" as json
say data
```

**Exemplo 2: GET com nome de variável**
```mython
get users from "https://api.example.com/users" as json
for each user in users:
    say user.name
```

**Exemplo 3: GET texto/HTML**
```mython
get page from "https://example.com" as html
say page
```

**Exemplo 4: POST com dados**
```mython
set payload = {"name": "Mython", "version": "1.0"}
post payload to "https://api.example.com/submit" as response
say response
```

**Exemplo 5: POST com headers**
```mython
set data = {"key": "value"}
set headers = {"Authorization": "Bearer token123"}
post data to "https://api.example.com/endpoint" with headers as json
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

### Implementação Detalhada

#### Gramática:
```lark
// Macros Data Science
load_data_stmt: ("load" | "read" | "import") STRING ("into" | "as") NAME
filter_data_stmt: "filter" NAME "where" "column" STRING comparison_op expr -> filtered_data
group_data_stmt: "group" NAME "by" STRING ("as" NAME)? -> grouped_data
sum_data_stmt: "sum" NAME "by" STRING ("as" NAME)? -> summed_data
mean_data_stmt: "mean" NAME "by" STRING ("as" NAME)? -> mean_data
count_data_stmt: "count" NAME ("by" STRING)? ("as" NAME)? -> counted_data
```

#### Transformer:
```python
def load_data_stmt(self, children: List[Any]) -> str:
    """
    load_data_stmt: load "file.csv" into data
    load_data_stmt: read "data.json" as json_data
    """
    self.needs_imports['pandas'] = True
    
    file_path = None
    var_name = None
    
    # Parsear children
    i = 0
    while i < len(children):
        child = children[i]
        
        # Verificar se é caminho do arquivo (STRING)
        if isinstance(child, Token) and child.type == 'STRING':
            file_path = child.value
            i += 1
            continue
        
        # Verificar se é nome de variável (NAME depois de "into"/"as")
        if isinstance(child, Token) and child.type == 'NAME' and var_name is None:
            var_name = child.value
            i += 1
            continue
        
        i += 1
    
    if not file_path or not var_name:
        raise SyntaxError("load_data_stmt requer arquivo e nome de variável")
    
    # Detectar extensão e tipo de arquivo
    file_path_str = file_path.strip('"\'')
    extension = file_path_str.split('.')[-1].lower() if '.' in file_path_str else 'csv'
    
    # Mapear extensão para método pandas
    load_methods = {
        'csv': 'pd.read_csv',
        'json': 'pd.read_json',
        'xlsx': 'pd.read_excel',
        'xls': 'pd.read_excel',
        'parquet': 'pd.read_parquet',
        'feather': 'pd.read_feather',
        'html': 'pd.read_html',
        'xml': 'pd.read_xml',
    }
    
    method = load_methods.get(extension, 'pd.read_csv')
    indent = self.indent()
    
    return f"{indent}{var_name} = {method}({file_path})"

def filter_data_stmt(self, children: List[Any]) -> str:
    """
    filter_data_stmt: filter data where column "age" is over 18
    """
    # children: [NAME, "where", "column", STRING, comparison_op, expr]
    df_name = None
    column = None
    condition = None
    
    i = 0
    while i < len(children):
        child = children[i]
        
        if isinstance(child, Token) and child.type == 'NAME' and df_name is None:
            df_name = child.value
            i += 1
            continue
        
        if isinstance(child, Token) and child.type == 'STRING' and column is None:
            column = child.value.strip('"\'')
            i += 1
            continue
        
        # Processar condition (comparison_op + expr)
        if isinstance(child, Tree) and child.data == 'comparison':
            condition = self._expr(child)
            i += 1
            continue
        
        i += 1
    
    if not df_name or not column:
        raise SyntaxError("filter_data_stmt requer dataframe e coluna")
    
    indent = self.indent()
    return f"{indent}filtered_{df_name} = {df_name}[{df_name}['{column}'] {condition}]"

def group_data_stmt(self, children: List[Any]) -> str:
    """
    group_data_stmt: group data by "category" as grouped
    """
    # Implementação similar...
    pass
```

#### Exemplos de Uso:

**Exemplo 1: Carregar CSV**
```mython
load "sales.csv" into sales
say sales.head()
```

**Exemplo 2: Carregar JSON**
```mython
read "config.json" as config
say config
```

**Exemplo 3: Filtrar dados**
```mython
load "users.csv" into users
filter users where column "age" is over 18
say filtered_users
```

**Exemplo 4: Agrupar e somar**
```mython
load "sales.csv" into sales
group sales by "category" as grouped
sum sales by "category" as totals
say totals
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

## 🔧 8. Sistema de Extensibilidade

### Problema Atual
Adicionar novas macros requer modificar gramática e transformer manualmente.

### Solução: Sistema de Plugins/Macros

**Estrutura Proposta:**
```python
# mython/macros/__init__.py
from mython.macros.http import HTTPMacros
from mython.macros.data import DataMacros
from mython.macros.ai import AIMacros

MACROS_REGISTRY = {
    'http': HTTPMacros(),
    'data': DataMacros(),
    'ai': AIMacros(),
}
```

**Base Class para Macros:**
```python
class MacroBase:
    """Classe base para todas as macros."""
    
    def register_grammar_rules(self) -> List[str]:
        """Retorna regras de gramática para esta macro."""
        return []
    
    def register_transformer_methods(self) -> Dict[str, callable]:
        """Retorna métodos do transformer para esta macro."""
        return {}
    
    def detect_usage(self, code: str) -> bool:
        """Detecta se a macro é usada no código."""
        return False
    
    def get_required_imports(self) -> List[str]:
        """Retorna imports necessários."""
        return []
```

### Exemplo: Macro HTTP Modular

```python
# mython/macros/http.py
class HTTPMacros(MacroBase):
    
    def register_grammar_rules(self) -> List[str]:
        return [
            'http_get_stmt: ("get" | "fetch") expr? ("from" | "from url") STRING ("as" ("json" | "text" | "binary"))?',
            'http_post_stmt: ("post" | "send") expr? ("to" | "to url") STRING ("with" expr)? ("as" ("json" | "text" | "binary"))?',
        ]
    
    def register_transformer_methods(self) -> Dict[str, callable]:
        return {
            'http_get_stmt': self.transform_get,
            'http_post_stmt': self.transform_post,
        }
    
    def detect_usage(self, code: str) -> bool:
        return any(keyword in code for keyword in ['get', 'fetch', 'post', 'send'])
    
    def get_required_imports(self) -> List[str]:
        return ['httpx', 'asyncio']
    
    def transform_get(self, children: List[Any]) -> str:
        # Implementação da transformação
        pass
```

---

## 📚 9. Documentação e Exemplos

### Problema Atual
Falta documentação prática e exemplos de uso das macros.

### Solução: Sistema de Exemplos Interativos

**Estrutura:**
```
examples/
├── http/
│   ├── basic_get.logic
│   ├── basic_get.py  # Gerado
│   └── README.md
├── data/
│   ├── load_csv.logic
│   └── README.md
└── ai/
    ├── chat_completion.logic
    └── README.md
```

**Exemplo de README:**
```markdown
# HTTP Macros - Exemplos

## GET Request Básico

**Mython:**
```mython
get data from "https://api.example.com/data" as json
say data
```

**Python Gerado:**
```python
import httpx
import asyncio

async def _async_get():
    async with httpx.AsyncClient() as client:
        response = await client.get("https://api.example.com/data")
        return response.json()

data = asyncio.run(_async_get())
print(data)
```

## POST Request com Dados

**Mython:**
```mython
set payload = {"name": "Mython", "version": "1.0"}
post payload to "https://api.example.com/submit" with {"Content-Type": "application/json"} as response
say response
```
```

---

## 🎯 10. Validação e Error Handling

### Problema Atual
Erros de macros não são claros para o usuário.

### Solução: Mensagens de Erro Amigáveis

**Exemplo:**
```python
class MacroError(Exception):
    """Erro específico de macro."""
    
    def __init__(self, macro_name: str, suggestion: str):
        self.macro_name = macro_name
        self.suggestion = suggestion
        super().__init__(
            f"Erro na macro '{macro_name}'. "
            f"Dica: {suggestion}"
        )

# Uso:
if not url.startswith(('http://', 'https://')):
    raise MacroError(
        'http_get_stmt',
        'A URL deve começar com http:// ou https://'
    )
```

**Output para o Usuário:**
```
💡 Erro na macro 'http_get_stmt'
   Linha 3: get data from "api.example.com" as json
                              ^
   Dica: A URL deve começar com http:// ou https://
   Tente: get data from "https://api.example.com" as json
```

---

## 📊 11. Métricas e Analytics

### Problema Atual
Não sabemos quais macros são mais usadas ou onde melhorar.

### Solução: Sistema de Métricas Opcional

**Tracking de Uso:**
```python
class MacroMetrics:
    """Coleta métricas de uso das macros."""
    
    def track_macro_usage(self, macro_name: str, success: bool):
        """Registra uso de uma macro."""
        # Opcional: enviar para analytics
        pass
    
    def get_popular_macros(self) -> List[Tuple[str, int]]:
        """Retorna macros mais usadas."""
        return sorted(
            self.usage_stats.items(),
            key=lambda x: x[1],
            reverse=True
        )[:10]
```

**Uso:**
- Identificar macros mais populares
- Priorizar melhorias
- Detectar problemas comuns

---

## 🔄 12. Backwards Compatibility

### Problema Atual
Novas macros podem quebrar código existente.

### Solução: Versionamento de Macros

**Estrutura:**
```python
MACRO_VERSIONS = {
    'http_get_stmt': '1.0.0',
    'load_data_stmt': '1.0.0',
    # Versões antigas podem ter fallback
    'http_get_legacy': '0.1.0',  # Deprecated
}
```

**Migration Guide:**
```markdown
## Migração de Macros v0.1 para v1.0

### HTTP GET
**Antigo (v0.1):**
```mython
http_get "url"
```

**Novo (v1.0):**
```mython
get data from "url" as json
```
```

---

## 🚀 Plano de Implementação Detalhado

### Fase 1: Infraestrutura (1 semana)
- [ ] Sistema de plugins/macros modular
- [ ] Base class para macros
- [ ] Sistema de registro
- [ ] Error handling melhorado

### Fase 2: Macros Básicas (2 semanas)
- [ ] HTTP: GET, POST básicos
- [ ] Data: load CSV, JSON, Excel
- [ ] Data: filter, group, sum básicos
- [ ] Testes unitários para cada macro

### Fase 3: Macros Avançadas (3 semanas)
- [ ] HTTP: PUT, DELETE, PATCH
- [ ] HTTP: Headers customizados
- [ ] Data: join, merge, pivot
- [ ] GUI: Streamlit básico
- [ ] IA: OpenAI, Anthropic básico

### Fase 4: Polimento (1 semana)
- [ ] Documentação completa
- [ ] Exemplos interativos
- [ ] Validação robusta
- [ ] Mensagens de erro amigáveis

### Fase 5: Extensibilidade (2 semanas)
- [ ] Sistema de plugins externos
- [ ] Marketplace de macros
- [ ] Comunidade contribuindo

---

## 📈 Métricas de Sucesso Aprimoradas

### Quantitativas
- **Cobertura:** 50+ macros implementadas em 3 meses
- **Redução de Código:** 70%+ menos código vs Python puro
- **Velocidade:** Desenvolvimento 3x mais rápido para tarefas comuns
- **Adoção:** 1000+ projetos usando macros em 6 meses

### Qualitativas
- **Simplicidade:** Usuários iniciantes conseguem usar macros em 5 minutos
- **Clareza:** Código Mython mais legível que Python equivalente
- **Satisfação:** 90%+ de satisfação em pesquisas de usuários
- **Produtividade:** Desenvolvedores reportam 2x mais produtividade

---

## 🎓 13. Curva de Aprendizado

### Nível 1: Iniciante (Dia 1)
**Aprende:**
- Macros básicas: `say`, `ask`, `if`, `while`
- Macros HTTP: `get data from "url"`
- Macros Data: `load "file.csv" into data`

**Projeto:** Criar um script que faz GET request e salva dados

### Nível 2: Intermediário (Semana 1)
**Aprende:**
- Macros HTTP avançadas: `post`, `with headers`
- Macros Data: `filter`, `group`, `sum`
- Macros GUI: `create app`, `add button`

**Projeto:** Criar uma aplicação web simples com Streamlit

### Nível 3: Avançado (Mês 1)
**Aprende:**
- Macros IA: `ask model`, `load model`
- Macros customizadas
- Otimização de código gerado

**Projeto:** Criar um chatbot completo com IA

---

## 🚀 Próximos Passos Imediatos

1. **Criar sistema de macros modular** (3 dias)
   - Base class `MacroBase`
   - Sistema de registro
   - Loader dinâmico

2. **Implementar macros HTTP básicas** (2 dias)
   - GET request
   - POST request
   - Error handling

3. **Implementar macros Data Science básicas** (2 dias)
   - Load CSV/JSON
   - Filter básico
   - Group básico

4. **Criar documentação e exemplos** (2 dias)
   - README para cada macro
   - Exemplos interativos
   - Guia de migração

**Total: ~1.5 semanas para MVP de macros**

---

**Última atualização:** 2025-01-27
**Status:** Análise completa e aprimorada, pronto para implementação modular


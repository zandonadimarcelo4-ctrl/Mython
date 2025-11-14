# Mython Language Specification v0.1

## Visão da Linguagem

**Mython é:**

* 🧠 **Sintaxe simples tipo Python** (indentação, sem ponto e vírgula, sem tipos explícitos pro iniciante)
* 🎨 **Frontend nível Apple**: UI declarativa bonitona, estilo React/SwiftUI, mas em sintaxe muito mais simples
* 🧱 **Backend tipo Python**: dá pra fazer API, servidor web, automação, bots, scripts de sistema
* ⚙️ **Motor interno em Rust**: VM + bytecode + GC + JIT → performance de gente grande
* 🤖 **Pronta pra IA**: bindings pra libs de IA, LLMs locais, GPU etc.
* 🌐 **Fullstack de verdade**: mesma linguagem no servidor e no navegador (via WASM)

Ela é meio que:

> "Python para humanos + Mojo/Rust por dentro + React/SwiftUI para UI"

---

## Roadmap em Fases

### 🔹 Fase 0 – Protótipo rápido (em Python) ✅ **EM ANDAMENTO**

**Objetivo:** Testar a **sintaxe** e o **"feeling"** da linguagem.

* Usar **Lark** (Python) para:
  * definir gramática
  * gerar AST
* Fazer um **transpilador Mython → Python**:
  * você escreve Mython
  * ele gera Python
  * Python executa

Isso dá uma linguagem "fake", mas **perfeita pra testar ideia sem sofrer com Rust ainda**.

**Status:** Transpilador funcional com Lark, correções em andamento.

---

### 🔹 Fase 1 – Especificação oficial da linguagem ✅ **ESTE DOCUMENTO**

**Objetivo:** Definir "as leis" da linguagem.

* Como são:
  * variáveis
  * blocos
  * funções
  * módulos
  * erros
  * tipos básicos
* O que **um programa válido** precisa ter
* Sintaxe oficial (em PT ou EN ou os dois)

**Status:** Especificação em andamento (este documento).

---

### 🔹 Fase 2 – Parser e AST em Rust ⏳ **PLANEJADO**

**Ferramentas:**
* **Pest** (parser): https://pest.rs/ - Muito fácil de escrever gramáticas
* **Logos** (lexer): https://github.com/maciejhirsz/logos - Melhor lexer automático

**Objetivo:**
* Criar:
  * `grammar.pest` (gramática da linguagem)
  * `Token` (enum do lexer)
  * `AstNode` (enum/struct do AST)

---

### 🔹 Fase 3 – Bytecode + VM em Rust ⏳ **PLANEJADO**

**Objetivo:** Mython vira uma linguagem de verdade.

1. Definir um conjunto de **instruções de bytecode**:
   * `LOAD_CONST`
   * `LOAD_NAME`
   * `STORE_NAME`
   * `CALL`
   * `RETURN`
   * `JUMP`
   * `JUMP_IF_FALSE`
   * `BINARY_ADD`, `BINARY_SUB`, etc.

2. Compilar AST → Bytecode

3. Implementar uma **máquina virtual de pilha**

---

### 🔹 Fase 4 – Garbage Collector (GC) ⏳ **PLANEJADO**

**Objetivo:** Ter listas, strings, mapas, funções, closures etc sem vazar memória.

**Versão inicial:** Mark-and-sweep simples

---

### 🔹 Fase 5 – JIT com Cranelift ⏳ **PLANEJADO**

**Objetivo:** Compilar funções "quentes" para código nativo.

**Estratégia:**
* Contar quantas vezes cada função é chamada
* Acima de um limite (ex: 1000 execuções), mandar essa função pra JIT
* Guardar ponteiro pro código nativo e chamar direto dali em diante

---

### 🔹 Fase 6 – WASM (rodar no navegador) ⏳ **PLANEJADO**

**Objetivo:** Compilar a própria VM Mython para **wasm32-unknown-unknown**.

* O mesmo bytecode roda no servidor e no navegador
* No navegador: Mython → bytecode → VM em WASM → DOM / Canvas / WebGPU

---

### 🔹 Fase 7 – UI & componentes "nível Apple" ⏳ **PLANEJADO**

**Objetivo:** Criar um **mini-React/SwiftUI da sua linguagem**, mas muito mais fácil.

**Exemplo de sintaxe Mython-UI:**
```my
page:
    hero:
        title "Bem-vindo"
        subtitle "Experiência nível Apple"
        button "Começar" -> iniciar()

func iniciar():
    say "Iniciando..."
```

---

### 🔹 Fase 8 – IA e Backend ⏳ **PLANEJADO**

**Backend:**
* Biblioteca `http` em Mython:
  * `server.get("/rota", func)`
  * `server.post(...)`
* Por trás, implementado em Rust com alguma lib HTTP (tipo axum, hyper etc)

**IA:**
* Módulo `ai`:
  * `ai.load_model("qwen")`
  * `ai.chat(model, "mensagem")`
  * `ai.embed(texto)`
* Por trás, chama:
  * bindings pra LLM local (llama.cpp, etc.)
  * ONNX Runtime
  * libs de GPU

---

## Design da Sintaxe (Lado "Fácil tipo Python")

### 📌 Regras Gerais

* **Indentação = blocos** (igual Python)
* **Sem `{}`, sem `;`**
* **Sem tipos obrigatórios**
* **Palavras-chave simples**

### 📌 Exemplo Completo

```my
ask nome "Qual seu nome?"

func saudacao(pessoa):
    if pessoa == "Marcelo":
        return "Fala, mestre!"
    else:
        return "Oi, " + pessoa

msg = saudacao(nome)
say msg

contador = 0
while contador < 3:
    say "Loop " + contador
    contador = contador + 1
```

---

## Especificação da Sintaxe (v0.1)

### 🔹 Statements Simples

#### `say` - Saída

```my
say "Hello, World!"
say variavel
say expressao + " concatenada"
```

**Gera:**
```python
print("Hello, World!")
print(variavel)
print(expressao + " concatenada")
```

---

#### `ask` - Entrada

```my
ask nome "Qual seu nome?"
ask number idade "Qual sua idade?"
ask email
```

**Gera:**
```python
nome = input("Qual seu nome?")
idade = int(input("Qual sua idade?"))
email = input("")
```

**Regras:**
* `ask NAME STRING?` → `NAME = input(STRING)`
* `ask number NAME STRING?` → `NAME = int(input(STRING))`
* `ask text NAME STRING?` → `NAME = input(STRING)` (padrão)

---

#### `if` / `else` - Condicionais

```my
if idade > 18:
    say "Você é adulto"
else:
    say "Você é menor"
```

**Gera:**
```python
if idade > 18:
    print("Você é adulto")
else:
    print("Você é menor")
```

**Regras:**
* Indentação obrigatória após `:`
* `else:` no mesmo nível do `if:`
* Blocos podem ter múltiplos statements

---

#### `while` - Loops

```my
contador = 0
while contador < 10:
    say contador
    contador = contador + 1
```

**Gera:**
```python
contador = 0
while contador < 10:
    print(contador)
    contador = contador + 1
```

---

#### `func` - Funções

```my
func soma(a, b):
    return a + b

resultado = soma(5, 3)
say resultado
```

**Gera:**
```python
def soma(a, b):
    return a + b

resultado = soma(5, 3)
print(resultado)
```

---

### 🔹 Expressões

#### Operadores Aritméticos

```my
soma = a + b
subtracao = a - b
multiplicacao = a * b
divisao = a / b
modulo = a % b
potencia = a ** b
```

---

#### Operadores de Comparação

```my
if a == b:  # igual
if a != b:  # diferente
if a > b:   # maior
if a < b:   # menor
if a >= b:  # maior ou igual
if a <= b:  # menor ou igual
```

**Suporte a linguagem natural (futuro):**
```my
if a is b:        # igual
if a is not b:    # diferente
if a is over b:   # maior
if a is under b:  # menor
if a is at least b:  # maior ou igual
if a is at most b:   # menor ou igual
```

---

#### Operadores Lógicos

```my
if a and b:
if a or b:
if not a:
```

---

### 🔹 Tipos Básicos

#### Números

```my
inteiro = 42
decimal = 3.14
negativo = -10
```

---

#### Strings

```my
texto = "Hello, World!"
texto2 = 'Single quotes'
fstring = f"Valor: {variavel}"
```

---

#### Listas

```my
lista = [1, 2, 3]
lista_vazia = []
lista_mista = [1, "dois", 3.0]
```

---

#### Dicionários

```my
dicio = {"nome": "Marcelo", "idade": 30}
dicio_vazio = {}
```

---

### 🔹 Atribuição

```my
variavel = valor
variavel += 1
variavel -= 1
variavel *= 2
variavel /= 2
```

---

## Ferramentas

### 🔹 CLI (Planejado)

Comandos:
* `mython run arquivo.my`
* `mython repl`
* `mython build` (gera binário ou bundle WASM)
* `mython fmt` (formatador de código)
* `mython check` (lint/erros sem executar)

---

### 🔹 Syntax Highlighting (Planejado)

* Criar uma gramática **Tree-sitter** da linguagem:
  * https://tree-sitter.github.io/tree-sitter/
  * Isso libera highlight:
    * em VSCode
    * em Neovim
    * em editores modernos
* Opcional: extensão VSCode:
  * syntax highlight
  * auto-complete
  * snippets

---

## Experiência de Aprendizado (Iniciante → Mestre)

### 🔹 Erros Amigáveis

Ao invés de:
> SyntaxError at line 3

Você faz:
> 💡 "Você esqueceu de indentar a linha 4 depois do `if`
> Tenta assim:
> `if condição:`
> `    ação`"

---

### 🔹 Comando "explica" (Planejado)

Dentro da própria linguagem:
```my
explain erro
```

Ou no CLI:
```bash
mython explain erro-123
```

E ele devolve uma explicação passo a passo.

---

### 🔹 Exemplos Oficiais (Planejado)

Pacote de exemplos:
* `mython examples ui`
* `mython examples api`
* `mython examples ai`

---

## Tempo Aproximado para 2 Pessoas

Se duas pessoas focarem de forma consistente:

* **Fase 0–1** (protótipo em Python + spec): **1–2 meses** ✅ **EM ANDAMENTO**
* **Fase 2–3** (parser + VM + bytecode em Rust): **3–6 meses**
* **Fase 4–5** (GC + JIT simples): **3–6 meses**
* **Fase 6–7** (WASM + UI): **4–8 meses**
* **Fase 8** (IA + polimento): **4–8 meses**

**Total: ~1 a 2 anos** pra uma linguagem *real* e usável.

---

## Referências e Ferramentas

### Parsers

* **Lark** (Python - Fase 0): https://github.com/lark-parser/lark
  * ✅ **Atual:** Usado para transpilação Mython → Python
  * ✅ Gramática em `mython/grammar.lark`
  * ✅ Transpilador funcional

* **Pest** (Rust - Fase 2): https://pest.rs/
  * ⏳ **Planejado:** Parser em Rust para VM
  * ⏳ Muito fácil de escrever gramáticas
  * ⏳ Ideal para Fase 2 (parser + AST em Rust)

* **Logos** (Rust - Fase 2): https://github.com/maciejhirsz/logos
  * ⏳ **Planejado:** Lexer automático em Rust
  * ⏳ Melhor lexer automático
  * ⏳ Ideal para Fase 2 (parser + AST em Rust)

* **Tree-sitter** (Syntax Highlighting): https://tree-sitter.github.io/tree-sitter/
  * ⏳ **Planejado:** Syntax highlighting e IDEs
  * ⏳ Parsing incremental (parse a cada keystroke)
  * ⏳ Robustez mesmo com erros de sintaxe
  * ⏳ Integração nativa com VSCode, Neovim, etc.
  * 📄 Veja `TREE_SITTER_INTEGRATION.md` para detalhes

### Inspirações

* **Python**: Sintaxe simples e legível
* **Moonscript**: Transpilação para linguagem host
* **Mojo**: Performance com sintaxe simples
* **React/SwiftUI**: UI declarativa
* **Rust**: Performance e segurança de memória

---

## Status Atual (Fase 0)

### ✅ Implementado

* Transpilador Mython → Python usando Lark
* Gramática básica com indentação (INDENT/DEDENT)
* Statements: `say`, `ask`, `if`, `else`, `while`, `func`
* Sistema de i18n (tradução automática de keywords)
* Interface Streamlit (IDE web)

### 🔧 Em Correção

* `ask number` não gera `int(input())` corretamente
* Indentação do `else:` com espaçamento extra

### ⏳ Planejado

* Syntax highlighting com Pygments no Streamlit
* Tree-sitter grammar para editores
* Mais statements e expressões
* Sistema de módulos
* Tratamento de erros amigável

---

## Próximos Passos

1. ✅ **Corrigir `ask number` e `else` indentation** (em andamento)
2. ✅ **Criar especificação oficial** (este documento)
3. ⏳ **Integrar Pygments no Streamlit** (syntax highlighting)
4. ⏳ **Expandir gramática** (mais statements e expressões)
5. ⏳ **Preparar Fase 2** (parser em Rust com Pest + Logos)

---

**Última atualização:** 2025-01-27
**Versão:** 0.1.0


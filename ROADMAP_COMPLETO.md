# Roadmap Completo do Mython

## Visão Geral

**Mython** é uma linguagem de programação que combina:
- 🧠 **Sintaxe simples tipo Python** (indentação, sem ponto e vírgula, sem tipos explícitos pro iniciante)
- 🎨 **Frontend nível Apple**: UI declarativa bonitona, estilo React/SwiftUI
- 🧱 **Backend tipo Python**: API, servidor web, automação, bots
- ⚙️ **Motor interno em Rust**: VM + bytecode + GC + JIT → performance de gente grande
- 🤖 **Pronta pra IA**: bindings pra libs de IA, LLMs locais, GPU
- 🌐 **Fullstack de verdade**: mesma linguagem no servidor e no navegador (via WASM)

> "Python para humanos + Mojo/Rust por dentro + React/SwiftUI para UI"

---

## Fase 0 – Protótipo Rápido (Python) ✅ **EM ANDAMENTO**

**Status:** Transpilador funcional com Lark

**Objetivo:** Testar a **sintaxe** e o **"feeling"** da linguagem.

**Ferramentas:**
- **Lark** (Python): https://github.com/lark-parser/lark
- Gramática em `mython/grammar.lark`
- Transpilador Mython → Python

**Implementado:**
- ✅ Transpilador funcional
- ✅ Gramática básica com indentação (INDENT/DEDENT)
- ✅ Statements: `say`, `ask`, `if`, `else`, `while`, `func`
- ✅ Sistema de i18n (tradução automática de keywords)
- ✅ Interface Streamlit (IDE web)

**Em Correção:**
- 🔧 `ask number` não gera `int(input())` corretamente
- 🔧 Indentação do `else:` com espaçamento extra

**Próximos Passos:**
1. Corrigir bugs técnicos (ask number, else indentation)
2. Integrar Pygments para syntax highlighting no Streamlit
3. Expandir gramática (mais statements e expressões)
4. Preparar Fase 2 (parser em Rust)

---

## Fase 1 – Especificação Oficial ✅ **COMPLETA**

**Status:** Especificação criada

**Objetivo:** Definir "as leis" da linguagem.

**Documentos:**
- `MYTHON_SPEC.md` - Especificação oficial v0.1
- `TREE_SITTER_INTEGRATION.md` - Integração Tree-sitter
- `ROADMAP_COMPLETO.md` - Este documento

**Conteúdo:**
- Sintaxe oficial
- Regras de parsing
- Semântica básica
- Exemplos

---

## Fase 2 – Parser e AST em Rust ⏳ **PLANEJADO**

**Status:** Planejado

**Objetivo:** Criar parser e AST em Rust.

**Ferramentas:**
- **Pest** (Rust): https://pest.rs/ - Muito fácil de escrever gramáticas
- **Logos** (Rust): https://github.com/maciejhirsz/logos - Melhor lexer automático

**Tarefas:**
1. Converter gramática Lark para Pest
2. Criar lexer com Logos
3. Criar AST em Rust
4. Testes unitários

**Tempo Estimado:** 3-6 meses

---

## Fase 3 – Bytecode + VM em Rust ⏳ **PLANEJADO**

**Status:** Planejado

**Objetivo:** Mython vira uma linguagem de verdade.

**Tarefas:**
1. Definir conjunto de instruções de bytecode
2. Compilar AST → Bytecode
3. Implementar máquina virtual de pilha
4. Testes de execução

**Tempo Estimado:** 3-6 meses

---

## Fase 4 – Garbage Collector (GC) ⏳ **PLANEJADO**

**Status:** Planejado

**Objetivo:** Ter listas, strings, mapas, funções, closures etc sem vazar memória.

**Estratégia:**
- Versão inicial: Mark-and-sweep simples
- Depois: geração jovem/velha, arenas, etc.

**Tempo Estimado:** 3-6 meses

---

## Fase 5 – JIT com Cranelift ⏳ **PLANEJADO**

**Status:** Planejado

**Objetivo:** Compilar funções "quentes" para código nativo.

**Estratégia:**
- Contar quantas vezes cada função é chamada
- Acima de um limite (ex: 1000 execuções), mandar essa função pra JIT
- Guardar ponteiro pro código nativo e chamar direto dali em diante

**Tempo Estimado:** 3-6 meses

---

## Fase 6 – WASM (Rodar no Navegador) ⏳ **PLANEJADO**

**Status:** Planejado

**Objetivo:** Compilar a própria VM Mython para **wasm32-unknown-unknown**.

**Resultado:**
- O mesmo bytecode roda no servidor e no navegador
- No navegador: Mython → bytecode → VM em WASM → DOM / Canvas / WebGPU

**Tempo Estimado:** 4-8 meses

---

## Fase 7 – UI & Componentes "Nível Apple" ⏳ **PLANEJADO**

**Status:** Planejado

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

**Tempo Estimado:** 4-8 meses

---

## Fase 8 – IA e Backend ⏳ **PLANEJADO**

**Status:** Planejado

**Backend:**
- Biblioteca `http` em Mython
- `server.get("/rota", func)`
- `server.post(...)`
- Por trás, implementado em Rust com alguma lib HTTP (tipo axum, hyper etc)

**IA:**
- Módulo `ai`
- `ai.load_model("qwen")`
- `ai.chat(model, "mensagem")`
- `ai.embed(texto)`
- Por trás, chama bindings pra LLM local (llama.cpp, etc.), ONNX Runtime, libs de GPU

**Tempo Estimado:** 4-8 meses

---

## Ferramentas e Tecnologias

### Parsers

| Ferramenta | Fase | Status | Link |
|------------|------|--------|------|
| **Lark** | 0 | ✅ Atual | https://github.com/lark-parser/lark |
| **Pest** | 2 | ⏳ Planejado | https://pest.rs/ |
| **Logos** | 2 | ⏳ Planejado | https://github.com/maciejhirsz/logos |
| **Tree-sitter** | Syntax Highlight | ⏳ Planejado | https://tree-sitter.github.io/tree-sitter/ |

### Syntax Highlighting

| Ferramenta | Fase | Status | Link |
|------------|------|--------|------|
| **Pygments** | 0 | ⏳ Planejado | https://pygments.org/ |
| **Tree-sitter** | 1 | ⏳ Planejado | https://tree-sitter.github.io/tree-sitter/ |

### IDEs e Editores

| Editor | Fase | Status |
|--------|------|--------|
| **Streamlit** | 0 | ✅ Implementado |
| **VSCode** | 1 | ⏳ Planejado |
| **Neovim** | 1 | ⏳ Planejado |

---

## Tempo Aproximado para 2 Pessoas

Se duas pessoas focarem de forma consistente:

| Fase | Tempo Estimado | Status |
|------|----------------|--------|
| **Fase 0–1** (protótipo em Python + spec) | 1–2 meses | ✅ **EM ANDAMENTO** |
| **Fase 2–3** (parser + VM + bytecode em Rust) | 3–6 meses | ⏳ Planejado |
| **Fase 4–5** (GC + JIT simples) | 3–6 meses | ⏳ Planejado |
| **Fase 6–7** (WASM + UI) | 4–8 meses | ⏳ Planejado |
| **Fase 8** (IA + polimento) | 4–8 meses | ⏳ Planejado |

**Total: ~1 a 2 anos** pra uma linguagem *real* e usável.

---

## Documentação

### Documentos Principais

- `MYTHON_SPEC.md` - Especificação oficial da linguagem
- `TREE_SITTER_INTEGRATION.md` - Integração Tree-sitter
- `ROADMAP_COMPLETO.md` - Este documento (roadmap completo)

### Documentos de Referência

- `README.md` - Documentação principal do projeto
- `VISAO_REVOLUCIONARIA.md` - Visão da linguagem
- `STATUS_IMPLEMENTACAO.md` - Status de implementação
- `PLANO_ACAO_CORE.md` - Plano de ação core
- `ROADMAP_REALISTA.md` - Roadmap realista

---

## Próximos Passos Imediatos

1. ✅ **Criar especificação oficial** (MYTHON_SPEC.md) - COMPLETA
2. ✅ **Documentar integração Tree-sitter** (TREE_SITTER_INTEGRATION.md) - COMPLETA
3. 🔧 **Corrigir `ask number`** (gerar `int(input())` corretamente) - EM ANDAMENTO
4. 🔧 **Corrigir indentação do `else:`** (não ter indentação extra) - PENDENTE
5. ⏳ **Integrar Pygments no Streamlit** (syntax highlighting) - PENDENTE
6. ⏳ **Expandir gramática** (mais statements e expressões) - PENDENTE
7. ⏳ **Preparar Fase 2** (parser em Rust com Pest + Logos) - PENDENTE

---

**Última atualização:** 2025-01-27
**Versão:** 0.1.0


# Tree-sitter Integration para Mython

## Visão Geral

**Tree-sitter** é um gerador de parsers e biblioteca de parsing incremental que permite:

* ✅ **Syntax highlighting** de alta qualidade em editores
* ✅ **Parsing incremental** (parse a cada keystroke)
* ✅ **Robustez** mesmo com erros de sintaxe
* ✅ **Bindings** para múltiplas linguagens (Python, Rust, JavaScript, etc.)

**Website:** https://tree-sitter.github.io/tree-sitter/

---

## Por Que Tree-sitter para Mython?

### 🎨 Syntax Highlighting

Tree-sitter é usado por:
* **VSCode** (via extensões)
* **Neovim** (via nvim-treesitter)
* **Atom** (editor base)
* **GitHub** (highlighting de código)

Criar uma gramática Tree-sitter para Mython permite syntax highlighting automático em todos esses editores.

---

### 🚀 Parsing Incremental

Tree-sitter é **extremamente rápido** para parsing incremental:

* Parse apenas as partes modificadas
* Atualiza a árvore de sintaxe eficientemente
* Ideal para IDEs e editores em tempo real

---

### 🛡️ Robustez

Tree-sitter continua funcionando mesmo com:
* Erros de sintaxe
* Código incompleto
* Arquivos parcialmente editados

Isso é perfeito para IDEs, onde o código raramente está "completo" durante a edição.

---

## Estratégia de Integração

### 🔹 Fase 0 (Atual) - Lark para Transpilação

**Status:** ✅ Implementado

* Usar **Lark** (Python) para transpilação Mython → Python
* Gramática em `mython/grammar.lark`
* Transpilador funcional

---

### 🔹 Fase 1 (Futuro) - Tree-sitter para Syntax Highlighting

**Objetivo:** Criar gramática Tree-sitter para syntax highlighting

**Ferramentas:**
* **tree-sitter** (Python): https://github.com/tree-sitter/py-tree-sitter
* **tree-sitter-cli**: Ferramenta CLI para gerar parsers

**Arquivos:**
* `tree-sitter-mython/grammar.js` - Gramática Tree-sitter
* `tree-sitter-mython/src/parser.c` - Parser gerado
* `tree-sitter-mython/bindings/python/` - Bindings Python

---

### 🔹 Fase 2 (Futuro) - Tree-sitter para IDE

**Objetivo:** Integrar Tree-sitter em IDEs e editores

**VSCode:**
* Criar extensão VSCode com Tree-sitter
* Syntax highlighting
* Auto-complete
* Snippets

**Neovim:**
* Plugin nvim-treesitter
* Syntax highlighting
* Folding
* Incremental selection

---

## Gramática Tree-sitter vs Lark

### Similaridades

Ambas usam gramáticas baseadas em regras:
* Regras recursivas
* Precedência de operadores
* Indentação (com suporte especial)

### Diferenças

| Aspecto | Lark | Tree-sitter |
|---------|------|-------------|
| **Linguagem** | Python | JavaScript (grammar.js) |
| **Parser** | LALR(1) | LR(1) incremental |
| **Performance** | Bom | Excelente (incremental) |
| **Syntax Highlight** | Não | Sim (nativo) |
| **Robustez a erros** | Moderada | Excelente |
| **Uso principal** | Transpilação | Syntax highlighting, IDEs |

---

## Exemplo de Gramática Tree-sitter

### Grammar.js (Tree-sitter)

```javascript
module.exports = grammar({
  name: 'mython',

  rules: {
    source_file: $ => repeat($._statement),

    _statement: $ => choice(
      $.say_stmt,
      $.ask_stmt,
      $.if_stmt,
      $.while_stmt,
      $.func_def,
      $.assignment
    ),

    say_stmt: $ => seq(
      'say',
      $._expression
    ),

    ask_stmt: $ => seq(
      'ask',
      optional($.ask_type),
      $.name,
      optional($.string)
    ),

    ask_type: $ => choice('number', 'text'),

    if_stmt: $ => seq(
      'if',
      $._condition,
      ':',
      $.block,
      optional($.else_block)
    ),

    else_block: $ => seq(
      'else',
      ':',
      $.block
    ),

    block: $ => repeat1($._statement),

    _expression: $ => choice(
      $.string,
      $.number,
      $.name,
      $.binary_expr
    ),

    binary_expr: $ => prec.left(seq(
      $._expression,
      choice('+', '-', '*', '/'),
      $._expression
    )),

    string: $ => /"[^"]*"|'[^']*'/,
    number: $ => /\d+(\.\d+)?/,
    name: $ => /[a-zA-Z_][a-zA-Z0-9_]*/
  }
});
```

---

## Plano de Implementação

### 1. Criar Gramática Tree-sitter

**Arquivo:** `tree-sitter-mython/grammar.js`

**Objetivo:** Converter gramática Lark para Tree-sitter

**Desafios:**
* Tree-sitter usa JavaScript, não EBNF
* Indentação precisa ser tratada diferente
* Precedência de operadores

---

### 2. Gerar Parser

**Comando:**
```bash
tree-sitter generate
```

**Resultado:**
* `src/parser.c` - Parser em C
* `bindings/python/` - Bindings Python
* `bindings/rust/` - Bindings Rust (opcional)

---

### 3. Testar Syntax Highlighting

**Teste local:**
```bash
tree-sitter test
```

**Teste em VSCode:**
* Criar extensão VSCode
* Usar tree-sitter para highlighting
* Testar em código real

---

### 4. Integrar em Editores

**VSCode:**
* Criar extensão `mython-vscode`
* Usar tree-sitter para highlighting
* Adicionar snippets e auto-complete

**Neovim:**
* Criar plugin `nvim-mython`
* Usar nvim-treesitter
* Configurar highlighting

---

## Comparação com Outras Ferramentas

### Tree-sitter vs Pygments

| Aspecto | Tree-sitter | Pygments |
|---------|-------------|----------|
| **Syntax Highlight** | ✅ Excelente | ✅ Bom |
| **Parsing Incremental** | ✅ Sim | ❌ Não |
| **Robustez a erros** | ✅ Excelente | ⚠️ Moderada |
| **Integração IDE** | ✅ Nativa | ⚠️ Limitada |
| **Performance** | ✅ Excelente | ⚠️ Moderada |
| **Facilidade de uso** | ⚠️ Moderada | ✅ Fácil |

**Conclusão:** Tree-sitter é melhor para IDEs, Pygments é melhor para renderização HTML simples.

---

### Tree-sitter vs Lark

| Aspecto | Tree-sitter | Lark |
|---------|-------------|------|
| **Uso principal** | Syntax highlighting | Transpilação |
| **Performance** | ✅ Excelente (incremental) | ✅ Bom |
| **Robustez a erros** | ✅ Excelente | ⚠️ Moderada |
| **Facilidade de gramática** | ⚠️ Moderada | ✅ Fácil |
| **Integração IDE** | ✅ Nativa | ❌ Não |

**Conclusão:** Use Lark para transpilação, Tree-sitter para syntax highlighting.

---

## Roadmap

### 🔹 Fase 0 (Atual) ✅

* ✅ Transpilador Lark funcional
* ✅ Gramática básica
* ⏳ Corrigir bugs (ask number, else indentation)

---

### 🔹 Fase 1 (Próximo) ⏳

* ⏳ Criar gramática Tree-sitter
* ⏳ Gerar parser Tree-sitter
* ⏳ Testar syntax highlighting
* ⏳ Integrar Pygments no Streamlit (temporário)

---

### 🔹 Fase 2 (Futuro) ⏳

* ⏳ Criar extensão VSCode
* ⏳ Criar plugin Neovim
* ⏳ Adicionar auto-complete
* ⏳ Adicionar snippets

---

## Recursos

### Documentação

* **Tree-sitter:** https://tree-sitter.github.io/tree-sitter/
* **Tree-sitter Python:** https://github.com/tree-sitter/py-tree-sitter
* **Tree-sitter CLI:** https://github.com/tree-sitter/tree-sitter/blob/master/cli/README.md

### Exemplos

* **tree-sitter-python:** https://github.com/tree-sitter/tree-sitter-python
* **tree-sitter-javascript:** https://github.com/tree-sitter/tree-sitter-javascript
* **tree-sitter-rust:** https://github.com/tree-sitter/tree-sitter-rust

### Tutoriais

* **Creating a Tree-sitter Grammar:** https://tree-sitter.github.io/tree-sitter/creating-parsers
* **Syntax Highlighting:** https://tree-sitter.github.io/tree-sitter/syntax-highlighting

---

## Conclusão

Tree-sitter é uma ferramenta **excelente** para syntax highlighting e integração com IDEs. Para o Mython:

1. **Fase 0 (Atual):** Use Lark para transpilação ✅
2. **Fase 1 (Próximo):** Crie gramática Tree-sitter para syntax highlighting ⏳
3. **Fase 2 (Futuro):** Integre Tree-sitter em VSCode e Neovim ⏳

**Próximo passo:** Corrigir bugs atuais (ask number, else indentation) e depois criar gramática Tree-sitter.

---

**Última atualização:** 2025-01-27
**Status:** Planejado


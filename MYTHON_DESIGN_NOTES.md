# 📘 Mython Design Notes v1.0

**Status:** ✅ **ESTÁVEL** - Decisões de design documentadas  
**Data:** 2025-01-27  
**Versão:** 1.0

---

## 📋 Índice

1. [Visão Geral](#visão-geral)
2. [Objetivos](#objetivos)
3. [Decisões de Design](#decisões-de-design)
4. [Filosofia](#filosofia)
5. [Conceitos de Simplicidade](#conceitos-de-simplicidade)
6. [O que Foi Deixado de Fora](#o-que-foi-deixado-de-fora)
7. [Conceitos Fundamentais](#conceitos-fundamentais)

---

## 1. Visão Geral

Mython é uma linguagem de programação que transpila para Python, focada em **simplicidade extrema** e **acessibilidade universal**.

**Filosofia Central:** "Python para humanos + blocos + frases naturais"

---

## 2. Objetivos

### 2.1 Objetivo Principal

**Criar a linguagem de programação mais simples possível que ainda seja 100% compatível com Python.**

---

### 2.2 Objetivos Secundários

1. **Acessibilidade:** Qualquer pessoa pode começar em minutos
2. **Intuitividade:** Não requer memorização de sintaxe
3. **Naturalidade:** Código que parece conversa
4. **Educação:** Ensina lógica básica, não sintaxe
5. **Compatibilidade:** 100% compatível com Python

---

## 3. Decisões de Design

### 3.1 Sintaxe

#### 3.1.1 Palavras-chave Simples

**Decisão:** Usar palavras-chave em inglês A2/B1 (nível básico).

**Exemplos:**
- `say` ao invés de `print`
- `ask` ao invés de `input`
- `if` (mantido do Python)
- `while` (mantido do Python)

**Justificativa:** Inglês A2 é universalmente ensinado e compreendido.

---

#### 3.1.2 Indentação Estilo Python

**Decisão:** Usar indentação com espaços (4 espaços por nível).

**Justificativa:**
- Remove necessidade de `{}` ou `end`
- Visualmente claro
- Já familiar para usuários Python

---

#### 3.1.3 Sem Tipos Explícitos

**Decisão:** Não exigir tipos explícitos (inferência dinâmica).

**Exemplo:**
```mython
idade = 25  # int
nome = "Marcelo"  # str
lista = [1, 2, 3]  # list
```

**Justificativa:** Reduz barreira de entrada para iniciantes.

---

#### 3.1.4 Sem Ponto e Vírgula

**Decisão:** Não usar `;` para terminar statements.

**Justificativa:** Redundante quando há newlines.

---

### 3.2 Estruturas de Dados

#### 3.2.1 Literais Simplificados

**Decisão:** Usar sintaxe Python para literais (`[]`, `{}`, `()`).

**Exemplo:**
```mython
list items = [1, 2, 3]
dict data = {"key": "value"}
tuple coords = (10, 20)
```

**Justificativa:** Familiar para usuários Python, simples para iniciantes.

---

#### 3.2.2 Distinção Dict vs Set

**Decisão:** `dict_literal` usa `pair (STRING ":" expr)`, `set_literal` não.

**Exemplo:**
```mython
dict data = {"key": "value"}  # Dict
make set numbers = {1, 2, 3}  # Set
```

**Justificativa:** Resolve ambiguidade `{}` vazio (é dict em Python).

---

### 3.3 Controle de Fluxo

#### 3.3.1 If/Else Padrão Python

**Decisão:** Manter sintaxe `if/else` do Python (com `:` e indentação).

**Exemplo:**
```mython
if idade > 18:
    say "Adulto"
else:
    say "Menor"
```

**Justificativa:** Familiar e funcional.

---

#### 3.3.2 Loops Simplificados

**Decisão:** Manter `while` e `for`, adicionar `repeat`.

**Exemplo:**
```mython
while idade < 18:
    say idade

for item in lista:
    say item

repeat 5:
    say "Hello"
```

**Justificativa:** Cobre todos os casos de uso de loops.

---

### 3.4 Funções

#### 3.4.1 Sintaxe `func` ou `def`

**Decisão:** Aceitar tanto `func` quanto `def`.

**Exemplo:**
```mython
func soma(a, b):
    return a + b

def multiplica(a, b):
    return a * b
```

**Justificativa:** `func` é mais amigável, `def` mantém compatibilidade.

---

### 3.5 Imports

#### 3.5.1 Sintaxe `use` Simplificada

**Decisão:** Aceitar `use`, `import`, `load`, `require`, `include`.

**Exemplo:**
```mython
use requests
import json
load math
```

**Justificativa:** Mais natural para iniciantes.

---

## 4. Filosofia

### 4.1 Princípios Fundamentais

1. **Apenas Lógica, Nada Mais:** Foco em lógica básica, não programação complexa
2. **Simplicidade sobre Complexidade:** Priorizar clareza sobre brevidade
3. **Linguagem Humana:** Código que parece conversa
4. **Zero Fricção Sintática:** Eliminar símbolos e palavras-chave complicadas
5. **Transpilação, não Interpretação:** Gerar Python, não executar diretamente

---

### 4.2 Conceito: "Python para Humanos"

Mython não é uma linguagem completamente nova. É **Python simplificado para humanos**.

**Exemplos:**
- `say` é `print` simplificado
- `ask` é `input` simplificado
- `func` é `def` simplificado
- Sintaxe idêntica ao Python para estruturas complexas

---

### 4.3 Conceito: "Blocos + Frases"

Mython combina:
- **Blocos indentados** (estilo Python)
- **Frases naturais** (estilo linguagem humana)

**Exemplo:**
```mython
if idade > 18:
    say "Você é adulto"
else:
    say "Você é menor"
```

- Bloco: Indentação estilo Python
- Frase: "say" ao invés de "print"

---

## 5. Conceitos de Simplicidade

### 5.1 Redução de Sintaxe

**Eliminado:**
- `{}` para blocos (usa indentação)
- `;` para terminar statements
- Tipos explícitos obrigatórios
- Parênteses desnecessários
- Símbolos estranhos

---

### 5.2 Palavras-chave Amigáveis

**Substituições:**
- `print` → `say`
- `input` → `ask`
- `def` → `func` (opcional)
- `import` → `use` (opcional)

---

### 5.3 Expressões Naturais

**Exemplos:**
- `idade > 18` (mantido - já é claro)
- `a + b` (mantido - já é claro)
- `not condição` (mantido - já é claro)

---

## 6. O que Foi Deixado de Fora

### 6.1 Recursos Avançados (Por enquanto)

- **Macros:** Planejado para futuro
- **Decorators avançados:** Simplificado
- **Metaclasses:** Não suportado
- **Descriptors:** Não suportado
- **Context managers avançados:** Simplificado

**Justificativa:** Foco em simplicidade e acessibilidade.

---

### 6.2 Recursos Complexos

- **Tipos estáticos:** Não suportado (mantém dinâmico)
- **Generics:** Não suportado
- **Protocols:** Não suportado
- **Structural subtyping:** Não suportado

**Justificativa:** Adiciona complexidade desnecessária.

---

### 6.3 Recursos Técnicos

- **Bytecode direto:** Usa transpilação para Python
- **VM própria:** Usa Python runtime
- **GC customizado:** Usa Python GC
- **JIT compiler:** Usa Python JIT (PyPy)

**Justificativa:** Foco em simplicidade de uso, não em implementação.

---

## 7. Conceitos Fundamentais

### 7.1 Transpilação

**Conceito:** Mython não executa código diretamente. Ela transpila para Python.

**Fluxo:**
```
Mython (.logic) → Transpiler → Python (.py) → Python Runtime
```

**Vantagens:**
- Compatibilidade total com Python
- Acesso a todas as bibliotecas Python
- Performance nativa do Python
- Debugging com ferramentas Python

---

### 7.2 Indentação como Sintaxe

**Conceito:** Indentação define blocos, não símbolos.

**Exemplo:**
```mython
if condição:
    ação1  # 4 espaços = dentro do if
    ação2  # 4 espaços = dentro do if
ação3  # 0 espaços = fora do if
```

**Justificativa:** Visualmente claro, sem símbolos extras.

---

### 7.3 Expressões como Python

**Conceito:** Expressões aritméticas, lógicas e de comparação são idênticas ao Python.

**Exemplo:**
```mython
idade + 1
idade > 18
a and b
not condição
```

**Justificativa:** Já são claras e intuitivas.

---

### 7.4 Statements como Frases

**Conceito:** Statements principais usam palavras amigáveis.

**Exemplo:**
```mython
say "Hello"  # print("Hello")
ask nome "Digite seu nome: "  # nome = input("Digite seu nome: ")
```

**Justificativa:** Mais natural para iniciantes.

---

## 8. Decisões Técnicas

### 8.1 Parser LALR

**Decisão:** Usar Lark com parser LALR.

**Justificativa:**
- Eficiente
- Determinístico
- Fácil de debugar
- Sem ambiguidades

---

### 8.2 Indenter Customizado

**Decisão:** Usar `lark.indenter.Indenter` com `MythonIndenter`.

**Justificativa:**
- Suporte oficial do Lark
- Gera `INDENT`/`DEDENT` automaticamente
- Compatível com Python

---

### 8.3 Transformer Recursivo

**Decisão:** Transformer não chama `self.transform()` dentro dos métodos.

**Justificativa:**
- Lark já faz transformação recursiva
- Evita re-transformação
- Mais eficiente
- Menos bugs

---

### 8.4 Resolução de Conflitos

**Decisão:** Resolver conflitos Reduce/Reduce na gramática.

**Estratégias:**
1. `dict_literal` usa `pair` - distingue de `set_literal`
2. `tuple_literal` requer vírgula final - distingue de `paren_expr`
3. `set_literal` removido de `atom` - evita conflito com `set_stmt`

**Justificativa:** Mantém gramática LALR válida sem ambiguidades.

---

## 9. Compromissos

### 9.1 Simplicidade vs. Poder

**Compromisso:** Priorizar simplicidade, mas manter compatibilidade com Python.

**Exemplo:** Usar `say` ao invés de `print`, mas gerar `print()` no Python.

---

### 9.2 Naturalidade vs. Precisão

**Compromisso:** Priorizar naturalidade, mas manter precisão técnica.

**Exemplo:** `ask number idade` é mais natural que `idade = int(input())`, mas gera código preciso.

---

### 9.3 Acessibilidade vs. Flexibilidade

**Compromisso:** Priorizar acessibilidade, mas permitir flexibilidade.

**Exemplo:** Aceitar tanto `func` quanto `def`, tanto `use` quanto `import`.

---

## 10. Princípios de Design

### 10.1 Princípio de Menor Surpresa

**Conceito:** O comportamento deve ser o que o usuário espera.

**Exemplos:**
- `say "Hello"` gera `print("Hello")` (esperado)
- `idade > 18` gera `idade > 18` (esperado)
- `a + b` gera `a + b` (esperado)

---

### 10.2 Princípio de Simplicidade

**Conceito:** A solução mais simples é a melhor.

**Exemplos:**
- Usar indentação ao invés de `{}`
- Usar `say` ao invés de `print`
- Usar palavras-chave simples

---

### 10.3 Princípio de Compatibilidade

**Conceito:** Manter compatibilidade máxima com Python.

**Exemplos:**
- Expressões idênticas ao Python
- Estruturas de dados idênticas ao Python
- Semântica idêntica ao Python

---

## 11. Referências

- **Filosofia Original:** `PHILOSOPHY.md`
- **Gramática:** `MYTHON_GRAMMAR_SPEC.md`
- **Transformer:** `MYTHON_TRANSFORMER_SPEC.md`
- **Especificação:** `MYTHON_SPEC.md`

---

**Última atualização:** 2025-01-27  
**Versão:** 1.0  
**Status:** ✅ Estável - Pronto para expansão


# 🔧 Correção de Bugs - Em Progresso

## Status Atual

Aplicando correções conforme instruções detalhadas do usuário, mas encontrando **conflitos Reduce/Reduce** na gramática Lark (LALR parser).

## Bugs a Corrigir

### BUG 1: `set_assign_stmt` - Erro de parsing
- **Problema:** `Unexpected token Token('$END')` - parser espera `_NEWLINE` após `expr`
- **Solução proposta:** Adicionar `_NEWLINE?` após `expr` na regra `set_assign_stmt`
- **Status:** ⚠️ **CONFLITO** - Conflitos Reduce/Reduce ao adicionar literais em `atom`

### BUG 2: `call_stmt` - Erro com dicionários
- **Problema:** `Unexpected token Token('COLON', ':')` - parser não reconhece dicionários em argumentos
- **Solução proposta:** Incluir `dict_literal` em `expr` usando `pair (STRING ":" expr)`
- **Status:** ⚠️ **CONFLITO** - Conflitos Reduce/Reduce ao incluir `dict_literal` em `atom` ou `expr`

## Conflitos Encontrados

### Conflito 1: `tuple_literal` vs `paren_expr`
- Ambos usam `()` - `(expr)` pode ser tupla OU expressão com parênteses
- Python: `()` é tupla vazia, `(expr,)` é tupla com 1 elemento, `(expr)` é expressão com parênteses

### Conflito 2: `dict_literal` vs `set_literal`
- Ambos usam `{}` - `{}` pode ser dict vazio OU set vazio
- Python: `{}` é dict vazio, `{value}` é set, `{"key": value}` é dict

### Conflito 3: `set_stmt` vs `set_literal` em `atom`
- `set_stmt: SET NAME EQUAL set_literal` conflita com `atom: set_literal`
- Ambos podem começar com `SET` terminal

## Próximos Passos

1. **Resolver conflitos de ambiguidade** na gramática
2. **Simplificar regras** para evitar conflitos Reduce/Reduce
3. **Testar correções** após resolver conflitos

## Abordagem Atual

Tentando incluir `dict_literal` diretamente em `expr` (não em `atom`) para evitar conflitos, mas ainda há problemas com `tuple_literal` vs `paren_expr`.

**Última atualização:** 2025-01-27
**Status:** Em progresso - resolvendo conflitos de gramática


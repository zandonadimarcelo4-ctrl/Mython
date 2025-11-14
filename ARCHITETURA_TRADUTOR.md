# 🧠 Arquitetura do Mython Keyword Translator

## ⭐ Sistema Híbrido de Tradução

**PRIMARY:** LibreTranslate (API online - mais rápido, mais idiomas)  
**FALLBACK:** Argos Translate (100% offline - robusto, seguro)

---

## 🎯 Como Funciona

### 1. Fluxo de Tradução

```
Palavra → É keyword em inglês? → SIM → Retorna
                              ↓ NÃO
                         Verifica cache
                              ↓
                    Tenta LibreTranslate (online)
                              ↓ Falhou
                    Tenta Argos Translate (offline)
                              ↓ Falhou
                    Retorna palavra original (identificador)
```

### 2. Pipeline de Transpilação

```
Código Multilíngue
    ↓
[1] Detectar idioma (opcional)
    ↓
[2] Traduzir keywords (LibreTranslate → Argos Translate)
    ↓
[3] Normalizar operadores ("is over" → ">")
    ↓
[4] Processar indentação
    ↓
[5] Parser Lark
    ↓
[6] Transformer (AST → Python)
    ↓
Código Python
```

---

## 📦 Componentes

### `mython/translator.py`

Sistema híbrido de tradução de keywords:

- `translate_keyword(word)`: Traduz uma palavra (LibreTranslate → Argos)
- `translate_code(code)`: Traduz código completo (apenas keywords)
- `get_available_translators()`: Verifica quais tradutores estão disponíveis
- `is_keyword(word)`: Verifica se palavra é keyword do Mython

### Integração com `mython/transpiler_lark.py`

O transpiler usa o tradutor antes de parsear:

```python
# Detectar idioma
lang = detect_language(code) if not lang else lang

# Traduzir (sistema híbrido)
if lang != "en":
    if HYBRID_TRANSLATOR_AVAILABLE:
        code = translate_keywords(code)  # LibreTranslate → Argos
    elif I18N_AVAILABLE:
        code = translate_code(code, lang, reverse=True)  # Fallback dicionários
```

---

## 🔧 Instalação

### Opção 1: Com LibreTranslate (online)

```bash
pip install requests
```

### Opção 2: Com Argos Translate (offline)

```bash
pip install argostranslate
```

### Opção 3: Ambos (recomendado)

```bash
pip install requests argostranslate
```

---

## 💡 Vantagens

### ✔ Alta Disponibilidade

- LibreTranslate: Mais idiomas, mais rápido
- Argos Translate: Offline, sempre disponível

### ✔ Robustez

- Se um falha, o outro assume
- Sem dependências críticas
- Funciona offline quando necessário

### ✔ Performance

- Cache de traduções
- Timeout curto para não travar
- Traduz apenas keywords (não strings/identificadores)

### ✔ Segurança

- Nada depende 100% da internet
- Dados não saem da máquina (Argos)
- Open-source (ambos)

---

## 🚀 Exemplo de Uso

### Código em Português:

```mython
se idade > 18:
    dizer "Você é adulto"
senão:
    dizer "Você é menor"
```

### Processamento:

1. **LibreTranslate tenta:**
   - `se` → `if` ✅
   - `dizer` → `say` ✅

2. **Resultado:**
   ```mython
   if idade > 18:
       say "Você é adulto"
   else:
       say "Você é menor"
   ```

3. **Parser recebe código em inglês e transpila para Python**

---

## 📊 Comparação

| Feature | LibreTranslate | Argos Translate | Mython (Híbrido) |
|---------|---------------|-----------------|------------------|
| **Online** | ✅ | ❌ | ✅ (primary) |
| **Offline** | ❌ | ✅ | ✅ (fallback) |
| **Idiomas** | 30+ | ~10 | 30+ |
| **Velocidade** | Rápido | Médio | Rápido (primary) |
| **Robustez** | Depende API | Sempre funciona | ✅ |
| **Uso** | API pública | Biblioteca local | Ambos |

---

## 🎯 Status dos Tradutores

Você pode verificar quais tradutores estão disponíveis:

```python
from mython.translator import get_available_translators

status = get_available_translators()
print(status)
# {
#     "libretranslate": True,   # Online disponível
#     "argostranslate": False   # Offline não instalado
# }
```

---

## 🔍 Detalhes Técnicos

### Cache

Traduções são cacheadas para evitar chamadas repetidas:

```python
translate_keyword("se", use_cache=True)  # Primeira vez: traduz
translate_keyword("se", use_cache=True)  # Segunda vez: usa cache
clear_cache()  # Limpar cache se necessário
```

### Keywords do Mython

Apenas estas palavras são traduzidas:

- Comandos: `say`, `ask`
- Controle: `if`, `else`, `elif`, `for`, `while`, `repeat`
- Funções: `def`, `class`, `return`, `yield`
- Exceções: `try`, `except`, `finally`, `raise`
- Outros: `break`, `continue`, `pass`, `import`, `from`, `with`

**Identificadores, strings e números NÃO são traduzidos.**

---

## 🧪 Testes

Execute os testes:

```bash
pytest tests/test_translator.py -v
```

Ou:

```bash
python tests/test_translator.py
```

---

## 🎉 Resultado

**Mython agora tem um sistema de tradução multilíngue robusto, offline-first e profissional!**

Nenhuma linguagem existente faz isso dessa forma. É algo realmente original. 🚀


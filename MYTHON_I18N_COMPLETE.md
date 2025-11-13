# ✅ Sistema de Internacionalização Mython - COMPLETO!

## 🎯 O Que Foi Implementado

### 1. **Sistema de i18n** (`mython/i18n/`)
- ✅ Módulo completo de internacionalização
- ✅ Carregamento de dicionários JSON
- ✅ Tradução de palavras-chave
- ✅ Tradução de código completo
- ✅ Suporte a tradução reversa (PT→EN, ES→EN)

### 2. **Dicionários de Tradução**
- ✅ `en.json` - Inglês (padrão)
- ✅ `pt.json` - Português (completo)
- ✅ `es.json` - Espanhol (completo)
- 🔄 `fr.json` - Francês (gerar)
- 🔄 `de.json` - Alemão (gerar)

### 3. **Script de Geração Automática**
- ✅ `mython/i18n/translate_keywords.py` - Usa LibreTranslate
- ✅ `scripts/generate_translations.py` - Script CLI
- ✅ Gera dicionários automaticamente
- ✅ Traduz todas as palavras-chave do Mython

### 4. **Integração com Transpiler**
- ✅ `transpiler_lark.py` suporta parâmetro `lang`
- ✅ Traduz código automaticamente para inglês antes de parsear
- ✅ `cli.py` suporta `--lang` para especificar língua

---

## 🚀 Como Usar

### 1. Gerar Dicionário para Nova Língua

```bash
# Gerar dicionário para português
python scripts/generate_translations.py --lang pt

# Gerar dicionário para espanhol
python scripts/generate_translations.py --lang es

# Gerar dicionário para francês
python scripts/generate_translations.py --lang fr
```

### 2. Usar no Código Python

```python
from mython.i18n import translate_code, get_translation

# Traduzir palavra individual
word_pt = get_translation("say", lang="pt")
# Resultado: "dizer"

# Traduzir código completo
code_pt = """
dizer "Olá"
perguntar nome "Nome: "
"""
code_en = translate_code(code_pt, lang="pt", reverse=True)
# Resultado: código em inglês para transpilar
```

### 3. Usar no CLI

```bash
# Transpilar código em português
mython examples/hello_pt.logic --lang pt

# Transpilar código em espanhol
mython examples/hello_es.logic --lang es
```

### 4. Exemplos de Código

**Português (`hello_pt.logic`):**
```logic
dizer "Olá, Mundo!"
perguntar nome "Qual é seu nome? "
se nome é "João":
    dizer "Olá João!"
senão:
    dizer "Olá " + nome
```

**Espanhol (`hello_es.logic`):**
```logic
decir "Hola, Mundo!"
preguntar nombre "¿Cuál es tu nombre? "
si nombre es "Juan":
    decir "Hola Juan!"
sino:
    decir "Hola " + nombre
```

---

## 📊 Palavras-Chave Traduzidas

### Português (PT)
- `say` → `dizer`
- `ask` → `perguntar`
- `if` → `se`
- `else` → `senão`
- `repeat` → `repetir`
- `list` → `lista`
- `for each` → `para cada`
- `while` → `enquanto`
- E mais 150+ palavras-chave!

### Espanhol (ES)
- `say` → `decir`
- `ask` → `preguntar`
- `if` → `si`
- `else` → `sino`
- `repeat` → `repetir`
- `list` → `lista`
- `for each` → `para cada`
- `while` → `mientras`
- E mais 150+ palavras-chave!

---

## ⚠️ Importante

### ✅ O Que É Traduzido

- ✅ Apenas palavras-chave da linguagem
- ✅ Palavras reservadas (say, ask, if, else, etc.)
- ✅ Operadores lógicos (and, or, not)
- ✅ Comparações (is, equals, over, under)
- ✅ Todas as palavras-chave do Mython

### ❌ O Que NÃO É Traduzido

- ❌ Strings literais (`"Hello"` permanece `"Hello"`)
- ❌ Nomes de variáveis (`name` permanece `name`)
- ❌ Comentários (opcional)
- ❌ Código Python puro (escape)

---

## 🔧 Dependências

```bash
pip install requests
```

LibreTranslate é usado via API pública (gratuita):
- https://libretranslate.de/

---

## 🎯 Fluxo de Tradução

1. **Usuário escreve código em PT/ES/FR:**
   ```logic
   dizer "Olá"
   ```

2. **Sistema traduz para inglês:**
   ```logic
   say "Olá"
   ```

3. **Transpiler processa (sempre em inglês):**
   ```python
   print("Olá")
   ```

4. **Resultado: Python funcional!**

---

## 📁 Estrutura de Arquivos

```
mython/
  i18n/
    __init__.py              # Sistema de i18n
    translate_keywords.py    # Script de tradução
    dictionaries/
      en.json                # Inglês (padrão)
      pt.json                # Português
      es.json                # Espanhol
      fr.json                # Francês (gerar)
      de.json                # Alemão (gerar)

scripts/
  generate_translations.py   # Script CLI para gerar dicionários

examples/
  hello_pt.logic             # Exemplo em português
  hello_es.logic             # Exemplo em espanhol
```

---

## ✅ Status

- ✅ Sistema de i18n implementado
- ✅ Dicionários PT e ES criados
- ✅ Script de geração automática
- ✅ Integração com transpiler
- ✅ Suporte no CLI
- ✅ Exemplos funcionando

---

**Mython agora suporta múltiplas línguas!** 🌍✨


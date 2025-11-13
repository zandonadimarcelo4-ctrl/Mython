# 🌍 Mython i18n - Sistema de Internacionalização

## 🎯 O Que É

Sistema para traduzir **apenas as palavras-chave** do Mython para outras línguas, mantendo a sintaxe e lógica intactas.

## ✅ Como Funciona

### 1. **Tradução de Palavras-Chave Apenas**

O sistema traduz **só as palavras reservadas**, não código, não lógica, não frases.

**Exemplo em Português:**
```logic
dizer "Olá, Mundo!"
perguntar nome "Qual é seu nome? "
se idade é maior que 18:
    dizer "Você é adulto"
senão:
    dizer "Você é menor"
```

**Exemplo em Espanhol:**
```logic
decir "Hola, Mundo!"
preguntar nombre "¿Cuál es tu nombre? "
si edad es mayor que 18:
    decir "Eres adulto"
sino:
    decir "Eres menor"
```

### 2. **Dicionários JSON**

Cada língua tem um arquivo JSON com as traduções:

```json
{
  "say": "dizer",
  "ask": "perguntar",
  "if": "se",
  "else": "senão",
  "repeat": "repetir"
}
```

### 3. **Tradução Automática com LibreTranslate**

Script que usa LibreTranslate para gerar dicionários automaticamente:

```bash
python scripts/generate_translations.py --lang pt
python scripts/generate_translations.py --lang es
python scripts/generate_translations.py --lang fr
```

## 📁 Estrutura

```
mython/
  i18n/
    __init__.py          # Sistema de i18n
    translate_keywords.py # Script de tradução
    dictionaries/
      en.json            # Inglês (padrão)
      pt.json            # Português
      es.json            # Espanhol
      fr.json            # Francês (gerar)
      de.json            # Alemão (gerar)
```

## 🚀 Como Usar

### Gerar Dicionário para Nova Língua

```bash
# Gerar dicionário para português
python scripts/generate_translations.py --lang pt

# Gerar dicionário para espanhol
python scripts/generate_translations.py --lang es

# Gerar dicionário para francês
python scripts/generate_translations.py --lang fr
```

### Usar no Código Python

```python
from mython.i18n import translate_code, get_translation

# Traduzir código completo
code_pt = translate_code("say 'Hello'", lang="pt")
# Resultado: "dizer 'Hello'"

# Traduzir palavra individual
word_pt = get_translation("say", lang="pt")
# Resultado: "dizer"
```

### Integrar com Transpiler

O transpiler pode ser atualizado para aceitar código em múltiplas línguas:

```python
from mython.i18n import translate_code
from mython.transpiler_lark import transpile_file

# Código em português
code_pt = """
dizer "Olá"
perguntar nome "Nome: "
se nome é "João":
    dizer "Olá João!"
"""

# Traduzir para inglês antes de transpilar
code_en = translate_code(code_pt, lang="pt", reverse=True)
python_code = transpile_file(code_en)
```

## 📊 Línguas Suportadas

- ✅ **en** - English (padrão)
- ✅ **pt** - Português
- ✅ **es** - Español
- 🔄 **fr** - Français (gerar)
- 🔄 **de** - Deutsch (gerar)
- 🔄 **it** - Italiano (gerar)

## ⚠️ Importante

### ✅ O Que É Traduzido

- Apenas palavras-chave da linguagem
- Palavras reservadas (say, ask, if, else, etc.)
- Operadores lógicos (and, or, not)
- Comparações (is, equals, over, under)

### ❌ O Que NÃO É Traduzido

- Strings literais (`"Hello"` permanece `"Hello"`)
- Nomes de variáveis (`name` permanece `name`)
- Comentários (opcional, pode ser traduzido depois)
- Código Python puro (escape)

## 🔧 Dependências

```bash
pip install requests
```

LibreTranslate é usado via API pública (gratuita):
- https://libretranslate.de/

## 🎯 Exemplo Completo

### Código em Inglês:
```logic
say "Hello, World!"
ask name "What is your name? "
if name is "Alice":
    say "Hello Alice!"
else:
    say "Hello stranger!"
```

### Código em Português:
```logic
dizer "Hello, World!"
perguntar nome "What is your name? "
se nome é "Alice":
    dizer "Hello Alice!"
senão:
    dizer "Hello stranger!"
```

### Código em Espanhol:
```logic
decir "Hello, World!"
preguntar nombre "What is your name? "
si nombre es "Alice":
    decir "Hello Alice!"
sino:
    decir "Hello stranger!"
```

**Note:** As strings literais não são traduzidas (isso é intencional - você pode traduzi-las manualmente se quiser).

## 🚀 Próximos Passos

1. ✅ Sistema básico implementado
2. ✅ Dicionários PT e ES criados
3. 🔄 Integrar com transpiler
4. 🔄 Adicionar suporte a mais línguas
5. 🔄 Interface Streamlit multi-idioma

---

**Mython agora suporta múltiplas línguas!** 🌍✨


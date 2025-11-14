"""
Mython Keyword Translator - Sistema híbrido de tradução
PRIMARY: LibreTranslate (mais rápido, mais idiomas)
FALLBACK: Argos Translate (100% offline)
"""

import re
from typing import Optional, Set, Dict

# Palavras-chave do Mython em inglês
MYTHON_KEYWORDS: Set[str] = {
    # Comandos básicos
    "say", "ask",
    # Controle de fluxo
    "if", "else", "elif", "for", "while", "repeat",
    # Funções e classes
    "def", "class", "return", "yield", "await",
    # Exceções
    "try", "except", "finally", "raise",
    # Controle
    "break", "continue", "pass",
    # Operadores
    "and", "or", "not", "in", "is",
    # Imports
    "import", "from", "as",
    # Outros
    "with", "match", "case", "lambda",
}

# Cache de traduções para evitar chamadas repetidas
_translation_cache: Dict[str, str] = {}


def translate_libre(word: str, source_lang: str = "auto", target_lang: str = "en") -> Optional[str]:
    """
    Traduz palavra usando LibreTranslate API (online).
    
    Args:
        word: Palavra a traduzir
        source_lang: Idioma de origem (padrão: "auto" para detectar)
        target_lang: Idioma de destino (padrão: "en")
    
    Returns:
        Palavra traduzida ou None em caso de erro
    """
    try:
        import requests
        
        response = requests.post(
            "https://libretranslate.com/translate",
            json={
                "q": word,
                "source": source_lang,
                "target": target_lang,
                "format": "text"
            },
            timeout=5  # Timeout curto para não travar
        )
        
        if response.status_code == 200:
            result = response.json()
            translated = result.get("translatedText", "").strip().lower()
            return translated if translated else None
        
        return None
    except Exception:
        # Silenciosamente falha - usar fallback
        return None


def translate_argos(word: str, source_lang: str = "auto", target_lang: str = "en") -> Optional[str]:
    """
    Traduz palavra usando Argos Translate (offline).
    
    Args:
        word: Palavra a traduzir
        source_lang: Idioma de origem (padrão: "auto" para detectar)
        target_lang: Idioma de destino (padrão: "en")
    
    Returns:
        Palavra traduzida ou None em caso de erro
    """
    try:
        import argostranslate.translate
        
        # Se source_lang é "auto", tentar detectar
        if source_lang == "auto":
            # Lista de idiomas comuns do Argos
            common_langs = ["pt", "es", "fr", "de", "it", "ru", "zh", "ja"]
            for lang in common_langs:
                try:
                    translated = argostranslate.translate.translate(word, lang, target_lang)
                    if translated.lower() in MYTHON_KEYWORDS:
                        return translated.lower()
                except:
                    continue
            # Tentar tradução genérica
            translated = argostranslate.translate.translate(word, source_lang, target_lang)
        else:
            translated = argostranslate.translate.translate(word, source_lang, target_lang)
        
        return translated.strip().lower() if translated else None
    except ImportError:
        # Argos não instalado
        return None
    except Exception:
        # Falha na tradução
        return None


def translate_keyword(word: str, use_cache: bool = True) -> str:
    """
    Traduz uma palavra para keyword do Mython (inglês).
    
    Sistema híbrido:
    1. Verifica se já é keyword em inglês
    2. Verifica cache
    3. Tenta LibreTranslate (online)
    4. Fallback para Argos Translate (offline)
    5. Se não traduzir, retorna palavra original (identificador)
    
    Args:
        word: Palavra a traduzir
        use_cache: Se True, usa cache de traduções anteriores
    
    Returns:
        Keyword traduzida em inglês ou palavra original se não for keyword
    """
    # Normalizar: minúsculas, sem espaços
    word = word.strip().lower()
    
    # 1. Já é keyword em inglês?
    if word in MYTHON_KEYWORDS:
        return word
    
    # 2. Verificar cache
    if use_cache and word in _translation_cache:
        cached = _translation_cache[word]
        if cached in MYTHON_KEYWORDS:
            return cached
    
    # 3. Tentar LibreTranslate (PRIMARY - online)
    translated = translate_libre(word)
    if translated and translated in MYTHON_KEYWORDS:
        _translation_cache[word] = translated
        return translated
    
    # 4. Fallback Argos Translate (offline)
    translated = translate_argos(word)
    if translated and translated in MYTHON_KEYWORDS:
        _translation_cache[word] = translated
        return translated
    
    # 5. Não é keyword → é variável/identificador normal
    return word


def translate_code(code: str, use_cache: bool = True) -> str:
    """
    Traduz código Mython multilíngue para inglês.
    
    Apenas palavras-chave são traduzidas. Identificadores, strings
    e outros tokens permanecem inalterados.
    
    Args:
        code: Código Mython em qualquer língua
        use_cache: Se True, usa cache de traduções
    
    Returns:
        Código traduzido para inglês (apenas keywords)
    """
    lines = code.split('\n')
    translated_lines = []
    
    for line in lines:
        # Encontrar todas as palavras na linha
        words = re.findall(r'\b\w+\b', line)
        
        # Traduzir cada palavra
        translated_line = line
        for word in words:
            # Tentar traduzir apenas se parece ser keyword (não é número, não começa com maiúscula após primeira letra)
            if word.isalpha() and not word[0].isupper():
                translated_word = translate_keyword(word, use_cache=use_cache)
                # Substituir apenas se diferente (foi traduzido)
                if translated_word != word.lower():
                    # Substituir palavra mantendo maiúsculas/minúsculas originais
                    pattern = r'\b' + re.escape(word) + r'\b'
                    translated_line = re.sub(pattern, translated_word, translated_line, count=1)
        
        translated_lines.append(translated_line)
    
    return '\n'.join(translated_lines)


def clear_cache():
    """Limpa o cache de traduções."""
    global _translation_cache
    _translation_cache.clear()


def is_keyword(word: str) -> bool:
    """
    Verifica se uma palavra é uma keyword do Mython.
    
    Args:
        word: Palavra a verificar
    
    Returns:
        True se for keyword, False caso contrário
    """
    return word.lower() in MYTHON_KEYWORDS


def get_available_translators() -> Dict[str, bool]:
    """
    Verifica quais tradutores estão disponíveis.
    
    Returns:
        Dicionário com status de cada tradutor:
        {
            "libretranslate": True/False,
            "argostranslate": True/False
        }
    """
    available = {
        "libretranslate": False,
        "argostranslate": False,
    }
    
    # Verificar LibreTranslate
    try:
        import requests
        # Testar se consegue fazer uma requisição
        response = requests.get("https://libretranslate.com", timeout=2)
        available["libretranslate"] = response.status_code < 500
    except:
        pass
    
    # Verificar Argos Translate
    try:
        import argostranslate.translate
        available["argostranslate"] = True
    except ImportError:
        pass
    
    return available


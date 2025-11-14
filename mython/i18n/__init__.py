"""
Mython i18n - Sistema de internacionalização
Tradução de palavras-chave para múltiplas línguas
"""

from pathlib import Path
import json
import unicodedata

# Diretório base para dicionários
_I18N_DIR = Path(__file__).parent / "dictionaries"

# Carregar dicionários
def load_dictionary(lang: str) -> dict:
    """Carrega dicionário de tradução para uma língua."""
    dict_file = _I18N_DIR / f"{lang}.json"
    if dict_file.exists():
        with open(dict_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}

def remove_accents(text: str) -> str:
    """Remove acentos de uma string."""
    # Normalizar para NFD (decompor) e remover marcas diacríticas
    nfd = unicodedata.normalize('NFD', text)
    return ''.join(char for char in nfd if unicodedata.category(char) != 'Mn')

def get_translation(word: str, lang: str = "en") -> str:
    """Obtém tradução de uma palavra-chave."""
    if lang == "en":
        return word  # Inglês é o padrão
    
    dictionary = load_dictionary(lang)
    # Tentar encontrar com acento primeiro
    if word in dictionary:
        return dictionary[word]
    # Tentar sem acento
    word_no_accents = remove_accents(word)
    if word_no_accents in dictionary:
        return dictionary[word_no_accents]
    return word  # Retorna a palavra original se não encontrar

def translate_code(code: str, lang: str = "en", reverse: bool = False, source_lang: str = None) -> str:
    """
    Traduz código Mython de uma língua para outra (bidirecional).
    
    Args:
        code: Código Mython
        lang: Código da língua de destino (pt, es, fr, etc.)
        reverse: Se True, traduz de volta para inglês (de lang para en)
        source_lang: Código da língua de origem (None = detectar automaticamente)
    
    Returns:
        Código traduzido
    """
    # Se não é reverse e destino é inglês, não traduzir
    if lang == "en" and not reverse:
        return code
    
    # Se source_lang não foi especificado, detectar automaticamente
    if source_lang is None:
        source_lang = detect_language(code)
    
    # Se source_lang == lang, não traduzir
    if source_lang == lang and not reverse:
        return code
    
    # Se reverse, traduzir de lang para en
    if reverse:
        dictionary = load_dictionary(lang)
        if not dictionary:
            return code
    else:
        # Traduzir de source_lang (geralmente en) para lang
        # Se source_lang é en, usar dicionário normal
        if source_lang == "en":
            dictionary = load_dictionary(lang)
            if not dictionary:
                return code
        else:
            # Se source_lang não é en, primeiro traduzir para en, depois para lang
            # Mas isso é complexo, vamos fazer direto do source_lang para lang
            # Carregar dicionário de source_lang e criar inverso
            source_dict = load_dictionary(source_lang)
            target_dict = load_dictionary(lang)
            if not source_dict or not target_dict:
                return code
            
            # Criar mapeamento: source_lang -> en -> lang
            # Primeiro, traduzir source_lang para en (inverso)
            inverted_source = {v: k for k, v in source_dict.items()}
            # Depois, traduzir en para lang
            # Criar dicionário composto: source_lang -> lang
            dictionary = {}
            for source_word, en_word in inverted_source.items():
                if en_word in target_dict:
                    dictionary[source_word] = target_dict[en_word]
            
            if not dictionary:
                return code
    
    lines = code.split('\n')
    translated_lines = []
    
    # Se reverse, criar dicionário invertido (lang -> en)
    if reverse:
        # Criar dicionário invertido básico
        inverted_dict = {v: k for k, v in dictionary.items()}
        # Adicionar versões sem acentos para facilitar tradução
        # Se a palavra tem acento, adicionar versão sem acento que aponta para a mesma tradução
        for word_lang, word_en in list(inverted_dict.items()):
            word_lang_no_accents = remove_accents(word_lang)
            if word_lang_no_accents != word_lang and word_lang_no_accents not in inverted_dict:
                inverted_dict[word_lang_no_accents] = word_en
        dictionary = inverted_dict
        if not dictionary:
            return code
    else:
        # Não é reverse, usar dicionário normal
        pass
    
    import re
    
    for line in lines:
        translated_line = line
        
        # Primeiro, encontrar todas as palavras na linha
        words_in_line = re.findall(r'\b\w+\b', translated_line)
        
        # Criar mapeamento de palavras normalizadas para suas versões originais
        word_to_normalized = {}
        for original_word in words_in_line:
            normalized = remove_accents(original_word)
            word_to_normalized[original_word] = normalized
        
        # Processar cada palavra encontrada na linha
        # Ordenar por tamanho (maior primeiro) para evitar substituições parciais
        words_to_process = sorted(set(words_in_line), key=len, reverse=True)
        
        for original_word in words_to_process:
            normalized_word = word_to_normalized[original_word]
            
            # Buscar no dicionário: primeiro pela palavra original, depois pela normalizada
            translation = None
            dict_key = None
            
            # Tentar palavra original
            if original_word in dictionary:
                translation = dictionary[original_word]
                dict_key = original_word
            # Tentar palavra normalizada
            elif normalized_word in dictionary:
                translation = dictionary[normalized_word]
                dict_key = normalized_word
            # Tentar normalizada de todas as palavras do dicionário
            else:
                for dict_word, dict_translation in dictionary.items():
                    dict_normalized = remove_accents(dict_word)
                    if dict_normalized == normalized_word:
                        translation = dict_translation
                        dict_key = dict_word
                        break
            
            # Se encontrou tradução, substituir
            if translation:
                pattern = r'\b' + re.escape(original_word) + r'\b'
                translated_line = re.sub(pattern, translation, translated_line)
        
        translated_lines.append(translated_line)
    
    return '\n'.join(translated_lines)

# Línguas suportadas
SUPPORTED_LANGUAGES = {
    "en": "English",
    "pt": "Português",
    "es": "Español",
    "fr": "Français",
    "de": "Deutsch",
    "it": "Italiano",
}

def detect_language(code: str) -> str:
    """
    Detecta automaticamente a língua do código Mython.
    
    Analisa palavras-chave únicas de cada língua para determinar
    qual língua está sendo usada. Reconhece português, inglês e outras línguas.
    
    Args:
        code: Código Mython a analisar
    
    Returns:
        Código da língua detectada (en, pt, es, etc.) ou "en" se não detectar
    """
    # Palavras-chave únicas de cada língua (que não aparecem em outras)
    language_keywords = {
        "pt": ["dizer", "perguntar", "senão", "se", "é", "repetir", "enquanto", 
               "para", "cada", "lista", "adicionar", "remover", "definir", 
               "retornar", "classe", "tarefa", "tentar", "capturar", "sempre",
               "senao", "senao",  # sem acentos
               "perguntar número", "número"],  # combinações comuns
        "es": ["decir", "preguntar", "sino", "si", "es", "repetir", "mientras",
               "para", "cada", "lista", "añadir", "eliminar", "definir",
               "devolver", "clase", "tarea", "intentar", "capturar", "siempre"],
        "fr": ["dire", "demander", "sinon", "si", "est", "répéter", "pendant",
               "pour", "chaque", "liste", "ajouter", "supprimer", "définir",
               "retourner", "classe", "tâche", "essayer", "attraper", "toujours"],
        "de": ["sagen", "fragen", "sonst", "wenn", "ist", "wiederholen", "während",
               "für", "jede", "liste", "hinzufügen", "entfernen", "definieren",
               "zurückgeben", "klasse", "aufgabe", "versuchen", "fangen", "immer"],
        "it": ["dire", "chiedere", "altrimenti", "se", "è", "ripetere", "mentre",
               "per", "ogni", "lista", "aggiungere", "rimuovere", "definire",
               "restituire", "classe", "compito", "provare", "catturare", "sempre"],
    }
    
    # Palavras-chave do Mython em inglês (para distinguir de código Python puro)
    mython_keywords = ["say", "ask", "repeat", "define", "class", "if", "else", 
                       "for", "while", "def", "return", "try", "except"]
    
    # Contar ocorrências de palavras-chave de cada língua
    import re
    code_lower = code.lower()
    scores = {}
    
    # Encontrar todas as palavras no código (normalizadas)
    words_in_code = re.findall(r'\b\w+\b', code_lower)
    words_normalized = {w: remove_accents(w) for w in words_in_code}
    
    # Verificar palavras-chave Mython em inglês
    has_mython_keywords = any(kw in words_in_code for kw in mython_keywords)
    
    # Se tem palavras-chave Mython mas não tem palavras de outras línguas, é inglês
    if has_mython_keywords:
        scores["en"] = len([kw for kw in mython_keywords if kw in words_in_code])
    
    # Verificar outras línguas
    for lang, keywords in language_keywords.items():
        score = 0
        for keyword in keywords:
            keyword_lower = keyword.lower()
            keyword_normalized = remove_accents(keyword_lower)
            
            # Tentar encontrar palavra exata
            if keyword_lower in words_in_code:
                score += words_in_code.count(keyword_lower)
            # Tentar encontrar palavra normalizada
            elif keyword_normalized in words_normalized.values():
                # Contar quantas palavras normalizadas correspondem
                for word, word_norm in words_normalized.items():
                    if word_norm == keyword_normalized:
                        score += 1
        
        if score > 0:
            scores[lang] = scores.get(lang, 0) + score
    
    # Se não encontrou nenhuma palavra-chave, assumir inglês (código Mython padrão)
    if not scores:
        return "en"
    
    # Retornar a língua com maior score
    detected_lang = max(scores.items(), key=lambda x: x[1])[0]
    
    # Retornar a língua detectada
    return detected_lang


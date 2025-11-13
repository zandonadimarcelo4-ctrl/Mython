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

def translate_code(code: str, lang: str = "en", reverse: bool = False) -> str:
    """
    Traduz código Mython de uma língua para outra.
    
    Args:
        code: Código Mython
        lang: Código da língua de destino (pt, es, fr, etc.)
        reverse: Se True, traduz de volta para inglês (de lang para en)
    
    Returns:
        Código traduzido
    """
    if lang == "en" and not reverse:
        return code
    
    dictionary = load_dictionary(lang)
    if not dictionary:
        return code
    
    lines = code.split('\n')
    translated_lines = []
    
    # Se reverse, criar dicionário invertido
    if reverse:
        # Criar dicionário invertido básico
        inverted_dict = {v: k for k, v in dictionary.items()}
        # Adicionar versões sem acentos para facilitar tradução
        # Se a palavra tem acento, adicionar versão sem acento que aponta para a mesma tradução
        for word_pt, word_en in list(inverted_dict.items()):
            word_pt_no_accents = remove_accents(word_pt)
            if word_pt_no_accents != word_pt and word_pt_no_accents not in inverted_dict:
                inverted_dict[word_pt_no_accents] = word_en
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
    qual língua está sendo usada.
    
    Args:
        code: Código Mython a analisar
    
    Returns:
        Código da língua detectada (en, pt, es, etc.) ou "en" se não detectar
    """
    # Palavras-chave únicas de cada língua (que não aparecem em outras)
    language_keywords = {
        "pt": ["dizer", "perguntar", "senão", "se", "é", "repetir", "enquanto", 
               "para", "cada", "lista", "adicionar", "remover", "definir", 
               "retornar", "classe", "tarefa", "tentar", "capturar", "sempre"],
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
    
    # Contar ocorrências de palavras-chave de cada língua
    import re
    code_lower = code.lower()
    scores = {}
    
    # Encontrar todas as palavras no código (normalizadas)
    words_in_code = re.findall(r'\b\w+\b', code_lower)
    words_normalized = {w: remove_accents(w) for w in words_in_code}
    
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
            scores[lang] = score
    
    # Se não encontrou nenhuma palavra-chave, assumir inglês
    if not scores:
        return "en"
    
    # Retornar a língua com maior score
    detected_lang = max(scores.items(), key=lambda x: x[1])[0]
    
    # Retornar a língua detectada (mesmo que seja apenas 1 palavra)
    # Se detectou alguma palavra-chave, provavelmente está correto
    return detected_lang


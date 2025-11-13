"""
Mython i18n - Sistema de internacionalização
Tradução de palavras-chave para múltiplas línguas
"""

from pathlib import Path
import json

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

def get_translation(word: str, lang: str = "en") -> str:
    """Obtém tradução de uma palavra-chave."""
    if lang == "en":
        return word  # Inglês é o padrão
    
    dictionary = load_dictionary(lang)
    return dictionary.get(word, word)  # Retorna a palavra original se não encontrar

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
    lines = code.split('\n')
    translated_lines = []
    
    # Se reverse, criar dicionário invertido
    if reverse:
        dictionary = {v: k for k, v in dictionary.items()}
    
    for line in lines:
        translated_line = line
        # Substituir palavras-chave (ordem importa: palavras mais longas primeiro)
        sorted_words = sorted(dictionary.keys(), key=len, reverse=True)
        for word in sorted_words:
            translation = dictionary[word]
            # Substituir apenas palavras completas (não partes de outras palavras)
            # Usar regex para substituição precisa
            import re
            # Substituir palavra completa (com limites de palavra)
            pattern = r'\b' + re.escape(word) + r'\b'
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
    code_lower = code.lower()
    scores = {}
    
    for lang, keywords in language_keywords.items():
        score = 0
        for keyword in keywords:
            # Usar regex para encontrar palavras completas
            import re
            pattern = r'\b' + re.escape(keyword) + r'\b'
            matches = len(re.findall(pattern, code_lower))
            score += matches
        
        if score > 0:
            scores[lang] = score
    
    # Se não encontrou nenhuma palavra-chave, assumir inglês
    if not scores:
        return "en"
    
    # Retornar a língua com maior score
    detected_lang = max(scores.items(), key=lambda x: x[1])[0]
    
    # Se o score for muito baixo (apenas 1-2 palavras), pode ser falso positivo
    # Nesse caso, assumir inglês
    if scores[detected_lang] < 2:
        return "en"
    
    return detected_lang


"""
Script para traduzir palavras-chave do Mython usando LibreTranslate
Gera dicionários JSON para múltiplas línguas
"""

import json
import requests
from pathlib import Path
from typing import Dict, List

# Palavras-chave do Mython (em inglês)
MYTHON_KEYWORDS = [
    # Saída
    "say", "print", "show", "display", "tell",
    
    # Entrada
    "ask", "get", "read", "prompt",
    
    # Condições
    "if", "when", "whenever", "else", "otherwise", "elif", "or",
    
    # Loops
    "repeat", "do", "loop", "for", "each", "every", "while", "through", "iterate", "over",
    
    # Controle
    "break", "stop", "continue", "skip", "next", "pass", "ignore",
    
    # Estruturas
    "list", "dict", "dictionary", "tuple", "set",
    
    # Operações
    "add", "append", "put", "insert", "remove", "delete", "take", "out",
    "to", "into", "from",
    
    # Funções
    "define", "function", "to", "create", "return", "give", "back", "send",
    
    # Classes
    "class", "init", "constructor", "initialize", "setup", "task", "method",
    "perform", "execute",
    
    # Atribuições
    "set", "assign", "let", "make", "store", "save",
    
    # Utilitários
    "wait", "pause", "sleep", "delay", "random", "number", "between", "pick",
    "choose", "select",
    
    # Arquivos
    "open", "file", "read", "load", "save", "write", "store",
    
    # Imports
    "use", "import", "require", "include",
    
    # Exceções
    "attempt", "try", "catch", "except", "handle", "error", "finally", "always",
    "raise", "throw",
    
    # Assert
    "assert", "check", "verify", "ensure",
    
    # Avançado
    "lambda", "yield", "produce", "generate", "match", "case",
    "async", "await",
    
    # Decorators
    "decorator", "staticmethod", "classmethod", "property", "abstractmethod", "dataclass",
    
    # Magic methods
    "magic",
    
    # Macros
    "sum", "plus", "subtract", "minus", "multiply", "times", "divide",
    "join", "combine", "split", "separate", "uppercase", "lowercase",
    "length", "size", "count", "items", "first", "last", "reverse", "flip",
    "sort", "order", "exists", "current", "time", "now", "date", "today",
    "exit", "program", "quit",
    
    # Operadores lógicos
    "and", "not", "in",
    
    # Comparações
    "is", "equals", "equal", "over", "under", "above", "below",
    "greater", "than", "less", "at", "least", "most",
    
    # Outros
    "as", "seconds", "second", "times", "time",
]

# API do LibreTranslate (pública e gratuita)
LIBRETRANSLATE_API = "https://libretranslate.de/translate"

def translate_word(word: str, target_lang: str, source_lang: str = "en") -> str:
    """
    Traduz uma palavra usando LibreTranslate.
    
    Args:
        word: Palavra a traduzir
        target_lang: Código da língua de destino (pt, es, fr, etc.)
        source_lang: Código da língua de origem (padrão: en)
    
    Returns:
        Palavra traduzida ou palavra original em caso de erro
    """
    if target_lang == source_lang:
        return word
    
    try:
        response = requests.post(
            LIBRETRANSLATE_API,
            json={
                "q": word,
                "source": source_lang,
                "target": target_lang,
                "format": "text"
            },
            timeout=10
        )
        
        if response.status_code == 200:
            result = response.json()
            translated = result.get("translatedText", word)
            # Limpar espaços extras
            translated = translated.strip()
            return translated
        else:
            print(f"Erro ao traduzir '{word}': {response.status_code}")
            return word
            
    except Exception as e:
        print(f"Erro ao traduzir '{word}': {e}")
        return word

def generate_dictionary(target_lang: str, keywords: List[str] = None) -> Dict[str, str]:
    """
    Gera dicionário de tradução para uma língua.
    
    Args:
        target_lang: Código da língua de destino
        keywords: Lista de palavras-chave (padrão: MYTHON_KEYWORDS)
    
    Returns:
        Dicionário {palavra_original: palavra_traduzida}
    """
    if keywords is None:
        keywords = MYTHON_KEYWORDS
    
    dictionary = {}
    
    print(f"\n🔄 Gerando dicionário para {target_lang}...")
    print(f"📝 Traduzindo {len(keywords)} palavras-chave...\n")
    
    for i, word in enumerate(keywords, 1):
        translated = translate_word(word, target_lang)
        dictionary[word] = translated
        print(f"[{i}/{len(keywords)}] {word} → {translated}")
    
    return dictionary

def save_dictionary(dictionary: Dict[str, str], lang: str, output_dir: Path = None):
    """Salva dicionário em arquivo JSON."""
    if output_dir is None:
        output_dir = Path(__file__).parent / "dictionaries"
    
    output_dir.mkdir(parents=True, exist_ok=True)
    output_file = output_dir / f"{lang}.json"
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(dictionary, f, ensure_ascii=False, indent=2)
    
    print(f"\n✅ Dicionário salvo em: {output_file}")

def main():
    """Função principal para gerar dicionários."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Gerar dicionários de tradução Mython")
    parser.add_argument("--lang", "-l", required=True, help="Código da língua (pt, es, fr, etc.)")
    parser.add_argument("--output", "-o", help="Diretório de saída (padrão: mython/i18n/dictionaries)")
    parser.add_argument("--keywords", "-k", help="Arquivo JSON com palavras-chave customizadas")
    
    args = parser.parse_args()
    
    # Carregar palavras-chave customizadas se fornecido
    keywords = MYTHON_KEYWORDS
    if args.keywords:
        with open(args.keywords, 'r', encoding='utf-8') as f:
            custom_keywords = json.load(f)
            keywords = custom_keywords if isinstance(custom_keywords, list) else list(custom_keywords.keys())
    
    # Gerar dicionário
    dictionary = generate_dictionary(args.lang, keywords)
    
    # Salvar
    output_dir = Path(args.output) if args.output else None
    save_dictionary(dictionary, args.lang, output_dir)
    
    print(f"\n🎉 Dicionário {args.lang} gerado com sucesso!")
    print(f"📊 Total de palavras: {len(dictionary)}")

if __name__ == "__main__":
    main()


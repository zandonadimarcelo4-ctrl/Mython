"""
Transpiler usando Lark - Versão robusta e formal.
"""

from pathlib import Path
from lark import Lark, Tree
from lark.exceptions import LarkError, UnexpectedToken, UnexpectedCharacters
import re

from .transformer_lark import MythonTransformer

# Importar sistema de i18n
try:
    from .i18n import translate_code, detect_language
    I18N_AVAILABLE = True
except ImportError:
    I18N_AVAILABLE = False
    detect_language = None


def normalize_operators(code: str) -> str:
    """
    Normaliza expressões naturais para operadores Python simples ANTES do parsing.
    Isso simplifica o transformer e garante que o Lark receba código já normalizado.
    """
    lines = code.split('\n')
    normalized_lines = []
    
    for line in lines:
        # Normalizar condições em if/elif/while
        # Buscar padrões como "if X is over Y:", "if X is greater than Y:", etc.
        if re.search(r'\b(if|elif|while|when|whenever)\s+', line, re.IGNORECASE):
            # Extrair a condição (tudo entre "if/elif/while" e ":")
            match = re.search(r'\b(if|elif|while|when|whenever)\s+(.+?)\s*:', line, re.IGNORECASE)
            if match:
                keyword = match.group(1)
                condition = match.group(2)
                
                # Normalizar a condição - substituir expressões naturais por operadores Python
                # Ordem importa: mais longas primeiro
                # IMPORTANTE: manter espaços ao redor dos operadores para o parser reconhecer
                replacements = [
                    (" is greater than or equal to ", " >= "),
                    (" greater than or equal to ", " >= "),
                    (" is less than or equal to ", " <= "),
                    (" less than or equal to ", " <= "),
                    (" is greater than ", " > "),
                    (" greater than ", " > "),
                    (" is less than ", " < "),
                    (" less than ", " < "),
                    (" is at least ", " >= "),
                    (" is at most ", " <= "),
                    (" is over ", " > "),
                    (" is above ", " > "),
                    (" above ", " > "),
                    (" is under ", " < "),
                    (" is below ", " < "),
                    (" is not equal to ", " != "),
                    (" not equal to ", " != "),
                    (" equals ", " == "),
                    (" equal to ", " == "),
                ]
                
                for old, new in replacements:
                    condition = condition.replace(old, new)
                
                # Substituir "is not in" primeiro (antes de "is not")
                condition = re.sub(r'\bis not in\b', ' not in ', condition, flags=re.IGNORECASE)
                condition = re.sub(r'\bis not\b', ' != ', condition, flags=re.IGNORECASE)
                condition = re.sub(r'\bis in\b', ' in ', condition, flags=re.IGNORECASE)
                
                # Substituir "is" simples por "==" (mas não se for parte de outras expressões)
                condition = re.sub(r'\bis\b(?!\s+(?:not|in|over|under|above|below|greater|less|at|equal))', ' == ', condition, flags=re.IGNORECASE)
                
                # Limpar espaços múltiplos
                condition = re.sub(r'\s+', ' ', condition).strip()
                
                # Reconstruir a linha
                line = line[:match.start(2)] + condition + line[match.end(2):]
        
        normalized_lines.append(line)
    
    return '\n'.join(normalized_lines)


def transpile_file(input_path: str, output_path: str = None, lang: str = None) -> str:
    """
    Transpila um arquivo .logic para Python usando Lark.
    
    Args:
        input_path: Caminho do arquivo .logic
        output_path: Caminho do arquivo .py de saída (opcional)
        lang: Código da língua do código (en, pt, es, etc.) - se None, detecta automaticamente
        
    Returns:
        Código Python gerado
        
    Raises:
        FileNotFoundError: Se o arquivo não existir
        SyntaxError: Se houver erro de sintaxe no código Mython
    """
    src_path = Path(input_path)
    
    if not src_path.exists():
        raise FileNotFoundError(f"Arquivo não encontrado: {input_path}")
    
    # Carregar gramática
    grammar_path = Path(__file__).parent / "grammar.lark"
    if not grammar_path.exists():
        raise FileNotFoundError(f"Gramática não encontrada: {grammar_path}")
    
    with open(grammar_path, 'r', encoding='utf-8') as f:
        grammar = f.read()
    
    # Criar parser
    try:
        parser = Lark(
            grammar,
            start='start',
            parser='earley',  # Earley para lidar com ambiguidades
            propagate_positions=True,  # Manter posições para erros
        )
    except Exception as e:
        raise RuntimeError(f"Erro ao criar parser: {e}")
    
    # Ler arquivo
    try:
        code = src_path.read_text(encoding='utf-8')
    except Exception as e:
        raise IOError(f"Erro ao ler arquivo: {e}")
    
    # Detectar língua automaticamente se não especificada
    if lang is None and I18N_AVAILABLE and detect_language:
        try:
            lang = detect_language(code)
            if lang != "en":
                # Opcional: imprimir língua detectada (pode ser removido em produção)
                pass
        except Exception as e:
            # Se falhar a detecção, assumir inglês
            lang = "en"
    elif lang is None:
        lang = "en"
    
    # Traduzir código para inglês se necessário (antes de parsear)
    if I18N_AVAILABLE and lang != "en":
        try:
            code = translate_code(code, lang=lang, reverse=True)
        except Exception as e:
            # Se falhar a tradução, continuar com código original
            import warnings
            warnings.warn(f"Não foi possível traduzir código de {lang} para inglês: {e}")
    
    # Normalizar operadores ANTES do parsing (simplifica o transformer)
    code = normalize_operators(code)
    
    # Parsear
    try:
        tree = parser.parse(code)
    except UnexpectedToken as e:
        # Erro de token inesperado
        expected = ", ".join(e.accepts or ["token"])
        found = e.token.value if e.token else "fim do arquivo"
        raise SyntaxError(
            f"Erro de sintaxe na linha {e.line}, coluna {e.column}:\n"
            f"  Esperado: {expected}\n"
            f"  Encontrado: {found}\n"
            f"  Contexto: {e.get_context(code)}"
        )
    except UnexpectedCharacters as e:
        # Erro de caractere inesperado
        raise SyntaxError(
            f"Erro de sintaxe na linha {e.line}, coluna {e.column}:\n"
            f"  Caractere inesperado: {e.char}\n"
            f"  Contexto: {e.get_context(code)}"
        )
    except LarkError as e:
        # Outro erro do Lark
        raise SyntaxError(f"Erro ao parsear código: {e}")
    
    # Transformar
    try:
        transformer = MythonTransformer(source_code=code)
        python_code = transformer.transform(tree)
    except Exception as e:
        raise RuntimeError(f"Erro ao transformar código: {e}")
    
    # Salvar arquivo se output_path foi fornecido
    if output_path:
        try:
            out_path = Path(output_path)
            out_path.parent.mkdir(parents=True, exist_ok=True)
            out_path.write_text(python_code, encoding='utf-8')
        except Exception as e:
            raise IOError(f"Erro ao salvar arquivo: {e}")
    
    return python_code


def transpile_string(code: str) -> str:
    """
    Transpila código Mython de uma string.
    
    Args:
        code: Código Mython como string
        
    Returns:
        Código Python gerado
        
    Raises:
        SyntaxError: Se houver erro de sintaxe
    """
    # Carregar gramática
    grammar_path = Path(__file__).parent / "grammar.lark"
    if not grammar_path.exists():
        raise FileNotFoundError(f"Gramática não encontrada: {grammar_path}")
    
    with open(grammar_path, 'r', encoding='utf-8') as f:
        grammar = f.read()
    
    # Criar parser
    parser = Lark(
        grammar,
        start='start',
        parser='earley',  # Earley para lidar com ambiguidades
        propagate_positions=True,
    )
    
    # Normalizar operadores ANTES do parsing (simplifica o transformer)
    code = normalize_operators(code)
    
    # Parsear
    try:
        tree = parser.parse(code)
    except (UnexpectedToken, UnexpectedCharacters, LarkError) as e:
        raise SyntaxError(f"Erro de sintaxe: {e}")
    
    # Transformar
    transformer = MythonTransformer(source_code=code)
    python_code = transformer.transform(tree)
    
    return python_code


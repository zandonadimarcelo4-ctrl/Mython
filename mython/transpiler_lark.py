"""
Transpiler usando Lark - Versão robusta e formal.
"""

from pathlib import Path
from lark import Lark, Tree
from lark.exceptions import LarkError, UnexpectedToken, UnexpectedCharacters

from .transformer_lark import MythonTransformer

# Importar sistema de i18n
try:
    from .i18n import translate_code, detect_language
    I18N_AVAILABLE = True
except ImportError:
    I18N_AVAILABLE = False
    detect_language = None


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
        transformer = MythonTransformer()
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
    
    # Parsear
    try:
        tree = parser.parse(code)
    except (UnexpectedToken, UnexpectedCharacters, LarkError) as e:
        raise SyntaxError(f"Erro de sintaxe: {e}")
    
    # Transformar
    transformer = MythonTransformer()
    python_code = transformer.transform(tree)
    
    return python_code


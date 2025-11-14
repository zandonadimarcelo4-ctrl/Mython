"""
Transpiler usando Lark - Versão robusta e formal.
"""

from pathlib import Path
from lark import Lark, Tree
from lark.exceptions import LarkError, UnexpectedToken, UnexpectedCharacters
import re

from .transformer_lark import MythonTransformer
from .indenter import MythonIndenter

# Importar sistema de i18n
try:
    from .i18n import translate_code, detect_language
    I18N_AVAILABLE = True
except ImportError:
    I18N_AVAILABLE = False
    detect_language = None

# Importar sistema de tradução híbrido (LibreTranslate + Argos Translate)
try:
    from .translator import translate_code as translate_keywords, get_available_translators
    HYBRID_TRANSLATOR_AVAILABLE = True
except ImportError:
    HYBRID_TRANSLATOR_AVAILABLE = False
    translate_keywords = None
    get_available_translators = None

# Importar sistema de macros modular
try:
    from .macros import registry as macro_registry
    MACROS_AVAILABLE = True
except ImportError:
    MACROS_AVAILABLE = False
    macro_registry = None


def auto_fstring(code: str) -> str:
    """
    Detecta strings com interpolação {variable} e converte automaticamente para f-strings.
    
    Inspirado nos exemplos do Lark: syntax sugar para tornar código mais intuitivo.
    
    IMPORTANTE: Aplica apenas DEPOIS do parsing, no transformer, para evitar conflitos.
    Por enquanto, apenas marca strings que precisam ser convertidas.
    """
    # Por enquanto, deixamos o transformer fazer isso
    # Retornar código sem alterações aqui
    return code


def dict_sem_aspas(code: str) -> str:
    """
    Permite dict literals sem aspas nas chaves: {name: "John"} -> {"name": "John"}
    
    Inspirado nos exemplos do Lark: syntax sugar para estruturas de dados.
    """
    lines = code.split('\n')
    normalized_lines = []
    
    for line in lines:
        # Buscar padrões como {key: value} onde key é um NAME (não uma string)
        # Padrão: { name : value } ou {name:value} (com ou sem espaços)
        # IMPORTANTE: Não aplicar se já for {"key": value} ou se key já estiver entre aspas
        
        # Buscar dict literals que não tenham aspas nas chaves
        # Exemplo: {name: "John", age: 30}
        def replace_dict_key(match):
            # match.group(0) = {name: "John", ...}
            content = match.group(1)  # name: "John", age: 30
            
            # Processar cada par chave:valor
            pairs = []
            # Split por vírgulas, mas cuidado com vírgulas dentro de strings
            current_pair = ""
            depth = 0  # Para rastrear parênteses, colchetes, etc.
            in_string = False
            string_char = None
            
            for char in content:
                if char in ('"', "'") and (not in_string or char == string_char):
                    in_string = not in_string
                    if in_string:
                        string_char = char
                    else:
                        string_char = None
                elif not in_string:
                    if char in ('(', '[', '{'):
                        depth += 1
                    elif char in (')', ']', '}'):
                        depth -= 1
                    elif char == ',' and depth == 0:
                        pairs.append(current_pair.strip())
                        current_pair = ""
                        continue
                
                current_pair += char
            
            if current_pair.strip():
                pairs.append(current_pair.strip())
            
            # Processar cada par
            new_pairs = []
            for pair in pairs:
                if ':' in pair:
                    key, value = pair.split(':', 1)
                    key = key.strip()
                    value = value.strip()
                    
                    # Se a chave não começar com aspas e for um NAME válido, adicionar aspas
                    if re.match(r'^[a-zA-Z_][a-zA-Z0-9_]*$', key):
                        new_pairs.append(f'"{key}": {value}')
                    else:
                        new_pairs.append(pair)
                else:
                    new_pairs.append(pair)
            
            return '{' + ', '.join(new_pairs) + '}'
        
        # Buscar dict literals na linha
        # Padrão: { ... } onde ... pode conter name: value
        line = re.sub(r'\{([^}]*)\}', replace_dict_key, line)
        
        normalized_lines.append(line)
    
    return '\n'.join(normalized_lines)


def normalize_operators(code: str) -> str:
    """
    Normaliza expressões naturais para operadores Python simples ANTES do parsing.
    Isso simplifica o transformer e garante que o Lark receba código já normalizado.
    
    Também aplica melhorias de syntax sugar inspiradas nos exemplos do Lark:
    - Dict sem aspas: {name: "John"} -> {"name": "John"}
    """
    # Aplicar dict sem aspas (isso funciona bem antes do parsing)
    code = dict_sem_aspas(code)
    
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


def preprocess_indentation(code: str) -> str:
    """
    Preprocessa indentação para garantir que blocos baseados em indentação sejam
    reconhecidos corretamente pelo parser Lark.
    
    PROBLEMA: O Lark não processa indentação automaticamente. Quando há múltiplos
    statements no nível raiz seguidos de blocos indentados, o parser não reconhece
    que as linhas indentadas pertencem ao bloco do statement anterior.
    
    SOLUÇÃO: Processamos o código manualmente e garantimos que blocos baseados em
    indentação sejam processados corretamente. A gramática do Lark espera que os
    blocos estejam claramente associados aos statements que os definem.
    
    A chave é garantir que quando um statement que termina com ':' é encontrado,
    as linhas seguintes com indentação maior sejam agrupadas como parte do bloco
    desse statement.
    """
    lines = code.split('\n')
    processed_lines = []
    i = 0
    
    while i < len(lines):
        line = lines[i]
        stripped = line.strip()
        leading_spaces = len(line) - len(line.lstrip())
        
        # Linha vazia ou comentário - manter como está
        if not stripped or stripped.startswith('#'):
            processed_lines.append(line)
            i += 1
            continue
        
        # Verificar se é um statement que abre um bloco (termina com ':')
        # Keywords que abrem blocos
        block_keywords = [
            'if', 'elif', 'else', 'for', 'while', 'def', 'class',
            'try', 'except', 'finally', 'with', 'when', 'whenever'
        ]
        
        is_block_starter = (
            stripped.endswith(':') and
            any(
                stripped.startswith(kw + ' ') or
                stripped == kw + ':' or
                stripped.startswith(kw + ':')
                for kw in block_keywords
            )
        )
        
        if is_block_starter:
            # Adicionar a linha do statement
            processed_lines.append(line)
            i += 1
            
            # Agora coletar todas as linhas que fazem parte do bloco
            # Um bloco consiste em linhas que têm indentação maior que o statement
            block_indent = leading_spaces + 4  # Python usa 4 espaços por padrão
            
            while i < len(lines):
                next_line = lines[i]
                next_stripped = next_line.strip()
                
                # Linha vazia ou comentário - incluir no bloco
                if not next_stripped or next_stripped.startswith('#'):
                    processed_lines.append(next_line)
                    i += 1
                    continue
                
                next_indent = len(next_line) - len(next_line.lstrip())
                
                # Se a indentação é maior que o statement original, faz parte do bloco
                if next_indent > leading_spaces:
                    processed_lines.append(next_line)
                    i += 1
                    continue
                # Se a indentação é igual ao statement original, pode ser outro statement
                # no mesmo nível (elif, else, except, finally) - processar recursivamente
                elif next_indent == leading_spaces:
                    # Verificar se é um statement relacionado (elif, else, except, finally)
                    related_keywords = ['elif', 'else', 'except', 'finally']
                    is_related = (
                        next_stripped.endswith(':') and
                        any(next_stripped.startswith(kw + ' ') or next_stripped == kw + ':'
                            for kw in related_keywords)
                    )
                    if is_related:
                        # É um statement relacionado - processar recursivamente
                        # Adicionar a linha e processar seu bloco
                        processed_lines.append(next_line)
                        i += 1
                        # Agora processar o bloco deste statement relacionado
                        while i < len(lines):
                            related_line = lines[i]
                            related_stripped = related_line.strip()
                            
                            # Linha vazia ou comentário - incluir
                            if not related_stripped or related_stripped.startswith('#'):
                                processed_lines.append(related_line)
                                i += 1
                                continue
                            
                            related_indent = len(related_line) - len(related_line.lstrip())
                            
                            # Se indentação maior, faz parte do bloco
                            if related_indent > leading_spaces:
                                processed_lines.append(related_line)
                                i += 1
                                continue
                            # Se indentação igual, pode ser outro statement relacionado
                            elif related_indent == leading_spaces:
                                # Verificar se é outro statement relacionado
                                is_another_related = (
                                    related_stripped.endswith(':') and
                                    any(related_stripped.startswith(kw + ' ') or related_stripped == kw + ':'
                                        for kw in related_keywords)
                                )
                                if is_another_related:
                                    # Outro statement relacionado - continuar processando
                                    processed_lines.append(related_line)
                                    i += 1
                                    continue
                                else:
                                    # Não é relacionado - sair do loop
                                    break
                            # Se indentação menor, saiu do bloco
                            else:
                                break
                        # Continuar processando do ponto onde paramos
                        continue
                    else:
                        # Não é relacionado - saiu do bloco original
                        break
                # Se a indentação é menor, saiu do bloco
                else:
                    break
        else:
            # Statement normal - adicionar e continuar
            processed_lines.append(line)
            i += 1
    
    return '\n'.join(processed_lines)


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
    
    # Criar parser com indenter para processar indentação estilo Python
    try:
        parser = Lark(
            grammar,
            start='start',
            parser='lalr',  # LALR para usar com indenter (mais eficiente)
            postlex=MythonIndenter(),  # ESSENCIAL: processa indentação automaticamente
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
    # PRIORIDADE: Sistema híbrido (LibreTranslate + Argos Translate)
    # FALLBACK: Sistema i18n tradicional (dicionários)
    
    # Se lang não foi especificado, tentar detectar automaticamente
    if lang is None:
        if I18N_AVAILABLE and detect_language:
            try:
                detected_lang = detect_language(code)
                if detected_lang and detected_lang != "en":
                    lang = detected_lang
            except Exception as e:
                import warnings
                warnings.warn(f"Não foi possível detectar idioma automaticamente: {e}")
    
    # Traduzir para inglês se necessário (inglês é a base do Mython)
    if lang and lang != "en":
        # Tentar sistema híbrido primeiro (mais robusto)
        if HYBRID_TRANSLATOR_AVAILABLE and translate_keywords:
            try:
                code = translate_keywords(code, source_lang=lang, target_lang="en", use_cache=True)
                # Se traduziu com sucesso, assumir que funcionou
            except Exception as e:
                # Se falhar, tentar sistema i18n tradicional
                if I18N_AVAILABLE:
                    try:
                        code = translate_code(code, lang=lang, reverse=True)
                    except Exception as e2:
                        import warnings
                        warnings.warn(f"Não foi possível traduzir código: {e2}")
                else:
                    import warnings
                    warnings.warn(f"Tradução híbrida falhou e i18n não disponível: {e}")
        # Fallback para sistema i18n tradicional
        elif I18N_AVAILABLE:
            try:
                code = translate_code(code, lang=lang, reverse=True)
            except Exception as e:
                import warnings
                warnings.warn(f"Não foi possível traduzir código de {lang} para inglês: {e}")
    # Se lang ainda é None mas i18n está disponível, tentar detecção e tradução automática
    elif lang is None and I18N_AVAILABLE and detect_language:
        try:
            detected_lang = detect_language(code)
            if detected_lang and detected_lang != "en":
                # Tentar sistema híbrido primeiro
                if HYBRID_TRANSLATOR_AVAILABLE and translate_keywords:
                    try:
                        code = translate_keywords(code, source_lang=detected_lang, target_lang="en", use_cache=True)
                    except Exception:
                        # Fallback para i18n tradicional
                        code = translate_code(code, lang=detected_lang, reverse=True)
                else:
                    code = translate_code(code, lang=detected_lang, reverse=True)
        except Exception as e:
            import warnings
            warnings.warn(f"Tradução automática falhou: {e}")
    
    # Normalizar operadores ANTES do parsing (simplifica o transformer)
    code = normalize_operators(code)
    
    # Garantir que o código termine com newline (necessário para o parser)
    if code and not code.endswith('\n'):
        code = code + '\n'
    
    # NÃO precisamos mais pré-processar indentação - o Indenter faz isso automaticamente!
    # code = preprocess_indentation(code)  # REMOVIDO - não é mais necessário
    
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


def transpile_string(code: str, lang: str = None, use_hybrid_translator: bool = True) -> str:
    """
    Transpila código Mython de uma string.
    
    Args:
        code: Código Mython como string
        lang: Código da língua do código (en, pt, es, etc.) - se None, detecta automaticamente
        use_hybrid_translator: Se True, usa sistema híbrido (LibreTranslate + Argos Translate)
        
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
    
    # Adicionar regras de macros à gramática se disponível
    if MACROS_AVAILABLE and macro_registry:
        macro_rules = macro_registry.get_grammar_rules()
        if macro_rules:
            # Adicionar regras de macros antes de simple_stmt
            # IMPORTANTE: Macros devem estar antes de outros statements para precedência
            macro_grammar = "\n".join(["\n// Macros (geradas dinamicamente)"] + macro_rules + [""])
            
            # Criar regra macro_stmt que agrupa todas as macros
            macro_stmt_rule = "macro_stmt: " + " | ".join([rule.split(":")[0] for rule in macro_rules]) + "\n"
            
            # Inserir antes de simple_stmt
            if "simple_stmt:" in grammar:
                # Encontrar a linha simple_stmt: e inserir antes
                grammar = grammar.replace(
                    "simple_stmt:",
                    macro_grammar + macro_stmt_rule + "\nsimple_stmt: macro_stmt\n           | "
                )
    
    # Criar parser com indenter para processar indentação estilo Python
    parser = Lark(
        grammar,
        start='start',
        parser='lalr',  # LALR para usar com indenter (mais eficiente)
        postlex=MythonIndenter(),  # ESSENCIAL: processa indentação automaticamente
        propagate_positions=True,
    )
    
    # Detectar língua automaticamente se necessário
    # IMPORTANTE: Sempre detectar se lang é None para garantir tradução automática
    if lang is None:
        if I18N_AVAILABLE and detect_language:
            try:
                detected_lang = detect_language(code)
                if detected_lang and detected_lang != "en":
                    lang = detected_lang
                else:
                    lang = "en"  # Default para inglês se não detectar ou já for inglês
            except Exception as e:
                import warnings
                warnings.warn(f"Não foi possível detectar idioma automaticamente: {e}")
                lang = "en"  # Default para inglês em caso de erro
        else:
            lang = "en"  # Default para inglês se i18n não estiver disponível
    
    # Traduzir código para inglês se necessário (antes de parsear)
    # PRIORIDADE: Sistema híbrido (LibreTranslate + Argos Translate)
    # FALLBACK: Sistema i18n tradicional (dicionários)
    # IMPORTANTE: Inglês é a base do Mython - sempre traduzir para inglês se necessário
    if lang and lang != "en":
        # Tentar sistema híbrido primeiro (mais robusto)
        if use_hybrid_translator and HYBRID_TRANSLATOR_AVAILABLE and translate_keywords:
            try:
                code = translate_keywords(code, source_lang=lang, target_lang="en", use_cache=True)
                # Se traduziu com sucesso, assumir que funcionou
            except Exception as e:
                # Se falhar, tentar sistema i18n tradicional
                if I18N_AVAILABLE:
                    try:
                        code = translate_code(code, lang=lang, reverse=True)
                    except Exception:
                        pass  # Continuar com código original se falhar
        # Fallback para sistema i18n tradicional
        elif I18N_AVAILABLE:
            try:
                code = translate_code(code, lang=lang, reverse=True)
            except Exception:
                pass  # Continuar com código original se falhar
    
    # Normalizar operadores ANTES do parsing (simplifica o transformer)
    code = normalize_operators(code)
    
    # NÃO precisamos mais pré-processar indentação - o Indenter faz isso automaticamente!
    # code = preprocess_indentation(code)  # REMOVIDO - não é mais necessário
    
    # Parsear
    try:
        tree = parser.parse(code)
    except (UnexpectedToken, UnexpectedCharacters, LarkError) as e:
        raise SyntaxError(f"Erro de sintaxe: {e}")
    
    # Transformar
    transformer = MythonTransformer(source_code=code)
    python_code = transformer.transform(tree)
    
    return python_code


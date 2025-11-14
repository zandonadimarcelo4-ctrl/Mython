"""
Transformer para converter AST do Lark em código Python.
"""

from lark import Transformer, Token, Tree
from typing import List, Any


class MythonTransformer(Transformer):
    """Transforma a árvore de parse do Mython em código Python."""
    
    def __init__(self, source_code: str = None):
        super().__init__()
        self.indent_level = 0
        self.in_class = False
        self.source_code = source_code  # Armazenar código original para extrair tokens
        self.needs_imports = {
            'time': False,
            'random': False,
            'asyncio': False,
            'os': False,
            'datetime': False,
            'sys': False,
        }
    
    def indent(self) -> str:
        """Retorna a indentação atual."""
        return "    " * self.indent_level
    
    # ============================================
    # Statements
    # ============================================
    
    def start(self, statements: List[Any]) -> str:
        """
        start: statement+
        
        CORRIGIDO: Apenas junta as strings já transformadas pelos métodos filhos.
        NÃO chama self.transform() - o Lark já fez isso.
        """
        lines = []
        
        # Adicionar imports necessários
        imports = []
        if self.needs_imports['time']:
            imports.append("import time")
        if self.needs_imports['random']:
            imports.append("import random")
        if self.needs_imports['asyncio']:
            imports.append("import asyncio")
        if self.needs_imports['os']:
            imports.append("import os")
        if self.needs_imports['datetime']:
            imports.append("import datetime")
        if self.needs_imports['sys']:
            imports.append("import sys")
        
        if imports:
            lines.extend(imports)
            lines.append("")
        
        # Cada statement já foi transformado em string pelos métodos filhos
        # Apenas juntar as linhas
        for stmt in statements:
            if stmt and isinstance(stmt, str) and stmt.strip():
                # Adicionar linhas preservando indentação
                for line in stmt.split('\n'):
                    if line.strip():
                        lines.append(line)
            elif stmt and not isinstance(stmt, str):
                # Se não é string, converter (não deveria acontecer)
                stmt_str = str(stmt)
                if stmt_str.strip():
                    for line in stmt_str.split('\n'):
                        if line.strip():
                            lines.append(line)
        
        return "\n".join(lines) + "\n"
    
    def simple_stmt(self, children: List[Any]) -> str:
        """
        simple_stmt: say_stmt | ask_stmt | assign_stmt | ...
        
        CORRIGIDO: Apenas retorna o resultado do filho.
        NÃO chama self.transform() - o Lark já transformou o filho.
        """
        if not children:
            return ""
        
        # Filtrar _NEWLINE se presente
        filtered = [c for c in children if not (isinstance(c, Token) and c.type == '_NEWLINE')]
        
        if not filtered:
            return ""
        
        # O primeiro child já foi transformado pelo Lark em string
        # Apenas retornar
        result = filtered[0]
        
        # Se ainda é Tree (não deveria acontecer), converter para string
        if isinstance(result, Tree):
            return str(result)
        
        # Se é string, retornar diretamente
        if isinstance(result, str):
            return result
        
        # Fallback: converter para string
        return str(result) if result else ""
    
    def statement(self, children: List[Any]) -> str:
        """
        statement: simple_stmt _NEWLINE | compound_stmt
        
        CORRIGIDO: Apenas retorna o resultado do filho.
        NÃO chama self.transform() - o Lark já transformou o filho.
        """
        if not children:
            return ""
        
        # Filtrar _NEWLINE se presente
        filtered = [c for c in children if not (isinstance(c, Token) and c.type == '_NEWLINE')]
        
        if not filtered:
            return ""
        
        # O primeiro child já foi transformado pelo Lark em string
        result = filtered[0]
        
        # Se ainda é Tree (não deveria acontecer), converter para string
        if isinstance(result, Tree):
            return str(result)
        
        # Se é string, retornar diretamente
        if isinstance(result, str):
            return result
        
        # Fallback: converter para string
        return str(result) if result else ""
    
    def block_stmt(self, children: List[Any]) -> str:
        """
        block_stmt: simple_stmt _NEWLINE? | compound_stmt
        
        CORRIGIDO: Processa o filho já transformado e indenta o conteúdo.
        NÃO chama self.transform() - o Lark já transformou o filho.
        """
        if not children:
            return "    pass"
        
        # Filtrar _NEWLINE se presente
        filtered = [c for c in children if not (isinstance(c, Token) and c.type == '_NEWLINE')]
        
        if not filtered:
            return "    pass"
        
        # O primeiro child já foi transformado pelo Lark em string
        result = filtered[0]
        
        # Se ainda é Tree (não deveria acontecer), converter para string
        if isinstance(result, Tree):
            result = str(result)
        
        # Se não é string, converter
        if not isinstance(result, str):
            result = str(result)
        
        # Se está vazio, retornar pass indentado
        if not result.strip():
            return "    pass"
        
        # Indentar SOMENTE o conteúdo interno (linha por linha)
        # IMPORTANTE: Não indentar se já começa com "else:" (isso seria erro)
        lines = result.split('\n')
        indented_lines = []
        for line in lines:
            if line.strip():
                # Adicionar indentação de 4 espaços
                indented_lines.append("    " + line.strip())
            else:
                indented_lines.append("")
        
        return "\n".join(indented_lines)
    
    def compound_stmt(self, args: List[Any]) -> str:
        """Statement composto - transforma recursivamente."""
        if not args:
            return ""
        # args[0] é o compound statement (if_stmt, while_stmt, etc.)
        result = args[0]
        
        # Se é Tree, transformar recursivamente
        if isinstance(result, Tree):
            transformed = self.transform(result)
            if transformed:
                result = transformed
        
        # Garantir que é string
        if not isinstance(result, str):
            result = str(result)
        
        # Se parece ser uma representação de Tree, tentar extrair o conteúdo
        if isinstance(result, str) and result.startswith("Tree("):
            # Isso significa que o transform falhou - tentar transformar children diretamente
            if hasattr(args[0], 'children') and args[0].children:
                # Transformar cada filho
                transformed_children = []
                for child in args[0].children:
                    if isinstance(child, Tree):
                        transformed = self.transform(child)
                        if transformed and isinstance(transformed, str):
                            transformed_children.append(transformed)
                    elif isinstance(child, str):
                        transformed_children.append(child)
                
                if transformed_children:
                    # Juntar children transformados
                    result = "\n".join(str(c) for c in transformed_children if c and str(c).strip())
        
        return result
    
    def INDENT(self, token):
        """Token INDENT - incrementa nível de indentação."""
        self.indent_level += 1
        return ""
    
    def DEDENT(self, token):
        """Token DEDENT - decrementa nível de indentação."""
        self.indent_level -= 1
        return ""
    
    def _NEWLINE(self, token):
        """Token _NEWLINE - nova linha."""
        return ""
    
    def block(self, statements: List[Any]) -> str:
        """
        Bloco de código.
        NOTA: Com INDENT/DEDENT, os statements já vêm indentados corretamente.
        Precisamos apenas processá-los mantendo a indentação.
        """
        result_lines = []
        for stmt in statements:
            if stmt:
                # Ignorar tokens INDENT/DEDENT/_NEWLINE - já foram processados
                if isinstance(stmt, str) and stmt.strip() in ['INDENT', 'DEDENT', '_NEWLINE', '']:
                    continue
                
                # Se for Tree object, transformar recursivamente
                if not isinstance(stmt, str):
                    if hasattr(stmt, 'children'):
                        stmt = self.transform(stmt)
                    else:
                        stmt = str(stmt)
                
                # Garantir que é string
                if not isinstance(stmt, str):
                    stmt = str(stmt)
                
                # Se stmt está vazio após strip, pular
                if not stmt.strip():
                    continue
                
                # Processar statement com indentação correta
                # O indent_level já está ajustado pelos tokens INDENT/DEDENT
                lines = stmt.split('\n')
                for line in lines:
                    stripped = line.strip()
                    if stripped:
                        # Adicionar indentação apropriada baseada no indent_level atual
                        result_lines.append(self.indent() + stripped)
        
        result = "\n".join(result_lines)
        return result if result_lines else ""
    
    # ============================================
    # Saída
    # ============================================
    
    def say_stmt(self, children: List[Any]) -> str:
        """
        say_stmt: SAY expr
        
        CORRIGIDO: Processa expr já transformado.
        """
        if not children:
            return self.indent() + 'print("")'
        
        # Filtrar tokens SAY, _NEWLINE
        filtered = [c for c in children if not (isinstance(c, Token) and c.type in ['SAY', '_NEWLINE'])]
        
        if not filtered:
            return self.indent() + 'print("")'
        
        # Primeiro arg é expr (já transformado ou Token)
        expr_arg = filtered[0]
        
        # Se é Token, processar
        if isinstance(expr_arg, Token):
            expr = expr_arg.value if expr_arg.type == 'STRING' else self._expr(expr_arg)
        else:
            # Se já é string, usar diretamente
            expr = str(expr_arg)
        
        # Retornar com indentação atual
        return self.indent() + f"print({expr})"
    
    # ============================================
    # Entrada
    # ============================================
    
    def ask_stmt(self, children: List[Any]) -> str:
        """
        ask_stmt: ASK ask_type NAME STRING?
                | ASK ask_type NAME
                | ASK NAME STRING?
                | ASK NAME
        
        CORRIGIDO: Processa diretamente os tokens sem chamar self.transform().
        """
        if not children:
            return self.indent() + 'input()'
        
        # Filtrar tokens ASK, _NEWLINE - manter apenas argumentos importantes
        filtered = [c for c in children if not (isinstance(c, Token) and c.type in ['ASK', '_NEWLINE'])]
        
        if not filtered:
            return self.indent() + 'input()'
        
        ask_type_val = "text"  # Padrão
        var_name = None
        prompt = '""'
        
        # Padrão 1: ASK ask_type NAME STRING?
        # filtered[0] = resultado de ask_type (já transformado: "number" ou "text")
        # filtered[1] = Token(NAME) ou já transformado
        # filtered[2] = Token(STRING)? (opcional) ou já transformado
        
        first_arg = filtered[0] if filtered else None
        
        # Se primeiro arg é string "number" ou "text" (já transformado pelo método number/text)
        if isinstance(first_arg, str) and first_arg in ['number', 'text']:
            ask_type_val = first_arg
            
            # Segundo arg é NAME (variável)
            if len(filtered) > 1:
                name_arg = filtered[1]
                if isinstance(name_arg, Token) and name_arg.type == 'NAME':
                    var_name = name_arg.value
                elif isinstance(name_arg, str):
                    var_name = name_arg
                else:
                    var_name = str(name_arg)
            
            # Terceiro arg é STRING (prompt) - opcional
            if len(filtered) > 2:
                str_arg = filtered[2]
                if isinstance(str_arg, Token) and str_arg.type == 'STRING':
                    prompt = str_arg.value
                elif isinstance(str_arg, str):
                    prompt = str_arg
                else:
                    prompt = str(str_arg)
        # Padrão 2: ASK NAME STRING? (sem ask_type)
        elif isinstance(first_arg, Token) and first_arg.type == 'NAME':
            ask_type_val = "text"
            var_name = first_arg.value
            # Segundo arg é STRING (prompt) - opcional
            if len(filtered) > 1:
                str_arg = filtered[1]
                if isinstance(str_arg, Token) and str_arg.type == 'STRING':
                    prompt = str_arg.value
                elif isinstance(str_arg, str):
                    prompt = str_arg
                else:
                    prompt = str(str_arg)
        elif isinstance(first_arg, str):
            # Se é string mas não é "number" ou "text", pode ser NAME já transformado
            ask_type_val = "text"
            var_name = first_arg
            if len(filtered) > 1:
                str_arg = filtered[1]
                if isinstance(str_arg, Token) and str_arg.type == 'STRING':
                    prompt = str_arg.value
                elif isinstance(str_arg, str):
                    prompt = str_arg
                else:
                    prompt = str(str_arg)
        
        # Valores padrão
        if not var_name:
            var_name = "value"
        if not prompt or prompt == '""':
            prompt = '""'
        
        # Gerar código Python
        if ask_type_val == "number":
            return self.indent() + f'{var_name} = int(input({prompt}))'
        else:
            return self.indent() + f'{var_name} = input({prompt})'
    
    def number(self, children: List[Any]) -> str:
        """
        number: NUMBER_TYPE -> number
        
        CORRIGIDO: Retorna "number" como string.
        Com aliases (->), o Lark chama este método diretamente.
        """
        return "number"
    
    def text(self, children: List[Any]) -> str:
        """
        text: TEXT_TYPE -> text
        
        CORRIGIDO: Retorna "text" como string.
        Com aliases (->), o Lark chama este método diretamente.
        """
        return "text"
    
    # ============================================
    # Condições
    # ============================================
    
    def if_stmt(self, children: List[Any]) -> str:
        """
        if_stmt: IF condition ":" _NEWLINE INDENT block_stmt+ DEDENT else_block?
        
        CORRIGIDO: Processa condition, block_stmt+ e else_block? já transformados.
        NÃO chama self.transform() - o Lark já transformou os filhos.
        """
        if not children:
            return ""
        
        # Filtrar tokens IF, _NEWLINE, ":", INDENT, DEDENT
        # Manter apenas: condition (string), block_stmt+ (strings), else_block? (string)
        filtered = []
        condition = ""
        blocks = []
        else_part = ""
        
        i = 0
        while i < len(children):
            arg = children[i]
            
            # Ignorar tokens de controle
            if isinstance(arg, Token):
                if arg.type in ['IF', '_NEWLINE', 'INDENT', 'DEDENT']:
                    i += 1
                    continue
                if arg.value == ':':
                    i += 1
                    continue
            
            # Primeiro não-token é a condition
            if not condition:
                condition = self._expr(arg) if hasattr(arg, 'children') else str(arg)
                i += 1
                continue
            
            # Depois vem block_stmt+ (strings já transformadas)
            # Até encontrar else_block
            if isinstance(arg, Tree) and arg.data == 'else_block':
                # else_block já foi transformado pelo Lark
                else_part = str(arg)  # Não deveria ser Tree, mas se for, converter
                i += 1
                continue
            
            # Se é string, é um block_stmt já transformado
            if isinstance(arg, str) and arg.strip():
                blocks.append(arg)
            # Se é Tree, pode ser block_stmt não transformado (não deveria acontecer)
            elif isinstance(arg, Tree):
                blocks.append(str(arg))
            
            i += 1
        
        # Construir bloco if
        if blocks:
            block_code = "\n".join(blocks)
        else:
            block_code = "    pass"
        
        # Construir resultado
        code = f"if {condition}:"
        if block_code:
            code += "\n" + block_code
        
        # Adicionar else_block se existir
        if else_part:
            code += "\n" + else_part
        
        return code
    
    def else_block(self, children: List[Any]) -> str:
        """
        else_block: _NEWLINE* ELSE ":" _NEWLINE INDENT block_stmt+ DEDENT
        
        CORRIGIDO: Processa block_stmt+ já transformados.
        NÃO chama self.transform() - o Lark já transformou os filhos.
        Retorna "else:" sem indentação extra (mesmo nível do if).
        """
        if not children:
            return "else:\n    pass"
        
        # Filtrar tokens INDENT, DEDENT, _NEWLINE, ELSE, ":"
        # Manter apenas block_stmt+ (strings já transformadas)
        blocks = []
        
        for arg in children:
            # Ignorar tokens de controle
            if isinstance(arg, Token):
                if arg.type in ['INDENT', 'DEDENT', '_NEWLINE', 'ELSE']:
                    continue
                if arg.value == ':':
                    continue
            
            # Se é string, é um block_stmt já transformado
            if isinstance(arg, str) and arg.strip():
                blocks.append(arg)
            # Se é Tree, pode ser block_stmt não transformado (não deveria acontecer)
            elif isinstance(arg, Tree):
                blocks.append(str(arg))
        
        # Construir bloco else
        if blocks:
            block = "\n".join(stmt for stmt in blocks if stmt.strip())
        else:
            block = "    pass"
        
        # Construir resultado: else: SEM indentação extra (mesmo nível do if)
        result = "else:"
        if block:
            result += "\n" + block
        
        return result
    
    # ============================================
    # Loops
    # ============================================
    
    def while_stmt(self, children: List[Any]) -> str:
        """
        while_stmt: WHILE condition ":" _NEWLINE INDENT block_stmt+ DEDENT
        
        CORRIGIDO: Processa condition e block_stmt+ já transformados.
        NÃO chama self.transform() - o Lark já transformou os filhos.
        """
        if not children:
            return ""
        
        # Filtrar tokens WHILE, _NEWLINE, ":", INDENT, DEDENT
        # Manter apenas: condition (string), block_stmt+ (strings)
        filtered = []
        condition = ""
        blocks = []
        
        i = 0
        while i < len(children):
            arg = children[i]
            
            # Ignorar tokens de controle
            if isinstance(arg, Token):
                if arg.type in ['WHILE', '_NEWLINE', 'INDENT', 'DEDENT']:
                    i += 1
                    continue
                if arg.value == ':':
                    i += 1
                    continue
            
            # Primeiro não-token é a condition
            if not condition:
                condition = self._expr(arg) if hasattr(arg, 'children') else str(arg)
                i += 1
                continue
            
            # Depois vem block_stmt+ (strings já transformadas)
            if isinstance(arg, str) and arg.strip():
                blocks.append(arg)
            # Se é Tree, pode ser block_stmt não transformado (não deveria acontecer)
            elif isinstance(arg, Tree):
                blocks.append(str(arg))
            
            i += 1
        
        # Construir bloco while
        if blocks:
            block_code = "\n".join(blocks)
        else:
            block_code = "    pass"
        
        # Construir resultado
        code = f"while {condition}:"
        if block_code:
            code += "\n" + block_code
        
        return code
    
    def for_each_stmt(self, children: List[Any]) -> str:
        """
        for_each_stmt: FOR NAME IN expr ":" _NEWLINE INDENT block_stmt+ DEDENT
        
        CORRIGIDO: Processa NAME, expr e block_stmt+ já transformados.
        """
        if not children:
            return ""
        
        # Filtrar tokens FOR, IN, _NEWLINE, ":", INDENT, DEDENT
        # Manter apenas: NAME (string), expr (string), block_stmt+ (strings)
        filtered = []
        var_name = None
        expr_value = None
        blocks = []
        
        i = 0
        while i < len(children):
            arg = children[i]
            
            # Ignorar tokens de controle
            if isinstance(arg, Token):
                if arg.type in ['FOR', 'IN', '_NEWLINE', 'INDENT', 'DEDENT']:
                    i += 1
                    continue
                if arg.value == ':':
                    i += 1
                    continue
                # Se é NAME, é a variável do loop
                if arg.type == 'NAME':
                    var_name = arg.value
                    i += 1
                    continue
            
            # Se não é Token, pode ser expr ou block_stmt
            if not var_name:
                # Ainda não pegamos o var_name, então este é expr
                expr_value = self._expr(arg) if hasattr(arg, 'children') else str(arg)
                i += 1
                continue
            
            # Depois vem block_stmt+ (strings já transformadas)
            if isinstance(arg, str) and arg.strip():
                blocks.append(arg)
            # Se é Tree, pode ser block_stmt não transformado
            elif isinstance(arg, Tree):
                blocks.append(str(arg))
            
            i += 1
        
        # Valores padrão
        if not var_name:
            var_name = "item"
        if not expr_value:
            expr_value = "[]"
        
        # Construir bloco for
        if blocks:
            block_code = "\n".join(blocks)
        else:
            block_code = "    pass"
        
        # Construir resultado
        code = f"for {var_name} in {expr_value}:"
        if block_code:
            code += "\n" + block_code
        
        return code
    
    def repeat_stmt(self, children: List[Any]) -> str:
        """
        repeat_stmt: REPEAT NUMBER ":" _NEWLINE INDENT block_stmt+ DEDENT
        
        CORRIGIDO: Processa NUMBER e block_stmt+ já transformados.
        """
        if not children:
            return ""
        
        # Filtrar tokens REPEAT, _NEWLINE, ":", INDENT, DEDENT
        # Manter apenas: NUMBER (string), block_stmt+ (strings)
        filtered = []
        number_value = None
        blocks = []
        
        i = 0
        while i < len(children):
            arg = children[i]
            
            # Ignorar tokens de controle
            if isinstance(arg, Token):
                if arg.type in ['REPEAT', '_NEWLINE', 'INDENT', 'DEDENT']:
                    i += 1
                    continue
                if arg.value == ':':
                    i += 1
                    continue
                # Se é NUMBER, é o número de repetições
                if arg.type == 'NUMBER':
                    number_value = arg.value
                    i += 1
                    continue
            
            # Depois vem block_stmt+ (strings já transformadas)
            if isinstance(arg, str) and arg.strip():
                blocks.append(arg)
            # Se é Tree, pode ser block_stmt não transformado
            elif isinstance(arg, Tree):
                blocks.append(str(arg))
            
            i += 1
        
        # Valor padrão
        if not number_value:
            number_value = "1"
        
        # Construir bloco repeat
        if blocks:
            block_code = "\n".join(blocks)
        else:
            block_code = "    pass"
        
        # Construir resultado
        code = f"for _ in range({number_value}):"
        if block_code:
            code += "\n" + block_code
        
        return code
    
    def break_stmt(self, children: List[Any]) -> str:
        """
        break_stmt: BREAK
        
        CORRIGIDO: Retorna "break" sem processamento extra.
        """
        return self.indent() + "break"
    
    def continue_stmt(self, children: List[Any]) -> str:
        """
        continue_stmt: CONTINUE
        
        CORRIGIDO: Retorna "continue" sem processamento extra.
        """
        return self.indent() + "continue"
    
    def elif_stmt(self, args: List[Any]) -> str:
        """elif/else if/or if - Com INDENT/DEDENT, os blocos já vêm estruturados corretamente."""
        if not args or len(args) < 1:
            return ""
        
        # Processar condição
        cond_tree = args[0]
        if hasattr(cond_tree, 'children') and cond_tree.children:
            try:
                condition = self.transform(cond_tree)
                if not isinstance(condition, str):
                    condition = self._expr(cond_tree)
            except:
                condition = self._expr(cond_tree)
        else:
            condition = self._expr(cond_tree)
        
        # Processar statements do bloco (pular _NEWLINE, INDENT e DEDENT)
        statements = []
        for arg in args[1:]:
            # Ignorar tokens de controle
            if isinstance(arg, str):
                if arg.strip() in ['INDENT', 'DEDENT', '_NEWLINE']:
                    continue
            # Verificar se é um Token
            if hasattr(arg, 'type'):
                if arg.type in ['INDENT', 'DEDENT', '_NEWLINE']:
                    if arg.type == 'INDENT':
                        self.indent_level += 1
                    elif arg.type == 'DEDENT':
                        self.indent_level -= 1
                    continue
            statements.append(arg)
        
        # Construir o bloco
        block = self.block(statements) if statements else ""
        
        # Construir resultado
        result = self.indent() + f"elif {condition}:"
        if block:
            result += "\n" + block
        
        return result
    
    def else_stmt(self, args: List[Any]) -> str:
        """else/otherwise - Com INDENT/DEDENT, os blocos já vêm estruturados corretamente."""
        # args[0] = _NEWLINE (ignorar)
        # args[1] = INDENT token (ignorar)
        # args[2:] = statements do bloco (até DEDENT)
        # args[-1] = DEDENT token (ignorar)
        
        # Processar statements do bloco (pular INDENT/DEDENT/_NEWLINE)
        statements = []
        for arg in args:
            if isinstance(arg, str):
                if arg.strip() in ['INDENT', 'DEDENT', '_NEWLINE']:
                    continue
            statements.append(arg)
        
        # Remover DEDENT do final se presente
        if statements and isinstance(statements[-1], str) and statements[-1].strip() == 'DEDENT':
            statements = statements[:-1]
        
        # Construir o bloco
        block = self.block(statements) if statements else ""
        
        # Construir resultado
        result = self.indent() + "else:"
        if block:
            result += "\n" + block
        
        return result
    
    def _condition(self, cond: Any) -> str:
        """Normaliza condição."""
        # Primeiro converter Tree/Token para string usando _expr
        cond_str = self._expr(cond)
        
        # Normalizar expressões naturais para operadores Python (ordem importa!)
        # Fazer as mais longas primeiro para evitar substituições parciais
        replacements = [
            (" is greater than or equal to ", " >= "),
            (" greater than or equal to ", " >= "),
            (" is less than or equal to ", " <= "),
            (" less than or equal to ", " <= "),
            (" is greater than ", " > "),
            (" greater than ", " > "),
            (" is less than ", " < "),
            (" less than ", " < "),
            (" is not equal to ", " != "),
            (" not equal to ", " != "),
            (" is at least ", " >= "),
            (" is at most ", " <= "),
            (" is over ", " > "),
            (" is above ", " > "),
            (" above ", " > "),
            (" is under ", " < "),
            (" is below ", " < "),
            (" below ", " < "),
            (" equals ", " == "),
            (" equal to ", " == "),
        ]
        
        for old, new in replacements:
            if old in cond_str:
                cond_str = cond_str.replace(old, new)
        
        # Substituir "is not in" primeiro (antes de "is not")
        import re
        cond_str = re.sub(r'\bis not in\b', ' not in ', cond_str)
        cond_str = re.sub(r'\bis not\b', ' != ', cond_str)
        
        # Substituir "is in" por "in" (mas não "is not in" que já foi processado)
        cond_str = re.sub(r'\bis in\b', ' in ', cond_str)
        
        # Se ainda contém "is" simples (que não foi processado), substituir por ==
        # Mas só se não for parte de palavras já processadas
        cond_str = re.sub(r'\bis\b(?!\s+(?:not|in|over|under|above|below|greater|less|at|equal))', ' == ', cond_str)
        
        # Limpar espaços múltiplos
        cond_str = re.sub(r'\s+', ' ', cond_str).strip()
        
        return cond_str
    
    def comparison(self, args: List[Any]) -> str:
        """
        comparison: atom comparison_op atom
        
        args[0] = left atom (NAME, NUMBER, STRING)
        args[1] = comparison_op (Tree com Token(GREATER, '>'), etc.)
        args[2] = right atom (NAME, NUMBER, STRING)
        """
        if len(args) < 3:
            # Se não tem 3 args, retornar apenas o primeiro
            return self._expr(args[0]) if args else ""
        
        left = self._expr(args[0])
        op = self._expr(args[1])  # comparison_op
        right = self._expr(args[2])
        
        return f"{left} {op} {right}"
    
    def comparison_op(self, args: List[Any]) -> str:
        """
        comparison_op: GREATER | LESS | GREATER_EQUAL | LESS_EQUAL | EQUALS | NOT_EQUAL
        
        args[0] = Token(GREATER, '>') ou Token(LESS, '<'), etc.
        """
        if not args:
            return ""
        
        # Se é Token, retornar valor diretamente
        if isinstance(args[0], Token):
            return args[0].value
        
        # Se é Tree, transformar recursivamente
        if isinstance(args[0], Tree):
            return self.transform(args[0])
        
        # Se é string, retornar diretamente
        return str(args[0])
    
    def condition(self, args: List[Any]) -> str:
        """
        condition: comparison | atom
        
        Pode ser Tree(comparison, ...) ou Tree(atom, ...)
        """
        if not args:
            return ""
        
        # Transformar recursivamente
        return self._expr(args[0])
    
    # ============================================
    # Operadores aritméticos
    # ============================================
    
    def add(self, children: List[Any]) -> str:
        """Soma: a + b"""
        if len(children) < 2:
            return str(children[0]) if children else ""
        left = self._expr(children[0])
        right = self._expr(children[1])
        return f"{left} + {right}"
    
    def sub(self, children: List[Any]) -> str:
        """Subtração: a - b"""
        if len(children) < 2:
            return str(children[0]) if children else ""
        left = self._expr(children[0])
        right = self._expr(children[1])
        return f"{left} - {right}"
    
    def mul(self, children: List[Any]) -> str:
        """Multiplicação: a * b"""
        if len(children) < 2:
            return str(children[0]) if children else ""
        left = self._expr(children[0])
        right = self._expr(children[1])
        return f"{left} * {right}"
    
    def div(self, children: List[Any]) -> str:
        """Divisão: a / b"""
        if len(children) < 2:
            return str(children[0]) if children else ""
        left = self._expr(children[0])
        right = self._expr(children[1])
        return f"{left} / {right}"
    
    def floordiv(self, children: List[Any]) -> str:
        """Divisão inteira: a // b"""
        if len(children) < 2:
            return str(children[0]) if children else ""
        left = self._expr(children[0])
        right = self._expr(children[1])
        return f"{left} // {right}"
    
    def mod(self, children: List[Any]) -> str:
        """Módulo: a % b"""
        if len(children) < 2:
            return str(children[0]) if children else ""
        left = self._expr(children[0])
        right = self._expr(children[1])
        return f"{left} % {right}"
    
    def pow(self, children: List[Any]) -> str:
        """Potência: a ** b"""
        if len(children) < 2:
            return str(children[0]) if children else ""
        left = self._expr(children[0])
        right = self._expr(children[1])
        return f"{left} ** {right}"
    
    def paren_expr(self, children: List[Any]) -> str:
        """Parênteses: (expr)"""
        if not children:
            return ""
        expr = self._expr(children[0])
        return f"({expr})"
    
    # ============================================
    # Loops (métodos já foram adicionados acima após else_block)
    # ============================================
    
    # ============================================
    # Estruturas de dados
    # ============================================
    
    def list_stmt(self, args: List[Any]) -> str:
        """list/create list/make list"""
        var_name = args[0].value if isinstance(args[0], Token) else str(args[0])
        value = self._expr(args[1])
        return self.indent() + f"{var_name} = {value}"
    
    def dict_stmt(self, args: List[Any]) -> str:
        """dict/dictionary/create dict"""
        var_name = args[0].value if isinstance(args[0], Token) else str(args[0])
        value = self._expr(args[1])
        return self.indent() + f"{var_name} = {value}"
    
    def tuple_stmt(self, args: List[Any]) -> str:
        """tuple/create tuple"""
        var_name = args[0].value if isinstance(args[0], Token) else str(args[0])
        value = self._expr(args[1])
        return self.indent() + f"{var_name} = {value}"
    
    def set_stmt(self, args: List[Any]) -> str:
        """set/create set"""
        var_name = args[0].value if isinstance(args[0], Token) else str(args[0])
        value = self._expr(args[1])
        return self.indent() + f"{var_name} = {value}"
    
    def add_to_list_stmt(self, args: List[Any]) -> str:
        """add/append/put/insert to list"""
        value = self._expr(args[0])
        list_name = args[1].value if isinstance(args[1], Token) else str(args[1])
        return self.indent() + f"{list_name}.append({value})"
    
    def remove_from_list_stmt(self, args: List[Any]) -> str:
        """remove/delete/take out from list"""
        value = self._expr(args[0])
        list_name = args[1].value if isinstance(args[1], Token) else str(args[1])
        return self.indent() + f"{list_name}.remove({value})"
    
    # ============================================
    # Funções
    # ============================================
    
    # ============================================
    # Funções
    # ============================================
    
    def function_def(self, children: List[Any]) -> str:
        """
        function_def: (DEF | FUNC) NAME "(" params? ")" ":" _NEWLINE INDENT block_stmt+ DEDENT
        
        CORRIGIDO: Processa NAME, params e block_stmt+ já transformados.
        NÃO chama self.transform() - o Lark já transformou os filhos.
        """
        if not children:
            return ""
        
        # Filtrar tokens DEF, FUNC, _NEWLINE, ":", INDENT, DEDENT
        # Manter apenas: NAME (string), params (string ou lista), block_stmt+ (strings)
        func_name = None
        params_str = ""
        blocks = []
        
        i = 0
        while i < len(children):
            arg = children[i]
            
            # Ignorar tokens de controle
            if isinstance(arg, Token):
                if arg.type in ['DEF', 'FUNC', '_NEWLINE', 'INDENT', 'DEDENT']:
                    i += 1
                    continue
                if arg.value in [':', '(']:
                    i += 1
                    continue
                if arg.value == ')':
                    i += 1
                    continue
                # Se é NAME, é o nome da função
                if arg.type == 'NAME':
                    func_name = arg.value
                    i += 1
                    continue
            
            # Se não é Token e ainda não temos func_name, processar params
            if func_name and not params_str:
                # Params pode ser Tree ou lista de Tokens
                if hasattr(arg, 'children'):
                    # É Tree (params), processar
                    params_list = []
                    for child in arg.children:
                        if isinstance(child, Token) and child.type == 'NAME':
                            params_list.append(child.value)
                        elif isinstance(child, str):
                            params_list.append(child)
                    params_str = ", ".join(params_list)
                elif isinstance(arg, list):
                    # É lista de params
                    params_list = []
                    for p in arg:
                        if isinstance(p, Token) and p.type == 'NAME':
                            params_list.append(p.value)
                        elif isinstance(p, str):
                            params_list.append(p)
                    params_str = ", ".join(params_list)
                elif isinstance(arg, Tree) and arg.data == 'params':
                    # É Tree de params, processar children
                    params_list = []
                    for child in arg.children:
                        if isinstance(child, Token) and child.type == 'NAME':
                            params_list.append(child.value)
                        elif isinstance(child, str):
                            params_list.append(child)
                    params_str = ", ".join(params_list)
                i += 1
                continue
            
            # Depois vem block_stmt+ (strings já transformadas)
            if isinstance(arg, str) and arg.strip():
                blocks.append(arg)
            # Se é Tree, pode ser block_stmt não transformado
            elif isinstance(arg, Tree):
                blocks.append(str(arg))
            
            i += 1
        
        # Valor padrão
        if not func_name:
            func_name = "func"
        
        # Construir bloco da função
        if blocks:
            block_code = "\n".join(blocks)
        else:
            block_code = "    pass"
        
        # Construir resultado
        code = f"def {func_name}({params_str}):"
        if block_code:
            code += "\n" + block_code
        
        return code
    
    def return_stmt(self, children: List[Any]) -> str:
        """
        return_stmt: RETURN expr?
        
        CORRIGIDO: Processa expr já transformado.
        """
        if not children:
            return self.indent() + "return"
        
        # Filtrar tokens RETURN, _NEWLINE
        filtered = [c for c in children if not (isinstance(c, Token) and c.type in ['RETURN', '_NEWLINE'])]
        
        if not filtered:
            return self.indent() + "return"
        
        # Primeiro arg é expr (já transformado ou Token)
        expr_arg = filtered[0]
        
        # Se é Token, processar
        if isinstance(expr_arg, Token):
            expr = self._expr(expr_arg)
        else:
            # Se já é string, usar diretamente
            expr = str(expr_arg)
        
        # Retornar com indentação atual
        return self.indent() + f"return {expr}"
    
    # ============================================
    # Classes
    # ============================================
    
    def class_def(self, args: List[Any]) -> str:
        """class/create class/make class"""
        class_name = args[0].value if isinstance(args[0], Token) else str(args[0])
        inheritance = f"({self._expr(args[1])})" if len(args) > 1 and args[1] else ""
        self.in_class = True
        return self.indent() + f"class {class_name}{inheritance}:"
    
    def init_stmt(self, args: List[Any]) -> str:
        """init/constructor/initialize/create/setup"""
        params = self._params(args[0]) if args and args[0] else ""
        if params and not params.startswith("self"):
            params = "self, " + params if params else "self"
        elif not params:
            params = "self"
        return self.indent() + f"def __init__({params}):"
    
    def task_stmt(self, args: List[Any]) -> str:
        """task/method/function/do/perform/execute"""
        method_name = args[0].value if isinstance(args[0], Token) else str(args[0])
        params = self._params(args[1]) if len(args) > 1 and args[1] else ""
        if self.in_class and params and not params.startswith("self"):
            params = "self, " + params if params else "self"
        elif self.in_class and not params:
            params = "self"
        return self.indent() + f"def {method_name}({params}):"
    
    # ============================================
    # Atribuições
    # ============================================
    
    def assign_stmt(self, children: List[Any]) -> str:
        """
        assign_stmt: NAME "=" expr
        
        CORRIGIDO: Processa NAME e expr já transformados.
        NÃO chama self.transform() - o Lark já transformou os filhos.
        """
        if not children or len(children) < 2:
            return ""
        
        # Filtrar tokens "="
        filtered = [c for c in children if not (isinstance(c, Token) and c.value == '=')]
        
        if len(filtered) < 2:
            return ""
        
        # Primeiro é NAME, segundo é expr (já transformado)
        var_name = None
        expr_value = None
        
        # Primeiro arg é NAME
        name_arg = filtered[0]
        if isinstance(name_arg, Token) and name_arg.type == 'NAME':
            var_name = name_arg.value
        elif isinstance(name_arg, str):
            var_name = name_arg
        else:
            var_name = str(name_arg)
        
        # Segundo arg é expr (já transformado)
        expr_arg = filtered[1]
        if isinstance(expr_arg, Token):
            expr_value = self._expr(expr_arg)
        else:
            # Se já é string, usar diretamente
            expr_value = str(expr_arg)
        
        # Valor padrão
        if not var_name:
            var_name = "value"
        if not expr_value:
            expr_value = ""
        
        # Retornar com indentação atual
        return self.indent() + f"{var_name} = {expr_value}"
    
    def assignment_stmt(self, args: List[Any]) -> str:
        """Alias para assign_stmt - compatibilidade"""
        return self.assign_stmt(args)
    
    def augmented_assignment_stmt(self, args: List[Any]) -> str:
        """+=/-=/*=//= etc"""
        var_name = args[0].value if isinstance(args[0], Token) else str(args[0])
        op = args[1].value if isinstance(args[1], Token) else str(args[1])
        value = self._expr(args[2])
        return self.indent() + f"{var_name} {op} {value}"
    
    # ============================================
    # Utilitários
    # ============================================
    
    def wait_stmt(self, args: List[Any]) -> str:
        """wait/pause/sleep/delay N seconds"""
        self.needs_imports['time'] = True
        number = args[0].value if isinstance(args[0], Token) else str(args[0])
        return self.indent() + f"time.sleep({number})"
    
    def random_stmt(self, args: List[Any]) -> str:
        """random number from A to B"""
        self.needs_imports['random'] = True
        left = self._expr(args[0])
        right = self._expr(args[1])
        return self.indent() + f"random.randint({left}, {right})"
    
    # ============================================
    # Arquivos
    # ============================================
    
    def open_file_stmt(self, args: List[Any]) -> str:
        """open/read/load file"""
        file_path = self._expr(args[0])
        var_name = args[1].value if isinstance(args[1], Token) else str(args[1])
        return self.indent() + f'with open({file_path}, "r", encoding="utf-8") as {var_name}:'
    
    def save_file_stmt(self, args: List[Any]) -> str:
        """save/write/store to file"""
        content = self._expr(args[0])
        file_path = self._expr(args[1])
        indent = self.indent()
        return indent + f'with open({file_path}, "w", encoding="utf-8") as f:\n{indent}    f.write(str({content}))'
    
    def read_file_stmt(self, args: List[Any]) -> str:
        """read/load/get from file"""
        file_path = self._expr(args[0])
        var_name = args[1].value if isinstance(args[1], Token) else str(args[1])
        indent = self.indent()
        return indent + f'with open({file_path}, "r", encoding="utf-8") as f:\n{indent}    {var_name} = f.read()'
    
    # ============================================
    # Imports
    # ============================================
    
    def use_stmt(self, args: List[Any]) -> str:
        """use/import/load/require/include"""
        module = args[0].value if isinstance(args[0], Token) else str(args[0])
        alias = args[1].value if len(args) > 1 and args[1] else None
        if alias:
            return self.indent() + f"import {module} as {alias}"
        return self.indent() + f"import {module}"
    
    def from_import_stmt(self, args: List[Any]) -> str:
        """from module import item"""
        module = args[0].value if isinstance(args[0], Token) else str(args[0])
        item = args[1].value if len(args) > 1 and args[1] else "*"
        alias = args[2].value if len(args) > 2 and args[2] else None
        if alias:
            return self.indent() + f"from {module} import {item} as {alias}"
        return self.indent() + f"from {module} import {item}"
    
    # ============================================
    # Exceções
    # ============================================
    
    def attempt_stmt(self, args: List[Any]) -> str:
        """attempt/try/attempt to"""
        return self.indent() + "try:"
    
    def catch_stmt(self, args: List[Any]) -> str:
        """catch/except/handle/on error"""
        if args:
            exc_type = args[0].value if isinstance(args[0], Token) else str(args[0])
            exc_var = args[1].value if len(args) > 1 and args[1] else None
            if exc_var:
                return self.indent() + f"except {exc_type} as {exc_var}:"
            return self.indent() + f"except {exc_type}:"
        return self.indent() + "except:"
    
    def finally_stmt(self, args: List[Any]) -> str:
        """finally/always/in the end"""
        return self.indent() + "finally:"
    
    def raise_stmt(self, args: List[Any]) -> str:
        """raise/throw/raise error"""
        expr = self._expr(args[0])
        return self.indent() + f"raise {expr}"
    
    def assert_stmt(self, args: List[Any]) -> str:
        """assert/check/verify/ensure"""
        condition = self._expr(args[0])
        message = self._expr(args[1]) if len(args) > 1 and args[1] else None
        if message:
            return self.indent() + f"assert {condition}, {message}"
        return self.indent() + f"assert {condition}"
    
    # ============================================
    # Avançado
    # ============================================
    
    def lambda_stmt(self, args: List[Any]) -> str:
        """lambda x => x * 2"""
        params = args[0].value if isinstance(args[0], Token) else str(args[0])
        expr = self._expr(args[1])
        return self.indent() + f"lambda {params}: {expr}"
    
    def yield_stmt(self, args: List[Any]) -> str:
        """yield/produce/generate"""
        value = self._expr(args[0])
        return self.indent() + f"yield {value}"
    
    def match_stmt(self, args: List[Any]) -> str:
        """match expression:"""
        expr = self._expr(args[0])
        return self.indent() + f"match {expr}:"
    
    def case_stmt(self, args: List[Any]) -> str:
        """case pattern:"""
        pattern = self._expr(args[0])
        return self.indent() + f"case {pattern}:"
    
    # ============================================
    # Decorators
    # ============================================
    
    def decorator_stmt(self, args: List[Any]) -> str:
        """decorator name:"""
        name = args[0].value if isinstance(args[0], Token) else str(args[0])
        return self.indent() + f"@{name}"
    
    def staticmethod_stmt(self, args: List[Any]) -> str:
        """@staticmethod"""
        return self.indent() + "@staticmethod"
    
    def classmethod_stmt(self, args: List[Any]) -> str:
        """@classmethod"""
        return self.indent() + "@classmethod"
    
    def property_stmt(self, args: List[Any]) -> str:
        """@property"""
        return self.indent() + "@property"
    
    def abstractmethod_stmt(self, args: List[Any]) -> str:
        """@abstractmethod"""
        return self.indent() + "@abstractmethod"
    
    def dataclass_stmt(self, args: List[Any]) -> str:
        """@dataclass"""
        return self.indent() + "@dataclass"
    
    def magic_method_stmt(self, args: List[Any]) -> str:
        """magic __str__():"""
        method_name = args[0].value if isinstance(args[0], Token) else str(args[0])
        params = self._params(args[1]) if len(args) > 1 and args[1] else ""
        if self.in_class and params and not params.startswith("self"):
            params = "self, " + params if params else "self"
        elif self.in_class and not params:
            params = "self"
        return self.indent() + f"def {method_name}({params}):"
    
    # ============================================
    # Macros
    # ============================================
    
    def macro_stmt(self, args: List[Any]) -> str:
        """Macro (math/string/list/file/date/system)"""
        return args[0] if args else ""
    
    def math_macro(self, args: List[Any]) -> str:
        """add/sum/plus, subtract/minus, multiply/times, divide"""
        if len(args) >= 3:
            op = str(args[1]).lower()
            if op in ("and", "plus"):
                return f"({self._expr(args[0])} + {self._expr(args[2])})"
            elif op == "from":
                return f"({self._expr(args[2])} - {self._expr(args[0])})"
            elif op == "by":
                if "multiply" in str(args[0]).lower() or "times" in str(args[0]).lower():
                    return f"({self._expr(args[0])} * {self._expr(args[2])})"
                elif "divide" in str(args[0]).lower():
                    return f"({self._expr(args[0])} / {self._expr(args[2])})"
        return self._expr(args[0]) if args else ""
    
    def string_macro(self, args: List[Any]) -> str:
        """join/combine, split/separate, uppercase/lowercase"""
        if len(args) >= 3:
            # join/combine list with separator
            if "join" in str(args[0]).lower() or "combine" in str(args[0]).lower():
                list_name = self._expr(args[0])
                separator = self._expr(args[2])
                return f"{separator}.join({list_name})"
            # split/separate string by separator
            elif "split" in str(args[0]).lower() or "separate" in str(args[0]).lower():
                string_name = self._expr(args[0])
                separator = self._expr(args[2])
                return f"{string_name}.split({separator})"
        elif len(args) >= 2:
            # uppercase/lowercase string
            var_name = self._expr(args[1])
            if "uppercase" in str(args[0]).lower():
                return f"{var_name}.upper()"
            elif "lowercase" in str(args[0]).lower():
                return f"{var_name}.lower()"
        return ""
    
    def list_macro(self, args: List[Any]) -> str:
        """length/size/count, first/last, reverse/flip, sort/order"""
        if not args:
            return ""
        var_name = self._expr(args[-1])  # Último argumento é sempre a variável
        
        # length/size/count
        if any(x in str(args[0]).lower() for x in ["length", "size", "count"]):
            return f"len({var_name})"
        # first item
        elif "first" in str(args[0]).lower():
            return f"{var_name}[0]"
        # last item
        elif "last" in str(args[0]).lower():
            return f"{var_name}[-1]"
        # reverse/flip
        elif any(x in str(args[0]).lower() for x in ["reverse", "flip"]):
            return f"list(reversed({var_name}))"
        # sort/order
        elif any(x in str(args[0]).lower() for x in ["sort", "order"]):
            return f"sorted({var_name})"
        return ""
    
    def file_macro(self, args: List[Any]) -> str:
        """exists file, delete file"""
        self.needs_imports['os'] = True
        if not args:
            return ""
        file_path = self._expr(args[-1])  # Último argumento é sempre o caminho
        
        # exists file
        if any(x in str(args[0]).lower() for x in ["exists", "file exists"]):
            return f"os.path.exists({file_path})"
        # delete/remove file
        elif any(x in str(args[0]).lower() for x in ["delete", "remove"]):
            return f"os.remove({file_path})"
        return ""
    
    def date_macro(self, args: List[Any]) -> str:
        """current time/now/today"""
        self.needs_imports['datetime'] = True
        if not args:
            return ""
        macro_type = str(args[0]).lower()
        
        if "today" in macro_type:
            return "datetime.date.today()"
        else:  # current time/now/current date
            return "datetime.datetime.now()"
    
    def system_macro(self, args: List[Any]) -> str:
        """exit program/quit program"""
        self.needs_imports['sys'] = True
        return self.indent() + "sys.exit()"
    
    # ============================================
    # Recursos Avançados (99% Python)
    # ============================================
    
    def async_function_def(self, args: List[Any]) -> str:
        """async define/function/task"""
        self.needs_imports['asyncio'] = True
        func_name = args[1].value if isinstance(args[1], Token) else str(args[1])
        params = self._params(args[2]) if len(args) > 2 and args[2] else ""
        return self.indent() + f"async def {func_name}({params}):"
    
    def await_stmt(self, args: List[Any]) -> str:
        """await expression"""
        self.needs_imports['asyncio'] = True
        expr = self._expr(args[0])
        return self.indent() + f"await {expr}"
    
    def generator_function_def(self, args: List[Any]) -> str:
        """Generator function"""
        func_name = args[0].value if isinstance(args[0], Token) else str(args[0])
        params = self._params(args[1]) if len(args) > 1 and args[1] else ""
        return self.indent() + f"def {func_name}({params}):"
    
    def slice_stmt(self, args: List[Any]) -> str:
        """slice list from 1 to 5"""
        var_name = args[0].value if isinstance(args[0], Token) else str(args[0])
        start = self._expr(args[1])
        end = self._expr(args[2])
        return self.indent() + f"{var_name}[{start}:{end}]"
    
    def walrus_stmt(self, args: List[Any]) -> str:
        """x := value"""
        var_name = args[0].value if isinstance(args[0], Token) else str(args[0])
        value = self._expr(args[1])
        return self.indent() + f"{var_name} := {value}"
    
    def type_hint_stmt(self, args: List[Any]) -> str:
        """x: int = 10"""
        var_name = args[0].value if isinstance(args[0], Token) else str(args[0])
        type_ann = self._expr(args[1])
        value = self._expr(args[2]) if len(args) > 2 and args[2] else None
        if value:
            return self.indent() + f"{var_name}: {type_ann} = {value}"
        return self.indent() + f"{var_name}: {type_ann}"
    
    def decorator_with_args_stmt(self, args: List[Any]) -> str:
        """decorator name(args):"""
        name = args[0].value if isinstance(args[0], Token) else str(args[0])
        decorator_args = self._args(args[1]) if len(args) > 1 and args[1] else ""
        return self.indent() + f"@{name}({decorator_args})"
    
    def case_pattern(self, args: List[Any]) -> str:
        """Case pattern"""
        return self._expr(args[0]) if args else "_"
    
    def tuple_pattern(self, args: List[Any]) -> str:
        """Tuple pattern"""
        patterns = [self._expr(arg) for arg in args]
        return "(" + ", ".join(patterns) + ")"
    
    def list_pattern(self, args: List[Any]) -> str:
        """List pattern"""
        patterns = [self._expr(arg) for arg in args]
        return "[" + ", ".join(patterns) + "]"
    
    def args_varargs(self, args: List[Any]) -> str:
        """*args"""
        var_name = args[0].value if isinstance(args[0], Token) else str(args[0])
        return f"*{var_name}"
    
    def kwargs_varargs(self, args: List[Any]) -> str:
        """**kwargs"""
        var_name = args[0].value if isinstance(args[0], Token) else str(args[0])
        return f"**{var_name}"
    
    # ============================================
    # Expressões
    # ============================================
    
    def expression(self, args: List[Any]) -> str:
        """Expressão."""
        if len(args) == 1:
            result = self._expr(args[0])
            # Se result parece ser uma string quebrada, tentar corrigir
            if isinstance(result, str) and '\n' in result:
                lines = result.split('\n')
                if len(lines) > 1 and all(len(line.strip()) == 1 for line in lines if line.strip()):
                    # Pode ser uma string quebrada - verificar se é uma string Python
                    joined = "".join(line.strip() for line in lines if line.strip())
                    if (joined.startswith('"') and joined.endswith('"')) or (joined.startswith("'") and joined.endswith("'")):
                        return joined
            return result
        # Processar operadores
        result = self._expr(args[0])
        for i in range(1, len(args), 2):
            if i + 1 < len(args):
                op = self._expr(args[i])
                right = self._expr(args[i + 1])
                result = f"({result} {op} {right})"
        return result
    
    def term(self, args: List[Any]) -> str:
        """Termo (adição/subtração)."""
        if len(args) == 1:
            return self._expr(args[0])
        result = self._expr(args[0])
        for i in range(1, len(args), 2):
            if i + 1 < len(args):
                op = self._expr(args[i])
                right = self._expr(args[i + 1])
                result = f"({result} {op} {right})"
        return result
    
    def factor(self, args: List[Any]) -> str:
        """Fator (multiplicação/divisão)."""
        if len(args) == 1:
            arg = args[0]
            # Se é um Token STRING, retornar diretamente
            if isinstance(arg, Token) and arg.type == 'STRING':
                return arg.value
            return self._expr(arg)
        result = self._expr(args[0])
        for i in range(1, len(args), 2):
            if i + 1 < len(args):
                op = self._expr(args[i])
                right = self._expr(args[i + 1])
                result = f"({result} {op} {right})"
        return result
    
    def power(self, args: List[Any]) -> str:
        """Power (exponenciação)."""
        if len(args) == 1:
            return self._expr(args[0])
        base = self._expr(args[0])
        exponent = self._expr(args[2]) if len(args) > 2 else None
        if exponent:
            return f"({base} ** {exponent})"
        return base
    
    def atom(self, args: List[Any]) -> str:
        """Atom (número, string, variável, etc.)."""
        return self._expr(args[0])
    
    def attribute_access(self, args: List[Any]) -> str:
        """obj.attr"""
        obj = args[0].value if isinstance(args[0], Token) else str(args[0])
        attr = args[1].value if isinstance(args[1], Token) else str(args[1])
        return f"{obj}.{attr}"
    
    def subscription(self, args: List[Any]) -> str:
        """obj[key] ou obj[start:end:step]"""
        obj = args[0].value if isinstance(args[0], Token) else str(args[0])
        if len(args) > 1:
            key = self._expr(args[1])
            return f"{obj}[{key}]"
        return obj
    
    def slice_expr(self, args: List[Any]) -> str:
        """obj[start:end:step]"""
        obj = args[0].value if isinstance(args[0], Token) else str(args[0])
        start = self._expr(args[1]) if len(args) > 1 else ""
        end = self._expr(args[2]) if len(args) > 2 else ""
        step = self._expr(args[3]) if len(args) > 3 else ""
        if step:
            return f"{obj}[{start}:{end}:{step}]"
        elif end:
            return f"{obj}[{start}:{end}]"
        elif start:
            return f"{obj}[{start}:]"
        return f"{obj}[:]"
    
    def function_call(self, args: List[Any]) -> str:
        """Chamada de função."""
        func_name = args[0].value if isinstance(args[0], Token) else str(args[0])
        func_args = self._args(args[1]) if len(args) > 1 and args[1] else ""
        return f"{func_name}({func_args})"
    
    def _expr(self, expr: Any) -> str:
        """Converte expressão para string."""
        if isinstance(expr, Token):
            # Se é um Token STRING, retornar diretamente (não processar como string Python)
            if expr.type == 'STRING':
                return expr.value
            return expr.value
        elif isinstance(expr, str):
            return expr
        elif hasattr(expr, 'children'):
            # É um nó da árvore - transformar recursivamente
            try:
                # Tentar transformar recursivamente
                transformed = self.transform(expr)
                if isinstance(transformed, str):
                    # Se a string transformada parece quebrada, tentar corrigir
                    if '\n' in transformed:
                        lines = transformed.split('\n')
                        # Se todas as linhas têm apenas um caractere, pode ser uma string quebrada
                        if all(len(line.strip()) == 1 for line in lines if line.strip()):
                            # Verificar se juntando forma uma string Python válida
                            joined = "".join(line.strip() for line in lines if line.strip())
                            if (joined.startswith('"') and joined.endswith('"')) or (joined.startswith("'") and joined.endswith("'")):
                                return joined
                    return transformed
                else:
                    # Se não retornou string, tentar transformar children
                    if hasattr(expr, 'children') and expr.children:
                        parts = []
                        for child in expr.children:
                            part = self._expr(child)
                            if part:
                                parts.append(part)
                        
                        # Se temos apenas uma parte e é uma string completa, retornar diretamente
                        if len(parts) == 1 and isinstance(parts[0], str):
                            return parts[0]
                        
                        # Se todos os parts são strings de um caractere, pode ser uma string quebrada
                        if parts and all(isinstance(p, str) and len(p) == 1 for p in parts):
                            # Pode ser uma string quebrada - tentar juntar
                            joined = "".join(parts)
                            # Se parece com uma string Python (começa e termina com aspas), retornar
                            if (joined.startswith('"') and joined.endswith('"')) or (joined.startswith("'") and joined.endswith("'")):
                                return joined
                        
                        # Se temos apenas uma string completa entre aspas, retornar diretamente
                        if len(parts) == 1 and isinstance(parts[0], str) and ((parts[0].startswith('"') and parts[0].endswith('"')) or (parts[0].startswith("'") and parts[0].endswith("'"))):
                            return parts[0]
                        
                        # Juntar as partes normalmente (mas não se for uma string quebrada)
                        joined = "".join(parts) if parts else str(expr)
                        # Se o resultado final parece ser uma string Python quebrada, tentar corrigir
                        if isinstance(joined, str) and '\n' in joined:
                            lines = joined.split('\n')
                            if all(len(line.strip()) == 1 for line in lines if line.strip()):
                                fixed = "".join(line.strip() for line in lines if line.strip())
                                if (fixed.startswith('"') and fixed.endswith('"')) or (fixed.startswith("'") and fixed.endswith("'")):
                                    return fixed
                        return joined
                    return str(expr)
            except Exception as e:
                # Se falhar, tentar transformar children diretamente
                if hasattr(expr, 'children') and expr.children:
                    parts = []
                    for child in expr.children:
                        part = self._expr(child)
                        if part:
                            parts.append(part)
                    
                    if len(parts) == 1 and isinstance(parts[0], str):
                        return parts[0]
                    
                    if parts and all(isinstance(p, str) and len(p) == 1 for p in parts):
                        joined = "".join(parts)
                        if (joined.startswith('"') and joined.endswith('"')) or (joined.startswith("'") and joined.endswith("'")):
                            return joined
                    return "".join(parts) if parts else str(expr)
                return str(expr)
        else:
            return str(expr)
    
    
    def _params(self, params: Any) -> str:
        """Converte parâmetros para string."""
        if not params:
            return ""
        if isinstance(params, Token):
            return params.value
        if isinstance(params, list):
            return ", ".join(p.value if isinstance(p, Token) else str(p) for p in params)
        return str(params)
    
    def _args(self, args: Any) -> str:
        """Converte argumentos para string."""
        return self._params(args)
    
    # ============================================
    # Literais
    # ============================================
    
    def list_literal(self, args: List[Any]) -> str:
        """Lista literal."""
        if not args:
            return "[]"
        items = [self._expr(arg) for arg in args]
        return "[" + ", ".join(items) + "]"
    
    def dict_literal(self, args: List[Any]) -> str:
        """Dicionário literal."""
        if not args:
            return "{}"
        items = []
        for i in range(0, len(args), 2):
            if i + 1 < len(args):
                key = self._expr(args[i])
                value = self._expr(args[i + 1])
                items.append(f"{key}: {value}")
        return "{" + ", ".join(items) + "}"
    
    def tuple_literal(self, args: List[Any]) -> str:
        """Tupla literal."""
        if not args:
            return "()"
        items = [self._expr(arg) for arg in args]
        return "(" + ", ".join(items) + ")"
    
    def set_literal(self, args: List[Any]) -> str:
        """Set literal."""
        if not args:
            return "set()"
        items = [self._expr(arg) for arg in args]
        return "{" + ", ".join(items) + "}"
    
    # ============================================
    # Outros
    # ============================================
    
    def python_escape(self, args: List[Any]) -> str:
        """Python puro (escape)."""
        return self.indent() + (args[0].value if isinstance(args[0], Token) else str(args[0]))
    
    def comment(self, args: List[Any]) -> str:
        """Comentário."""
        return args[0].value if isinstance(args[0], Token) else str(args[0])
    
    def empty_line(self, args: List[Any]) -> str:
        """Linha vazia."""
        return ""


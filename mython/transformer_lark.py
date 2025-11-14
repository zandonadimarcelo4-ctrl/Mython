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
        """Início do programa."""
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
        
        # Processar cada statement e adicionar às linhas
        for stmt in statements:
            if stmt:
                # Se é Tree, transformar recursivamente
                if isinstance(stmt, Tree):
                    transformed = self.transform(stmt)
                    if transformed:
                        stmt = transformed
                # Se não é string, converter
                if not isinstance(stmt, str):
                    stmt = str(stmt)
                # Adicionar as linhas do statement PRESERVANDO indentação
                if stmt.strip():
                    for line in stmt.split('\n'):
                        # Não fazer strip - preservar indentação completamente
                        if line.strip():  # Apenas verificar se não é linha vazia
                            lines.append(line)
        
        return "\n".join(lines) + "\n"
    
    def statement(self, args: List[Any]) -> str:
        """Um statement."""
        if not args:
            return ""
        result = args[0]
        
        # Se é Tree, transformar recursivamente
        if isinstance(result, Tree):
            transformed = self.transform(result)
            if transformed:
                result = transformed
        
        # Garantir que é string
        if not isinstance(result, str):
            result = str(result)
        
        # Se parece ser uma string quebrada em caracteres (TODAS as linhas têm apenas 1 caractere), tentar corrigir
        if '\n' in result:
            lines = result.split('\n')
            non_empty = [line.strip() for line in lines if line.strip()]
            # Verificar se TODAS as linhas (sem strip) têm exatamente 1 caractere (sem espaços)
            # Isso indica que é uma string realmente quebrada, não código com indentação
            if non_empty and all(len(line) == 1 for line in non_empty):
                # Pode ser uma string quebrada
                joined = "".join(non_empty)
                # Se parece ser código Python válido, usar
                if any(keyword in joined for keyword in ['if', 'else', 'print', '=', '(', ')', ':', '"', "'"]):
                    return joined
        # Retornar resultado como está (preservar indentação e quebras de linha)
        return result
    
    def block_stmt(self, args: List[Any]) -> str:
        """Um statement dentro de um bloco (if, while, for, etc.)."""
        # block_stmt: simple_stmt _NEWLINE? | compound_stmt
        # args[0] = simple_stmt ou compound_stmt
        # args[1] = _NEWLINE? (opcional)
        if not args:
            return ""
        
        # Processar o primeiro argumento (simple_stmt ou compound_stmt)
        result = args[0]
        
        # Se é Tree, transformar recursivamente
        if isinstance(result, Tree):
            transformed = self.transform(result)
            if transformed:
                result = transformed
        
        # Garantir que é string
        if not isinstance(result, str):
            result = str(result)
        
        # Retornar resultado (preservar indentação)
        return result
    
    def simple_stmt(self, args: List[Any]) -> str:
        """Statement simples - transforma recursivamente."""
        if not args:
            return ""
        # args[0] é o statement (say_stmt, ask_stmt, etc.)
        # args[1] pode ser _NEWLINE (opcional)
        result = args[0]
        
        # Se é Tree, transformar recursivamente
        if isinstance(result, Tree):
            transformed = self.transform(result)
            if transformed:
                result = transformed
        
        # Garantir que é string
        if not isinstance(result, str):
            result = str(result)
        
        # Retornar resultado (NEWLINE já foi processado)
        return result
    
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
    
    def say_stmt(self, args: List[Any]) -> str:
        """say - ULTRA SIMPLES: apenas "say" """
        # args[0] = expr
        # args[-1] = _NEWLINE (ignorar)
        expr = self._expr(args[0])
        # Se expr parece ser uma string quebrada (múltiplas linhas de um caractere), tentar corrigir
        if isinstance(expr, str):
            # Verificar se é uma string quebrada em caracteres (sem indentação)
            if '\n' in expr:
                lines = expr.split('\n')
                non_empty = [line.strip() for line in lines if line.strip()]
                # Se TODAS as linhas (sem strip) têm exatamente 1 caractere, é uma string quebrada
                if non_empty and all(len(line) == 1 for line in non_empty):
                    # Juntar todas as linhas
                    expr = "".join(non_empty)
        # Retornar com indentação atual
        return self.indent() + f"print({expr})"
    
    # ============================================
    # Entrada
    # ============================================
    
    def ask_stmt(self, args: List[Any]) -> str:
        """
        ask - ULTRA SIMPLES: apenas "ask" + opcional "number"
        ask name = input() ou ask name number = int(input())
        Também suporta: ask number name = int(input())
        """
        # Detectar padrão: pode ser "ask NAME number STRING?" ou "ask number NAME STRING?"
        # args pode ser:
        # - [NAME, "number", STRING?] - "ask name number ..."
        # - [NAME, "number"] - "ask name number"
        # - ["number", NAME, STRING?] - "ask number name ..."
        # - ["number", NAME] - "ask number name"
        # - [NAME, STRING?] - "ask name ..."
        # - [NAME] - "ask name"
        
        var_name = None
        is_number = False
        prompt = '""'
        
        # Verificar se primeiro argumento é "number" (padrão "ask number NAME")
        if args and isinstance(args[0], Token) and args[0].value == "number":
            is_number = True
            # args[1] deve ser o NAME
            if len(args) > 1:
                var_name = args[1].value if isinstance(args[1], Token) else self._expr(args[1])
            # args[2] pode ser STRING (prompt)
            if len(args) > 2 and hasattr(args[2], 'type') and args[2].type == 'STRING':
                prompt = args[2].value if isinstance(args[2], Token) else self._expr(args[2])
        else:
            # Padrão normal: "ask NAME ..."
            var_name = args[0].value if isinstance(args[0], Token) else self._expr(args[0])
            
            # Verificar se tem "number" ou STRING (prompt)
            for arg in args[1:]:
                # Ignorar _NEWLINE
                if hasattr(arg, 'type') and arg.type == '_NEWLINE':
                    continue
                
                # Verificar se é "number"
                if isinstance(arg, Token) and arg.value == "number":
                    is_number = True
                # Se é STRING, é o prompt
                elif hasattr(arg, 'type') and arg.type == 'STRING':
                    prompt = self._expr(arg)
        
        # Gerar código
        if is_number:
            return self.indent() + f'{var_name} = int(input({prompt}))'
        else:
            return self.indent() + f'{var_name} = input({prompt})'
    
    # ============================================
    # Condições
    # ============================================
    
    def if_stmt(self, args: List[Any]) -> str:
        """
        if_stmt: "if" condition ":" _NEWLINE INDENT block_stmt+ DEDENT else_block?
        
        IMPORTANTE: O Lark injeta INDENT/DEDENT como tokens nos args.
        Estrutura esperada dos args:
        - args[0] = condition (Tree(comparison, ...) ou Tree(atom, ...))
        - args[1] = Token(INDENT, ...) (ignorar - apenas ajustar indent_level)
        - args[2:-2] = block_stmt+ (Tree(simple_stmt, ...) ou Tree(compound_stmt, ...))
        - args[-2] = Token(DEDENT, ...) (ignorar - apenas ajustar indent_level)
        - args[-1] = Tree(else_block, ...) (opcional)
        """
        if not args:
            return ""
        
        # Processar condição
        condition = self._expr(args[0])
        
        # Separar block_stmt+ e else_block?
        block_stmts = []
        else_block_str = None
        
        # Processar args[1:] (pular condition)
        i = 1
        while i < len(args):
            arg = args[i]
            
            # Processar INDENT (ajustar indent_level)
            if isinstance(arg, Token) and arg.type == 'INDENT':
                self.indent_level += 1
                i += 1
                continue
            
            # Processar DEDENT (ajustar indent_level)
            if isinstance(arg, Token) and arg.type == 'DEDENT':
                self.indent_level -= 1
                # Tudo depois do DEDENT é else_block (se existir)
                if i + 1 < len(args):
                    else_block_tree = args[i + 1]
                    if isinstance(else_block_tree, Tree) and else_block_tree.data == 'else_block':
                        # Transformar else_block
                        else_block_str = self.transform(else_block_tree)
                break
            
            # Se é Tree com data 'else_block', é o else_block
            if isinstance(arg, Tree) and arg.data == 'else_block':
                # Transformar else_block
                else_block_str = self.transform(arg)
                break
            
            # Se é Tree com data 'block_stmt' ou 'simple_stmt', transformar recursivamente
            if isinstance(arg, Tree):
                transformed = self.transform(arg)
                if transformed and isinstance(transformed, str) and transformed.strip():
                    block_stmts.append(transformed)
            
            # Se já é string, adicionar diretamente
            elif isinstance(arg, str) and arg.strip() and arg not in ['INDENT', 'DEDENT', '_NEWLINE']:
                block_stmts.append(arg)
            
            i += 1
        
        # Construir bloco if
        if block_stmts:
            # Juntar block_stmts com quebras de linha
            # Cada block_stmt já deve estar indentado corretamente
            block_lines = []
            for stmt in block_stmts:
                for line in stmt.split('\n'):
                    if line.strip():
                        # Adicionar indentação do bloco if (4 espaços)
                        block_lines.append("    " + line.strip())
            block = "\n".join(block_lines)
        else:
            block = "    pass"
        
        # Construir resultado
        result = f"if {condition}:"
        if block:
            result += "\n" + block
        
        # Adicionar else_block se existir
        if else_block_str and isinstance(else_block_str, str):
            # O else_block já retorna "else:" sem indentação extra
            result += "\n" + else_block_str
        
        return result
    
    def else_block(self, args: List[Any]) -> str:
        """
        else_block: _NEWLINE* "else" ":" _NEWLINE INDENT block_stmt+ DEDENT
        
        Estrutura esperada dos args (após o parser processar):
        - args[0] = Token(INDENT, ...) (ignorar - apenas ajustar indent_level)
        - args[1:-1] = block_stmt+ (Tree(simple_stmt, ...) ou Tree(compound_stmt, ...))
        - args[-1] = Token(DEDENT, ...) (ignorar - apenas ajustar indent_level)
        
        NOTA: "else" e ":" já foram consumidos pela gramática e não aparecem nos args.
        """
        if not args:
            return "else:\n    pass"
        
        # Processar block_stmt+
        block_stmts = []
        
        # Processar args (pular INDENT/DEDENT)
        for arg in args:
            # Processar INDENT (ajustar indent_level)
            if isinstance(arg, Token) and arg.type == 'INDENT':
                self.indent_level += 1
                continue
            
            # Processar DEDENT (ajustar indent_level)
            if isinstance(arg, Token) and arg.type == 'DEDENT':
                self.indent_level -= 1
                continue
            
            # Se é Tree, transformar recursivamente
            if isinstance(arg, Tree):
                transformed = self.transform(arg)
                if transformed and isinstance(transformed, str) and transformed.strip():
                    block_stmts.append(transformed)
            
            # Se já é string, adicionar diretamente
            elif isinstance(arg, str) and arg.strip() and arg not in ['INDENT', 'DEDENT', '_NEWLINE', 'else', ':']:
                block_stmts.append(arg)
        
        # Construir bloco else
        if block_stmts:
            # Juntar block_stmts com quebras de linha
            block_lines = []
            for stmt in block_stmts:
                for line in stmt.split('\n'):
                    if line.strip():
                        # Adicionar indentação do bloco else (4 espaços)
                        block_lines.append("    " + line.strip())
            block = "\n".join(block_lines)
        else:
            block = "    pass"
        
        # Construir resultado (else: sem indentação extra - mesmo nível do if)
        result = "else:"
        if block:
            result += "\n" + block
        
        return result
    
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
    # Loops
    # ============================================
    
    def repeat_stmt(self, args: List[Any]) -> str:
        """repeat/do/loop N times"""
        number = args[0].value if isinstance(args[0], Token) else str(args[0])
        block = args[1] if len(args) > 1 else ""
        return self.indent() + f"for _ in range({number}):\n{block}"
    
    def for_each_stmt(self, args: List[Any]) -> str:
        """for each/for every/loop through/iterate over"""
        var_name = args[0].value if isinstance(args[0], Token) else str(args[0])
        expr = self._expr(args[1])
        block = args[2] if len(args) > 2 else ""
        return self.indent() + f"for {var_name} in {expr}:\n{block}"
    
    def while_stmt(self, args: List[Any]) -> str:
        """while/as long as"""
        condition = self._condition(args[0])
        block = args[1] if len(args) > 1 else ""
        return self.indent() + f"while {condition}:\n{block}"
    
    def break_stmt(self, args: List[Any]) -> str:
        """break/stop/exit loop"""
        return self.indent() + "break"
    
    def continue_stmt(self, args: List[Any]) -> str:
        """continue/skip/next"""
        return self.indent() + "continue"
    
    def pass_stmt(self, args: List[Any]) -> str:
        """pass/do nothing"""
        return self.indent() + "pass"
    
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
    
    def function_def(self, args: List[Any]) -> str:
        """define/function/to/create function"""
        func_name = args[0].value if isinstance(args[0], Token) else str(args[0])
        params = self._params(args[1]) if len(args) > 1 and args[1] else ""
        return self.indent() + f"def {func_name}({params}):"
    
    def return_stmt(self, args: List[Any]) -> str:
        """return/give back/send back"""
        value = self._expr(args[0]) if args else ""
        return self.indent() + f"return {value}" if value else self.indent() + "return"
    
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
    
    def assignment_stmt(self, args: List[Any]) -> str:
        """set/assign/let/make/put/store/save/create/initialize"""
        var_name = args[0].value if isinstance(args[0], Token) else str(args[0])
        value = self._expr(args[1])
        return self.indent() + f"{var_name} = {value}"
    
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


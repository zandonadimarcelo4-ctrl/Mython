"""
Transformer para converter AST do Lark em código Python.
Versão simplificada e corrigida - garante que retorna strings, não Trees.
"""

from lark import Transformer, Token, Tree
from typing import List, Any


class MythonTransformer(Transformer):
    """Transforma a árvore de parse do Mython em código Python."""
    
    def __init__(self, source_code: str = None):
        super().__init__()
        self.indent_level = 0
        self.in_class = False
        self.source_code = source_code
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
    # Tokens INDENT/DEDENT/_NEWLINE
    # ============================================
    
    def INDENT(self, token):
        """Token INDENT - incrementa nível de indentação."""
        self.indent_level += 1
        return None  # Não retorna nada - apenas ajusta indent_level
    
    def DEDENT(self, token):
        """Token DEDENT - decrementa nível de indentação."""
        self.indent_level -= 1
        return None  # Não retorna nada - apenas ajusta indent_level
    
    def _NEWLINE(self, token):
        """Token _NEWLINE - nova linha."""
        return None  # Não retorna nada - apenas marca nova linha
    
    # ============================================
    # Top-level: start
    # ============================================
    
    def start(self, statements: List[Any]) -> str:
        """Início do programa - junta todos os statements."""
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
        
        # Processar cada statement
        for stmt in statements:
            if stmt is None:
                continue
            # Se é Tree, transformar recursivamente
            if isinstance(stmt, Tree):
                stmt = self.transform(stmt)
            # Se não é string, converter
            if not isinstance(stmt, str):
                stmt = str(stmt)
            # Adicionar se não estiver vazio
            if stmt.strip():
                lines.append(stmt)
        
        return "\n".join(lines) + "\n"
    
    # ============================================
    # Statements
    # ============================================
    
    def statement(self, args: List[Any]) -> str:
        """statement: simple_stmt _NEWLINE | compound_stmt"""
        if not args:
            return ""
        # args[0] é simple_stmt ou compound_stmt
        # args[1] pode ser _NEWLINE (ignorar)
        result = args[0]
        # Se é Tree, transformar recursivamente
        if isinstance(result, Tree):
            result = self.transform(result)
        # Se não é string, converter
        if not isinstance(result, str):
            result = str(result)
        return result
    
    def simple_stmt(self, args: List[Any]) -> str:
        """simple_stmt: say_stmt | ask_stmt | assign_stmt | ..."""
        if not args:
            return ""
        # args[0] é o statement (say_stmt, ask_stmt, etc.)
        # args[1] pode ser _NEWLINE? (ignorar)
        result = args[0]
        # Se é Tree, transformar recursivamente
        if isinstance(result, Tree):
            result = self.transform(result)
        # Se não é string, converter
        if not isinstance(result, str):
            result = str(result)
        return result
    
    def block_stmt(self, args: List[Any]) -> str:
        """block_stmt: simple_stmt _NEWLINE? | compound_stmt"""
        if not args:
            return ""
        # args[0] é simple_stmt ou compound_stmt
        # args[1] pode ser _NEWLINE? (ignorar)
        result = args[0]
        # Se é Tree, transformar recursivamente
        if isinstance(result, Tree):
            result = self.transform(result)
        # Se não é string, converter
        if not isinstance(result, str):
            result = str(result)
        # Indentar o resultado
        if result.strip():
            lines = result.split('\n')
            indented_lines = []
            for line in lines:
                if line.strip():
                    indented_lines.append(self.indent() + line.strip())
                else:
                    indented_lines.append("")
            return "\n".join(indented_lines)
        return result
    
    def compound_stmt(self, args: List[Any]) -> str:
        """compound_stmt: if_stmt | while_stmt | for_each_stmt | ..."""
        if not args:
            return ""
        # args[0] é o compound statement
        result = args[0]
        # Se é Tree, transformar recursivamente
        if isinstance(result, Tree):
            result = self.transform(result)
        # Se não é string, converter
        if not isinstance(result, str):
            result = str(result)
        return result
    
    # ============================================
    # Saída
    # ============================================
    
    def say_stmt(self, args: List[Any]) -> str:
        """say expr"""
        if not args:
            return self.indent() + "print()"
        expr = self._expr(args[0])
        return self.indent() + f"print({expr})"
    
    # ============================================
    # Entrada
    # ============================================
    
    def ask_stmt(self, args: List[Any]) -> str:
        """ask number NAME STRING? | ask NAME STRING?"""
        var_name = None
        is_number = False
        prompt = '""'
        
        # Processar args para encontrar NAME, "number", e STRING
        for arg in args:
            if isinstance(arg, Token):
                if arg.type == 'NAME':
                    var_name = arg.value
                elif arg.value == "number":
                    is_number = True
                elif arg.type == 'STRING':
                    prompt = arg.value
            elif isinstance(arg, Tree):
                # Se é Tree, transformar recursivamente
                transformed = self.transform(arg)
                if isinstance(transformed, str) and transformed.startswith('"'):
                    prompt = transformed
        
        if not var_name:
            return self.indent() + "input()"
        
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
        
        args deve conter:
        - args[0] = condition (Tree ou string)
        - args[1] = _NEWLINE (None - ignorado)
        - args[2] = INDENT (None - já processado)
        - args[3:-1] = block_stmt+ (já transformados em strings)
        - args[-1] = DEDENT (None - já processado) ou else_block?
        """
        if not args:
            return ""
        
        # Processar condição
        condition = self._expr(args[0])
        
        # Separar block_stmt+ e else_block?
        block_stmts = []
        else_block_str = None
        
        # Processar args[1:] (pular condition)
        # Ignorar None (INDENT/DEDENT/_NEWLINE já processados)
        # Coletar block_stmt+ e else_block?
        i = 1
        while i < len(args):
            arg = args[i]
            if arg is None:
                i += 1
                continue
            # Se é Tree, verificar se é else_block
            if isinstance(arg, Tree) and arg.data == 'else_block':
                # Transformar else_block
                else_block_str = self.transform(arg)
                break
            # Se é string, é um block_stmt já transformado
            elif isinstance(arg, str):
                block_stmts.append(arg)
            # Se é Tree, transformar recursivamente
            elif isinstance(arg, Tree):
                transformed = self.transform(arg)
                if transformed and isinstance(transformed, str):
                    block_stmts.append(transformed)
            i += 1
        
        # Construir bloco if
        if block_stmts:
            # Juntar block_stmts com quebras de linha
            block = "\n".join(stmt for stmt in block_stmts if stmt.strip())
        else:
            block = self.indent() + "    pass"
        
        # Construir resultado
        result = self.indent() + f"if {condition}:"
        if block:
            result += "\n" + block
        
        # Adicionar else_block se existir
        if else_block_str and isinstance(else_block_str, str):
            result += "\n" + else_block_str
        
        return result
    
    def else_block(self, args: List[Any]) -> str:
        """
        else_block: _NEWLINE* "else" ":" _NEWLINE INDENT block_stmt+ DEDENT
        
        args deve conter:
        - args[0:] = _NEWLINE* (None - ignorados)
        - Um arg com "else" (string ou Token)
        - args seguintes = _NEWLINE, INDENT (None - já processados)
        - block_stmt+ (já transformados em strings)
        - DEDENT (None - já processado)
        """
        if not args:
            return ""
        
        # Processar block_stmt+
        block_stmts = []
        
        # Processar args - ignorar None e coletar block_stmt+
        for arg in args:
            if arg is None:
                continue
            # Se é string e não é "else", é um block_stmt já transformado
            if isinstance(arg, str) and arg != "else":
                block_stmts.append(arg)
            # Se é Tree, transformar recursivamente
            elif isinstance(arg, Tree):
                transformed = self.transform(arg)
                if transformed and isinstance(transformed, str):
                    block_stmts.append(transformed)
        
        # Construir bloco else
        if block_stmts:
            # Juntar block_stmts com quebras de linha
            block = "\n".join(stmt for stmt in block_stmts if stmt.strip())
        else:
            block = self.indent() + "    pass"
        
        # Construir resultado
        result = self.indent() + "else:"
        if block:
            result += "\n" + block
        
        return result
    
    # ============================================
    # Expressões
    # ============================================
    
    def condition(self, args: List[Any]) -> str:
        """condition: comparison | atom"""
        if not args:
            return ""
        return self._expr(args[0])
    
    def comparison(self, args: List[Any]) -> str:
        """comparison: atom comparison_op atom"""
        if len(args) < 3:
            return self._expr(args[0]) if args else ""
        left = self._expr(args[0])
        op = self._expr(args[1])
        right = self._expr(args[2])
        return f"{left} {op} {right}"
    
    def comparison_op(self, args: List[Any]) -> str:
        """comparison_op: GREATER | LESS | ..."""
        if not args:
            return ""
        return str(args[0])
    
    def expr(self, args: List[Any]) -> str:
        """expr: atom | function_call | attribute_access | subscription"""
        if not args:
            return ""
        return self._expr(args[0])
    
    def atom(self, args: List[Any]) -> str:
        """atom: NAME | NUMBER | STRING"""
        if not args:
            return ""
        return self._expr(args[0])
    
    def function_call(self, args: List[Any]) -> str:
        """function_call: NAME "(" args? ")" """
        if not args:
            return "()"
        func_name = args[0].value if isinstance(args[0], Token) else str(args[0])
        if len(args) > 1:
            # args[1] pode ser args (Tree) ou "(" / ")" (Token)
            func_args = ""
            for arg in args[1:]:
                if isinstance(arg, Tree) and arg.data == 'args':
                    func_args = self.transform(arg)
                elif isinstance(arg, str) and arg not in ['(', ')']:
                    func_args = arg
            return f"{func_name}({func_args})"
        return f"{func_name}()"
    
    def args(self, args: List[Any]) -> str:
        """args: expr ("," expr)*"""
        if not args:
            return ""
        arg_list = [self._expr(arg) for arg in args if arg not in [',', '(', ')']]
        return ", ".join(arg_list)
    
    def attribute_access(self, args: List[Any]) -> str:
        """attribute_access: NAME "." NAME"""
        if len(args) < 2:
            return self._expr(args[0]) if args else ""
        obj = args[0].value if isinstance(args[0], Token) else str(args[0])
        attr = args[1].value if isinstance(args[1], Token) else str(args[1])
        return f"{obj}.{attr}"
    
    def subscription(self, args: List[Any]) -> str:
        """subscription: NAME "[" expr "]" """
        if len(args) < 2:
            return self._expr(args[0]) if args else ""
        obj = args[0].value if isinstance(args[0], Token) else str(args[0])
        key = self._expr(args[1]) if len(args) > 1 else ""
        return f"{obj}[{key}]"
    
    def _expr(self, expr: Any) -> str:
        """Converte expressão para string."""
        if expr is None:
            return ""
        if isinstance(expr, Token):
            return expr.value
        if isinstance(expr, str):
            return expr
        if isinstance(expr, Tree):
            # Transformar recursivamente
            try:
                transformed = self.transform(expr)
                if isinstance(transformed, str):
                    return transformed
                return str(transformed)
            except Exception as e:
                # Se falhar, tentar processar children
                if hasattr(expr, 'children') and expr.children:
                    parts = [self._expr(child) for child in expr.children if child is not None]
                    return " ".join(parts) if parts else str(expr)
                return str(expr)
        return str(expr)
    
    # ============================================
    # Tokens
    # ============================================
    
    def NAME(self, token):
        return str(token)
    
    def NUMBER(self, token):
        return str(token)
    
    def STRING(self, token):
        return str(token)
    
    def GREATER(self, token):
        return ">"
    
    def LESS(self, token):
        return "<"
    
    def GREATER_EQUAL(self, token):
        return ">="
    
    def LESS_EQUAL(self, token):
        return "<="
    
    def EQUALS(self, token):
        return "=="
    
    def NOT_EQUAL(self, token):
        return "!="


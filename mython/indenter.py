"""
Indenter para Mython - Processa indentação estilo Python.
"""

from lark.indenter import Indenter


class MythonIndenter(Indenter):
    """
    Indenter para Mython que processa indentação estilo Python.
    
    O indenter do Lark processa NEWLINE e gera tokens INDENT/DEDENT
    automaticamente baseado na indentação das linhas.
    """
    
    NL_type = '_NEWLINE'
    OPEN_PAREN_types = ['LPAR', 'LSQB', 'LBRACE']
    CLOSE_PAREN_types = ['RPAR', 'RSQB', 'RBRACE']
    INDENT_type = 'INDENT'
    DEDENT_type = 'DEDENT'
    tab_len = 4


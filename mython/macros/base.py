"""
Sistema base para macros Mython.

Macros permitem expandir comandos simples Mython em código Python complexo.
"""

from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Tuple, Any
from lark import Tree, Token


class MacroError(Exception):
    """Erro relacionado a macros."""
    
    def __init__(self, message: str, line: int = None, col: int = None):
        super().__init__(message)
        self.message = message
        self.line = line
        self.col = col
    
    def __str__(self):
        if self.line is not None:
            return f"MacroError na linha {self.line}, coluna {self.col}: {self.message}"
        return f"MacroError: {self.message}"


class MacroBase(ABC):
    """
    Classe base para todas as macros Mython.
    
    Macros expandem comandos simples em código Python complexo.
    Exemplo: `get data from "url"` → `requests.get("url").json()`
    """
    
    @abstractmethod
    def get_patterns(self) -> Dict[str, str]:
        """
        Retorna dicionário de padrões Mython → regras de gramática Lark.
        
        Exemplo:
        {
            "get_data_from": "GET NAME \"from\" STRING",
            "post_data_to": "POST expr \"to\" STRING \"with\" dict_literal?"
        }
        """
        pass
    
    @abstractmethod
    def expand(self, pattern_name: str, args: List[Any], tree: Tree, transformer=None) -> str:
        """
        Expande um padrão macro em código Python.
        
        Args:
            pattern_name: Nome do padrão (chave do dicionário retornado por get_patterns)
            args: Lista de argumentos parseados da árvore
            tree: Árvore completa do padrão (para contexto)
            transformer: Instância do transformer para processar expressões (opcional)
        
        Returns:
            Código Python gerado
        
        Raises:
            MacroError: Se houver erro na expansão
        """
        pass
    
    def validate(self, pattern_name: str, args: List[Any]) -> bool:
        """
        Valida se os argumentos do padrão são válidos.
        
        Padrão: retorna True se válido, False caso contrário.
        Pode ser sobrescrito para validações específicas.
        """
        return True
    
    def get_required_imports(self, pattern_name: str) -> List[str]:
        """
        Retorna lista de imports necessários para esta macro.
        
        Exemplo: ["import requests", "import json"]
        """
        return []


class MacroRegistry:
    """
    Registro central de macros.
    
    Permite registrar módulos de macros e buscar padrões.
    """
    
    def __init__(self):
        self.macros: List[MacroBase] = []
        self.patterns: Dict[str, Tuple[MacroBase, str]] = {}  # pattern_rule → (macro, pattern_name)
        self.grammar_rules: List[str] = []  # Regras de gramática para adicionar
    
    def register_module(self, macro_module: MacroBase):
        """
        Registra um módulo de macros.
        
        Args:
            macro_module: Instância de MacroBase com padrões e expansões
        """
        self.macros.append(macro_module)
        
        # Registrar padrões deste módulo
        patterns = macro_module.get_patterns()
        for pattern_name, grammar_rule in patterns.items():
            rule_name = f"macro_{pattern_name}"
            
            # Adicionar regra de gramática
            grammar_rule_full = f"{rule_name}: {grammar_rule}"
            self.grammar_rules.append(grammar_rule_full)
            
            # Registrar mapeamento
            self.patterns[rule_name] = (macro_module, pattern_name)
    
    def get_grammar_rules(self) -> List[str]:
        """
        Retorna lista de regras de gramática para adicionar à gramática principal.
        """
        return self.grammar_rules
    
    def find_macro(self, rule_name: str) -> Optional[Tuple[MacroBase, str]]:
        """
        Busca macro por nome de regra.
        
        Args:
            rule_name: Nome da regra (ex: "macro_get_data_from")
        
        Returns:
            Tupla (MacroBase, pattern_name) ou None se não encontrado
        """
        return self.patterns.get(rule_name)
    
    def expand_macro(self, rule_name: str, args: List[Any], tree: Tree, transformer=None) -> str:
        """
        Expande uma macro em código Python.
        
        Args:
            rule_name: Nome da regra (ex: "macro_get_data_from")
            args: Argumentos parseados
            tree: Árvore completa
            transformer: Instância do transformer para processar expressões (opcional)
        
        Returns:
            Código Python gerado
        
        Raises:
            MacroError: Se macro não encontrada ou erro na expansão
        """
        result = self.find_macro(rule_name)
        if result is None:
            raise MacroError(f"Macro não encontrada: {rule_name}")
        
        macro, pattern_name = result
        
        # Validar argumentos
        if not macro.validate(pattern_name, args):
            raise MacroError(f"Argumentos inválidos para macro {pattern_name}")
        
        # Expandir
        try:
            return macro.expand(pattern_name, args, tree, transformer)
        except Exception as e:
            raise MacroError(f"Erro ao expandir macro {pattern_name}: {str(e)}")
    
    def get_all_imports(self) -> List[str]:
        """
        Retorna lista de todos os imports necessários de todas as macros.
        """
        imports = set()
        for macro in self.macros:
            patterns = macro.get_patterns()
            for pattern_name in patterns.keys():
                pattern_imports = macro.get_required_imports(pattern_name)
                imports.update(pattern_imports)
        return sorted(list(imports))


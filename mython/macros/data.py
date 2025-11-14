"""
Macros Data Science para Mython.

Permite trabalhar com dados de forma simples:
- `load "file.csv" into data` → `import pandas as pd; data = pd.read_csv("file.csv")`
- `filter data where column "age" is over 18` → `data[data["age"] > 18]`
"""

from typing import Dict, List, Any
from lark import Tree, Token
from mython.macros.base import MacroBase, MacroError


class DataScienceMacros(MacroBase):
    """Macros para Data Science."""
    
    def get_patterns(self) -> Dict[str, str]:
        """
        Retorna padrões Data Science.
        
        Sintaxe:
        - `load STRING into NAME` → Carregar arquivo CSV/JSON
        - `filter NAME where column STRING is over expr` → Filtrar dataframe
        - `group NAME by STRING` → Agrupar dataframe
        - `sum NAME by STRING` → Somar agrupado
        
        IMPORTANTE: Usar palavras-chave específicas para evitar conflitos.
        """
        return {
            "load_file": '"load" STRING "into" NAME',
            "filter_data": '"filter" NAME "where" "column" STRING comparison_op expr',
            "group_data": '"group" NAME "by" STRING ("as" NAME)?',
            "sum_data": '"sum" NAME "by" STRING ("as" NAME)?',
        }
    
    def expand(self, pattern_name: str, args: List[Any], tree: Tree) -> str:
        """
        Expande padrão Data Science em código Python.
        """
        if pattern_name == "load_file":
            return self._expand_load_file(args)
        elif pattern_name == "filter_data":
            return self._expand_filter_data(args)
        elif pattern_name == "group_data":
            return self._expand_group_data(args)
        elif pattern_name == "sum_data":
            return self._expand_sum_data(args)
        else:
            raise MacroError(f"Padrão desconhecido: {pattern_name}")
    
    def _expand_load_file(self, args: List[Any], transformer=None) -> str:
        """Expande load "file.csv" into data"""
        file_path = None
        var_name = None
        
        for i, arg in enumerate(args):
            if isinstance(arg, Token):
                if arg.type == "STRING":
                    file_path = arg.value
                elif arg.type == "NAME" and i > 0:
                    # Verificar se é "into NAME"
                    if i > 0 and isinstance(args[i-1], Token) and args[i-1].value == "into":
                        var_name = arg.value
        
        if not file_path:
            raise MacroError("Caminho do arquivo não encontrado em load")
        if not var_name:
            raise MacroError("Nome da variável não encontrado em load")
        
        # Detectar tipo de arquivo
        if file_path.endswith('.csv'):
            return f"{var_name} = pd.read_csv({file_path})"
        elif file_path.endswith('.json'):
            return f"{var_name} = pd.read_json({file_path})"
        else:
            # Tentar CSV por padrão
            return f"{var_name} = pd.read_csv({file_path})"
    
    def _expand_filter_data(self, args: List[Any], transformer=None) -> str:
        """Expande filter data where column "age" is over 18"""
        df_name = None
        column = None
        operator = None
        value = None
        
        for i, arg in enumerate(args):
            if isinstance(arg, Token):
                if arg.type == "NAME" and i == 0:
                    df_name = arg.value
                elif arg.type == "STRING" and i > 0:
                    # Verificar se é "column STRING"
                    if i > 0 and isinstance(args[i-1], Token) and args[i-1].value == "column":
                        column = arg.value
                elif arg.type in ["GREATER", "LESS", "GREATER_EQUAL", "LESS_EQUAL", "EQUALS", "NOT_EQUAL"]:
                    operator = arg.value
                elif arg.type in ["NUMBER", "STRING"]:
                    value = arg.value
            elif isinstance(arg, Tree):
                if arg.data == "expr":
                    value = str(arg.children[0]) if arg.children else ""
        
        if not df_name:
            raise MacroError("Nome do dataframe não encontrado em filter")
        if not column:
            raise MacroError("Nome da coluna não encontrado em filter")
        if not operator:
            raise MacroError("Operador não encontrado em filter")
        if value is None:
            raise MacroError("Valor não encontrado em filter")
        
        # Mapear operadores
        op_map = {
            ">": ">",
            "<": "<",
            ">=": ">=",
            "<=": "<=",
            "==": "==",
            "!=": "!=",
        }
        
        python_op = op_map.get(operator, operator)
        return f"{df_name} = {df_name}[{df_name}[{column}] {python_op} {value}]"
    
    def _expand_group_data(self, args: List[Any], transformer=None) -> str:
        """Expande group data by "category" as grouped"""
        df_name = None
        column = None
        var_name = None
        
        for i, arg in enumerate(args):
            if isinstance(arg, Token):
                if arg.type == "NAME":
                    if i == 0:
                        df_name = arg.value
                    elif i > 0 and isinstance(args[i-1], Token) and args[i-1].value == "as":
                        var_name = arg.value
                elif arg.type == "STRING" and i > 0:
                    if isinstance(args[i-1], Token) and args[i-1].value == "by":
                        column = arg.value
        
        if not df_name:
            raise MacroError("Nome do dataframe não encontrado em group")
        if not column:
            raise MacroError("Nome da coluna não encontrado em group")
        
        result_var = var_name or f"{df_name}_grouped"
        return f"{result_var} = {df_name}.groupby({column})"
    
    def _expand_sum_data(self, args: List[Any], transformer=None) -> str:
        """Expande sum data by "category" as summed"""
        df_name = None
        column = None
        var_name = None
        
        for i, arg in enumerate(args):
            if isinstance(arg, Token):
                if arg.type == "NAME":
                    if i == 0:
                        df_name = arg.value
                    elif i > 0 and isinstance(args[i-1], Token) and args[i-1].value == "as":
                        var_name = arg.value
                elif arg.type == "STRING" and i > 0:
                    if isinstance(args[i-1], Token) and args[i-1].value == "by":
                        column = arg.value
        
        if not df_name:
            raise MacroError("Nome do dataframe não encontrado em sum")
        if not column:
            raise MacroError("Nome da coluna não encontrado em sum")
        
        result_var = var_name or f"{df_name}_summed"
        return f"{result_var} = {df_name}.groupby({column}).sum()"
    
    def get_required_imports(self, pattern_name: str) -> List[str]:
        """Retorna imports necessários para macros Data Science."""
        return ["import pandas as pd"]


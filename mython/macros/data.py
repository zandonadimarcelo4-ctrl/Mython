"""
Macros Data Science para Mython.

Permite trabalhar com dados de forma simples:
- `load "file.csv" into data` → `import pandas as pd; data = pd.read_csv("file.csv")`
- `filter data where column "age" is over 18` → `data[data["age"] > 18]`
- `describe data as summary` → `summary = data.describe()`
- `show data head 10` → `print(data.head(10))`
- `plot data column "price" as bar chart` → gráfico pronto com pandas + matplotlib
"""

import ast
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
            "describe_data": '"describe" NAME ("as" NAME)?',
            "show_head": '"show" NAME "head" NUMBER?',
            "plot_column": '"plot" NAME "column" STRING ("as" ("line" | "bar" | "area" | "hist") ("chart")?)?',
        }

    def expand(self, pattern_name: str, args: List[Any], tree: Tree, transformer=None) -> str:
        """
        Expande padrão Data Science em código Python.
        """
        if pattern_name == "load_file":
            return self._expand_load_file(args, transformer)
        elif pattern_name == "filter_data":
            return self._expand_filter_data(args, transformer)
        elif pattern_name == "group_data":
            return self._expand_group_data(args)
        elif pattern_name == "sum_data":
            return self._expand_sum_data(args)
        elif pattern_name == "describe_data":
            return self._expand_describe_data(args)
        elif pattern_name == "show_head":
            return self._expand_show_head(args)
        elif pattern_name == "plot_column":
            return self._expand_plot_column(args)
        else:
            raise MacroError(f"Padrão desconhecido: {pattern_name}")

    # =============================
    # Utilidades internas
    # =============================

    def _token_to_python_string(self, token: Token) -> str:
        """Converte token STRING para valor Python (sem aspas externas)."""
        if not isinstance(token, Token):
            return str(token)
        try:
            return ast.literal_eval(token.value)
        except Exception:
            text = token.value
            if text and text[0] in {'"', "'"} and text[-1] == text[0]:
                return text[1:-1]
            return text

    def _expand_load_file(self, args: List[Any], transformer=None) -> str:
        """Expande load "file.csv" into data"""
        file_path_token = None
        var_name = None

        for i, arg in enumerate(args):
            if isinstance(arg, Token):
                if arg.type == "STRING":
                    file_path_token = arg
                elif arg.type == "NAME" and i > 0:
                    # Verificar se é "into NAME"
                    if i > 0 and isinstance(args[i-1], Token) and args[i-1].value == "into":
                        var_name = arg.value

        if not file_path_token:
            raise MacroError("Caminho do arquivo não encontrado em load")
        if not var_name:
            raise MacroError("Nome da variável não encontrado em load")

        file_path_value = self._token_to_python_string(file_path_token)
        file_literal = file_path_token.value

        # Detectar tipo de arquivo
        lower_path = file_path_value.lower()
        if lower_path.endswith('.csv'):
            return f"{var_name} = pd.read_csv({file_literal})"
        elif lower_path.endswith('.json'):
            return f"{var_name} = pd.read_json({file_literal})"
        else:
            # Tentar CSV por padrão
            return f"{var_name} = pd.read_csv({file_literal})"
    
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
                    if transformer:
                        value = transformer._expr(arg)
                    else:
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

    def _expand_describe_data(self, args: List[Any]) -> str:
        """Gera resumo estatístico com pandas.describe."""
        df_name = None
        target_var = None

        for i, arg in enumerate(args):
            if isinstance(arg, Token) and arg.type == "NAME":
                if df_name is None:
                    df_name = arg.value
                elif i > 0 and isinstance(args[i-1], Token) and args[i-1].value == "as":
                    target_var = arg.value

        if not df_name:
            raise MacroError("Nome do dataframe não encontrado em describe")

        if target_var:
            return f"{target_var} = {df_name}.describe()"
        return f"print({df_name}.describe())"

    def _expand_show_head(self, args: List[Any]) -> str:
        """Mostra as primeiras linhas de um dataframe."""
        df_name = None
        rows = None

        for arg in args:
            if isinstance(arg, Token):
                if arg.type == "NAME" and df_name is None:
                    df_name = arg.value
                elif arg.type == "NUMBER":
                    rows = arg.value

        if not df_name:
            raise MacroError("Nome do dataframe não encontrado em show head")

        row_count = rows or "5"
        return f"print({df_name}.head({row_count}))"

    def _expand_plot_column(self, args: List[Any]) -> str:
        """Cria gráfico simples de uma coluna usando pandas + matplotlib."""
        df_name = None
        column_token = None
        chart_type = "line"

        for i, arg in enumerate(args):
            if isinstance(arg, Token):
                if arg.type == "NAME" and df_name is None:
                    df_name = arg.value
                elif arg.type == "STRING" and column_token is None:
                    column_token = arg
                elif arg.value in {"line", "bar", "area", "hist"}:
                    chart_type = arg.value

        if not df_name:
            raise MacroError("Nome do dataframe não encontrado em plot")
        if not column_token:
            raise MacroError("Nome da coluna não encontrado em plot")

        column_literal = column_token.value
        column_name = self._token_to_python_string(column_token)
        title_text = f"{df_name} {column_name} {chart_type} chart".strip()
        title_literal = repr(title_text)

        lines = [
            "plt.figure()",
            f"{df_name}[{column_literal}].plot(kind='{chart_type}', title={title_literal})",
            "plt.tight_layout()",
            "plt.show()",
        ]
        return "\n".join(lines)

    def get_required_imports(self, pattern_name: str) -> List[str]:
        """Retorna imports necessários para macros Data Science."""
        imports = ["import pandas as pd"]
        if pattern_name == "plot_column":
            imports.append("import matplotlib.pyplot as plt")
        return imports


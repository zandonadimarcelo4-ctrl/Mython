"""
Macros HTTP para Mython.

Permite fazer requisições HTTP de forma simples:
- `get data from "url"` → `requests.get("url").json()`
- `post data to "url" with {"key": "value"}` → `requests.post("url", json={"key": "value"}).json()`
"""

from typing import Dict, List, Any
from lark import Tree, Token
from mython.macros.base import MacroBase, MacroError


class HTTPMacros(MacroBase):
    """Macros para requisições HTTP."""
    
    def get_patterns(self) -> Dict[str, str]:
        """
        Retorna padrões HTTP.
        
        Sintaxe:
        - `get data from STRING as NAME` → GET com resposta JSON
        - `get text from STRING as NAME` → GET com resposta texto
        - `post data to STRING with dict_literal? as NAME` → POST com JSON
        - `post data to STRING as NAME` → POST sem corpo
        """
        return {
            "get_data_from": 'GET ("data" | "json") "from" STRING ("as" NAME)?',
            "get_text_from": 'GET "text" "from" STRING ("as" NAME)?',
            "post_data_to": 'POST ("data" | "json") "to" STRING ("with" dict_literal)? ("as" NAME)?',
            "post_text_to": 'POST "text" "to" STRING ("with" STRING)? ("as" NAME)?',
            "put_data_to": 'PUT ("data" | "json") "to" STRING ("with" dict_literal)? ("as" NAME)?',
            "delete_from": 'DELETE "from" STRING ("as" NAME)?',
        }
    
    def expand(self, pattern_name: str, args: List[Any], tree: Tree, transformer=None) -> str:
        """
        Expande padrão HTTP em código Python.
        
        Args:
            pattern_name: Nome do padrão
            args: Lista de argumentos parseados
            tree: Árvore completa
            transformer: Instância do transformer para processar expressões (opcional)
        """
        if pattern_name == "get_data_from":
            return self._expand_get_data(args, transformer)
        elif pattern_name == "get_text_from":
            return self._expand_get_text(args, transformer)
        elif pattern_name == "post_data_to":
            return self._expand_post_data(args, transformer)
        elif pattern_name == "post_text_to":
            return self._expand_post_text(args, transformer)
        elif pattern_name == "put_data_to":
            return self._expand_put_data(args, transformer)
        elif pattern_name == "delete_from":
            return self._expand_delete(args, transformer)
        else:
            raise MacroError(f"Padrão desconhecido: {pattern_name}")
    
    def _extract_args(self, args: List[Any], transformer=None) -> Dict[str, Any]:
        """
        Extrai argumentos comuns dos tokens.
        """
        result = {
            "url": None,
            "var_name": None,
            "data": None,
        }
        
        for i, arg in enumerate(args):
            if isinstance(arg, Token):
                if arg.type == "STRING":
                    result["url"] = arg.value
                elif arg.type == "NAME" and i > 0:
                    # Verificar se é "as NAME"
                    if i > 0 and isinstance(args[i-1], Token) and args[i-1].value == "as":
                        result["var_name"] = arg.value
                elif arg.value in ["data", "json", "text"]:
                    result["type"] = arg.value
            elif isinstance(arg, Tree):
                if arg.data == "dict_literal":
                    result["data"] = self._process_dict_literal(arg, transformer)
                elif arg.data == "expr":
                    result["data"] = self._process_expr(arg, transformer)

        return result

    def _process_dict_literal(self, tree: Tree, transformer=None) -> str:
        """
        Processa dict_literal em string Python.
        """
        if transformer:
            return transformer.dict_literal(tree.children)
        pairs = []
        for child in tree.children:
            if isinstance(child, Tree) and child.data == "pair":
                key = child.children[0].value if isinstance(child.children[0], Token) else str(child.children[0])
                value = str(child.children[1])
                pairs.append(f"{key}: {value}")
        return "{" + ", ".join(pairs) + "}"

    def _process_expr(self, tree: Tree, transformer=None) -> str:
        """
        Processa expressão em string Python.
        """
        if transformer:
            return transformer._expr(tree)
        return str(tree.children[0]) if tree.children else ""
    
    def _expand_get_data(self, args: List[Any], transformer=None) -> str:
        """Expande GET data from "url" as var_name"""
        extracted = self._extract_args(args, transformer)
        url = extracted["url"]
        var_name = extracted.get("var_name", "response")
        
        if not url:
            raise MacroError("URL não encontrada em get data from")
        
        return f"{var_name} = requests.get({url}).json()"
    
    def _expand_get_text(self, args: List[Any], transformer=None) -> str:
        """Expande GET text from "url" as var_name"""
        extracted = self._extract_args(args, transformer)
        url = extracted["url"]
        var_name = extracted.get("var_name", "response")
        
        if not url:
            raise MacroError("URL não encontrada em get text from")
        
        return f"{var_name} = requests.get({url}).text"
    
    def _expand_post_data(self, args: List[Any], transformer=None) -> str:
        """Expande POST data to "url" with {"key": "value"} as var_name"""
        extracted = self._extract_args(args, transformer)
        url = extracted["url"]
        var_name = extracted.get("var_name", "response")
        data = extracted.get("data")
        
        if not url:
            raise MacroError("URL não encontrada em post data to")
        
        if data:
            return f"{var_name} = requests.post({url}, json={data}).json()"
        else:
            return f"{var_name} = requests.post({url}).json()"
    
    def _expand_post_text(self, args: List[Any], transformer=None) -> str:
        """Expande POST text to "url" with "body" as var_name"""
        extracted = self._extract_args(args, transformer)
        url = extracted["url"]
        var_name = extracted.get("var_name", "response")
        data = extracted.get("data")
        
        if not url:
            raise MacroError("URL não encontrada em post text to")
        
        if data:
            return f"{var_name} = requests.post({url}, data={data}).text"
        else:
            return f"{var_name} = requests.post({url}).text"
    
    def _expand_put_data(self, args: List[Any], transformer=None) -> str:
        """Expande PUT data to "url" with {"key": "value"} as var_name"""
        extracted = self._extract_args(args, transformer)
        url = extracted["url"]
        var_name = extracted.get("var_name", "response")
        data = extracted.get("data")
        
        if not url:
            raise MacroError("URL não encontrada em put data to")
        
        if data:
            return f"{var_name} = requests.put({url}, json={data}).json()"
        else:
            return f"{var_name} = requests.put({url}).json()"
    
    def _expand_delete(self, args: List[Any], transformer=None) -> str:
        """Expande DELETE from "url" as var_name"""
        extracted = self._extract_args(args, transformer)
        url = extracted["url"]
        var_name = extracted.get("var_name", "response")
        
        if not url:
            raise MacroError("URL não encontrada em delete from")
        
        return f"{var_name} = requests.delete({url}).json()"
    
    def get_required_imports(self, pattern_name: str) -> List[str]:
        """Retorna imports necessários para macros HTTP."""
        return ["import requests"]


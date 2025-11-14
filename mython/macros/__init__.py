"""
Sistema de Macros para Mython.

Macros permitem expandir comandos simples em código Python complexo.
Exemplo: `get data from "url"` → `requests.get("url").json()`
"""

from mython.macros.base import MacroBase, MacroRegistry
from mython.macros.http import HTTPMacros
from mython.macros.data import DataScienceMacros

# Registrar macros padrão
registry = MacroRegistry()

# Registrar módulos de macros
registry.register_module(HTTPMacros())
registry.register_module(DataScienceMacros())

# Exportar interface principal
__all__ = [
    'MacroBase',
    'MacroRegistry',
    'registry',
    'HTTPMacros',
    'DataScienceMacros',
]


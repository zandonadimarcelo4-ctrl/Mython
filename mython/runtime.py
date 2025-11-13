"""
Funções auxiliares e built-ins para a linguagem Mython.
"""

import time
import random
from typing import Any, List


def log(message: str) -> None:
    """Registra uma mensagem no console."""
    print(f"[LOG] {message}")


def error(message: str) -> None:
    """Registra uma mensagem de erro."""
    print(f"[ERROR] {message}")


def debug(message: str) -> None:
    """Registra uma mensagem de debug."""
    print(f"[DEBUG] {message}")


def wait(seconds: float) -> None:
    """Aguarda um número de segundos."""
    time.sleep(seconds)


def random_number(min_value: int, max_value: int) -> int:
    """Gera um número aleatório entre min_value e max_value (inclusive)."""
    return random.randint(min_value, max_value)


def random_choice(items: List[Any]) -> Any:
    """Escolhe um item aleatório de uma lista."""
    return random.choice(items)


def read_file(filepath: str) -> str:
    """Lê o conteúdo de um arquivo."""
    with open(filepath, "r", encoding="utf-8") as f:
        return f.read()


def write_file(filepath: str, content: str) -> None:
    """Escreve conteúdo em um arquivo."""
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)


def append_file(filepath: str, content: str) -> None:
    """Adiciona conteúdo ao final de um arquivo."""
    with open(filepath, "a", encoding="utf-8") as f:
        f.write(content)


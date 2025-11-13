"""
Transpiler principal: converte código .logic para Python.
"""

from pathlib import Path
from typing import List


def normalize_condition(text: str) -> str:
    """
    Normaliza expressões naturais em inglês para operadores Python.
    
    Exemplos:
        "age is over 17" -> "age > 17"
        "name is not 'test'" -> "name != 'test'"
    """
    # Ordem importa: do mais longo para o mais curto
    replacements = [
        (" is at least ", " >= "),
        (" is at most ", " <= "),
        (" is over ", " > "),
        (" is under ", " < "),
        (" is not ", " != "),
        (" is ", " == "),
    ]
    
    result = text
    for old, new in replacements:
        result = result.replace(old, new)
    
    return result


def translate_line(line: str, in_class: bool = False) -> str:
    """
    Traduz uma linha de código .logic para Python.
    
    Args:
        line: Linha do arquivo .logic (com indentação preservada)
        in_class: Se estamos dentro de uma classe (para adicionar self aos métodos)
        
    Returns:
        Linha Python equivalente
    """
    indent_size = len(line) - len(line.lstrip(" "))
    indent = " " * indent_size
    stripped = line.strip()
    
    # Linha vazia
    if stripped == "":
        return ""
    
    # Comentário
    if stripped.startswith("#"):
        return indent + stripped
    
    # say
    if stripped.startswith("say "):
        content = stripped[len("say "):]
        return indent + f"print({content})"
    
    # ask number
    if stripped.startswith("ask number "):
        # ask number age "your age"
        parts = stripped.split(" ", 3)
        if len(parts) >= 4:
            var_name = parts[2]
            question = parts[3]
            return indent + f'{var_name} = int(input({question}))'
        # Fallback se não tiver aspas
        var_name = parts[2] if len(parts) > 2 else "value"
        return indent + f'{var_name} = int(input())'
    
    # ask
    if stripped.startswith("ask "):
        # ask name "your name"
        parts = stripped.split(" ", 2)
        if len(parts) >= 3:
            var_name = parts[1]
            question = parts[2]
            return indent + f'{var_name} = input({question})'
        # Fallback se não tiver aspas
        var_name = parts[1] if len(parts) > 1 else "value"
        return indent + f'{var_name} = input()'
    
    # if
    if stripped.startswith("if ") and stripped.endswith(":"):
        condition_text = stripped[len("if "):-1]
        condition_py = normalize_condition(condition_text)
        return indent + f"if {condition_py}:"
    
    # else
    if stripped == "else:":
        return indent + "else:"
    
    # elif
    if stripped.startswith("elif ") and stripped.endswith(":"):
        condition_text = stripped[len("elif "):-1]
        condition_py = normalize_condition(condition_text)
        return indent + f"elif {condition_py}:"
    
    # repeat
    if stripped.startswith("repeat ") and stripped.endswith(" times:"):
        # repeat 3 times:
        middle = stripped[len("repeat "):-len(" times:")].strip()
        return indent + f"for _ in range({middle}):"
    
    # list
    if stripped.startswith("list "):
        # list names = ["ana","bob"]
        return indent + stripped[len("list "):]
    
    # add to list
    if stripped.startswith("add ") and " to " in stripped:
        # add "carlos" to names
        before, after = stripped[len("add "):].split(" to ", 1)
        value = before.strip()
        list_name = after.strip()
        return indent + f"{list_name}.append({value})"
    
    # remove from list
    if stripped.startswith("remove ") and " from " in stripped:
        # remove "ana" from names
        before, after = stripped[len("remove "):].split(" from ", 1)
        value = before.strip()
        list_name = after.strip()
        return indent + f"{list_name}.remove({value})"
    
    # for each
    if stripped.startswith("for each ") and " in " in stripped and stripped.endswith(":"):
        # for each name in names:
        middle = stripped[len("for each "):-1]
        var_name, list_name = [p.strip() for p in middle.split(" in ", 1)]
        return indent + f"for {var_name} in {list_name}:"
    
    # define function
    if stripped.startswith("define ") and stripped.endswith(":"):
        # define greet(name):
        function_header = stripped[len("define "):]
        return indent + f"def {function_header}"
    
    # return
    if stripped.startswith("return "):
        value = stripped[len("return "):]
        return indent + f"return {value}"
    
    # wait
    if stripped.startswith("wait ") and stripped.endswith(" seconds"):
        # wait 3 seconds
        number = stripped[len("wait "):-len(" seconds")].strip()
        return indent + f"time.sleep({number})"
    
    # random number from A to B (pode estar em atribuição ou sozinho)
    if "random number from " in stripped and " to " in stripped:
        # Caso 1: atribuição: number = random number from 1 to 10
        if " = " in stripped:
            var_part, random_part = stripped.split(" = ", 1)
            var_name = var_part.strip()
            if random_part.strip().startswith("random number from "):
                middle = random_part.strip()[len("random number from "):]
                left, right = [p.strip() for p in middle.split(" to ", 1)]
                return indent + f"{var_name} = random.randint({left}, {right})"
        # Caso 2: sozinho: random number from 1 to 10
        elif stripped.startswith("random number from "):
            middle = stripped[len("random number from "):]
            left, right = [p.strip() for p in middle.split(" to ", 1)]
            return indent + f"random.randint({left}, {right})"
    
    # save text to file
    if stripped.startswith("save text ") and " to file " in stripped:
        # save text TEXT to file "name.txt"
        parts = stripped[len("save text "):].split(" to file ", 1)
        if len(parts) == 2:
            text_content = parts[0].strip()
            file_path = parts[1].strip()
            return indent + f'with open({file_path}, "w", encoding="utf-8") as f:\n{indent}    f.write(str({text_content}))'
    
    # read file
    if stripped.startswith("read file ") and " as " in stripped:
        # read file "name.txt" as data
        parts = stripped[len("read file "):].split(" as ", 1)
        if len(parts) == 2:
            file_path = parts[0].strip()
            var_name = parts[1].strip()
            return indent + f'with open({file_path}, "r", encoding="utf-8") as f:\n{indent}    {var_name} = f.read()'
    
    # class
    if stripped.startswith("class ") and stripped.endswith(":"):
        # class Engine:
        class_name = stripped[len("class "):-1].strip()
        return indent + f"class {class_name}:"
    
    # init method (constructor)
    if stripped.startswith("init(") and stripped.endswith("):"):
        # init(name):
        params = stripped[len("init("):-2]
        # Adiciona indentação extra se estiver dentro de uma classe
        if indent_size > 0:
            return indent + f"def __init__(self, {params}):"
        else:
            return indent + f"def __init__(self, {params}):"
    
    # set (atribuição)
    if stripped.startswith("set "):
        # set self.name = value
        # set x = 10
        assignment = stripped[len("set "):]
        if " = " in assignment:
            return indent + assignment
    
    # task (método/função)
    if stripped.startswith("task ") and stripped.endswith(":"):
        # task greet(name):
        method_def = stripped[len("task "):-1]  # Remove o : final
        # Se está dentro de uma classe e o método não tem parâmetros ou não começa com self
        if in_class:
            # Extrair nome do método e parâmetros
            if "(" in method_def:
                method_name, params = method_def.split("(", 1)
                method_name = method_name.strip()
                params = params.rstrip(")").strip()  # Remove o ) final
                if params and not params.strip().startswith("self"):
                    # Adicionar self como primeiro parâmetro
                    return indent + f"def {method_name}(self, {params}):"
                elif not params or params.strip() == "":
                    # Método sem parâmetros, adicionar apenas self
                    return indent + f"def {method_name}(self):"
            else:
                # Sem parênteses, método sem parâmetros
                method_name = method_def.strip()
                return indent + f"def {method_name}(self):"
        return indent + f"def {method_def}:"
    
    # async task
    if stripped.startswith("async task ") and stripped.endswith(":"):
        # async task fetch(url):
        method_def = stripped[len("async task "):]
        return indent + f"async def {method_def}"
    
    # await
    if stripped.startswith("await "):
        # await some_async_function()
        expr = stripped[len("await "):]
        return indent + f"await {expr}"
    
    # decorator
    if stripped.startswith("decorator ") and stripped.endswith(":"):
        # decorator cache:
        decorator_name = stripped[len("decorator "):-1].strip()
        return indent + f"@{decorator_name}"
    
    # attempt (try)
    if stripped == "attempt:":
        return indent + "try:"
    
    # catch (except)
    if stripped.startswith("catch "):
        # catch error:
        # catch Exception as error:
        exception_part = stripped[len("catch "):-1].strip()
        if " as " in exception_part:
            exc_type, exc_var = exception_part.split(" as ", 1)
            return indent + f"except {exc_type.strip()} as {exc_var.strip()}:"
        elif exception_part:
            return indent + f"except {exception_part}:"
        else:
            return indent + "except:"
    
    # finally
    if stripped == "finally:":
        return indent + "finally:"
    
    # open (context manager)
    if stripped.startswith("open ") and " as " in stripped and stripped.endswith(":"):
        # open "file.txt" as f:
        parts = stripped[len("open "):-1].split(" as ", 1)
        if len(parts) == 2:
            file_path = parts[0].strip()
            var_name = parts[1].strip()
            return indent + f'with open({file_path}, "r", encoding="utf-8") as {var_name}:'
    
    # use (import) - mas não processa se já está no header
    if stripped.startswith("use "):
        # use math
        # use json as j
        module_part = stripped[len("use "):].strip()
        if " as " in module_part:
            module, alias = module_part.split(" as ", 1)
            return indent + f"import {module.strip()} as {alias.strip()}"
        else:
            return indent + f"import {module_part}"
    
    # from import
    if stripped.startswith("from ") and " import " in stripped:
        # from math import sqrt
        # from transformers import AutoModel
        return indent + stripped
    
    # load model (IA macro)
    if stripped.startswith("load model ") and " as " in stripped:
        # load model "gpt2" as m
        parts = stripped[len("load model "):].split(" as ", 1)
        if len(parts) == 2:
            model_name = parts[0].strip()
            var_name = parts[1].strip()
            return indent + f'{var_name} = AutoModelForCausalLM.from_pretrained({model_name})'
    
    # agent (IA macro)
    if stripped.startswith("agent ") and stripped.endswith(":"):
        # agent jarvis:
        agent_name = stripped[len("agent "):-1].strip()
        return indent + f"# Agent: {agent_name}"
    
    # goal (para agentes)
    if stripped.startswith("goal "):
        # goal "help the user"
        goal_text = stripped[len("goal "):].strip()
        return indent + f"# Goal: {goal_text}"
    
    # tool (para agentes)
    if stripped.startswith("tool "):
        # tool browser
        tool_name = stripped[len("tool "):].strip()
        return indent + f"# Tool: {tool_name}"
    
    # while
    if stripped.startswith("while ") and stripped.endswith(":"):
        # while condition:
        condition = stripped[len("while "):-1]
        condition_py = normalize_condition(condition)
        return indent + f"while {condition_py}:"
    
    # break
    if stripped == "break":
        return indent + "break"
    
    # continue
    if stripped == "continue":
        return indent + "continue"
    
    # pass
    if stripped == "pass":
        return indent + "pass"
    
    # raise
    if stripped.startswith("raise "):
        # raise Exception("error")
        exception = stripped[len("raise "):]
        return indent + f"raise {exception}"
    
    # assert
    if stripped.startswith("assert "):
        # assert condition
        condition = stripped[len("assert "):]
        condition_py = normalize_condition(condition)
        return indent + f"assert {condition_py}"
    
    # lambda (expressão)
    if " => " in stripped:
        # x => x * 2
        parts = stripped.split(" => ", 1)
        if len(parts) == 2:
            params = parts[0].strip()
            expr = parts[1].strip()
            return indent + f"lambda {params}: {expr}"
    
    # Fallback: Python puro (copia como está)
    return indent + stripped


def transpile_file(input_path: str, output_path: str = None) -> str:
    """
    Transpila um arquivo .logic para Python.
    
    Args:
        input_path: Caminho do arquivo .logic
        output_path: Caminho do arquivo .py de saída (opcional)
        
    Returns:
        Código Python gerado
    """
    src_path = Path(input_path)
    
    if not src_path.exists():
        raise FileNotFoundError(f"Arquivo não encontrado: {input_path}")
    
    lines = src_path.read_text(encoding="utf-8").splitlines()
    py_lines: List[str] = []
    
    needs_time = False
    needs_random = False
    needs_async = False
    needs_transformers = False
    needs_torch = False
    
    # Rastrear contexto (se estamos dentro de uma classe)
    in_class = False
    class_indent = 0
    
    for line in lines:
        stripped = line.strip()
        indent_size = len(line) - len(line.lstrip(" "))
        
        # Detectar início/fim de classe
        if stripped.startswith("class ") and stripped.endswith(":"):
            in_class = True
            class_indent = indent_size
        elif in_class and indent_size <= class_indent and stripped and not stripped.startswith("#"):
            # Sair da classe se a indentação voltar ao nível da classe
            in_class = False
        
        # Detectar uso de time
        if "wait " in stripped and " seconds" in stripped:
            needs_time = True
        
        # Detectar uso de random
        if "random number from " in stripped:
            needs_random = True
        
        # Detectar async
        if stripped.startswith("async ") or "await " in stripped:
            needs_async = True
        
        # Detectar uso de modelos de IA
        if "load model " in stripped or "AutoModel" in stripped or "transformers" in stripped.lower():
            needs_transformers = True
            needs_torch = True
        
        py_line = translate_line(line, in_class=in_class)
        py_lines.append(py_line)
    
    # Montar código final
    header: List[str] = []
    if needs_time:
        header.append("import time")
    if needs_random:
        header.append("import random")
    if needs_async:
        header.append("import asyncio")
    if needs_transformers:
        header.append("from transformers import AutoModelForCausalLM, AutoTokenizer")
    if needs_torch:
        header.append("import torch")
    
    if header:
        full_code = "\n".join(header + [""] + py_lines) + "\n"
    else:
        full_code = "\n".join(py_lines) + "\n"
    
    # Salvar arquivo se output_path foi fornecido
    if output_path:
        out_path = Path(output_path)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(full_code, encoding="utf-8")
    
    return full_code


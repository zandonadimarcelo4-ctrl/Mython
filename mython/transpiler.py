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
        "age greater than 18" -> "age > 18"
    """
    result = text
    
    # Ordem importa: do mais longo para o mais curto
    replacements = [
        # Maior ou igual
        (" is greater than or equal to ", " >= "),
        (" greater than or equal to ", " >= "),
        (" is at least ", " >= "),
        # Menor ou igual
        (" is less than or equal to ", " <= "),
        (" less than or equal to ", " <= "),
        (" is at most ", " <= "),
        # Maior que
        (" is greater than ", " > "),
        (" greater than ", " > "),
        (" is over ", " > "),
        (" is above ", " > "),
        (" above ", " > "),
        # Menor que
        (" is less than ", " < "),
        (" less than ", " < "),
        (" is under ", " < "),
        (" is below ", " < "),
        (" below ", " < "),
        # Diferente
        (" is not equal to ", " != "),
        (" not equal to ", " != "),
        (" is not ", " != "),
        # Igual
        (" equals ", " == "),
        (" equal to ", " == "),
        (" is ", " == "),
    ]
    
    for old, new in replacements:
        result = result.replace(old, new)
    
    return result


def translate_line(line: str, in_class: bool = False, has_staticmethod: bool = False, has_classmethod: bool = False) -> str:
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
    
    # say / print / show / display / tell
    if stripped.startswith("say ") or stripped.startswith("print ") or stripped.startswith("show ") or stripped.startswith("display ") or stripped.startswith("tell "):
        # Extrair o comando usado
        if stripped.startswith("say "):
            content = stripped[len("say "):]
        elif stripped.startswith("print "):
            content = stripped[len("print "):]
        elif stripped.startswith("show "):
            content = stripped[len("show "):]
        elif stripped.startswith("display "):
            content = stripped[len("display "):]
        else:  # tell
            content = stripped[len("tell "):]
        return indent + f"print({content})"
    
    # ask number / ask for number / get number / read number
    if stripped.startswith("ask number ") or stripped.startswith("ask for number ") or stripped.startswith("get number ") or stripped.startswith("read number "):
        # ask number age "your age"
        # ask for number age "your age"
        if stripped.startswith("ask number "):
            parts = stripped.split(" ", 3)
        elif stripped.startswith("ask for number "):
            parts = stripped[len("ask for number "):].split(" ", 1)
            if len(parts) == 2:
                parts = ["ask", "number", parts[0], parts[1]]
            else:
                parts = ["ask", "number", parts[0], '""']
        elif stripped.startswith("get number "):
            parts = stripped.split(" ", 3)
            parts[0] = "ask"
        else:  # read number
            parts = stripped.split(" ", 3)
            parts[0] = "ask"
        
        if len(parts) >= 4:
            var_name = parts[2]
            question = parts[3]
            return indent + f'{var_name} = int(input({question}))'
        # Fallback se não tiver aspas
        var_name = parts[2] if len(parts) > 2 else "value"
        return indent + f'{var_name} = int(input())'
    
    # ask / ask for / get / read / prompt
    if stripped.startswith("ask ") or stripped.startswith("ask for ") or stripped.startswith("get ") or stripped.startswith("read ") or stripped.startswith("prompt "):
        # ask name "your name"
        # ask for name "your name"
        if stripped.startswith("ask for "):
            parts = stripped[len("ask for "):].split(" ", 1)
            if len(parts) == 2:
                parts = ["ask", parts[0], parts[1]]
            else:
                parts = ["ask", parts[0], '""']
        elif stripped.startswith("get "):
            parts = stripped.split(" ", 2)
            parts[0] = "ask"
        elif stripped.startswith("read "):
            parts = stripped.split(" ", 2)
            parts[0] = "ask"
        elif stripped.startswith("prompt "):
            parts = stripped.split(" ", 2)
            parts[0] = "ask"
        else:
            parts = stripped.split(" ", 2)
        
        if len(parts) >= 3:
            var_name = parts[1]
            question = parts[2]
            return indent + f'{var_name} = input({question})'
        # Fallback se não tiver aspas
        var_name = parts[1] if len(parts) > 1 else "value"
        return indent + f'{var_name} = input()'
    
    # if / when / whenever
    if (stripped.startswith("if ") or stripped.startswith("when ") or stripped.startswith("whenever ")) and stripped.endswith(":"):
        if stripped.startswith("if "):
            condition_text = stripped[len("if "):-1]
        elif stripped.startswith("when "):
            condition_text = stripped[len("when "):-1]
        else:  # whenever
            condition_text = stripped[len("whenever "):-1]
        condition_py = normalize_condition(condition_text)
        return indent + f"if {condition_py}:"
    
    # else / otherwise
    if stripped == "else:" or stripped == "otherwise:":
        return indent + "else:"
    
    # elif / else if / or if
    if (stripped.startswith("elif ") or stripped.startswith("else if ") or stripped.startswith("or if ")) and stripped.endswith(":"):
        if stripped.startswith("elif "):
            condition_text = stripped[len("elif "):-1]
        elif stripped.startswith("else if "):
            condition_text = stripped[len("else if "):-1]
        else:  # or if
            condition_text = stripped[len("or if "):-1]
        condition_py = normalize_condition(condition_text)
        return indent + f"elif {condition_py}:"
    
    # repeat / do / loop
    if (stripped.startswith("repeat ") or stripped.startswith("do ") or stripped.startswith("loop ")) and (" times:" in stripped or " time:" in stripped):
        # repeat 3 times: / do 3 times: / loop 3 times:
        if stripped.startswith("repeat "):
            base = stripped[len("repeat "):]
        elif stripped.startswith("do "):
            base = stripped[len("do "):]
        else:  # loop
            base = stripped[len("loop "):]
        
        if " times:" in base:
            middle = base[:-len(" times:")].strip()
        else:  # time:
            middle = base[:-len(" time:")].strip()
        return indent + f"for _ in range({middle}):"
    
    # list / create list / make list
    if stripped.startswith("list ") or stripped.startswith("create list ") or stripped.startswith("make list "):
        # list names = ["ana","bob"] / create list names = [...] / make list names = [...]
        if stripped.startswith("list "):
            return indent + stripped[len("list "):]
        elif stripped.startswith("create list "):
            return indent + stripped[len("create list "):]
        else:  # make list
            return indent + stripped[len("make list "):]
    
    # add to list / append to / put into / insert into
    if (stripped.startswith("add ") or stripped.startswith("append ") or stripped.startswith("put ") or stripped.startswith("insert ")) and (" to " in stripped or " into " in stripped):
        # add "carlos" to names / append "carlos" to names / put "carlos" into names
        if stripped.startswith("add ") and " to " in stripped:
            before, after = stripped[len("add "):].split(" to ", 1)
        elif stripped.startswith("append ") and " to " in stripped:
            before, after = stripped[len("append "):].split(" to ", 1)
        elif stripped.startswith("put ") and " into " in stripped:
            before, after = stripped[len("put "):].split(" into ", 1)
        elif stripped.startswith("insert ") and " into " in stripped:
            before, after = stripped[len("insert "):].split(" into ", 1)
        else:
            # Fallback
            if " to " in stripped:
                before, after = stripped.split(" to ", 1)
                before = before.split()[-1] if " " in before else before
            else:
                before, after = stripped.split(" into ", 1)
                before = before.split()[-1] if " " in before else before
        
        value = before.strip()
        list_name = after.strip()
        return indent + f"{list_name}.append({value})"
    
    # remove from list / delete from / take out from
    if (stripped.startswith("remove ") or stripped.startswith("delete ") or stripped.startswith("take out ")) and " from " in stripped:
        # remove "ana" from names / delete "ana" from names / take out "ana" from names
        if stripped.startswith("remove "):
            before, after = stripped[len("remove "):].split(" from ", 1)
        elif stripped.startswith("delete "):
            before, after = stripped[len("delete "):].split(" from ", 1)
        else:  # take out
            before, after = stripped[len("take out "):].split(" from ", 1)
        value = before.strip()
        list_name = after.strip()
        return indent + f"{list_name}.remove({value})"
    
    # for each / for every / loop through / iterate over
    if ((stripped.startswith("for each ") or stripped.startswith("for every ") or stripped.startswith("loop through ") or stripped.startswith("iterate over ")) and " in " in stripped and stripped.endswith(":")) or (stripped.startswith("for ") and " in " in stripped and stripped.endswith(":") and not stripped.startswith("for each")):
        # for each name in names: / for every item in items: / loop through items: / iterate over items:
        if stripped.startswith("for each "):
            middle = stripped[len("for each "):-1]
        elif stripped.startswith("for every "):
            middle = stripped[len("for every "):-1]
        elif stripped.startswith("loop through "):
            # loop through names as name:
            if " as " in middle:
                middle = stripped[len("loop through "):-1]
                list_name, var_name = [p.strip() for p in middle.split(" as ", 1)]
                return indent + f"for {var_name} in {list_name}:"
            else:
                middle = stripped[len("loop through "):-1]
                list_name = middle.strip()
                var_name = "item"
                return indent + f"for {var_name} in {list_name}:"
        elif stripped.startswith("iterate over "):
            # iterate over names as name:
            middle = stripped[len("iterate over "):-1]
            if " as " in middle:
                list_name, var_name = [p.strip() for p in middle.split(" as ", 1)]
                return indent + f"for {var_name} in {list_name}:"
            else:
                list_name = middle.strip()
                var_name = "item"
                return indent + f"for {var_name} in {list_name}:"
        else:  # for ... in ...:
            middle = stripped[len("for "):-1]
        
        var_name, list_name = [p.strip() for p in middle.split(" in ", 1)]
        return indent + f"for {var_name} in {list_name}:"
    
    # define / function / to / create function
    if (stripped.startswith("define ") or stripped.startswith("function ") or stripped.startswith("to ") or stripped.startswith("create function ")) and stripped.endswith(":"):
        # define greet(name): / function greet(name): / to greet(name): / create function greet(name):
        if stripped.startswith("define "):
            function_header = stripped[len("define "):]
        elif stripped.startswith("function "):
            function_header = stripped[len("function "):]
        elif stripped.startswith("to "):
            function_header = stripped[len("to "):]
        else:  # create function
            function_header = stripped[len("create function "):]
        return indent + f"def {function_header}"
    
    # return / give back / send back
    if stripped.startswith("return ") or stripped.startswith("give back ") or stripped.startswith("send back "):
        if stripped.startswith("return "):
            value = stripped[len("return "):]
        elif stripped.startswith("give back "):
            value = stripped[len("give back "):]
        else:  # send back
            value = stripped[len("send back "):]
        return indent + f"return {value}"
    
    # wait / pause / sleep / delay
    if (stripped.startswith("wait ") or stripped.startswith("pause ") or stripped.startswith("sleep ") or stripped.startswith("delay ")) and (" seconds" in stripped or " second" in stripped):
        # wait 3 seconds / pause 3 seconds / sleep 3 seconds / delay 3 seconds
        if stripped.startswith("wait "):
            base = stripped[len("wait "):]
        elif stripped.startswith("pause "):
            base = stripped[len("pause "):]
        elif stripped.startswith("sleep "):
            base = stripped[len("sleep "):]
        else:  # delay
            base = stripped[len("delay "):]
        
        if " seconds" in base:
            number = base[:-len(" seconds")].strip()
        else:  # second
            number = base[:-len(" second")].strip()
        return indent + f"time.sleep({number})"
    
    # random number from A to B / random between A and B / pick random number from A to B / get random number from A to B
    if ("random number from " in stripped or "random between " in stripped or "pick random number from " in stripped or "get random number from " in stripped) and (" to " in stripped or " and " in stripped):
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
    
    # save text to file / write to file / save to file / store in file
    if (stripped.startswith("save text ") or stripped.startswith("write ") or stripped.startswith("save ") or stripped.startswith("store ")) and (" to file " in stripped or " into file " in stripped or " in file " in stripped):
        # save text TEXT to file "name.txt" / write TEXT to file "name.txt" / save TEXT to file "name.txt"
        if stripped.startswith("save text "):
            base = stripped[len("save text "):]
            if " to file " in base:
                parts = base.split(" to file ", 1)
            elif " into file " in base:
                parts = base.split(" into file ", 1)
            else:
                parts = base.split(" in file ", 1)
        elif stripped.startswith("write "):
            base = stripped[len("write "):]
            if " to file " in base:
                parts = base.split(" to file ", 1)
            elif " into file " in base:
                parts = base.split(" into file ", 1)
            else:
                parts = base.split(" in file ", 1)
        elif stripped.startswith("save "):
            base = stripped[len("save "):]
            if " to file " in base:
                parts = base.split(" to file ", 1)
            elif " into file " in base:
                parts = base.split(" into file ", 1)
            else:
                parts = base.split(" in file ", 1)
        else:  # store
            base = stripped[len("store "):]
            if " in file " in base:
                parts = base.split(" in file ", 1)
            elif " into file " in base:
                parts = base.split(" into file ", 1)
            else:
                parts = base.split(" to file ", 1)
        
        if len(parts) == 2:
            text_content = parts[0].strip()
            file_path = parts[1].strip()
            return indent + f'with open({file_path}, "w", encoding="utf-8") as f:\n{indent}    f.write(str({text_content}))'
    
    # read file / load file / get from file
    if (stripped.startswith("read file ") or stripped.startswith("load file ") or stripped.startswith("get from file ")) and " as " in stripped:
        # read file "name.txt" as data / load file "name.txt" as data / get from file "name.txt" as data
        if stripped.startswith("read file "):
            base = stripped[len("read file "):]
        elif stripped.startswith("load file "):
            base = stripped[len("load file "):]
        else:  # get from file
            base = stripped[len("get from file "):]
        
        parts = base.split(" as ", 1)
        if len(parts) == 2:
            file_path = parts[0].strip()
            var_name = parts[1].strip()
            return indent + f'with open({file_path}, "r", encoding="utf-8") as f:\n{indent}    {var_name} = f.read()'
    
    # class (com ou sem herança)
    if stripped.startswith("class ") and stripped.endswith(":"):
        # class Engine:
        # class Child(Parent):
        class_def = stripped[len("class "):-1].strip()
        # Se já tem parênteses (herança), não adiciona nada
        if "(" in class_def and ")" in class_def:
            return indent + f"class {class_def}:"
        else:
            return indent + f"class {class_def}:"
    
    # init method (constructor)
    if stripped.startswith("init(") and stripped.endswith("):"):
        # init(name):
        params = stripped[len("init("):-2]
        # Adiciona indentação extra se estiver dentro de uma classe
        if indent_size > 0:
            return indent + f"def __init__(self, {params}):"
        else:
            return indent + f"def __init__(self, {params}):"
    
    # set (atribuição) - mas não se já tem operador aumentado
    if stripped.startswith("set ") and not any(op in stripped for op in [" += ", " -= ", " *= ", " /= ", " //= ", " %= ", " **= "]):
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
                
                # Se tem @staticmethod, não adiciona self
                if has_staticmethod:
                    if params:
                        return indent + f"def {method_name}({params}):"
                    else:
                        return indent + f"def {method_name}():"
                # Se tem @classmethod, adiciona cls como primeiro parâmetro
                elif has_classmethod:
                    if params and not params.strip().startswith("cls"):
                        return indent + f"def {method_name}(cls, {params}):"
                    elif not params or params.strip() == "":
                        return indent + f"def {method_name}(cls):"
                    else:
                        return indent + f"def {method_name}({params}):"
                # Método normal, adiciona self
                elif params and not params.strip().startswith("self") and not params.strip().startswith("cls"):
                    return indent + f"def {method_name}(self, {params}):"
                elif not params or params.strip() == "":
                    return indent + f"def {method_name}(self):"
            else:
                # Sem parênteses, método sem parâmetros
                method_name = method_def.strip()
                if has_staticmethod:
                    return indent + f"def {method_name}():"
                elif has_classmethod:
                    return indent + f"def {method_name}(cls):"
                else:
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
    
    # attempt / try / attempt to
    if stripped == "attempt:" or stripped == "try:" or stripped == "attempt to:":
        return indent + "try:"
    
    # catch / except / handle / on error
    if stripped.startswith("catch ") or stripped.startswith("except ") or stripped.startswith("handle ") or stripped.startswith("on error "):
        # catch error: / except error: / handle error: / on error:
        if stripped.startswith("catch "):
            exception_part = stripped[len("catch "):-1].strip()
        elif stripped.startswith("except "):
            exception_part = stripped[len("except "):-1].strip()
        elif stripped.startswith("handle "):
            exception_part = stripped[len("handle "):-1].strip()
        else:  # on error
            exception_part = stripped[len("on error "):-1].strip()
        
        if " as " in exception_part:
            exc_type, exc_var = exception_part.split(" as ", 1)
            return indent + f"except {exc_type.strip()} as {exc_var.strip()}:"
        elif exception_part:
            return indent + f"except {exception_part}:"
        else:
            return indent + "except:"
    
    # finally / always / in the end
    if stripped == "finally:" or stripped == "always:" or stripped == "in the end:":
        return indent + "finally:"
    
    # open / open file / read file / load file
    if (stripped.startswith("open ") or stripped.startswith("open file ") or stripped.startswith("read file ") or stripped.startswith("load file ")) and " as " in stripped and stripped.endswith(":"):
        # open "file.txt" as f: / open file "file.txt" as f: / read file "file.txt" as f:
        if stripped.startswith("open file "):
            base = stripped[len("open file "):-1]
        elif stripped.startswith("read file "):
            base = stripped[len("read file "):-1]
        elif stripped.startswith("load file "):
            base = stripped[len("load file "):-1]
        else:  # open
            base = stripped[len("open "):-1]
        
        parts = base.split(" as ", 1)
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
    
    # while / as long as / keep doing / continue while
    if (stripped.startswith("while ") or stripped.startswith("as long as ") or stripped.startswith("keep doing ") or stripped.startswith("continue while ")) and stripped.endswith(":"):
        # while condition: / as long as condition: / keep doing while condition:
        if stripped.startswith("while "):
            condition = stripped[len("while "):-1]
        elif stripped.startswith("as long as "):
            condition = stripped[len("as long as "):-1]
        elif stripped.startswith("keep doing "):
            if " while " in stripped:
                condition = stripped.split(" while ", 1)[1][:-1]
            else:
                condition = "True"
        else:  # continue while
            condition = stripped[len("continue while "):-1]
        condition_py = normalize_condition(condition)
        return indent + f"while {condition_py}:"
    
    # break / stop / exit loop / leave loop / quit loop
    if stripped == "break" or stripped == "stop" or stripped == "exit loop" or stripped == "leave loop" or stripped == "quit loop":
        return indent + "break"
    
    # continue / skip / next / go to next / proceed
    if stripped == "continue" or stripped == "skip" or stripped == "next" or stripped == "go to next" or stripped == "proceed":
        return indent + "continue"
    
    # pass / do nothing / skip this / ignore
    if stripped == "pass" or stripped == "do nothing" or stripped == "skip this" or stripped == "ignore":
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
    
    # dict (dicionário)
    if stripped.startswith("dict ") and " = " in stripped:
        # dict data = {"key": "value"}
        assignment = stripped[len("dict "):]
        return indent + assignment
    
    # tuple (tupla)
    if stripped.startswith("tuple ") and " = " in stripped:
        # tuple data = (1, 2, 3)
        assignment = stripped[len("tuple "):]
        return indent + assignment
    
    # set (conjunto)
    if stripped.startswith("set ") and " = " in stripped and not stripped.startswith("set self."):
        # set data = {1, 2, 3}
        assignment = stripped[len("set "):]
        return indent + assignment
    
    # Operadores de atribuição aumentada (remover "set " se presente)
    if " += " in stripped:
        # x += 1 ou set x += 1
        if stripped.startswith("set "):
            stripped = stripped[len("set "):]
        var, value = stripped.split(" += ", 1)
        return indent + f"{var.strip()} += {value.strip()}"
    
    if " -= " in stripped:
        if stripped.startswith("set "):
            stripped = stripped[len("set "):]
        var, value = stripped.split(" -= ", 1)
        return indent + f"{var.strip()} -= {value.strip()}"
    
    if " *= " in stripped:
        if stripped.startswith("set "):
            stripped = stripped[len("set "):]
        var, value = stripped.split(" *= ", 1)
        return indent + f"{var.strip()} *= {value.strip()}"
    
    if " /= " in stripped:
        if stripped.startswith("set "):
            stripped = stripped[len("set "):]
        var, value = stripped.split(" /= ", 1)
        return indent + f"{var.strip()} /= {value.strip()}"
    
    if " //= " in stripped:
        if stripped.startswith("set "):
            stripped = stripped[len("set "):]
        var, value = stripped.split(" //= ", 1)
        return indent + f"{var.strip()} //= {value.strip()}"
    
    if " %= " in stripped:
        if stripped.startswith("set "):
            stripped = stripped[len("set "):]
        var, value = stripped.split(" %= ", 1)
        return indent + f"{var.strip()} %= {value.strip()}"
    
    if " **= " in stripped:
        if stripped.startswith("set "):
            stripped = stripped[len("set "):]
        var, value = stripped.split(" **= ", 1)
        return indent + f"{var.strip()} **= {value.strip()}"
    
    # yield (generator)
    if stripped.startswith("yield "):
        value = stripped[len("yield "):]
        return indent + f"yield {value}"
    
    # match/case (Python 3.10+)
    if stripped.startswith("match ") and stripped.endswith(":"):
        expr = stripped[len("match "):-1]
        return indent + f"match {expr}:"
    
    if stripped.startswith("case ") and stripped.endswith(":"):
        pattern = stripped[len("case "):-1]
        return indent + f"case {pattern}:"
    
    # Herança de classes
    if stripped.startswith("class ") and "(" in stripped and ")" in stripped and stripped.endswith(":"):
        # class Child(Parent):
        class_def = stripped[len("class "):-1]
        return indent + f"class {class_def}:"
    
    # @staticmethod (decorator)
    if stripped == "staticmethod:" or stripped == "@staticmethod":
        return indent + "@staticmethod"
    
    # @classmethod (decorator)
    if stripped == "classmethod:" or stripped == "@classmethod":
        return indent + "@classmethod"
    
    # @property (decorator)
    if stripped == "property:" or stripped == "@property":
        return indent + "@property"
    
    # @abstractmethod (decorator)
    if stripped == "abstractmethod:" or stripped == "@abstractmethod":
        return indent + "@abstractmethod"
    
    # @dataclass (decorator)
    if stripped == "dataclass:" or stripped == "@dataclass":
        return indent + "@dataclass"
    
    # Comprehensions (list, dict, set)
    # list comprehension: list [x*2 for x in range(10)]
    if stripped.startswith("list [") and " for " in stripped and " in " in stripped:
        comp = stripped[len("list "):]
        return indent + comp
    
    # dict comprehension: dict {k: v*2 for k, v in data.items()}
    if stripped.startswith("dict {") and " for " in stripped and " in " in stripped:
        comp = stripped[len("dict "):]
        return indent + comp
    
    # set comprehension: set {x*2 for x in range(10)}
    if stripped.startswith("set {") and " for " in stripped and " in " in stripped and not stripped.startswith("set self."):
        comp = stripped[len("set "):]
        return indent + comp
    
    # Slicing (já funciona via Python puro, mas vamos adicionar sintaxe simplificada)
    # list slice: slice list from 1 to 5
    if stripped.startswith("slice ") and " from " in stripped and " to " in stripped:
        # slice list from 1 to 5
        parts = stripped[len("slice "):].split(" from ", 1)
        if len(parts) == 2:
            var_name = parts[0].strip()
            range_part = parts[1].split(" to ", 1)
            if len(range_part) == 2:
                start = range_part[0].strip()
                end = range_part[1].strip()
                return indent + f"{var_name}[{start}:{end}]"
    
    # set / assign / let / make / put / store / save / create / initialize (atribuição simples)
    # IMPORTANTE: Verificar antes do fallback final
    if " = " in stripped and not stripped.startswith("if ") and not stripped.startswith("elif ") and not stripped.startswith("for ") and not stripped.startswith("while ") and not stripped.startswith("when ") and not stripped.startswith("whenever ") and not stripped.startswith("list ") and not stripped.startswith("dict ") and not stripped.startswith("tuple ") and not stripped.startswith("set ") and not stripped.startswith("create list ") and not stripped.startswith("create dict ") and not stripped.startswith("create tuple ") and not stripped.startswith("create set ") and not stripped.startswith("make list ") and not stripped.startswith("make dict ") and not stripped.startswith("make tuple ") and not stripped.startswith("make set "):
        # set x = 10 / assign x = 10 / let x = 10 / make x = 10 / put x = 50 / store x = 60 / save x = 70 / create x = 80 / initialize x = 90
        if stripped.startswith("set "):
            assignment = stripped[len("set "):]
            return indent + assignment
        elif stripped.startswith("assign "):
            assignment = stripped[len("assign "):]
            return indent + assignment
        elif stripped.startswith("let "):
            assignment = stripped[len("let "):]
            return indent + assignment
        elif stripped.startswith("make ") and not stripped.startswith("make list ") and not stripped.startswith("make dict ") and not stripped.startswith("make tuple ") and not stripped.startswith("make set ") and not stripped.startswith("make class "):
            assignment = stripped[len("make "):]
            return indent + assignment
        elif stripped.startswith("put ") and " into " not in stripped and " to " not in stripped:
            assignment = stripped[len("put "):]
            return indent + assignment
        elif stripped.startswith("store ") and " in file " not in stripped and " in " not in stripped:
            assignment = stripped[len("store "):]
            return indent + assignment
        elif stripped.startswith("save ") and " to file " not in stripped and " in file " not in stripped:
            assignment = stripped[len("save "):]
            return indent + assignment
        elif stripped.startswith("create ") and not stripped.startswith("create list ") and not stripped.startswith("create dict ") and not stripped.startswith("create tuple ") and not stripped.startswith("create set ") and not stripped.startswith("create class ") and not stripped.startswith("create function "):
            assignment = stripped[len("create "):]
            return indent + assignment
        elif stripped.startswith("initialize "):
            assignment = stripped[len("initialize "):]
            return indent + assignment
    
    # ============================================
    # MACROS E ATALHOS COMUNS (Palavras Simples)
    # ============================================
    
    # Operações matemáticas comuns
    # add x and y / sum x and y / plus x and y
    if (stripped.startswith("add ") and " and " in stripped) or (stripped.startswith("sum ") and " and " in stripped) or (stripped.startswith("plus ") and " and " in stripped):
        if stripped.startswith("add "):
            parts = stripped[len("add "):].split(" and ", 1)
        elif stripped.startswith("sum "):
            parts = stripped[len("sum "):].split(" and ", 1)
        else:  # plus
            parts = stripped[len("plus "):].split(" and ", 1)
        if len(parts) == 2:
            a, b = parts[0].strip(), parts[1].strip()
            return indent + f"({a} + {b})"
    
    # subtract x from y / minus x from y
    if (stripped.startswith("subtract ") and " from " in stripped) or (stripped.startswith("minus ") and " from " in stripped):
        if stripped.startswith("subtract "):
            parts = stripped[len("subtract "):].split(" from ", 1)
        else:  # minus
            parts = stripped[len("minus "):].split(" from ", 1)
        if len(parts) == 2:
            a, b = parts[0].strip(), parts[1].strip()
            return indent + f"({b} - {a})"
    
    # multiply x by y / times x by y
    if (stripped.startswith("multiply ") and " by " in stripped) or (stripped.startswith("times ") and " by " in stripped):
        if stripped.startswith("multiply "):
            parts = stripped[len("multiply "):].split(" by ", 1)
        else:  # times
            parts = stripped[len("times "):].split(" by ", 1)
        if len(parts) == 2:
            a, b = parts[0].strip(), parts[1].strip()
            return indent + f"({a} * {b})"
    
    # divide x by y
    if stripped.startswith("divide ") and " by " in stripped:
        parts = stripped[len("divide "):].split(" by ", 1)
        if len(parts) == 2:
            a, b = parts[0].strip(), parts[1].strip()
            return indent + f"({a} / {b})"
    
    # Operações de string comuns
    # join list with separator / combine list with separator
    if (stripped.startswith("join ") and " with " in stripped) or (stripped.startswith("combine ") and " with " in stripped):
        if stripped.startswith("join "):
            parts = stripped[len("join "):].split(" with ", 1)
        else:  # combine
            parts = stripped[len("combine "):].split(" with ", 1)
        if len(parts) == 2:
            list_name, separator = parts[0].strip(), parts[1].strip()
            return indent + f"{separator}.join({list_name})"
    
    # split string by separator / separate string by separator
    if (stripped.startswith("split ") and " by " in stripped) or (stripped.startswith("separate ") and " by " in stripped):
        if stripped.startswith("split "):
            parts = stripped[len("split "):].split(" by ", 1)
        else:  # separate
            parts = stripped[len("separate "):].split(" by ", 1)
        if len(parts) == 2:
            string_name, separator = parts[0].strip(), parts[1].strip()
            return indent + f"{string_name}.split({separator})"
    
    # uppercase string / to uppercase string
    if stripped.startswith("uppercase ") or stripped.startswith("to uppercase "):
        if stripped.startswith("uppercase "):
            var_name = stripped[len("uppercase "):].strip()
        else:  # to uppercase
            var_name = stripped[len("to uppercase "):].strip()
        return indent + f"{var_name}.upper()"
    
    # lowercase string / to lowercase string
    if stripped.startswith("lowercase ") or stripped.startswith("to lowercase "):
        if stripped.startswith("lowercase "):
            var_name = stripped[len("lowercase "):].strip()
        else:  # to lowercase
            var_name = stripped[len("to lowercase "):].strip()
        return indent + f"{var_name}.lower()"
    
    # length of list / size of list / count items in list
    if (stripped.startswith("length of ") or stripped.startswith("size of ") or stripped.startswith("count items in ")):
        if stripped.startswith("length of "):
            var_name = stripped[len("length of "):].strip()
        elif stripped.startswith("size of "):
            var_name = stripped[len("size of "):].strip()
        else:  # count items in
            var_name = stripped[len("count items in "):].strip()
        return indent + f"len({var_name})"
    
    # Operações de lista comuns
    # first item in list / last item in list
    if stripped.startswith("first item in ") or stripped.startswith("last item in "):
        if stripped.startswith("first item in "):
            var_name = stripped[len("first item in "):].strip()
            return indent + f"{var_name}[0]"
        else:  # last item in
            var_name = stripped[len("last item in "):].strip()
            return indent + f"{var_name}[-1]"
    
    # reverse list / flip list
    if stripped.startswith("reverse ") or stripped.startswith("flip "):
        if stripped.startswith("reverse "):
            var_name = stripped[len("reverse "):].strip()
        else:  # flip
            var_name = stripped[len("flip "):].strip()
        return indent + f"list(reversed({var_name}))"
    
    # sort list / order list
    if stripped.startswith("sort ") or stripped.startswith("order "):
        if stripped.startswith("sort "):
            var_name = stripped[len("sort "):].strip()
        else:  # order
            var_name = stripped[len("order "):].strip()
        return indent + f"sorted({var_name})"
    
    # Operações de arquivo comuns
    # exists file "path" / file exists "path"
    if (stripped.startswith("exists file ") or stripped.startswith("file exists ")):
        if stripped.startswith("exists file "):
            file_path = stripped[len("exists file "):].strip()
        else:  # file exists
            file_path = stripped[len("file exists "):].strip()
        return indent + f"os.path.exists({file_path})"
    
    # delete file "path" / remove file "path"
    if (stripped.startswith("delete file ") or stripped.startswith("remove file ")):
        if stripped.startswith("delete file "):
            file_path = stripped[len("delete file "):].strip()
        else:  # remove file
            file_path = stripped[len("remove file "):].strip()
        return indent + f"os.remove({file_path})"
    
    # Operações de data/hora comuns
    # current time / now / current date
    if stripped == "current time" or stripped == "now" or stripped == "current date":
        return indent + "datetime.datetime.now()"
    
    # today / current date
    if stripped == "today":
        return indent + "datetime.date.today()"
    
    # Operações de sistema comuns
    # exit program / quit program / stop program
    if stripped == "exit program" or stripped == "quit program" or stripped == "stop program":
        return indent + "sys.exit()"
    
    # Operador in/not in (normalização)
    if " is in " in stripped:
        stripped = stripped.replace(" is in ", " in ")
    if " is not in " in stripped:
        stripped = stripped.replace(" is not in ", " not in ")
    
    # Walrus operator (Python 3.8+): set x := value
    if " := " in stripped:
        # Já funciona como Python puro, mas vamos garantir
        return indent + stripped
    
    # Métodos especiais (magic methods)
    # __str__, __len__, __repr__, etc. - já funciona via Python puro
    # Mas vamos adicionar sintaxe simplificada
    if stripped.startswith("magic ") and "(" in stripped:
        # magic __str__(): return "string"
        method_def = stripped[len("magic "):]
        if in_class:
            # Adicionar self se necessário
            if "(" in method_def and ")" in method_def:
                method_name, params = method_def.split("(", 1)
                method_name = method_name.strip()
                params = params.rstrip(")").strip()
                if not params.startswith("self"):
                    return indent + f"def {method_name}(self):"
                else:
                    return indent + f"def {method_def}"
            return indent + f"def {method_def}"
    
    # Múltipla herança: class Child(Parent1, Parent2):
    # Já funciona via Python puro, mas vamos garantir
    
    # Type hints: já funciona via Python puro
    # def func(x: int) -> str: - funciona como Python puro
    
    # Funções aninhadas: já funciona via Python puro
    
    # Context managers customizados: já funciona via Python puro
    
    # Import relativo: from .module import - já funciona via Python puro
    
    # Argumentos padrão: define func(x=10): - já funciona via Python puro
    # *args e **kwargs: define func(*args, **kwargs): - já funciona via Python puro
    
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
    previous_line = ""  # Para detectar decorators
    
    for i, line in enumerate(lines):
        stripped = line.strip()
        indent_size = len(line) - len(line.lstrip(" "))
        
        # Detectar início/fim de classe
        if stripped.startswith("class ") and stripped.endswith(":"):
            in_class = True
            class_indent = indent_size
        elif in_class and indent_size <= class_indent and stripped and not stripped.startswith("#"):
            # Sair da classe se a indentação voltar ao nível da classe
            in_class = False
        
        # Verificar linha anterior para decorators
        has_staticmethod = i > 0 and lines[i-1].strip() in ["@staticmethod", "staticmethod:"]
        has_classmethod = i > 0 and lines[i-1].strip() in ["@classmethod", "classmethod:"]
        
        # Atualizar previous_line
        previous_line = stripped
        
        # Detectar uso de os
        if "exists file " in stripped or "file exists " in stripped or "delete file " in stripped or "remove file " in stripped:
            needs_os = True
        
        # Detectar uso de datetime
        if stripped == "current time" or stripped == "now" or stripped == "current date" or stripped == "today":
            needs_datetime = True
        
        # Detectar uso de sys
        if stripped == "exit program" or stripped == "quit program" or stripped == "stop program":
            needs_sys = True
        
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
        
        # Verificar se linha anterior tem decorator
        has_staticmethod = i > 0 and lines[i-1].strip() in ["@staticmethod", "staticmethod:"]
        has_classmethod = i > 0 and lines[i-1].strip() in ["@classmethod", "classmethod:"]
        
        py_line = translate_line(line, in_class=in_class, has_staticmethod=has_staticmethod, has_classmethod=has_classmethod)
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


# Mython - Referência Rápida

## 🟩 Camada A2 - Básica

### Entrada/Saída
```logic
say "Hello"              # print("Hello")
ask name "Name? "        # name = input("Name? ")
ask number age "Age? "   # age = int(input("Age? "))
```

### Condições
```logic
if age is over 18:       # if age > 18:
    say "adult"
else:
    say "minor"
```

### Loops
```logic
repeat 5 times:          # for _ in range(5):
    say "hello"

for each item in items:  # for item in items:
    say item

while condition:         # while condition:
    say "running"
```

### Listas
```logic
list names = ["a", "b"]  # names = ["a", "b"]
add "c" to names         # names.append("c")
remove "a" from names    # names.remove("a")
```

### Funções
```logic
define greet(name):      # def greet(name):
    say "Hello " + name
```

### Arquivos
```logic
read file "a.txt" as data           # with open("a.txt") as f: data = f.read()
save text "hello" to file "a.txt"   # with open("a.txt", "w") as f: f.write("hello")
open "file.txt" as f:               # with open("file.txt") as f:
    set lines = f.readlines()
```

### Utilitários
```logic
wait 3 seconds                       # time.sleep(3)
set n = random number from 1 to 10   # n = random.randint(1, 10)
```

---

## 🟦 Camada A2-Advanced

### Classes
```logic
class Person:
    init(name):                      # def __init__(self, name):
        set self.name = name         #     self.name = name
    
    task greet():                    # def greet(self):
        say "Hello " + self.name
```

### Async/Await
```logic
async task fetch(url):               # async def fetch(url):
    await asyncio.sleep(1)           #     await asyncio.sleep(1)
    return "data"                    #     return "data"
```

### Exceções
```logic
attempt:                             # try:
    risky()                          #     risky()
catch ValueError as e:               # except ValueError as e:
    say str(e)                       #     print(str(e))
finally:                             # finally:
    cleanup()                        #     cleanup()
```

### Decorators
```logic
decorator cache:                     # @cache
    task func(x):                    # def func(x):
        return x * 2                 #     return x * 2
```

### Imports
```logic
use math                             # import math
use json as j                        # import json as j
from math import sqrt                # from math import sqrt
```

### Lambda
```logic
set double = x => x * 2              # double = lambda x: x * 2
```

### Controle
```logic
break                                # break
continue                             # continue
pass                                 # pass
raise ValueError("error")            # raise ValueError("error")
assert x is over 0                   # assert x > 0
```

---

## 🤖 Macros de IA

```logic
load model "gpt2" as model           # model = AutoModelForCausalLM.from_pretrained("gpt2")

agent Jarvis:                        # # Agent: Jarvis
    goal "help user"                 # # Goal: help user
    tool browser                     # # Tool: browser
```

---

## 🔧 Operadores

| Mython | Python |
|--------|--------|
| `is` | `==` |
| `is not` | `!=` |
| `is over` | `>` |
| `is under` | `<` |
| `is at least` | `>=` |
| `is at most` | `<=` |

---

**Mython 1.0** - Referência rápida 🐍


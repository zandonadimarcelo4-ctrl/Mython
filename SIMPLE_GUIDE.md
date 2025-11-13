# Guia Simples do Mython

## 🎯 Mython é para Lógica Simples

Mython existe para você escrever **lógica de computador de forma simples**. Só lógica. Nada complicado.

## ✅ O que você pode fazer

### Entrada e Saída
```logic
say "Hello"                    # Mostrar texto
ask name "Seu nome? "          # Pedir texto
ask number age "Sua idade? "   # Pedir número
```

### Condições
```logic
if idade is over 18:
    say "Maior de idade"
else:
    say "Menor de idade"
```

### Repetir
```logic
repeat 5 times:
    say "Olá"

for each item in lista:
    say item
```

### Listas
```logic
list nomes = ["Ana", "Bob"]
add "Carlos" to nomes
remove "Ana" from nomes
```

### Funções
```logic
define cumprimentar(nome):
    say "Olá, " + nome

cumprimentar("Maria")
```

### Arquivos
```logic
read file "arquivo.txt" as conteudo
save text "Olá" to file "saida.txt"
```

## ❌ O que NÃO fazer

- ❌ Não complique
- ❌ Não use coisas avançadas se não precisar
- ❌ Não tente fazer sistemas complexos
- ❌ Mantenha simples

## 💡 Dica

Se você precisa de algo complicado, use Python puro no seu código Mython:

```logic
# Lógica simples em Mython
say "Processando..."

# Python puro para coisas complicadas
import complex_library
result = complex_library.do_something()
say result
```

## 🎯 Lembre-se

**Mython = Lógica Simples**

Escreva o que você pensa. Mantenha simples. Só lógica.

---

**Mython** - Apenas lógica, nada mais. 🐍


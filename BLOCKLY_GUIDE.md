# Guia de Integração Blockly + Mython

## 🎯 Visão Geral

Blockly permite criar código visualmente usando blocos. Integrado com Mython, cria a **escada de aprendizado perfeita**.

---

## 🚀 Início Rápido

### 1. Abrir Workspace Blockly

Abra `mython/blockly/workspace.html` no navegador.

### 2. Arrastar Blocos

Arraste blocos da toolbox para criar seu programa.

### 3. Gerar Mython

Clique em "Gerar Mython" para ver o código `.logic` gerado.

### 4. Transpilar e Executar

```bash
mython generated.logic --run
```

---

## 📚 Blocos Disponíveis

### Básico
- **say**: Mostrar texto
- **ask**: Pedir entrada de texto
- **ask number**: Pedir número
- **set**: Definir variável
- **get**: Obter valor de variável

### Controle
- **if**: Condição
- **repeat**: Repetir N vezes
- **for each**: Loop em lista
- **while**: Loop condicional

### Listas
- **create list**: Criar lista
- **add to list**: Adicionar item

### Lógica
- **compare**: Comparações (is, is over, etc.)
- **and/or**: Operadores lógicos

### Matemática
- **number**: Número
- **arithmetic**: Operações matemáticas

### Texto
- **text**: Texto
- **join**: Juntar textos

---

## 🎯 Exemplos

### Exemplo 1: Hello World

**Blocos:**
```
┌─────────────┐
│   say       │
│ "Hello"     │
└─────────────┘
```

**Gera:**
```logic
say "Hello"
```

### Exemplo 2: Perguntar e Responder

**Blocos:**
```
┌─────────────┐
│   ask       │
│ name        │
│ "Name?"     │
└─────────────┘
┌─────────────┐
│   say       │
│ "Hello " +  │
│ name        │
└─────────────┘
```

**Gera:**
```logic
ask name "Name?"
say "Hello " + name
```

### Exemplo 3: Loop

**Blocos:**
```
┌─────────────┐
│   repeat    │
│   5 times   │
│   ┌───────┐ │
│   │  say  │ │
│   │"Hello"│ │
│   └───────┘ │
└─────────────┘
```

**Gera:**
```logic
repeat 5 times:
    say "Hello"
```

---

## 🔧 Como Funciona

### Fluxo Completo

```
1. Usuário arrasta blocos
   ↓
2. Blockly gera código Mython
   ↓
3. Transpiler converte para Python
   ↓
4. Python executa
```

### Gerador Blockly → Mython

O arquivo `generator.js` contém funções que convertem cada tipo de bloco para código Mython:

```javascript
Blockly.Mython['say'] = function(block) {
    var text = Blockly.Mython.valueToCode(block, 'TEXT',
        Blockly.Mython.ORDER_NONE) || '""';
    return 'say ' + text + '\n';
};
```

---

## 🎯 Modos de Uso

### Modo 1: Apenas Blocos
- Arrastar blocos
- Gerar Mython
- Transpilar e executar

### Modo 2: Blocos + Texto
- Começar com blocos
- Editar código Mython gerado
- Transpilar e executar

### Modo 3: Apenas Texto
- Escrever Mython diretamente
- Transpilar e executar

---

## 🚀 Próximos Passos

1. **Adicionar mais blocos**: Classes, async, IA
2. **Interface melhorada**: Editor visual completo
3. **Conversão bidirecional**: Mython → Blocos
4. **Exportar/Importar**: Salvar projetos
5. **Execução online**: Executar direto no navegador

---

## 💡 Dicas

1. **Comece simples**: Use blocos básicos primeiro
2. **Veja o código**: Sempre veja o Mython gerado
3. **Edite depois**: Você pode editar o Mython gerado
4. **Combine**: Use blocos + texto juntos

---

**Mython + Blockly** - Do visual ao código profissional! 🐍🧩✨


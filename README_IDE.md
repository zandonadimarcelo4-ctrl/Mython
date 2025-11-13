# 🐍 Mython IDE - Interface Streamlit

Interface web para escrever, transpilar e executar código Mython.

## 🚀 Como Usar

### Instalação

```bash
# Instalar dependências
pip install streamlit

# Ou instalar com dependências opcionais
pip install -e ".[ide]"
```

### Executar a IDE

**Windows (Recomendado):**
```bash
# Opção 1: Duplo clique no arquivo
start_ide.bat

# Opção 2: Versão simples
start_ide_simple.bat
```

**Linux/Mac ou Python direto:**
```bash
# Opção 1: Usando o script
python run_ide.py

# Opção 2: Diretamente com Streamlit
streamlit run streamlit_app.py
```

A IDE abrirá automaticamente no navegador em `http://localhost:8501`

## ✨ Funcionalidades

### 📝 Editor de Código
- Escreva código Mython diretamente no navegador
- Editor com syntax highlighting
- Exemplos prontos para carregar

### 🔄 Transpilação
- Transpila código Mython para Python em tempo real
- Mostra o código Python gerado
- Validação de sintaxe

### ▶️ Execução
- Execute o código Python gerado
- Veja a saída em tempo real
- Tratamento de erros

### 📚 Exemplos
- Hello World
- Verificar Idade
- Lista de Nomes
- Função Soma
- Classe Person
- Loop com Condição

## 🎯 Interface

A IDE possui:
- **Editor Mython**: Escreva seu código
- **Código Python Gerado**: Veja a tradução
- **Saída da Execução**: Veja os resultados
- **Sidebar**: Exemplos e documentação

## 💡 Exemplo de Uso

1. Abra a IDE
2. Escreva código Mython:
   ```logic
   say "Hello, World!"
   ask name "What is your name? "
   say "Hello, " + name
   ```
3. Clique em "Transpilar para Python"
4. Veja o código Python gerado
5. Clique em "Executar Python"
6. Veja a saída!

## 🎨 Recursos

- ✅ Editor de código integrado
- ✅ Transpilação em tempo real
- ✅ Execução de código
- ✅ Exemplos prontos
- ✅ Interface responsiva
- ✅ Tratamento de erros

---

**Mython IDE** - Desenvolvido com Streamlit 🐍✨


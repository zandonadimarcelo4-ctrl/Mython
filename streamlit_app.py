"""
Mython IDE - Interface Streamlit
IDE temporária para escrever, transpilar e executar código Mython
"""

import streamlit as st
import subprocess
import tempfile
import os
import sys
from pathlib import Path
# Tentar usar Lark primeiro, fallback para versão antiga
try:
    from mython.transpiler_lark import transpile_file
    LARK_AVAILABLE = True
except ImportError:
    from mython.transpiler import transpile_file
    LARK_AVAILABLE = False

# Configuração da página
st.set_page_config(
    page_title="Mython IDE",
    page_icon="🐍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS customizado
st.markdown("""
<style>
    .stTextArea textarea {
        font-family: 'Courier New', monospace;
        font-size: 14px;
    }
    .code-block {
        background-color: #f0f0f0;
        padding: 15px;
        border-radius: 5px;
        border-left: 4px solid #1f77b4;
    }
    .success-box {
        background-color: #d4edda;
        padding: 10px;
        border-radius: 5px;
        border-left: 4px solid #28a745;
        margin: 10px 0;
    }
    .error-box {
        background-color: #f8d7da;
        padding: 10px;
        border-radius: 5px;
        border-left: 4px solid #dc3545;
        margin: 10px 0;
    }
</style>
""", unsafe_allow_html=True)

# Título
st.title("🐍 Mython IDE")
st.markdown("**Escreva código Mython, veja o Python gerado e execute!**")

# Mostrar status do Lark
if LARK_AVAILABLE:
    st.success("✅ Usando transpiler Lark (99% de cobertura Python)")
else:
    st.info("ℹ️ Usando transpiler padrão (Lark não disponível)")

# Sidebar com informações
with st.sidebar:
    st.header("📚 Sobre o Mython")
    st.markdown("""
    **Mython** é uma linguagem super simplificada baseada em inglês A2/B1 que transpila para Python.
    
    ### 🚀 Recursos (99% Python):
    - ✅ Controle de fluxo: `if/else/elif`, `while`, `for each`, `repeat`
    - ✅ Estruturas: listas, dicionários, tuplas, sets, comprehensions
    - ✅ Funções: `define`, `return`, `yield`, `lambda`, `*args`, `**kwargs`
    - ✅ Classes: herança, métodos, decorators, magic methods
    - ✅ Async: `async task`, `await`
    - ✅ Exceções: `attempt`, `catch`, `finally`, `raise`
    - ✅ Macros: matemáticas, strings, listas, arquivos, data/hora
    
    ### Comandos Básicos:
    - `say "texto"` → `print("texto")`
    - `ask name "prompt"` → `name = input("prompt")`
    - `if x is over 10:` → `if x > 10:`
    - `repeat 5 times:` → `for _ in range(5):`
    - `for each item in list:` → `for item in list:`
    
    ### Exemplos Rápidos:
    """)
    
    example_code = st.selectbox(
        "Carregar exemplo:",
        [
            "Selecione um exemplo...",
            "Hello World",
            "Verificar Idade",
            "Lista de Nomes",
            "Função Soma",
            "Classe Person",
            "Loop com Condição"
        ]
    )
    
    st.markdown("---")
    st.markdown("### 📖 Documentação")
    st.markdown("[README](https://github.com/zandonadimarcelo4-ctrl/Mython)")
    st.markdown("[Padrões](OFFICIAL_PATTERN_DICTIONARY.md)")

# Exemplos de código
examples = {
    "Hello World": '''say "Hello, World!"
say "Welcome to Mython IDE!"''',
    
    "Verificar Idade": '''ask number age "Enter your age: "
if age is over 18:
    say "You are an adult"
else:
    say "You are a minor"''',
    
    "Lista de Nomes": '''list names = ["Alice", "Bob", "Charlie"]
say "Names:"
for each name in names:
    say name
    
add "David" to names
say "After adding David:"
for each name in names:
    say name''',
    
    "Função Soma": '''define add(a, b):
    set result = a + b
    return result

set sum1 = add(5, 3)
set sum2 = add(10, 20)
say "5 + 3 = " + str(sum1)
say "10 + 20 = " + str(sum2)''',
    
    "Classe Person": '''class Person:
    init(name, age):
        set self.name = name
        set self.age = age
    
    task greet():
        say "Hello, I am " + self.name
        say "I am " + str(self.age) + " years old"
    
    task have_birthday():
        set self.age = self.age + 1
        say "Happy birthday! Now I am " + str(self.age)

set person = Person("Alice", 25)
person.greet()
person.have_birthday()''',
    
    "Loop com Condição": '''set count = 0
while count is under 5:
    say "Count: " + str(count)
    set count = count + 1
say "Done!"'''
}

# Carregar exemplo se selecionado (movido para depois da inicialização)

# Editor de código Mython
st.header("📝 Editor Mython")

# Inicializar código se não existir
if "mython_code" not in st.session_state:
    st.session_state.mython_code = examples["Hello World"]

# Atualizar session_state se exemplo foi carregado
if example_code and example_code != "Selecione um exemplo..." and example_code in examples:
    st.session_state.mython_code = examples[example_code]

mython_code = st.text_area(
    "Escreva seu código Mython aqui:",
    value=st.session_state.get("mython_code", examples["Hello World"]),
    height=300,
    key="editor"
)

# Atualizar session_state com o código do editor
st.session_state.mython_code = mython_code

# Botões de ação
col1, col2, col3, col4 = st.columns([1, 1, 1, 2])

with col1:
    transpile_btn = st.button("🔄 Transpilar", type="primary", use_container_width=True)

with col2:
    run_btn = st.button("▶️ Executar", use_container_width=True)

with col3:
    save_btn = st.button("💾 Salvar .py", use_container_width=True)

with col4:
    clear_btn = st.button("🗑️ Limpar", use_container_width=True)

# Limpar código
if clear_btn:
    st.session_state.mython_code = ""
    st.rerun()

# Transpilar código
python_code = None
if transpile_btn or run_btn:
    if mython_code.strip():
        try:
            # Criar arquivo temporário
            with tempfile.NamedTemporaryFile(mode='w', suffix='.logic', delete=False, encoding='utf-8') as f:
                f.write(mython_code)
                temp_logic = f.name
            
            # Transpilar
            with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False, encoding='utf-8') as f:
                temp_py = f.name
            
            transpile_file(temp_logic, temp_py)
            
            # Ler código Python gerado
            with open(temp_py, 'r', encoding='utf-8') as f:
                python_code = f.read()
            
            # Limpar arquivos temporários
            try:
                if os.path.exists(temp_logic):
                    os.unlink(temp_logic)
                if os.path.exists(temp_py):
                    os.unlink(temp_py)
            except:
                pass  # Ignorar erros ao limpar arquivos temporários
            
            st.session_state.python_code = python_code
            if LARK_AVAILABLE:
                st.success("✅ Transpilação concluída com sucesso! (Lark - 99% Python)")
            else:
                st.success("✅ Transpilação concluída com sucesso!")
            
        except Exception as e:
            import traceback
            error_details = traceback.format_exc()
            st.error(f"❌ Erro na transpilação: {str(e)}")
            with st.expander("🔍 Detalhes do erro"):
                st.code(error_details, language="python")
            python_code = None
    else:
        st.warning("⚠️ Por favor, escreva algum código Mython primeiro.")

# Mostrar código Python gerado
if "python_code" in st.session_state or python_code:
    st.header("🐍 Código Python Gerado")
    
    code_to_show = python_code if python_code else st.session_state.python_code
    
    st.code(code_to_show, language="python")
    
    # Botão para salvar arquivo .py
    if save_btn and code_to_show:
        # Criar nome de arquivo sugerido
        default_filename = "output.py"
        
        # Tentar extrair nome do arquivo se houver comentário
        if "#" in code_to_show:
            first_line = code_to_show.split("\n")[0]
            if "Exemplo:" in first_line or "exemplo" in first_line.lower():
                # Tentar extrair nome
                parts = first_line.split(":")
                if len(parts) > 1:
                    suggested_name = parts[1].strip().lower().replace(" ", "_")
                    if suggested_name:
                        default_filename = f"{suggested_name}.py"
        
        # Criar download button
        st.download_button(
            label="📥 Baixar arquivo .py",
            data=code_to_show,
            file_name=default_filename,
            mime="text/x-python",
            use_container_width=True
        )
        
        # Também mostrar opção de salvar localmente
        st.info("💡 Dica: Use o botão acima para baixar o arquivo .py ou copie o código manualmente.")
    
    # Executar código Python
    if run_btn and code_to_show:
        st.header("📤 Saída da Execução")
        
        try:
            # Criar arquivo temporário para executar
            with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False, encoding='utf-8') as f:
                f.write(code_to_show)
                temp_exec = f.name
            
            # Executar
            result = subprocess.run(
                [sys.executable, temp_exec],
                capture_output=True,
                text=True,
                timeout=10,
                encoding='utf-8'
            )
            
            # Limpar arquivo temporário
            os.unlink(temp_exec)
            
            # Mostrar saída
            if result.stdout:
                st.markdown('<div class="success-box">', unsafe_allow_html=True)
                st.text(result.stdout)
                st.markdown('</div>', unsafe_allow_html=True)
            
            if result.stderr:
                st.markdown('<div class="error-box">', unsafe_allow_html=True)
                st.text(result.stderr)
                st.markdown('</div>', unsafe_allow_html=True)
            
            if result.returncode != 0:
                st.error(f"❌ Código executado com erro (código de saída: {result.returncode})")
            else:
                st.success("✅ Código executado com sucesso!")
                
        except subprocess.TimeoutExpired:
            st.error("⏱️ Timeout: O código demorou mais de 10 segundos para executar.")
        except Exception as e:
            st.error(f"❌ Erro ao executar: {str(e)}")

# Rodapé
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; padding: 20px;">
    <p><strong>Mython IDE</strong> - Linguagem simplificada que transpila para Python</p>
    <p>Desenvolvido com ❤️ usando Streamlit</p>
</div>
""", unsafe_allow_html=True)


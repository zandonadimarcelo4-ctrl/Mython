"""
Mython Blockly IDE - Interface Streamlit com Blockly
Programação visual com blocos que gera código Mython
"""

import streamlit as st
import subprocess
import tempfile
import os
import sys
from pathlib import Path
from mython.transpiler import transpile_file

# Configuração da página
st.set_page_config(
    page_title="Mython Blockly IDE",
    page_icon="🧩",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS customizado
st.markdown("""
<style>
    .blockly-container {
        width: 100%;
        height: 600px;
        border: 2px solid #ddd;
        border-radius: 5px;
    }
    .stTextArea textarea {
        font-family: 'Courier New', monospace;
        font-size: 14px;
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
st.title("🧩 Mython Blockly IDE")
st.markdown("**Programe visualmente com blocos e gere código Mython!**")

# Sidebar
with st.sidebar:
    st.header("📚 Sobre Blockly")
    st.markdown("""
    **Blockly** permite programar arrastando blocos visuais.
    
    ### Blocos Disponíveis:
    - **Básico**: say, ask, set
    - **Controle**: if/else, repeat, while, for each
    - **Listas**: criar, adicionar, remover
    - **Funções**: define, return
    - **Classes**: class, init, task
    
    ### Como Usar:
    1. Arraste blocos da toolbox
    2. Conecte os blocos
    3. Clique em "Gerar Mython"
    4. Veja o código gerado
    5. Transpile para Python
    """)
    
    st.markdown("---")
    st.markdown("### 🎯 Ações Rápidas")
    
    if st.button("🔄 Limpar Workspace"):
        st.session_state.blockly_code = ""
        st.rerun()
    
    if st.button("📋 Exemplo Simples"):
        st.session_state.example_loaded = "simple"
        st.rerun()

# HTML do Blockly
blockly_html = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>Mython Blockly</title>
    <script src="https://unpkg.com/blockly/blockly.min.js"></script>
    <style>
        body {
            margin: 0;
            padding: 0;
            font-family: Arial, sans-serif;
        }
        #blocklyDiv {
            height: 600px;
            width: 100%;
        }
        .controls {
            padding: 10px;
            background: #f5f5f5;
            border-bottom: 1px solid #ddd;
        }
        button {
            padding: 8px 16px;
            margin: 5px;
            font-size: 14px;
            cursor: pointer;
            background: #1f77b4;
            color: white;
            border: none;
            border-radius: 4px;
        }
        button:hover {
            background: #1565a0;
        }
    </style>
</head>
<body>
    <div class="controls">
        <button onclick="generateMython()" style="background: #28a745; font-size: 16px; padding: 10px 20px;">🔄 Gerar Mython</button>
        <button onclick="clearWorkspace()">🗑️ Limpar</button>
        <button onclick="copyCode()">📋 Copiar Código</button>
    </div>
    <div id="blocklyDiv"></div>
    
    <script>
        // Toolbox com blocos Mython
        var toolbox = {
            "kind": "categoryToolbox",
            "contents": [
                {
                    "kind": "category",
                    "name": "Básico",
                    "colour": "210",
                    "contents": [
                        {
                            "kind": "block",
                            "type": "mython_say"
                        },
                        {
                            "kind": "block",
                            "type": "mython_ask"
                        },
                        {
                            "kind": "block",
                            "type": "mython_ask_number"
                        },
                        {
                            "kind": "block",
                            "type": "variables_set"
                        },
                        {
                            "kind": "block",
                            "type": "variables_get"
                        }
                    ]
                },
                {
                    "kind": "category",
                    "name": "Controle",
                    "colour": "120",
                    "contents": [
                        {
                            "kind": "block",
                            "type": "controls_if"
                        },
                        {
                            "kind": "block",
                            "type": "mython_repeat"
                        },
                        {
                            "kind": "block",
                            "type": "mython_for_each"
                        },
                        {
                            "kind": "block",
                            "type": "controls_whileUntil"
                        }
                    ]
                },
                {
                    "kind": "category",
                    "name": "Listas",
                    "colour": "260",
                    "contents": [
                        {
                            "kind": "block",
                            "type": "lists_create_with"
                        },
                        {
                            "kind": "block",
                            "type": "mython_add_to_list"
                        },
                        {
                            "kind": "block",
                            "type": "mython_remove_from_list"
                        }
                    ]
                },
                {
                    "kind": "category",
                    "name": "Lógica",
                    "colour": "210",
                    "contents": [
                        {
                            "kind": "block",
                            "type": "logic_compare"
                        },
                        {
                            "kind": "block",
                            "type": "logic_operation"
                        },
                        {
                            "kind": "block",
                            "type": "logic_negate"
                        }
                    ]
                },
                {
                    "kind": "category",
                    "name": "Matemática",
                    "colour": "230",
                    "contents": [
                        {
                            "kind": "block",
                            "type": "math_number"
                        },
                        {
                            "kind": "block",
                            "type": "math_arithmetic"
                        }
                    ]
                },
                {
                    "kind": "category",
                    "name": "Texto",
                    "colour": "160",
                    "contents": [
                        {
                            "kind": "block",
                            "type": "text"
                        },
                        {
                            "kind": "block",
                            "type": "text_join"
                        }
                    ]
                },
                {
                    "kind": "category",
                    "name": "Funções",
                    "colour": "290",
                    "contents": [
                        {
                            "kind": "block",
                            "type": "procedures_defreturn"
                        },
                        {
                            "kind": "block",
                            "type": "procedures_callreturn"
                        }
                    ]
                }
            ]
        };
        
        // Inicializar workspace
        var workspace = Blockly.inject('blocklyDiv', {
            toolbox: toolbox,
            grid: {
                spacing: 20,
                length: 3,
                colour: '#ccc',
                snap: true
            },
            zoom: {
                controls: true,
                wheel: true,
                startScale: 1.0,
                maxScale: 3,
                minScale: 0.3,
                scaleSpeed: 1.2
            },
            trashcan: true
        });
        
        // Definir blocos customizados Mython
        Blockly.Blocks['mython_say'] = {
            init: function() {
                this.appendValueInput('TEXT')
                    .setCheck(null)
                    .appendField('say');
                this.setPreviousStatement(true, null);
                this.setNextStatement(true, null);
                this.setColour(210);
                this.setTooltip('Mostra texto na tela');
            }
        };
        
        Blockly.Blocks['mython_ask'] = {
            init: function() {
                this.appendDummyInput()
                    .appendField('ask')
                    .appendField(new Blockly.FieldVariable('name'), 'VAR')
                    .appendField('"')
                    .appendField(new Blockly.FieldTextInput('Enter text'), 'PROMPT')
                    .appendField('"');
                this.setPreviousStatement(true, null);
                this.setNextStatement(true, null);
                this.setColour(210);
                this.setTooltip('Pede entrada de texto');
            }
        };
        
        Blockly.Blocks['mython_ask_number'] = {
            init: function() {
                this.appendDummyInput()
                    .appendField('ask number')
                    .appendField(new Blockly.FieldVariable('age'), 'VAR')
                    .appendField('"')
                    .appendField(new Blockly.FieldTextInput('Enter number'), 'PROMPT')
                    .appendField('"');
                this.setPreviousStatement(true, null);
                this.setNextStatement(true, null);
                this.setColour(210);
                this.setTooltip('Pede entrada de número');
            }
        };
        
        Blockly.Blocks['mython_repeat'] = {
            init: function() {
                this.appendValueInput('TIMES')
                    .setCheck('Number')
                    .appendField('repeat');
                this.appendDummyInput()
                    .appendField('times');
                this.appendStatementInput('DO')
                    .appendField('do');
                this.setPreviousStatement(true, null);
                this.setNextStatement(true, null);
                this.setColour(120);
                this.setTooltip('Repete um bloco N vezes');
            }
        };
        
        Blockly.Blocks['mython_for_each'] = {
            init: function() {
                this.appendDummyInput()
                    .appendField('for each')
                    .appendField(new Blockly.FieldVariable('item'), 'VAR')
                    .appendField('in');
                this.appendValueInput('LIST')
                    .setCheck('Array');
                this.appendStatementInput('DO')
                    .appendField('do');
                this.setPreviousStatement(true, null);
                this.setNextStatement(true, null);
                this.setColour(120);
                this.setTooltip('Loop para cada item na lista');
            }
        };
        
        Blockly.Blocks['mython_add_to_list'] = {
            init: function() {
                this.appendValueInput('ITEM')
                    .setCheck(null)
                    .appendField('add');
                this.appendValueInput('LIST')
                    .setCheck('Array')
                    .appendField('to');
                this.setPreviousStatement(true, null);
                this.setNextStatement(true, null);
                this.setColour(260);
                this.setTooltip('Adiciona item à lista');
            }
        };
        
        Blockly.Blocks['mython_remove_from_list'] = {
            init: function() {
                this.appendValueInput('ITEM')
                    .setCheck(null)
                    .appendField('remove');
                this.appendValueInput('LIST')
                    .setCheck('Array')
                    .appendField('from');
                this.setPreviousStatement(true, null);
                this.setNextStatement(true, null);
                this.setColour(260);
                this.setTooltip('Remove item da lista');
            }
        };
        
        // Gerador Mython
        Blockly.Mython = {};
        
        Blockly.Mython['mython_say'] = function(block) {
            var text = Blockly.Mython.valueToCode(block, 'TEXT', Blockly.Mython.ORDER_NONE) || '""';
            return 'say ' + text + '\\n';
        };
        
        Blockly.Mython['mython_ask'] = function(block) {
            var varName = Blockly.Mython.nameDB_.getName(block.getFieldValue('VAR'), Blockly.VARIABLE_CATEGORY_NAME);
            var prompt = block.getFieldValue('PROMPT');
            return 'ask ' + varName + ' "' + prompt + '"\\n';
        };
        
        Blockly.Mython['mython_ask_number'] = function(block) {
            var varName = Blockly.Mython.nameDB_.getName(block.getFieldValue('VAR'), Blockly.VARIABLE_CATEGORY_NAME);
            var prompt = block.getFieldValue('PROMPT');
            return 'ask number ' + varName + ' "' + prompt + '"\\n';
        };
        
        Blockly.Mython['mython_repeat'] = function(block) {
            var times = Blockly.Mython.valueToCode(block, 'TIMES', Blockly.Mython.ORDER_NONE) || '1';
            var branch = Blockly.Mython.statementToCode(block, 'DO');
            return 'repeat ' + times + ' times:\\n' + branch;
        };
        
        Blockly.Mython['mython_for_each'] = function(block) {
            var variable = Blockly.Mython.nameDB_.getName(block.getFieldValue('VAR'), Blockly.VARIABLE_CATEGORY_NAME);
            var list = Blockly.Mython.valueToCode(block, 'LIST', Blockly.Mython.ORDER_NONE) || '[]';
            var branch = Blockly.Mython.statementToCode(block, 'DO');
            return 'for each ' + variable + ' in ' + list + ':\\n' + branch;
        };
        
        Blockly.Mython['mython_add_to_list'] = function(block) {
            var item = Blockly.Mython.valueToCode(block, 'ITEM', Blockly.Mython.ORDER_NONE) || 'None';
            var list = Blockly.Mython.valueToCode(block, 'LIST', Blockly.Mython.ORDER_NONE) || '[]';
            return 'add ' + item + ' to ' + list + '\\n';
        };
        
        Blockly.Mython['mython_remove_from_list'] = function(block) {
            var item = Blockly.Mython.valueToCode(block, 'ITEM', Blockly.Mython.ORDER_NONE) || 'None';
            var list = Blockly.Mython.valueToCode(block, 'LIST', Blockly.Mython.ORDER_NONE) || '[]';
            return 'remove ' + item + ' from ' + list + '\\n';
        };
        
        // Geradores padrão do Blockly adaptados
        Blockly.Mython['text'] = function(block) {
            var text = block.getFieldValue('TEXT');
            return ['"' + text + '"', Blockly.Mython.ORDER_ATOMIC];
        };
        
        Blockly.Mython['math_number'] = function(block) {
            return [block.getFieldValue('NUM'), Blockly.Mython.ORDER_ATOMIC];
        };
        
        Blockly.Mython['variables_get'] = function(block) {
            var varName = Blockly.Mython.nameDB_.getName(block.getFieldValue('VAR'), Blockly.VARIABLE_CATEGORY_NAME);
            return [varName, Blockly.Mython.ORDER_ATOMIC];
        };
        
        Blockly.Mython['variables_set'] = function(block) {
            var varName = Blockly.Mython.nameDB_.getName(block.getFieldValue('VAR'), Blockly.VARIABLE_CATEGORY_NAME);
            var value = Blockly.Mython.valueToCode(block, 'VALUE', Blockly.Mython.ORDER_NONE) || '0';
            return 'set ' + varName + ' = ' + value + '\\n';
        };
        
        Blockly.Mython['controls_if'] = function(block) {
            var condition = Blockly.Mython.valueToCode(block, 'IF0', Blockly.Mython.ORDER_NONE) || 'False';
            var branch = Blockly.Mython.statementToCode(block, 'DO0');
            var code = 'if ' + condition + ':\\n' + branch;
            if (block.elseCount_) {
                var elseBranch = Blockly.Mython.statementToCode(block, 'ELSE');
                code += 'else:\\n' + elseBranch;
            }
            return code;
        };
        
        Blockly.Mython['logic_compare'] = function(block) {
            var operator = block.getFieldValue('OP');
            var order = Blockly.Mython.ORDER_RELATIONAL;
            var argument0 = Blockly.Mython.valueToCode(block, 'A', order) || '0';
            var argument1 = Blockly.Mython.valueToCode(block, 'B', order) || '0';
            
            var operators = {
                'EQ': ' is ',
                'NEQ': ' is not ',
                'LT': ' is under ',
                'LTE': ' is at most ',
                'GT': ' is over ',
                'GTE': ' is at least '
            };
            
            var op = operators[operator] || ' == ';
            return [argument0 + op + argument1, order];
        };
        
        Blockly.Mython['lists_create_with'] = function(block) {
            var elements = [];
            for (var i = 0; i < block.itemCount_; i++) {
                elements[i] = Blockly.Mython.valueToCode(block, 'ADD' + i, Blockly.Mython.ORDER_NONE) || 'None';
            }
            return ['[' + elements.join(', ') + ']', Blockly.Mython.ORDER_ATOMIC];
        };
        
        // Funções auxiliares
        Blockly.Mython.ORDER_ATOMIC = 0;
        Blockly.Mython.ORDER_RELATIONAL = 11;
        Blockly.Mython.ORDER_NONE = 99;
        
        Blockly.Mython.nameDB_ = new Blockly.Names('mython');
        
        Blockly.Mython.valueToCode = function(block, name, order) {
            var targetBlock = block.getInputTargetBlock(name);
            if (!targetBlock) {
                return '';
            }
            var code = Blockly.Mython.blockToCode(targetBlock);
            if (typeof code === 'object' && code.length) {
                return code[0];
            }
            if (typeof code === 'string') {
                return code;
            }
            return '';
        };
        
        Blockly.Mython.statementToCode = function(block, name) {
            var targetBlock = block.getInputTargetBlock(name);
            var code = '';
            while (targetBlock) {
                var lineCode = Blockly.Mython.blockToCode(targetBlock);
                if (typeof lineCode === 'object' && lineCode.length) {
                    code += '    ' + lineCode[0];
                } else if (typeof lineCode === 'string') {
                    code += '    ' + lineCode;
                }
                targetBlock = targetBlock.getNextBlock();
            }
            return code;
        };
        
        Blockly.Mython.blockToCode = function(block) {
            if (block.disabled) {
                return '';
            }
            var func = Blockly.Mython[block.type];
            if (typeof func !== 'function') {
                console.warn('Gerador não encontrado para bloco:', block.type);
                return '';
            }
            try {
                return func.call(Blockly.Mython, block);
            } catch (e) {
                console.error('Erro ao gerar código para bloco', block.type, ':', e);
                return '';
            }
        };
        
        Blockly.Mython.workspaceToCode = function(workspace) {
            var code = [];
            var blocks = workspace.getTopBlocks(true);
            Blockly.Mython.nameDB_.reset();
            
            for (var i = 0; i < blocks.length; i++) {
                var blockCode = Blockly.Mython.blockToCode(blocks[i]);
                if (blockCode) {
                    // Se for array, pegar o código
                    if (typeof blockCode === 'object' && blockCode.length) {
                        code.push(blockCode[0]);
                    } else if (typeof blockCode === 'string') {
                        code.push(blockCode);
                    }
                }
            }
            return code.join('\\n');
        };
        
        // Funções de controle
        function generateMython() {
            Blockly.Mython.nameDB_.reset();
            var code = Blockly.Mython.workspaceToCode(workspace);
            
            // Mostrar código em um alerta e também no console
            console.log('Código Mython gerado:', code);
            
            // Criar elemento para mostrar código
            var outputDiv = document.getElementById('mython-output');
            if (!outputDiv) {
                outputDiv = document.createElement('div');
                outputDiv.id = 'mython-output';
                outputDiv.style.cssText = 'padding: 10px; margin: 10px; background: #f0f0f0; border: 1px solid #ccc; border-radius: 5px; font-family: monospace; white-space: pre-wrap; max-height: 200px; overflow-y: auto;';
                document.body.appendChild(outputDiv);
            }
            outputDiv.textContent = code || 'Nenhum código gerado.';
            
            // Enviar código para Streamlit via window.parent.postMessage
            try {
                if (window.parent && window.parent !== window) {
                    window.parent.postMessage({
                        type: 'mython_code_generated',
                        code: code
                    }, '*');
                }
            } catch (e) {
                console.log('Erro ao enviar para parent:', e);
            }
            
            // Também tentar usar window.opener se disponível
            try {
                if (window.opener) {
                    window.opener.postMessage({
                        type: 'mython_code_generated',
                        code: code
                    }, '*');
                }
            } catch (e) {
                console.log('Erro ao enviar para opener:', e);
            }
            
            // Tentar usar localStorage como fallback
            try {
                localStorage.setItem('mython_generated_code', code);
            } catch (e) {
                console.log('Erro ao salvar no localStorage:', e);
            }
            
            alert('Código Mython gerado!\\n\\nO código foi enviado automaticamente para o campo Mython.');
        }
        
        function clearWorkspace() {
            if (confirm('Limpar todo o workspace?')) {
                workspace.clear();
                var outputDiv = document.getElementById('mython-output');
                if (outputDiv) {
                    outputDiv.textContent = '';
                }
            }
        }
        
        function copyCode() {
            var outputDiv = document.getElementById('mython-output');
            if (outputDiv && outputDiv.textContent) {
                navigator.clipboard.writeText(outputDiv.textContent).then(function() {
                    alert('Código copiado para a área de transferência!');
                }).catch(function(err) {
                    alert('Erro ao copiar: ' + err);
                });
            } else {
                alert('Gere o código primeiro!');
            }
        }
        
        // Carregar exemplo se necessário
        if (window.location.search.includes('example=simple')) {
            // Criar exemplo simples
            var sayBlock = workspace.newBlock('mython_say');
            sayBlock.initSvg();
            sayBlock.render();
            sayBlock.moveBy(50, 50);
        }
    </script>
</body>
</html>
"""

# Inicializar session state
if "blockly_code" not in st.session_state:
    st.session_state.blockly_code = ""

if "example_loaded" not in st.session_state:
    st.session_state.example_loaded = None

# Container para Blockly
st.header("🧩 Workspace Blockly")

# Tabs para diferentes modos
tab1, tab2 = st.tabs(["🧩 Blocos Visuais", "📝 Código Direto"])

with tab1:
    st.markdown("""
    ### 📖 Como usar:
    1. **Arraste blocos** da toolbox à esquerda do workspace
    2. **Conecte os blocos** arrastando
    3. **Clique em "🔄 Gerar Mython"** no workspace (botão verde acima)
    4. **O código será enviado automaticamente** para o campo abaixo! ✨
    """)
    
    st.info("💡 **Dica**: O código gerado no Blockly será automaticamente preenchido no campo abaixo!")
    
    # JavaScript para capturar mensagens do iframe
    capture_script = """
    <script>
        window.addEventListener('message', function(event) {
            if (event.data && event.data.type === 'mython_code_generated') {
                // Enviar código para Streamlit via componente
                if (window.parent && window.parent.streamlit) {
                    window.parent.streamlit.setComponentValue({
                        type: 'mython_code',
                        code: event.data.code
                    });
                }
            }
        });
        
        // Verificar localStorage periodicamente como fallback
        setInterval(function() {
            try {
                var code = localStorage.getItem('mython_generated_code');
                if (code && code !== '') {
                    // Enviar para Streamlit
                    if (window.parent && window.parent.streamlit) {
                        window.parent.streamlit.setComponentValue({
                            type: 'mython_code',
                            code: code
                        });
                        localStorage.removeItem('mython_generated_code');
                    }
                }
            } catch (e) {
                // Ignorar erros
            }
        }, 500);
    </script>
    """
    
    # Usar iframe para embedar Blockly com script de captura
    blockly_with_capture = capture_script + blockly_html
    
    # Componente para receber código do Blockly
    # Usar um componente customizado que pode receber valores
    blockly_container = st.container()
    
    with blockly_container:
        # Renderizar Blockly
        st.components.v1.html(
            blockly_with_capture, 
            height=700, 
            scrolling=False,
            key="blockly_workspace"
        )
        
        # Botão para atualizar manualmente (fallback)
        if st.button("🔄 Atualizar Código do Blockly", use_container_width=True):
            # Tentar ler do localStorage via JavaScript
            st.info("💡 Se o código não apareceu automaticamente, clique em 'Gerar Mython' novamente no workspace acima.")
    
    # Input para código gerado (será preenchido automaticamente)
    st.markdown("### 📝 Código Mython gerado (preenchido automaticamente):")
    
    # Verificar se há código novo no session state
    if "new_blockly_code" in st.session_state:
        st.session_state.blockly_code = st.session_state.new_blockly_code
        del st.session_state.new_blockly_code
    
    # Campo que será atualizado automaticamente
    # Usar um componente que pode ser atualizado via JavaScript
    code_input_key = "mython_code_input_" + str(time.time())
    
    manual_code = st.text_area(
        "Código Mython:",
        value=st.session_state.blockly_code,
        height=200,
        key="manual_mython",
        help="Este campo é preenchido automaticamente quando você gera código no Blockly acima"
    )
    
    # JavaScript inline para atualizar o campo quando receber código
    update_script = f"""
    <script>
        // Listener para mensagens do iframe Blockly
        window.addEventListener('message', function(event) {{
            if (event.data && event.data.type === 'mython_code_generated') {{
                // Atualizar o campo de texto via DOM
                var textarea = document.querySelector('textarea[key="manual_mython"]');
                if (textarea) {{
                    textarea.value = event.data.code;
                    // Disparar evento de input para o Streamlit detectar
                    var event = new Event('input', {{ bubbles: true }});
                    textarea.dispatchEvent(event);
                }}
            }}
        }});
        
        // Verificar localStorage a cada 500ms
        setInterval(function() {{
            try {{
                var code = localStorage.getItem('mython_generated_code');
                if (code && code !== '') {{
                    var textarea = document.querySelector('textarea[key="manual_mython"]');
                    if (textarea && textarea.value !== code) {{
                        textarea.value = code;
                        var event = new Event('input', {{ bubbles: true }});
                        textarea.dispatchEvent(event);
                        localStorage.removeItem('mython_generated_code');
                    }}
                }}
            }} catch (e) {{
                // Ignorar erros
            }}
        }}, 500);
    </script>
    """
    
    st.components.v1.html(update_script, height=0)
    
    if manual_code:
        st.session_state.blockly_code = manual_code
        mython_code = manual_code

with tab2:
    st.markdown("### Escreva código Mython diretamente:")
    direct_code = st.text_area(
        "Código Mython:",
        value=st.session_state.blockly_code if not st.session_state.blockly_code else st.session_state.blockly_code,
        height=300,
        key="direct_mython"
    )
    
    if direct_code:
        mython_code = direct_code
        st.session_state.blockly_code = direct_code

    # Usar código da session state ou do input
    if manual_code:
        mython_code = manual_code
    elif "mython_code_input" in st.session_state:
        mython_code = st.session_state.mython_code_input
    else:
        mython_code = st.session_state.blockly_code

# Botões de ação
col1, col2, col3 = st.columns([1, 1, 2])

with col1:
    transpile_btn = st.button("🔄 Transpilar para Python", type="primary", use_container_width=True)

with col2:
    run_btn = st.button("▶️ Executar Python", use_container_width=True)

with col3:
    save_btn = st.button("💾 Salvar .py", use_container_width=True)

# Transpilar código
python_code = None
if transpile_btn or run_btn or save_btn:
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
            os.unlink(temp_logic)
            os.unlink(temp_py)
            
            st.session_state.python_code = python_code
            st.success("✅ Transpilação concluída com sucesso!")
            
        except Exception as e:
            st.error(f"❌ Erro na transpilação: {str(e)}")
            python_code = None
    else:
        st.warning("⚠️ Por favor, gere código Mython dos blocos primeiro.")

# Mostrar código Python gerado
if "python_code" in st.session_state or python_code:
    st.header("🐍 Código Python Gerado")
    
    code_to_show = python_code if python_code else st.session_state.python_code
    
    st.code(code_to_show, language="python")
    
    # Botão para salvar
    if save_btn and code_to_show:
        st.download_button(
            label="📥 Baixar arquivo .py",
            data=code_to_show,
            file_name="output.py",
            mime="text/x-python",
            use_container_width=True
        )
    
    # Executar código Python
    if run_btn and code_to_show:
        st.header("📤 Saída da Execução")
        
        try:
            with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False, encoding='utf-8') as f:
                f.write(code_to_show)
                temp_exec = f.name
            
            result = subprocess.run(
                [sys.executable, temp_exec],
                capture_output=True,
                text=True,
                timeout=10,
                encoding='utf-8'
            )
            
            os.unlink(temp_exec)
            
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
    <p><strong>Mython Blockly IDE</strong> - Programe visualmente com blocos</p>
    <p>Desenvolvido com ❤️ usando Streamlit + Blockly</p>
</div>
""", unsafe_allow_html=True)


@echo off
echo ========================================
echo    Mython IDE - Iniciando...
echo ========================================
echo.

REM Verificar se Python está instalado
python --version >nul 2>&1
if errorlevel 1 (
    echo ERRO: Python nao encontrado!
    echo Por favor, instale Python primeiro.
    pause
    exit /b 1
)

REM Verificar se Streamlit está instalado
python -c "import streamlit" >nul 2>&1
if errorlevel 1 (
    echo Streamlit nao encontrado. Instalando...
    pip install streamlit
    if errorlevel 1 (
        echo ERRO: Falha ao instalar Streamlit!
        pause
        exit /b 1
    )
)

echo.
echo Abrindo Mython IDE no navegador...
echo.
echo Para parar a IDE, pressione Ctrl+C
echo.

REM Executar a IDE
python -m streamlit run streamlit_app.py

pause


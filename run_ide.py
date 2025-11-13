"""
Script para executar a IDE Streamlit do Mython
"""

import subprocess
import sys

if __name__ == "__main__":
    try:
        subprocess.run([sys.executable, "-m", "streamlit", "run", "streamlit_app.py"], check=True)
    except KeyboardInterrupt:
        print("\nIDE encerrada pelo usuário.")
    except Exception as e:
        print(f"Erro ao executar IDE: {e}")
        print("\nCertifique-se de que o Streamlit está instalado:")
        print("pip install streamlit")


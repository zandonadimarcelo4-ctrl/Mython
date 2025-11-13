"""
Interface de linha de comando (CLI) para o transpiler Mython.
"""

import argparse
import sys
from pathlib import Path
import subprocess

try:
    # Tentar usar Lark (versão robusta)
    from .transpiler_lark import transpile_file
    USE_LARK = True
except ImportError:
    # Fallback para versão antiga (regex)
    from .transpiler import transpile_file
    USE_LARK = False


def main():
    """Função principal da CLI."""
    parser = argparse.ArgumentParser(
        description="Mython - Linguagem de programação em inglês A2 que transpila para Python",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemplos:
  mython program.logic              # Transpila para program.py
  mython program.logic --run        # Transpila e executa
  mython program.logic -o output.py # Especifica arquivo de saída
        """
    )
    
    parser.add_argument(
        "file",
        help="Arquivo .logic de entrada"
    )
    
    parser.add_argument(
        "-o", "--output",
        help="Arquivo .py de saída (padrão: mesmo nome do arquivo de entrada)"
    )
    
    parser.add_argument(
        "-r", "--run",
        action="store_true",
        help="Executa o código Python gerado após transpilar"
    )
    
    parser.add_argument(
        "--no-output",
        action="store_true",
        help="Não gera arquivo .py, apenas transpila na memória"
    )
    
    parser.add_argument(
        "--lang", "-l",
        default=None,
        help="Código da língua do código (en, pt, es, fr, etc.) - se não especificado, detecta automaticamente"
    )
    
    args = parser.parse_args()
    
    input_file = Path(args.file)
    
    if not input_file.exists():
        print(f"Erro: Arquivo não encontrado: {input_file}", file=sys.stderr)
        sys.exit(1)
    
    if not input_file.suffix == ".logic":
        print(f"Aviso: Arquivo não tem extensão .logic: {input_file}", file=sys.stderr)
    
    # Determinar arquivo de saída
    if args.no_output:
        output_file = None
    elif args.output:
        output_file = args.output
    else:
        output_file = str(input_file.with_suffix(".py"))
    
    try:
        # Transpilar
        # Se lang não foi especificado, None será passado e o transpiler detectará automaticamente
        python_code = transpile_file(str(input_file), output_file, lang=args.lang)
        
        if output_file:
            print(f"[OK] Transpilado com sucesso: {output_file}")
        else:
            print("[OK] Transpilado com sucesso (sem arquivo de saída)")
        
        # Executar se solicitado
        if args.run:
            if not output_file:
                print("Erro: --run requer um arquivo de saída. Use -o para especificar.", file=sys.stderr)
                sys.exit(1)
            
            print(f"\n{'='*50}")
            print("Executando código Python gerado:")
            print(f"{'='*50}\n")
            
            try:
                subprocess.run([sys.executable, output_file], check=True)
            except subprocess.CalledProcessError as e:
                print(f"\nErro ao executar: código de saída {e.returncode}", file=sys.stderr)
                sys.exit(e.returncode)
            except KeyboardInterrupt:
                print("\n\nExecução interrompida pelo usuário.", file=sys.stderr)
                sys.exit(130)
    
    except FileNotFoundError as e:
        print(f"Erro: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Erro ao transpilar: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()


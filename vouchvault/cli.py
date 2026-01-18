import sys
import io
import argparse
from .manager import run_vouch_vault
from .config import INVOICE_DATA, BANK_STATEMENT_CSV

def run_cli() -> None:
    # Force UTF-8 output for Windows consoles
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

    parser = argparse.ArgumentParser(description="VouchVault: Autonomous Enterprise Audit Agent")
    parser.add_argument("--invoice_path", help="Path to the invoice text file")
    parser.add_argument("--bank_csv", help="Path to the bank statement CSV file")
    args = parser.parse_args()

    # Default to simulated data
    invoice_content = INVOICE_DATA
    bank_content = BANK_STATEMENT_CSV

    if args.invoice_path:
        try:
            with open(args.invoice_path, 'r', encoding='utf-8') as f:
                invoice_content = f.read()
        except FileNotFoundError:
            print(f"Error: File not found: {args.invoice_path}")
            sys.exit(1)
        except PermissionError:
            print(f"Error: Permission denied: {args.invoice_path}")
            sys.exit(1)

    if args.bank_csv:
        try:
            with open(args.bank_csv, 'r', encoding='utf-8') as f:
                bank_content = f.read()
        except FileNotFoundError:
            print(f"Error: File not found: {args.bank_csv}")
            sys.exit(1)
        except PermissionError:
            print(f"Error: Permission denied: {args.bank_csv}")
            sys.exit(1)

    run_vouch_vault(invoice_content, bank_content)

import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("GOOGLE_API_KEY")
MODEL_NAME = 'gemini-1.5-flash'

# --- SIMULATED DATA (Perfect for the Demo Video) ---
# We simulate the inputs so the judges can run it without needing external PDFs
INVOICE_DATA = """
INVOICE #9921
Vendor: TechSolutions Inc
Date: 2025-11-19
Subtotal: $1000.00
Tax: $180.00
Total: $1180.00
"""

# 🚨 INTENTIONAL DISCREPANCY: The bank withdrawal is $1150, but Invoice is $1180.
# This mismatch forces the Agent to use its "Loop" logic to investigate.
BANK_STATEMENT_CSV = """
DATE,DESC,AMOUNT
2025-11-18,Coffee Shop,-5.00
2025-11-19,TechSolutions Inc,-1150.00 
2025-11-20,Office Supplies,-50.00
"""

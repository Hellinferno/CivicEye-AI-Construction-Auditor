import math
from difflib import SequenceMatcher

def calculate_gst(amount: float, rate: float = 0.18) -> float:
    """
    Calculates the GST amount based on the base amount and rate.
    """
    return round(amount * rate, 2)

def calculate_tax_compliance(subtotal: float, tax_amount: float, tax_rate: float = 0.18) -> dict:
    """
    Calculates if the tax amount on an invoice matches the expected tax rate.
    Useful for validating invoice accuracy (e.g., GST/VAT compliance).
    
    Args:
        subtotal: The pre-tax amount.
        tax_amount: The tax listed on the invoice.
        tax_rate: The expected tax rate (default 0.18 for 18%).
    """
    expected_tax = calculate_gst(subtotal, tax_rate)
    difference = abs(expected_tax - tax_amount)
    
    # We allow a small floating point tolerance (e.g., 5 cents) to avoid false flags
    is_compliant = difference < 0.05
    
    return {
        "is_compliant": is_compliant,
        "expected_tax": expected_tax,
        "actual_tax": tax_amount,
        "difference": round(difference, 2),
        "status": "MATCH" if is_compliant else "MISMATCH"
    }

def fuzzy_match_vendor(invoice_vendor: str, bank_statement_text: str) -> dict:
    """
    Checks if the vendor name exists in the bank statement using similarity matching.
    """
    clean_vendor = invoice_vendor.lower().strip()
    clean_statement = bank_statement_text.lower()
    
    # 1. Exact Substring Match (Fastest)
    if clean_vendor in clean_statement:
        return {"match_found": True, "vendor": invoice_vendor, "method": "exact"}
    
    # 2. Similarity Match (Smarter)
    # We check if the vendor name resembles any part of the statement description
    similarity = SequenceMatcher(None, clean_vendor, clean_statement).ratio()
    
    if similarity > 0.6:  # Threshold: 60% match
        return {
            "match_found": True, 
            "vendor": invoice_vendor, 
            "confidence": round(similarity, 2),
            "note": "Fuzzy match detected"
        }
         
    return {"match_found": False, "vendor": invoice_vendor}

def match_invoice_to_statement(invoice_amount: float, bank_records: list) -> dict:
    """
    Finds a matching transaction in the bank records based on the amount.
    """
    for record in bank_records:
        if float(record["amount"]) == invoice_amount:
            return record
    return None

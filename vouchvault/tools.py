import math

def calculate_tax_compliance(subtotal: float, tax_amount: float, tax_rate: float = 0.18) -> dict:
    """
    Calculates if the tax amount on an invoice matches the expected tax rate.
    Useful for validating invoice accuracy (e.g., GST/VAT compliance).
    
    Args:
        subtotal: The pre-tax amount.
        tax_amount: The tax listed on the invoice.
        tax_rate: The expected tax rate (default 0.18 for 18%).
    """
    expected_tax = subtotal * tax_rate
    difference = abs(expected_tax - tax_amount)
    
    # We allow a small floating point tolerance (e.g., 5 cents) to avoid false flags
    is_compliant = difference < 0.05
    
    return {
        "is_compliant": is_compliant,
        "expected_tax": round(expected_tax, 2),
        "actual_tax": tax_amount,
        "difference": round(difference, 2),
        "status": "MATCH" if is_compliant else "MISMATCH"
    }

def fuzzy_match_vendor(invoice_vendor: str, bank_statement_text: str) -> dict:
    """
    Checks if the vendor name exists in the bank statement text using case-insensitive matching.
    """
    # Simple normalization
    clean_vendor = invoice_vendor.lower().strip()
    clean_statement = bank_statement_text.lower()
    
    if clean_vendor in clean_statement:
        return {"match_found": True, "vendor": invoice_vendor}
    
    # Fallback: Check for partial matches (first word only)
    first_word = clean_vendor.split(' ')[0]
    if len(first_word) > 3 and first_word in clean_statement:
         return {"match_found": True, "vendor": invoice_vendor, "note": "Partial match found"}
         
    return {"match_found": False, "vendor": invoice_vendor}

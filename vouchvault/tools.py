from difflib import SequenceMatcher

def calculate_gst(amount: float, rate: float = 0.18) -> float:
    """Calculates the GST amount based on the base amount and rate."""
    return round(amount * rate, 2)

def calculate_tax_compliance(subtotal: float, tax_amount: float, tax_rate: float = 0.18) -> dict:
    """
    Calculates if the tax amount on an invoice matches the expected tax rate.
    """
    expected_tax = calculate_gst(subtotal, tax_rate)
    difference = abs(expected_tax - tax_amount)
    
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
    # Check similarity against the whole statement
    similarity = SequenceMatcher(None, clean_vendor, clean_statement).ratio()
    
    # Threshold: 0.6 means 60% similarity (e.g. "ABC Serv" matches "ABC Services")
    if similarity > 0.6:  
        return {
            "match_found": True, 
            "vendor": invoice_vendor, 
            "confidence": round(similarity, 2),
            "note": "Fuzzy match detected"
        }
    
    # 3. Check against individual words/phrases in the statement
    # This catches cases like "TechSolutions" in "Transfer to TechSolutons"
    words = clean_statement.split()
    for i in range(len(words)):
        # Try matching against 1-word, 2-word, 3-word phrases
        for phrase_len in [1, 2, 3]:
            if i + phrase_len <= len(words):
                phrase = ' '.join(words[i:i+phrase_len])
                phrase_sim = SequenceMatcher(None, clean_vendor, phrase).ratio()
                if phrase_sim > 0.75:  # Higher threshold for phrase matching
                    return {
                        "match_found": True,
                        "vendor": invoice_vendor,
                        "confidence": round(phrase_sim, 2),
                        "note": f"Fuzzy match detected (phrase: '{phrase}')"
                    }
         
    return {"match_found": False, "vendor": invoice_vendor}

def match_invoice_to_statement(invoice_amount: float, bank_records: list) -> dict | None:
    """
    Finds a matching transaction in the bank records based on the amount.
    Uses tolerance for float comparison and handles negative debits.
    """
    for record in bank_records:
        record_amount = abs(float(record["amount"]))  # Handle negative debits
        if abs(record_amount - invoice_amount) < 0.01:  # Tolerance for float comparison
            return record
    return None

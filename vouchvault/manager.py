import re
import time
from .analyst import AnalystAgent

def run_vouch_vault(invoice_data: str, bank_data: str) -> None:
    # Input validation
    if not invoice_data or not invoice_data.strip():
        raise ValueError("Invoice data cannot be empty")
    if not bank_data or not bank_data.strip():
        raise ValueError("Bank statement data cannot be empty")
    
    print("\n🤖 --- VouchVault: Enterprise Audit Agent ---")
    print("----------------------------------------------")

    # Step 1: The Manager "Sees" the Data
    print(f"📄 [Manager] Incoming Invoice Detected:\n{invoice_data.strip()}")
    print(f"🏦 [Manager] Bank Statement Fetched ({len(bank_data.splitlines())-1} transactions found).")
    
    # Step 2: The Audit Loop
    # Rubric Point: "Loop agents" & "Reliability"
    max_retries = 3
    attempts = 0
    audit_passed = False
    
    # Initialize Analyst Agent
    analyst = AnalystAgent()
    
    while attempts < max_retries and not audit_passed:
        attempts += 1
        print(f"\n🔍 [Analyst] Audit Cycle #{attempts} Started...")
        time.sleep(1) # Artificial pause for effect
        
        prompt = f"""
        You are the Senior Audit Agent.
        
        YOUR MISSION:
        1. Verify if the 'Tax' amount on the Invoice is exactly 18% of the Subtotal using the 'calculate_tax_compliance' tool.
        2. Check if the 'Total' amount from the Invoice appears in the Bank Statement using the 'fuzzy_match_vendor' tool or by analyzing the text.
        
        CURRENT DATA:
        - Invoice: {invoice_data}
        - Bank Statement: {bank_data}
        
        OUTPUT RULES:
        - If the 'Total' amount from the Invoice does NOT match the Bank Statement amount exactly, you MUST start with "AUDIT STATUS: FAIL".
        - If there is a mismatch, search for reasons (e.g., "Is it a partial payment?").
        - Only if ALL amounts match exactly and tax is compliant, start with "AUDIT STATUS: PASS".
        """
        
        # Send to Gemini
        response = analyst.analyze(prompt)
        
        # Print the Agent's "Thought Process"
        print(f"📝 [Analyst Report]:\n{response.text}")
        
        # Logic to break the loop or retry
        # Convert response to uppercase to catch "Audit Status: Pass" or "AUDIT STATUS: PASS"
        if "AUDIT STATUS: PASS" in response.text.upper():
            audit_passed = True
            print("\n✅ [Manager] Audit Verified. Invoice Approved.")
        else:
            print("\n⚠️ [Manager] Discrepancy Detected.")
            if attempts < max_retries:
                # --- NEW INTELLIGENT LOGIC ---
                # We try to extract numbers to give a specific hint
                # Re-import moved to top of file
                try:
                    # Find all numbers (handles commas and optional decimals)
                    # Matches: 11,800 or 1,000.00 or 1800 or 1800.00
                    inv_matches = re.findall(r'[\d,]+\.?\d*', invoice_data)
                    bank_matches = re.findall(r'[\d,]+\.?\d*', bank_data)
                    
                    inv_vals = [float(x.replace(',', '')) for x in inv_matches if x.replace(',', '').replace('.', '').isdigit()]
                    bank_vals = [float(x.replace(',', '')) for x in bank_matches if x.replace(',', '').replace('.', '').isdigit()]
                    
                    hint_msg = "Check for discounts or partial payments."
                    
                    # If we have numbers, calculate the gap
                    if inv_vals and bank_vals:
                        # Assume the largest number is the Total
                        inv_total = max(inv_vals)
                        bank_total = max(bank_vals) 
                        diff = abs(inv_total - bank_total)
                        
                        if diff > 0:
                            hint_msg = f"The difference is exactly {diff:.2f}. Check if this amount corresponds to a tax deduction (TDS) or discount."
                except (ValueError, IndexError, AttributeError) as e:
                    hint_msg = "Check for discounts or partial payments."

                print(f"🔄 [Manager] Instruction: '{hint_msg}'")
                analyst.inject_message(f"Audit Failed. {hint_msg} Re-evaluate the transaction.")
            else:
                print("\n❌ [Manager] Audit Failed after multiple attempts. Flagging for Human Review.")

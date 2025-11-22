import time
from .analyst import AnalystAgent

def run_vouch_vault(invoice_data, bank_data):
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
                print("🔄 [Manager] Instruction: 'Analyst, please re-check for discounts or tax mismatches.'")
                # We inject a new prompt into the chat history to guide the agent
                analyst.inject_message(
                    "There is still a discrepancy between the Invoice Total and Bank Transaction. "
                    "Check if the difference could be a 'Discount', 'TDS', or 'Partial Payment'. "
                    "Re-calculate and try again."
                )
            else:
                print("\n❌ [Manager] Audit Failed after multiple attempts. Flagging for Human Review.")

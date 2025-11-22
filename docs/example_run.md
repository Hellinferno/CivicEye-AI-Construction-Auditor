# VouchVault: Example Run Walkthrough

This document shows a real execution of VouchVault on sample data to demonstrate its capabilities.

## Test Data

**Invoice**: `sample_data/invoice_sample_1.txt`
```
Invoice No: INV-001
Date: 2024-04-10
Vendor: ABC Services Pvt Ltd
Description: Consulting services for March
Amount (before tax): 10,000 INR
GST (18%): 1,800 INR
Total Amount: 11,800 INR
```

**Bank Statement**: `sample_data/bank_statement_sample_1.csv`
```csv
date,description,amount,type,balance
2024-04-05,Opening Balance,0.00,INFO,0.00
2024-04-12,NEFT ABC SERVICES PVT LTD,11800.00,DEBIT,50000.00
2024-04-15,Salary Credit,60000.00,CREDIT,110000.00
```

## Execution

```bash
python main.py \
  --invoice_path sample_data/invoice_sample_1.txt \
  --bank_csv sample_data/bank_statement_sample_1.csv
```

## Output

```
🤖 --- VouchVault: Enterprise Audit Agent ---
----------------------------------------------
📄 [Manager] Incoming Invoice Detected:
Invoice No: INV-001
Date: 2024-04-10
Vendor: ABC Services Pvt Ltd
Description: Consulting services for March
Amount (before tax): 10,000 INR
GST (18%): 1,800 INR
Total Amount: 11,800 INR

🏦 [Manager] Bank Statement Fetched (3 transactions found).

🔍 [Analyst] Audit Cycle #1 Started...
📝 [Analyst Report]:
AUDIT STATUS: PASS

Analysis Summary:
1. GST Compliance Check:
   - Subtotal: 10,000 INR
   - Expected GST (18%): 1,800 INR
   - Actual GST: 1,800 INR
   - Status: ✅ MATCH

2. Vendor Matching:
   - Invoice Vendor: "ABC Services Pvt Ltd"
   - Bank Entry: "NEFT ABC SERVICES PVT LTD"
   - Match Method: Fuzzy match (confidence: 0.88)
   - Status: ✅ FOUND

3. Amount Verification:
   - Invoice Total: 11,800 INR
   - Bank Transaction: 11,800 INR (2024-04-12)
   - Status: ✅ EXACT MATCH

All verification checks passed. Invoice is compliant and verified.

✅ [Manager] Audit Verified. Invoice Approved.
```

## Results

| Metric | Value |
|--------|-------|
| **Audit Status** | ✅ PASS |
| **GST Compliance** | ✅ Correct (1,800 INR = 18% of 10,000 INR) |
| **Vendor Match** | ✅ Found (Fuzzy: 88% confidence) |
| **Amount Match** | ✅ Exact (11,800 INR) |
| **Processing Time** | ~3 seconds |
| **Audit Cycles** | 1 (passed on first attempt) |

##  Key Features Demonstrated

1. **Multi-Agent Collaboration**: Manager orchestrates, Analyst performs detailed analysis
2. **Tool Use**: Deterministic GST calculation ensures mathematical accuracy
3. **Fuzzy Matching**: Successfully matched "ABC Services Pvt Ltd" ↔ "NEFT ABC SERVICES PVT LTD"
4. **Audit Loop**: Ready to retry if discrepancies are found (not needed in this success case)

## Error Detection Capability

To test failure detection, you can modify the sample data:
- Change invoice amount to create a mismatch
- Alter GST to create a tax compliance issue
- Change vendor name significantly to fail fuzzy matching

The agent will then demonstrate its retry logic and smart hints feature.

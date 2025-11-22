# VouchVault Demo Video Script (2-3 minutes)

## Opening (15 seconds)
"Hi, I'm Ravi, a CA Intermediate student and AI & Data Science enthusiast. VouchVault automates the most tedious part of financial auditing: vouching invoices against bank statements using multi-agent AI."

## Problem Statement (20 seconds)
"Junior auditors spend hours manually matching invoices to payments. It's repetitive, error-prone, and wastes high-value professional time that could be spent on analysis."

## Live Demo (60 seconds)

### Demo 1: Successful Audit
```bash
python main.py --invoice_path sample_data/invoice_sample_1.txt \
               --bank_csv sample_data/bank_statement_sample_1.csv
```
"Here's a perfect match - 11,800 INR invoice, vendor ABC Services, GST compliant at 18%. Watch the Analyst Agent verify each check using deterministic Python tools."

**Show output**: ✅ Tax compliance, ✅ Vendor match, ✅ Amount verified

### Demo 2: Retry Logic
```bash
python main.py  # Uses simulated data with discrepancy
```
"Now with an intentional 30 INR mismatch - the Manager Agent triggers retry logic with intelligent hints. This demonstrates error recovery and looping agents."

**Show output**: Retry attempts with specific difference calculation

## Architecture (30 seconds)
"Two specialized agents: 
- **Manager**: Orchestrates the audit workflow
- **Analyst**: Uses Gemini 1.5 Flash with function calling

**Key innovation**: Deterministic Python tools for tax calculations—no LLM math hallucinations."

**Show diagram**: Manager → Analyst → Tools → Result

## Competition Capabilities (20 seconds)
"This project demonstrates **5 AI agent capabilities** from the Google Intensive:

1. ✅ Multi-Agent Architecture 
2. ✅ Tool Use & Function Calling
3. ✅ **Memory** - Audit history tracking
4. ✅ **Evaluation** - Performance metrics
5. ✅ Retry Logic & Error Recovery"

## Impact & Closing (15 seconds)
"Reduces 5-minute manual audits to **under 3 seconds**. Built for Indian accounting firms (GST compliance). All code and docs available on GitHub."

**End screen**: 
- GitHub link
- LinkedIn: Ravi
- Thank you!

---

## Recording Tips

- **Screen setup**: Terminal + VS Code side-by-side
- **Highlight**: Show the fuzzy matching catching "ABC Services" = "ABC SERVICES PVT LTD"
- **Emphasize**: Mention this is for **Google AI Agents Intensive Capstone**
- **Energy**: Stay enthusiastic - you're solving a real CA problem!

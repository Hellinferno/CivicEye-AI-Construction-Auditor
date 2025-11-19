
VouchVault: Autonomous Enterprise Audit Agent

Google AI Agents Intensive Capstone (Enterprise Track)

Author: [Your Name]
Role: CA Intermediate & AI Engineer

📖 Project Overview

VouchVault is a multi-agent AI system designed to automate the "Vouching" process in financial audits. It autonomously cross-references unstructured Invoice data (PDF/Text) against structured Bank Statements (CSV) to verify:

Occurrence: Does the transaction actually exist in the bank ledger?

Accuracy: Is the tax calculation (GST/VAT) mathematically compliant?

🤖 Architecture

The system utilizes a Sequential Multi-Agent Architecture powered by Google Gemini 1.5 Flash:

Manager Agent (Orchestrator):

Ingests raw financial documents.

Delegates tasks to the Analyst.

Reviews final output and decides whether to approve or flag for human review.

Analyst Agent (The Looping Worker):

Tools: Uses deterministic Python functions for math (Tax Calc) and logic (Fuzzy Matching).

Loop Protocol: If a discrepancy is found, the agent enters a "Self-Correction Loop" to hypothesize reasons (e.g., discounts, partial payments) before failing.

🛠️ Technical Stack

Model: Google Gemini 1.5 Flash (via google-generativeai SDK)

Language: Python 3.11+

Tools: Custom Python implementations for Arithmetic & Regex matching.

Environment: Google Antigravity (IDE) / VS Code.

🚀 How to Run

Clone the repository

Install dependencies:

pip install -r requirements.txt


Configure API Key:

Create a .env file and add: GOOGLE_API_KEY=your_key_here

Run the Agent:

python main.py


💡 Key Features Implemented (Rubric)

✅ Multi-Agent System: Manager & Analyst separation of concerns.

✅ Tool Use: calculate_tax_compliance ensures 100% arithmetic accuracy (solving LLM math hallucinations).

✅ Looping Agents: Implemented retry logic (while attempts < max) to handle data discrepancies.

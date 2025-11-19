Category 1: The Pitch

Problem Statement:
In the auditing world, "Vouching" (verifying documentary evidence) is the most labor-intensive phase. Junior accountants spend thousands of hours manually matching invoice totals to bank statements and recalculating tax percentages. This process is repetitive, prone to "alert fatigue," and purely deterministic—yet it consumes high-value human capital.

Solution:
VouchVault is an autonomous "Junior Auditor" agent. Unlike generic chat agents, VouchVault is engineered with deterministic guardrails. It uses an LLM for understanding unstructured invoice text (Vendor names, Dates) but hands off the critical verification logic to Python tools. This hybrid approach ensures the system has the flexibility of an LLM but the mathematical precision of a calculator.

Architecture & Value:
Built on the Google Gen AI SDK, VouchVault employs a Manager-Analyst pattern. The Manager delegates the audit to an Analyst Agent, which is equipped with a verify_tax tool. Crucially, the Analyst uses a Re-evaluation Loop: if data doesn't match, it doesn't just fail; it attempts to reconcile the difference (checking for discounts or partial payments), mirroring the behavior of a human auditor.

This tool reduces the time per invoice audit from ~5 minutes to <3 seconds.

Category 2: Implementation Details

Agents: 2 (Manager, Analyst)

Model: Gemini 1.5 Flash (optimized for latency/cost).

Tools: Custom Python logic for Tax Compliance and Fuzzy Vendor Matching.

Control Flow: While-loop based retry mechanism for handling anomalies.

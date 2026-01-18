 
Install dependencies:

pip install -r requirements.txt


Configure API Key:

Create a .env file and add: GOOGLE_API_KEY=your_key_here

Run the Agent:

python main.py

## Example Run

Using the sample invoice and bank statement provided:

```bash
python main.py \
  --invoice_path sample_data/invoice_sample_1.txt \
  --bank_csv sample_data/bank_statement_sample_1.csv
```
| Avg Processing Time | <3 seconds |

Install dependencies:

pip install -r requirements.txt


Configure API Key:

Create a .env file and add: GOOGLE_API_KEY=your_key_here

Run the Agent:

python main.py

## Example Run

Using the sample invoice and bank statement provided:

```bash
python main.py \
  --invoice_path sample_data/invoice_sample_1.txt \
  --bank_csv sample_data/bank_statement_sample_1.csv
```
| Avg Processing Time | <3 seconds |
| Tax Calculation Accuracy | 100% |
| Vendor Fuzzy Matching | 88%+ confidence |

## 🏆 Google AI Agents Intensive Capstone

**Capabilities Demonstrated:**
1. ✅ Multi-Agent System: Manager & Analyst separation of concerns.
✅ Tool Use: calculate_tax_compliance ensures 100% arithmetic accuracy.
✅ Looping Agents: Implemented retry logic to handle data discrepancies.
✅ Sessions & Memory: Implemented duplicate invoice detection.
✅ Agent Evaluation: Real-time latency and pass/fail metrics tracking.

## Running Tests

```bash
pytest -q
```

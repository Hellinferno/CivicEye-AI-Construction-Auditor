from vouchvault.tools import match_invoice_to_statement

def test_match_invoice_to_statement_exact():
    invoice_amount = 11800
    bank_records = [
        {"date": "2024-04-12", "description": "NEFT ABC SERVICES PVT LTD", "amount": 11800},
        {"date": "2024-04-15", "description": "Salary Credit", "amount": 60000},
    ]

    match = match_invoice_to_statement(invoice_amount, bank_records)
    assert match is not None
    assert match["amount"] == 11800

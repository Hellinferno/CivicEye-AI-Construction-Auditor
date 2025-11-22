from vouchvault.tools import calculate_tax_compliance

def test_tax_mismatch():
    """Test that the system correctly flags incorrect tax calculations."""
    # Invoice says Subtotal 1000, Tax 100 (Should be 180 for 18% rate)
    result = calculate_tax_compliance(1000.0, 100.0, 0.18)
    assert result["is_compliant"] is False
    assert result["status"] == "MISMATCH"
    assert result["expected_tax"] == 180.0
    assert result["actual_tax"] == 100.0

def test_tax_exact_match():
    """Test that correct tax calculations pass."""
    # Correct calculation: 1000 * 0.18 = 180
    result = calculate_tax_compliance(1000.0, 180.0, 0.18)
    assert result["is_compliant"] is True
    assert result["status"] == "MATCH"

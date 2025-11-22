from vouchvault.tools import calculate_gst

def test_calculate_gst_simple():
    base_amount = 10000
    rate = 0.18
    gst = calculate_gst(base_amount, rate)
    assert gst == 1800

import time
from vouchvault.evaluation import AuditMetrics, AuditEvaluator


def test_audit_metrics_duration():
    """Test duration calculation."""
    metrics = AuditMetrics(invoice_id="INV-001", start_time=time.time())
    time.sleep(0.1)
    metrics.end_time = time.time()
    assert metrics.duration_seconds >= 0.1


def test_audit_metrics_passed_checks():
    """Test passed checks counter."""
    metrics = AuditMetrics(invoice_id="INV-001", start_time=time.time())
    metrics.tax_compliant = True
    metrics.vendor_matched = True
    metrics.amount_matched = False
    assert metrics.passed_checks == 2


def test_audit_evaluator_summary():
    """Test evaluator aggregation."""
    evaluator = AuditEvaluator()
    
    m1 = evaluator.start_audit("INV-001")
    m1.end_time = time.time()
    m1.status = "PASS"
    
    m2 = evaluator.start_audit("INV-002")
    m2.end_time = time.time()
    m2.status = "FAIL"
    
    summary = evaluator.get_summary()
    assert summary["total_audits"] == 2
    assert summary["passed"] == 1
    assert summary["failed"] == 1

from vouchvault.memory import AuditMemory, AuditRecord


def test_add_and_count():
    """Test adding records."""
    memory = AuditMemory()
    record = AuditRecord("INV-001", "ABC Services", 11800.0, "PASS")
    memory.add_record(record)
    assert memory.total_processed == 1


def test_duplicate_detection():
    """Test duplicate invoice detection."""
    memory = AuditMemory()
    memory.add_record(AuditRecord("INV-001", "Test", 1000.0, "PASS"))
    
    assert memory.has_duplicate("INV-001") is True
    assert memory.has_duplicate("INV-002") is False


def test_vendor_search():
    """Test vendor lookup."""
    memory = AuditMemory()
    memory.add_record(AuditRecord("INV-001", "ABC Services", 1000.0, "PASS"))
    memory.add_record(AuditRecord("INV-002", "XYZ Corp", 2000.0, "FAIL"))
    
    results = memory.get_by_vendor("ABC")
    assert len(results) == 1
    assert results[0].vendor == "ABC Services"


def test_get_recent():
    """Test recent audits retrieval."""
    memory = AuditMemory()
    for i in range(10):
        memory.add_record(AuditRecord(f"INV-{i:03d}", "Vendor", 100.0, "PASS"))
    
    recent = memory.get_recent(3)
    assert len(recent) == 3
    assert recent[-1].invoice_id == "INV-009"

"""Simple audit memory for tracking processed invoices (Day 3 capability)."""
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional

@dataclass
class AuditRecord:
    """Record of a completed audit."""
    invoice_id: str
    vendor: str
    amount: float
    status: str
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())
    notes: Optional[str] = None

class AuditMemory:
    """Short-term memory for audit session."""
    
    def __init__(self):
        self._records: list[AuditRecord] = []
    
    def add_record(self, record: AuditRecord) -> None:
        """Add a new audit record to memory."""
        self._records.append(record)
    
    def get_by_vendor(self, vendor: str) -> list[AuditRecord]:
        """Retrieve past audits for a vendor (useful for pattern detection)."""
        return [r for r in self._records if vendor.lower() in r.vendor.lower()]
    
    def get_recent(self, n: int = 5) -> list[AuditRecord]:
        """Get the most recent N audits."""
        return self._records[-n:]
    
    def has_duplicate(self, invoice_id: str) -> bool:
        """Check if invoice was already processed."""
        return any(r.invoice_id == invoice_id for r in self._records)
    
    @property
    def total_processed(self) -> int:
        """Total number of processed invoices."""
        return len(self._records)

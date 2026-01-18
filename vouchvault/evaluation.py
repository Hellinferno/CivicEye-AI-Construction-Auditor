"""Evaluation metrics for audit accuracy (Day 4 capability)."""
import time
from dataclasses import dataclass, field
from typing import Optional, List

@dataclass
class AuditMetrics:
    """Metrics for a single audit."""
    invoice_id: str
    start_time: float
    end_time: Optional[float] = None
    attempts: int = 0
    status: str = "PENDING"
    tax_compliant: Optional[bool] = None
    vendor_matched: Optional[bool] = None
    amount_matched: Optional[bool] = None
    
    @property
    def duration_seconds(self) -> float:
        """Calculate audit duration."""
        if self.end_time:
            return round(self.end_time - self.start_time, 2)
        return 0.0
    
    @property
    def passed_checks(self) -> int:
        """Count how many checks passed."""
        checks = [self.tax_compliant, self.vendor_matched, self.amount_matched]
        return sum(1 for c in checks if c is True)
    
    def to_dict(self) -> dict:
        """Convert to dictionary for logging/display."""
        return {
            "invoice_id": self.invoice_id,
            "duration_seconds": self.duration_seconds,
            "attempts": self.attempts,
            "status": self.status,
            "checks_passed": f"{self.passed_checks}/3",
        }

class AuditEvaluator:
    """Tracks and aggregates audit metrics across sessions."""
    
    def __init__(self):
        self.history: List[AuditMetrics] = []
    
    def start_audit(self, invoice_id: str) -> AuditMetrics:
        """Start tracking a new audit."""
        metrics = AuditMetrics(invoice_id=invoice_id, start_time=time.time())
        self.history.append(metrics)
        return metrics
    
    def get_summary(self) -> dict:
        """Get aggregate statistics."""
        if not self.history:
            return {}
        total = len(self.history)
        passed = sum(1 for m in self.history if m.status == "PASS")
        avg_time = sum(m.duration_seconds for m in self.history) / total
        return {
            "total_audits": total,
            "passed": passed,
            "failed": total - passed,
            "pass_rate": f"{(passed/total)*100:.1f}%",
            "avg_duration": f"{avg_time:.2f}s",
        }

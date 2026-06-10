"""Task handover service placeholder.

This module reserves extension points for:
- script-driven task claim
- result parcel publishing
- cross-agent relay orchestration
"""

from app.schemas.result_parcel import ResultParcel


class TaskHandoverService:
    """Minimal placeholder service for future relay orchestration."""

    def accept_result_parcel(self, parcel: ResultParcel) -> ResultParcel:
        """Echo parcel in skeleton stage; real implementation will persist & emit events."""
        return parcel

"""Extension interfaces reserved for future script runtime and handover pipeline."""

from __future__ import annotations

from typing import Protocol

from app.schemas.result_parcel import ResultParcel
from app.schemas.tag_protocol import TagProtocol


class ScriptRule(Protocol):
    """Rule contract: determine whether an agent can claim a tagged task."""

    def should_trigger(self, tags: list[TagProtocol]) -> bool:
        """Return True if the rule matches and should trigger execution."""


class HandoverAdapter(Protocol):
    """Handover contract: publish iteration outputs to task center or registry."""

    def publish(self, parcel: ResultParcel) -> str:
        """Persist parcel and return registry reference id."""

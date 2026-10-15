"""NEWSLETTER_SEND_ENABLED becomes a hold. This module does not send."""

from __future__ import annotations

import os
from collections.abc import Mapping
from dataclasses import dataclass
from typing import Literal

__all__ = ["hold", "Held"]

_ON = frozenset({"1", "true", "yes", "on"})


@dataclass(frozen=True, slots=True)
class Held:
    """The only result this module can construct."""

    reason: Literal["disabled", "no_transport"]

    def __post_init__(self) -> None:
        if self.reason not in ("disabled", "no_transport"):
            raise ValueError("unknown hold reason")


def hold(env: Mapping[str, str] | None = None) -> Held:
    """Read NEWSLETTER_SEND_ENABLED. Off is disabled. On is no_transport."""
    source = os.environ if env is None else env
    raw = source.get("NEWSLETTER_SEND_ENABLED", "")
    if not isinstance(raw, str):
        return Held("disabled")
    if raw.strip().casefold() in _ON:
        return Held("no_transport")
    return Held("disabled")

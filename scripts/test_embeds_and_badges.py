#!/usr/bin/env python3
"""CI entry for the embeds and badge checks."""
from __future__ import annotations

import runpy
from pathlib import Path

runpy.run_path(str(Path(__file__).resolve().parents[1] / "tests" / "test_embeds_and_badges.py"), run_name="__main__")

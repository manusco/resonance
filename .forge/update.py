#!/usr/bin/env python3
"""Compatibility entrypoint for the installed Resonance updater."""
from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

spec = importlib.util.spec_from_file_location("_resonance_update_runtime", ROOT / "resonance_update.py")
runtime = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = runtime
spec.loader.exec_module(runtime)
for exported_name in dir(runtime):
    if not exported_name.startswith("_"):
        globals()[exported_name] = getattr(runtime, exported_name)


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))

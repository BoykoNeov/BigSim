#!/usr/bin/env pwsh
# Test runner (ARCHITECTURE.md §6 / steel plan §7; tiered gate = ADR 0003).
# No args = the FULL commit gate (every engine seal + per-project test) — the
# tracked invariant. Args pass through, so the tiered lanes are one flag away:
#   ./run_tests.ps1                  # full gate (the canonical green count)
#   ./run_tests.ps1 -m "not slow"    # fast inner loop (~8 s; live-solver/kernel tests deselected)
#   ./run_tests.ps1 projects/steel   # scope to one module under edit
#   ./run_tests.ps1 -k erfc          # filter by name
$ErrorActionPreference = "Stop"
python -m pytest @args
exit $LASTEXITCODE

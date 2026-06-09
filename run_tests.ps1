#!/usr/bin/env pwsh
# Test runner (ARCHITECTURE.md §6 / steel plan §7; tiered gate = ADR 0003).
# Args pass through to pytest, so the tiered lanes are one flag away:
#   ./run_tests.ps1 -m "not slow"    # ROUTINE commit gate (~8 s, whole-repo fast lane,
#                                    #   incl. the frozen-engine "used modules")
#   ./run_tests.ps1                  # FULL gate (the canonical 248) — EXCEPTIONAL only:
#                                    #   a shared engines/ edit, root-config, a release, CI
#   ./run_tests.ps1 projects/steel   # scope to one module under edit
#   ./run_tests.ps1 -k erfc          # filter by name
# (Docs-only changes need no gate at all — see ADR 0003.)
$ErrorActionPreference = "Stop"
python -m pytest @args
exit $LASTEXITCODE

#!/usr/bin/env pwsh
# Single-command test runner (ARCHITECTURE.md §6 / steel plan §7).
# Runs the whole BigSim suite: the engine seals (and, once they exist, the
# per-project tests). Pass extra args through, e.g. `./run_tests.ps1 -k erfc`.
$ErrorActionPreference = "Stop"
python -m pytest @args
exit $LASTEXITCODE

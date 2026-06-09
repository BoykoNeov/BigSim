#!/usr/bin/env pwsh
# Whole-repo test runner (ARCHITECTURE.md §6 / steel plan §7; tiered gate = ADR 0003).
# Args pass through to pytest, so the whole-repo lanes are one flag away:
#   ./run_tests.ps1 -m "not slow"    # ROUTINE whole-repo gate (~8 s, fast lane,
#                                    #   incl. the frozen-engine "used modules")
#   ./run_tests.ps1                  # FULL gate (the canonical suite) — EXCEPTIONAL only:
#                                    #   a shared engines/ edit, root-config, a release, CI
#   ./run_tests.ps1 projects/steel   # scope to one module under edit
#   ./run_tests.ps1 -k erfc          # filter by name
#
# PER-PROJECT gate (the ADR 0003 Successor — runs a project's own tests + the tests of
# the modules it uses, per the tools/gate.py manifest; the routine gate once 2+ projects
# exist). Cross-platform, so it's the same command here and in CI:
#   python -m tools.gate chip -m "not slow"   # chip's routine commit gate
#   python -m tools.gate steel                # steel's full per-project gate
# (Docs-only changes need no gate at all — see ADR 0003.)
$ErrorActionPreference = "Stop"
python -m pytest @args
exit $LASTEXITCODE

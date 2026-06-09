#!/usr/bin/env sh
# Whole-repo test runner (ARCHITECTURE.md §6 / steel plan §7; tiered gate = ADR 0003).
# Runs the whole BigSim suite: the engine seals + every project's tests. Pass extra
# args through, e.g. `./run_tests.sh -m "not slow"` (routine) or `./run_tests.sh -k erfc`.
#
# For the PER-PROJECT gate (ADR 0003 Successor — a project's own tests + the tests of
# the modules it uses, from the tools/gate.py manifest), use the cross-platform runner:
#   python -m tools.gate chip -m "not slow"
exec python -m pytest "$@"

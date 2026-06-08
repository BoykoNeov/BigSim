#!/usr/bin/env sh
# Single-command test runner (ARCHITECTURE.md §6 / steel plan §7).
# Runs the whole BigSim suite: the engine seals (and, once they exist, the
# per-project tests). Pass extra args through, e.g. `./run_tests.sh -k erfc`.
exec python -m pytest "$@"

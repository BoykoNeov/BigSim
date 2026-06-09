"""Per-project test gate — the ADR 0003 *Successor* (manifest-backed, post-Microchip).

ADR 0003 (``docs/decisions/0003-test-execution-policy.md``) established a tiered gate and
committed to a per-project successor once a 2nd project landed: *a commit to a project
runs only the tests concerning that project* — its own tests **plus the tests of the
modules it uses** — read from a **hand-declared manifest**, NOT a git-diff / import
heuristic. Microchip (project #2) is that landing; this module is the build.

The manifest is :data:`GATES` below — ``project -> the shared/engine modules it uses``.
:func:`paths_for` expands one entry into the pytest path set:

    tools/tests                # the gate's own self-check (manifest completeness)
    projects/<project>/tests   # the project's own tests
    <used module>/tests        # the frozen-engine tests it depends on (the "used modules")

Usage (cross-platform — identical on Windows-local and Linux-CI; project comes first,
everything after passes straight through to pytest)::

    python -m tools.gate chip                  # chip's FULL per-project gate
    python -m tools.gate chip -m "not slow"    # chip's ROUTINE commit gate (fast lane)
    python -m tools.gate steel -k erfc         # any extra pytest args pass through

The whole-repo lanes are unchanged (ADR 0003): ``./run_tests.ps1 -m "not slow"`` (routine,
all projects) and bare ``./run_tests.ps1`` (the full gate — shared-engine edit / root-config
change / release / CI).

**Hand-declared, not auto-derived-from-imports** (the open design call, advisor-reviewed
2026-06-09): ADR 0003 committed to an explicit single source of truth; an import scanner
that silently misses a dependency is the worst failure mode (a green run that quietly
under-tested). And at today's **N = 1 engine** the two approaches yield the *identical*
manifest — every project imports the one engine — so auto-derivation buys nothing. The
matching **drift guard** (assert each project's actual ``engines.*`` imports are all
declared here) is **deferred to engine #2**: at one engine it cannot fail and has nothing
to check. When built it must run *inside* this per-project gate (not only the whole-repo
lane), or it won't fire on a per-project commit.
"""
from __future__ import annotations

import subprocess
import sys

# The manifest: project -> the shared/engine modules it uses (repo-relative dirs).
# Both current projects reuse the single frozen diffusion spine (engines/diffusion) —
# Steel via jominy/carburize, Microchip via diffusion_dopant — so `uses` is identical
# today. Microchip is a second *row*, not yet a second distinct *value*: the manifest's
# discriminating feature stays unvalidated until a project uses a different module set
# (ADR 0003 Successor caveat). Keep this minimal accordingly.
GATES: dict[str, list[str]] = {
    "steel": ["engines/diffusion"],
    "chip": ["engines/diffusion"],
}


def paths_for(project: str) -> list[str]:
    """Return the pytest path set for *project*: the gate self-check, the project's own
    tests, and the tests of every module it uses ("the tests concerning the project")."""
    used = GATES[project]
    return ["tools/tests", f"projects/{project}/tests", *(f"{m}/tests" for m in used)]


def main(argv: list[str] | None = None) -> int:
    import argparse

    parser = argparse.ArgumentParser(
        prog="python -m tools.gate",
        description="Run a project's per-project test gate (the ADR 0003 successor).",
    )
    parser.add_argument("project", choices=sorted(GATES), help="the project to gate")
    parser.add_argument(
        "pytest_args",
        nargs=argparse.REMAINDER,
        help='extra args passed straight to pytest (e.g. -m "not slow", -k NAME)',
    )
    ns = parser.parse_args(argv)
    cmd = [sys.executable, "-m", "pytest", *paths_for(ns.project), *ns.pytest_args]
    return subprocess.run(cmd).returncode


if __name__ == "__main__":
    raise SystemExit(main())

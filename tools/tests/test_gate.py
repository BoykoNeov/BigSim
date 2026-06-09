"""The per-project gate's own self-check (ADR 0003 successor).

Pins the manifest's core invariant — **completeness** — and that every path the gate
hands to pytest actually exists. This file is the first entry in
:func:`tools.gate.paths_for`, so it runs *inside* every per-project gate: a scoped run
validates the manifest that scoped it.

NOT here (deferred to engine #2 — ADR 0003 / advisor 2026-06-09): the import-drift guard
that each project's actual ``engines.*`` imports are all declared in ``GATES``. At one
engine it cannot fail and has nothing to check.
"""
from pathlib import Path

from tools.gate import GATES, paths_for

REPO_ROOT = Path(__file__).resolve().parents[2]


def _projects_on_disk() -> set[str]:
    """Project packages under ``projects/`` — a dir with ``__init__.py`` and ``tests/``."""
    projects_dir = REPO_ROOT / "projects"
    return {
        p.name
        for p in projects_dir.iterdir()
        if p.is_dir() and (p / "__init__.py").exists() and (p / "tests").is_dir()
    }


def test_manifest_covers_every_project():
    # Every project that exists must have a gate entry, and no entry may be a phantom —
    # else a project's commits would silently have no per-project gate (the live failure
    # mode the moment project #3 lands).
    assert set(GATES) == _projects_on_disk()


def test_every_gated_path_exists():
    # A typo'd manifest entry must fail loudly here, not silently scope pytest to a
    # smaller set of tests.
    for project in GATES:
        for rel in paths_for(project):
            assert (REPO_ROOT / rel).is_dir(), f"{project}: gate path does not exist: {rel}"

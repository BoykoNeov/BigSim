"""The per-project gate's own self-check (ADR 0003 successor).

Pins the manifest's core invariants — **completeness**, that every path the gate hands to
pytest exists, and (since engine #2, Planet Phase 3) the **import-drift guard**: each
project's actual ``engines.*`` imports must all be declared in ``GATES``. This file is the
first entry in :func:`tools.gate.paths_for`, so it runs *inside* every per-project gate: a
scoped run validates the manifest that scoped it (so the drift guard fires on a per-project
commit, not only the whole-repo lane).

The drift guard was deferred until a *second* engine existed (ADR 0003 / advisor 2026-06-09):
at one engine it could not fail (every project imports the one engine). With ``engines/fluid``
it finally discriminates — a ``planet`` that imports ``engines.fluid`` but forgot to declare it
is exactly the silently-under-tested failure this catches.
"""
import ast
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


def _engine_imports(project: str) -> set[str]:
    """The set of ``engines/<sub>`` a project's *source* (non-test) modules import.

    Parses every ``projects/<project>/*.py`` (excluding ``tests/``) with ``ast`` and
    collects ``import engines.X`` / ``from engines.X import ...`` / ``from engines import X``
    as the repo-relative dir ``engines/X``. Source-only: the gate already runs the engines'
    own tests separately; what the *drift guard* checks is the project's real dependency.
    """
    used: set[str] = set()
    pkg = REPO_ROOT / "projects" / project
    for py in pkg.glob("*.py"):
        tree = ast.parse(py.read_text(encoding="utf-8"), filename=str(py))
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    parts = alias.name.split(".")
                    if parts[0] == "engines" and len(parts) >= 2:
                        used.add(f"engines/{parts[1]}")
            elif isinstance(node, ast.ImportFrom) and node.module:
                parts = node.module.split(".")
                if parts[0] == "engines" and len(parts) >= 2:
                    used.add(f"engines/{parts[1]}")          # from engines.fluid import ...
                elif parts == ["engines"]:
                    for alias in node.names:                  # from engines import fluid
                        used.add(f"engines/{alias.name}")
    return used


def test_no_import_drift_from_the_manifest():
    # The import-drift guard (live since engine #2): every engine a project actually imports
    # must be declared in GATES, or that project's per-project gate silently under-tests it.
    for project in GATES:
        imported = _engine_imports(project)
        declared = set(GATES[project])
        missing = imported - declared
        assert not missing, (
            f"{project} imports {sorted(missing)} but they are not declared in GATES "
            f"(declared: {sorted(declared)}); add them so the per-project gate runs their seals"
        )

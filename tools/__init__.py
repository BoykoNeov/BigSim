"""Program-level tooling (not a shipped package, not a simulator).

Home of the per-project test gate (:mod:`tools.gate`) — the ADR 0003 *Successor*.
Excluded from the wheel (``[tool.setuptools.packages.find]`` includes only
``engines*`` / ``projects*``); its own tests are collected via ``testpaths`` in
``pyproject.toml``.
"""

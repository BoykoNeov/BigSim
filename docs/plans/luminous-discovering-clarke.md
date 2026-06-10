# Split BigSim into three standalone repositories

## Context

BigSim is a monorepo holding three educational simulators — **steel**, **chip**,
**planet** — built on two shared, frozen solver engines (`engines/diffusion`,
`engines/fluid`). The shared engines are great for pedagogy ("one validated solver,
three sims"), but the multi-agent worktree workflow (PARALLEL.md) that coordinates
their *simultaneous* development carries real overhead — one serialized engine seam,
orchestrator-owned shared files, end-of-batch merge rituals — and that overhead will
keep recurring. The three projects are otherwise independent: they share **only** the
engines (verified — no cross-project imports), each has its own tests, docs, figures,
and extras.

**Goal:** separate the three into independent Git repositories, each fully standalone,
so they can evolve without cross-project coordination. The engines are **vendored**
(copied) into each repo — not a shared package/submodule, which would just relocate the
coordination cost (version → publish → re-pin ×3). The engines are frozen and small
(diffusion 385 LOC, fluid 436 LOC) with their own tests, so divergence risk is low and
the validated-solver pedagogy survives per-repo. The monorepo stays as a read-only
archive (the cross-project portfolio narrative).

**User-confirmed decisions:**
- **History:** preserve per-project via `git filter-repo` (the git log is part of the portfolio artifact).
- **Layout:** flatten to repo root — `engines/` + `steel/` (no `projects/` nesting).
- **Remotes:** create now under BoykoNeov as `steel-sim`, `chip-sim`, `planet-sim` (public, matching BigSim).
- **Monorepo:** keep `BoykoNeov/BigSim` as a read-only archive.

## Engine / infra ownership map

| Repo | Engines | ADRs | Extras (pyproject) | CI specials |
|---|---|---|---|---|
| **steel-sim** | diffusion | 0001, 0002, 0003 | viz, app, calphad, notebook | TDB download (`steel.calphad_backend.download_mc_fe`) |
| **chip-sim** | diffusion | 0001, 0002, 0003 | viz, notebook | chip notebook auto-skips under `CI=true` (already in test) |
| **planet-sim** | diffusion + **fluid** | 0001, 0002, 0003, **0004** | viz, webviz, climate, notebook | plotly + climlab in install guard |

Per-project carry-over (by current path → new path):
- `projects/<p>/` → `<p>/` (flatten), `projects/<p>/README.md` → repo `README.md` candidate
- `docs/plans/{steel-production,microchip-fabrication,planet-earth-system}.md` → one per repo
- `docs/figures/<p>-*.png` → one prefix per repo
- `data/tdb` is **gitignored** — nothing to carry (steel CI re-downloads)
- **Dropped from every repo:** `tools/gate.py` + `tools/tests` (multi-project gate is moot at one project), `PARALLEL.md` (the dismantled workflow), `ARCHITECTURE.md`/`PORTFOLIO.md`/root `README.md` (monorepo-level — replaced by a fresh per-repo README)

## Phase 0 — Final reconciliation (the split source must be complete)

The three work branches hold **unmerged, already-built** work that main lacks:
- `chip-work` (+1): v1.2 Phase 1↔2 back-coupling (OED + segregation)
- `planet-work` (+2): notebook tiering + full-arc winds/jet
- `steel-work` (+3): Phase 6c D_I cross-check, 6d austempering build, 6c precision fixes

One last PARALLEL.md orchestration pass so the archive (and the split source) is canonical:
1. From `main`: `git merge --no-ff chip-work`, `planet-work`, `steel-work` (disjoint files → conflict-free by the keystone invariant).
2. **Full gate:** `python -m pytest` (locally `CI` is unset, so the chip notebook test runs and passes ~8 s). Must be green.
3. Update root status docs (README/PORTFOLIO test counts) to the final state; commit; **push main**.

Each new repo is then cloned `--single-branch -b main` from this canonical archive.

## Phase 1 — Tooling + working clones

1. `pip install git-filter-repo` (one-file tool; confirm `git filter-repo --version`).
2. For each project, make a fresh **non-local** clone (filter-repo is destructive to the
   **clone only** — `--no-local` forces a real object copy so the irreplaceable archive is
   never shared via hardlinks/repacked):
   `git clone --no-local --single-branch -b main M:/claud_projects/BigSim M:/claud_projects/<p>-sim`

## Phase 2 — Split each repo (history-preserving flatten)

**Do chip-sim FIRST, fully, as the template** (simplest: diffusion-only, extras `viz,notebook`,
no TDB/CALPHAD). Prove the exact recipe green end-to-end (Phase 3) before replicating to steel
and planet. Don't fan out an untested filter-repo command across all three.

Two-step flatten per repo — `--path-rename` preserves the commit narrative (the portfolio-relevant
artifact) and moves the tree across history; a **single tip commit** then rewrites file contents +
adds standalone packaging. (We deliberately **drop** filter-repo `--replace-text`: rewriting all
history blobs buys only old-checkout import-consistency, which is moot anyway since the old-SHA
pyproject can't `pip install` the renamed package — and it's a heavier, riskier rewrite.)

**Step A — filter + rename (history).** Pattern for chip (steel/planet analogous; steel keeps
ADRs 0001–0003 only; planet adds `engines/fluid` + ADR 0004):

```
git filter-repo \
  --path .gitignore \
  --path engines/diffusion --path engines/__init__.py \
  --path projects/chip \
  --path docs/decisions/0001-language-and-performance.md \
  --path docs/decisions/0002-visualization-and-ux.md \
  --path docs/decisions/0003-test-execution-policy.md \
  --path docs/plans/microchip-fabrication.md \
  --path-glob 'docs/figures/chip-*' \
  --path-rename projects/chip:chip
```
`--path .gitignore` is **load-bearing** — without it the keep-only filter deletes the root
`.gitignore` (`data/`, `*.tdb`, `__pycache__/`, `*.egg-info/`) from all history. Verify it survived.
(filter-repo also **strips the `origin` remote** here by design — the clone has no remote until Phase 4.)

**Step B — one tip commit: flatten contents + standalone packaging.**
- Content rewrite over the current tree: `projects.chip` → `chip` and `projects/chip` → `chip`
  (scripted regex over every `.py`/`.ipynb`/`.md`/`.yml`; the `.ipynb` JSON strings match too).
- **`pyproject.toml`** — `packages.find` include `["engines*","chip*"]`; `pythonpath=["."]`;
  `testpaths=["engines","chip"]`; keep the `slow` marker; only this repo's extras.
- **`.github/workflows/full-gate.yml`** — trimmed copy: install only this repo's extras; prune the
  import-presence guard list accordingly; keep kernelspec registration; steel keeps the TDB
  cache+download steps (path now `steel.calphad_backend`), chip/planet drop them; `python -m pytest -rs`.
  (The chip notebook test already self-skips under `CI=true` — carried as-is.)
- **`README.md`** (root) — short: what it is, install (`pip install -e .[...]`), test
  (`pytest -m "not slow"` fast / `pytest` full), provenance line back to the BigSim archive.
- **`run_tests.ps1` / `run_tests.sh`** — trimmed single-repo runners (optional; pytest suffices).
- Confirm `tools/` and `PARALLEL.md` did **not** survive the filter (they shouldn't), and `.gitignore` did.

## Phase 3 — Verify each repo green (before any push)

In a fresh venv per repo:
1. `pip install -e ".[<all this repo's extras>]"`
2. `python -m pytest -m "not slow"` → green (the always-on suite)
3. Register a kernelspec (`python -m ipykernel install --user --name python3`) so the full run
   actually **exercises** the notebook smoke-test instead of importorskip-skipping it.
4. `python -m pytest` → green (full, incl. slow/live; chip runs the notebook locally since `CI` is unset).
5. Sanity: test count ≈ that project's slice of the 590-test monorepo total.

## Phase 4 — Create remotes + push

1. `gh repo create BoykoNeov/<p>-sim --public --source M:/claud_projects/<p>-sim --remote origin --push`
   (confirm public; repos can be flipped private later).
2. Watch each repo's first `full-gate` run to green (chip notebook skips under CI — expected).

## Phase 5 — Archive + cleanup the monorepo

In `BoykoNeov/BigSim` (the archive):
1. README banner: "Archived — split into [steel-sim], [chip-sim], [planet-sim]. Read-only."
2. Demote `PARALLEL.md` to historical (note at top: workflow retired, repos split).
3. Retire the three worktrees (`git worktree remove BigSim-chip|-planet|-steel`) and delete the
   `chip-work`/`planet-work`/`steel-work` branches (local + origin) — they're fully merged.
4. Leave history + PORTFOLIO intact.

## Phase 6 — Memory (auto-memory is path-keyed → new paths get empty stores)

The memory store lives at `~/.claude/projects/M--claud-projects-<name>/memory/`. New repos at new
paths start empty, stranding ~30 cited-source/phase-log files. Pre-populate each new store:
- **Per-project source/phase memories** → copy into that repo's store + build a fresh `MEMORY.md` index:
  - steel: `steel-*`, `maynier-*`, `hollomon-*`, `carburize-*`, `grain-growth-*`, `pickering-*`,
    `matcalc-*`, `ferrite-bay-*`, `bainite-anchoring-*`, `di-crosscheck-*`
  - chip: `dopant-*`, `deal-grove-*`, `massoud-*`, `irvin-*`, `litho-*`, `mos-*`, `oed-*`,
    `dopant-segregation-*`, `chip-coupling-*`, `chip-notebook-flake`
  - planet: `planet-*`, `ebm-radiation-*`, `whittaker-*`, `precip-*`, `shallow-water-*`,
    `stellar-spectrum-*`, `obliquity-*`
- **Cross-cutting memories stay in the BigSim archive store** (and noted as historical):
  `bigsim-program`, `parallel-dev`, `end-of-batch-ritual`, `test-execution-policy`,
  `notebook-pedagogy-tiers`, `notebook-slider-flicker`, `bigsim-github-repo`.
- Update each project memory's `[[links]]`/hooks that referenced the monorepo context.

## Verification (end-to-end)

- **Phase 0:** `python -m pytest` on merged main = green; `git log --oneline main..<branch>` empty for all three.
- **Per repo:** clean `pip install -e .[...]` + `pytest` green; `git log` shows preserved per-project
  history (shared-engine commits appear honestly); no `projects/` dir, no `tools/gate.py`, no `PARALLEL.md`;
  imports are `steel.*` / `engines.*`.
- **Remotes:** three `full-gate` CI runs green (chip notebook skipped under CI).
- **Archive:** BigSim README banner live; worktrees/branches retired; history intact.

## Risks / notes

- filter-repo is destructive — run **only** in fresh `--no-local` clones, never the archive or worktrees.
- `--path-rename` preserves the commit/authorship/phase narrative (the portfolio artifact) and moves
  the tree across history; the content rewrite lives in **one tip commit**. Old checkouts won't run
  (historical blobs still import `projects.<p>`) — accepted: nobody exercises old checkouts on a portfolio,
  and `--replace-text` wouldn't fully fix it either (old-SHA pyproject still can't install the renamed package).
- New repos get **new SHAs** — memory/doc references to archive SHAs (`d6e4f79`, etc.) resolve only in the
  archive, not the new repos. Fine for reference; don't expect `git show <sha>` to work in the new repo.
- Public push publishes code; confirmed no secrets (TDB never committed, no credentials).
- Phase 6 (memory) is outside the repos (low-risk) and can trail the code split if desired.

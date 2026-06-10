# Parallel multi-agent development

> **⚠️ Historical — workflow retired 2026-06-10.** This document describes the multi-agent
> worktree workflow used while the three simulators were developed *together* in this monorepo.
> That workflow has been **retired**: the simulators were split into standalone repos
> ([steel-sim](https://github.com/BoykoNeov/steel-sim) ·
> [chip-sim](https://github.com/BoykoNeov/chip-sim) ·
> [planet-sim](https://github.com/BoykoNeov/planet-sim)), so there is no longer cross-project
> orchestration to coordinate. Kept for the record of how the program was built.

How several Claude sessions develop different subprojects of BigSim at once
without clobbering each other. **Model A + Claude-managed merges**: separate
sessions in separate git worktrees, a human supervisor who approves merges, and
one **orchestrator** session that owns integration.

---

## Project session — READ THIS FIRST

> ### The one rule the whole model rests on
> **Shared files physically appear in your worktree** — `README.md`,
> `ARCHITECTURE.md`, `PORTFOLIO.md`, `MEMORY.md`, `pyproject.toml`,
> `tools/gate.py`, `engines/**`, `docs/decisions/**` — and *more* of them
> appear every time you `git merge main`. **They are NOT yours. Never edit
> them.** A single "helpful" tweak (e.g. bumping a test count in the root
> README) creates a real merge conflict and breaks the guarantee.
>
> You own **only** `projects/<name>/` plus your project's own
> `docs/plans/<name>-*.md` and `docs/figures/<name>-*.png`.
>
> If your work needs a shared file changed (a new `pyproject` extra, a new
> `GATES` `uses` entry, an engine change), **do not make the change** — record
> a `SHARED-FILE ASK` in your hand-off and the orchestrator makes it.

Your loop, as the `<project>` session in `BigSim-<project>` on branch
`<project>-work`:

1. **Batch start:** `git merge main` — pick up shared-file updates so your
   branch doesn't drift (conflict-free, by the rule above).
2. **Inner loop:** `python -m tools.gate <project> -m "not slow"` — your own
   tests + the tests of the engines you use. Fast, scoped feedback.
3. **Batch end:** gate green → commit **to your branch** (never `main`) → write
   the hand-off as the **commit-message body**, ending with a
   `SHARED-FILE ASKS:` section (list them, or `none`) and the new gate
   test-count.

Do **not** update `README` / `ARCHITECTURE` / `MEMORY.md` / `pyproject` / the
gate manifest — that is the orchestrator's half of the ritual.

---

## The seats

| Worktree | Branch | Role |
|---|---|---|
| `M:\claud_projects\BigSim` | `main` | **Orchestrator** — integration only, owns all shared files |
| `M:\claud_projects\BigSim-steel` | `steel-work` | Steel session |
| `M:\claud_projects\BigSim-chip` | `chip-work` | Chip session |
| `M:\claud_projects\BigSim-planet` | `planet-work` | Planet session |

The **human** supervises: approves each merge, answers questions. The
orchestrator never develops project code; project sessions never integrate.
**`main` is orchestrator-only — no project agent ever works in `main` again.**

## The keystone invariant

> A project session edits **only** `projects/<name>/` and that project's own
> prefixed docs/figures. It never edits a shared file.

Because the projects are disjoint directories, this makes *every* merge —
branch into `main`, and `main` back into a branch — **conflict-free by
construction** (the three-way merge always resolves shared files in `main`'s
favor, since the branch never changed them). The orchestrator is therefore not
resolving conflicts; it is updating shared files and running the gate.

## Shared files — orchestrator-only

- `README.md`, `ARCHITECTURE.md`, `PORTFOLIO.md`
- `MEMORY.md` and the `memory/` store
- `pyproject.toml` (deps / optional-dependency extras)
- `tools/gate.py` (the `GATES` manifest)
- `engines/**` (the freeze — see *Engine barrier*)
- `.github/**`, `docs/decisions/**` (ADRs)

## End-of-batch — orchestrator (the integration desk)

On the human's approval. **The shared-file updates split into two phases with
opposite timing** — get this order right:

1. **Read the hand-off:** `git log main..<branch>` (a batch may be several
   commits, not just the tip).
2. **Apply dependency-type asks _before_ the merge** — anything the merged code
   *needs* to run: a new `pyproject` extra, a new `GATES` `uses` entry. (If
   these land late, step 4's gate fails or silently skips.)
3. **`git merge <branch>` into `main`** — conflict-free by the invariant.
4. **Run `pytest -m "not slow"`** — whole-repo fast lane, to catch cross-project
   breakage the per-project gate could not see.
5. **Write descriptive updates _after_ the merge + gate** — root-doc test
   counts, `MEMORY.md` notes. (You can't know the true whole-repo count until
   the merged code is in and counted.)
6. **Tell the project session to `git merge main`** to pick up the shared-file
   updates.

## Merge trigger

**Human-gated.** A project signals ready → the orchestrator proposes the
integration → the human approves → the orchestrator runs the steps above.
(Switch to auto-on-green only if the human says so.)

## Engine barrier — the one serialization point

Any change under `engines/**` touches the freeze, the `GATES` manifest, the
import-drift guard, and *every* consumer. It is **not** parallel work:

1. Parallel project work pauses.
2. The orchestrator makes the change on `main`.
3. **Full** `pytest` (not the per-project gate) re-validates all consumers.
4. Re-freeze (update the engine's `CONTRACT.md`).
5. Project branches `git merge main` onto the new engine.

The import-drift guard (`tools/tests/test_gate.py`) asserts each project's
actual `engines.*` imports are all declared in `GATES`.

## Sync mechanics

All worktrees share one `.git`, so a branch committed in one is visible to the
others **instantly — no push/pull**. Project sessions `git merge main` at batch
start *and* after each integration; the orchestrator merges branch→`main`. All
conflict-free by the invariant. Engine changes are the barrier above.

## Caveats

- **Auto-memory is keyed to the working-directory path.** Each worktree
  (`BigSim-steel`, …) maps to a *different* memory store and will **not** see
  this repo's `MEMORY.md`. The orchestrator (the `BigSim` checkout) owns
  `MEMORY.md`; brief worktree sessions with the relevant facts up front (point
  them at this file), and fold their findings back through the hand-off.
  *Future option, not now:* symlink each worktree's memory dir to the canonical
  store so project sessions *read* full memory while only the orchestrator
  *writes* — **only viable if** the harness does not auto-write to the memory
  dir per session (else it reintroduces the write-contention this design kills).
  Verify that before attempting it.
- gitignored artifact dirs (`outputs/`, `.pytest_cache/`, `__pycache__/`,
  `bigsim.egg-info/`) are now **per-worktree**, so parallel test runs no longer
  collide. No editable install is needed — `pytest`'s `pythonpath = ["."]`
  resolves `engines.*` / `projects.*` from each worktree root.

## One-time transition (2026-06-09)

These seats were created mid-flight, with steel and planet sessions already
running in the `main` checkout:

- **Steel** — *Phase 6a (proeutectoid-ferrite bay)* was already committed
  straight to `main` (`19fcac2`) before the seats existed. `steel-work` branches
  from that commit, so `BigSim-steel` already contains it. The steel session
  should **move to `M:\claud_projects\BigSim-steel`** for its next batch and
  commit to `steel-work` from now on.
- **Planet** — move the planet session to `M:\claud_projects\BigSim-planet`
  and commit to `planet-work`.
- **From now on, nothing commits to `main` except the orchestrator's merges.**

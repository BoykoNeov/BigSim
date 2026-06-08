# Educational Simulator Program — Architecture

## 0. Purpose & how to read this

This is the **living program map** for a suite of educational, interactive,
experimentation-focused physics/engineering/science simulators. It carries the
cross-cutting decisions an individual project plan cannot re-derive on its own:
the shared toolkit, the build order, the architecture doctrine that keeps work
coherent under a limited context window, the validation methodology, and the
scope ceilings.

It is deliberately the **reconstitutable context** of §6: a session rebuilds the
program's mental model from this file plus the per-module contracts, rather than
holding the whole codebase in its head.

**How to use it when planning a project:** treat §1–§9 as fixed constraints
("invariants") that every per-project plan inherits, generate the project detail
with the §10 template, and check the result against these invariants rather than
re-litigating them.

**Where things live:**
- `PORTFOLIO.md` — the full project catalog (tiers, anchors, engines, the chosen
  first three). This file (§3) only points at it.
- `docs/plans/` — the per-project plans (`steel-production.md` is plan #1).
- `docs/decisions/` — the ADR log (`0001-language-and-performance.md` is the
  first entry).

---

## 1. Targets (unchanged across all projects)

- **Education** — teach real mechanisms, not black boxes.
- **Interactivity** — expose the parameters that produce dramatic, counter-
  intuitive transitions; those are simultaneously the best teaching moments and
  the cheapest verification.
- **Experimentation** — let the user run sweeps and "what-ifs."
- **Aim far/deep in perspective** — the deep end is a direction to grow toward,
  not a gate to clear. Every phase must bank a working, demonstrable artifact.

---

## 2. Program invariants (every project inherits these)

1. **Build the toolkit once, reuse it everywhere.** A small set of solver
   engines underlies the whole portfolio. Build the solver-heavy projects first;
   later ones become recomposition. (§5.)
2. **Phase so each stage banks a working artifact.** "Start simple" means a
   *complete, demonstrable* thing, with realism layered on top. This is how an
   over-ambitious project fails gracefully into something real.
3. **Wire in the validation triad from day one** — analytical limit +
   conservation law + known benchmark. This is what turns token spend into
   progress instead of spin. (§7.)
4. **Target the consequence, not the mechanism, where the mechanism is a wall.**
   (§8.)
5. **Reuse only frozen, validated modules.** For anything still in flux, a little
   duplication is safer than premature sharing. (§6.)
6. **Updating docs is part of every change.** Docs that drift are worse than
   none. (§6.)

---

## 3. The portfolio

The full catalog — every candidate simulator with its feasibility tier, the
simple→deep arc, its validation anchor, and the shared engine it draws on, plus
the chosen first three (★) — lives in **`PORTFOLIO.md`**. It is reference
material; this file carries the doctrine that governs all of it.

---

## 4. Build order for the chosen three, and why

**Steel → Microchip → Planet.** This is not only a difficulty ramp; the order
*is* part of the coupling solution (§6).

1. **Steel first.** Cleanest on every axis — terms of use, analytical validation
   (Fe-C lever rule, Avrami kinetics, Jominy hardenability all have exact/semi-
   exact answers), and the most dramatic payoff for the least scaffolding: *same
   steel, four cooling curves, four different materials.* The **diffusion/heat
   solver is built and frozen here**, validated against erfc carbon-diffusion
   profiles. The validation-triad habit is established on easy ground.

2. **Microchip second.** Reuses the frozen diffusion solver immediately (dopant
   profiles = the carbon-diffusion code). Adds the one genuinely new module
   (aerial-image Fourier optics, validated against Rayleigh resolution) and a
   second exact anchor (Deal-Grove oxidation). Closes a process→device loop
   analogous to steel's process→properties loop.

3. **Planet last** — the capstone it deserves. The diffusion solver becomes the
   EBM's heat transport. The phasing-and-validation discipline is already
   internalized before the coupler (the genuinely new systems-integration
   challenge) is attempted.

**Front-load the one new engine.** The planet needs a **fluid/PDE solver**
(shallow-water on a rotating sphere) that steel and chip do not. If de-risking is
a priority, prototype that solver early rather than at the end.

---

## 5. Shared toolkit

Build these as standalone, separately-tested libraries. The trio touches the
first three; the rest serve the wider portfolio.

| Engine | Used by (trio) | Used by (portfolio) | Validation |
|---|---|---|---|
| **Diffusion/heat (Fick/erfc)** — the spine of the trio | steel, chip, planet | landscape, groundwater, sediment, building-heat | erfc/Gaussian exact profiles |
| **Fluid/PDE (NS → shallow-water; wave eq)** | planet | traffic, seismic, glacier, acoustics | geostrophic balance, conservation, known wave speeds |
| **ODE integrators (RK4/Verlet/symplectic)** | planet, steel (cooling) | jet, star, supernova, biology, fractals | energy drift, analytic limits |
| Stiffness/FEM | — | dam, truss, earthquake building | exact statics |
| N-body gravity (Barnes-Hut) | — | galaxy | conservation; vs. direct-sum |
| Signal/detection | — | EW | ROC, radar range |
| Interpreter/parser | — | CAS, theorem prover, grammar parser | differentiate-back, proof/parse checks |
| FST/rule engine | — | sound-change, phonology, conlang | attested forms |

**Rule:** a shared engine is reused only after it is **frozen behind a passing
validation test**. The build order guarantees this for the trio — the diffusion
solver is sealed by the end of Steel, before Chip or Planet depend on it.

---

## 6. Architecture & context-management doctrine

This is the doctrine that answers the central operational risk: an LLM agent
cannot hold a growing multi-project codebase in its head, and re-derives its
mental model each session. Loose coupling and shared modules are
complexity-management tools whose benefit must be engineered for explicitly.

**The reframe:** the goal is *not* for the agent to hold the project in context.
The context window is fixed; the architecture's job is to keep the **working set
for any single task small** so the agent never needs the whole.

Three mechanisms do that work:

1. **Interface contracts are the unit of context.** Each module exposes a small,
   documented API. To work on the diffusion solver, the agent loads its internals
   plus the one-page *contracts* of what touches it — not the chip, steel, and
   planet code. Short contracts mean many fit at once.

2. **Tests substitute for context.** A frozen erfc validation test lets the agent
   modify the diffusion solver and *know from the test* whether it broke a
   contract that chip/steel/planet rely on — without ever seeing their code. The
   validation triad is therefore also the agent's **externalized memory** of
   every contract: the safety net for code not currently in context.

3. **Docs are reconstitutable context.** This `ARCHITECTURE.md`, per-module
   `README`s, and the decision log let each session rebuild the map cheaply.
   **Updating docs is part of every change** — non-negotiable.

**Consequences for how the work is structured:**

- **Build order = coupling solution.** Never do simultaneous shared development
  across live codebases. Freeze-before-reuse means you always reuse a sealed,
  tested unit, which is what makes reuse safe rather than fragile.
- **Reuse only frozen modules; rule-of-three over DRY-at-all-costs.** For code
  still in flux, deliberate duplication localizes the blast radius. Promote to a
  shared module only once the interface has stabilized across ≥3 uses.
- **The residual hard case: cross-cutting interface changes** — altering a shared
  API used in more code than fits in context. No clean automated answer. Make
  such changes rare, small, and deliberate; lean on the test suites to localize
  breakage; this is the point where the human holding the high-level map still
  matters. Plan to minimize the number of these.

**Practical hygiene (applies to every repo):** small files, clear names, a fast
single-command test runner (so the agent can navigate selectively and verify
cheaply), short contracts, and a per-session "load these files" pointer in the
docs.

---

## 7. The validation triad (methodology + memory)

Every solver and every phase must be checked three ways:

1. **Analytical limit** — an exact answer in a special case (Deal-Grove, erfc
   diffusion, 0-D EBM temperature, Lane-Emden, Feigenbaum constant…).
2. **Conservation law** — a free correctness check (energy, mass, momentum).
3. **Published/observed benchmark** — a reference tool or dataset (pycalphad,
   SUPREM, climlab; Jominy curves; observed light curves).

When neither the user nor the agent can tell whether output is correct, the loop
runs forever producing plausible nonsense. The validation scaffolding *is* the
project, and (per §6) doubles as externalized contract memory.

---

## 8. Scope discipline — consequence, not mechanism

Each project has a deep end that is a research/compute wall, not a token problem.
Name the ceiling in each plan and target the consequence instead.

- **Steel:** path-integrated kinetics (cooling curve → microstructure). *Avoid*
  spatially-resolved **phase-field** dendrite growth.
- **Chip:** 1-D process profiles + aerial-image litho + compact device model.
  *Avoid* full 2-D/3-D coupled **TCAD** on a mesh.
- **Planet:** loosely-coupled reduced modules (EBM + shallow-water + biome
  classification). *Avoid* a monolithic **GCM-grade** Earth-system model — it is
  squarely infeasible-tier (compute + long-horizon coherence). Respect
  **timescale separation** (weather in days, tectonics in millions of years):
  modules exchange boundary conditions through a **coupler** at appropriate
  cadences; never one shared time loop.

**Design for extension.** Keep structure loosely coupled and extendable, so that
in future steps the work *can* be taken into fields/features initially explicitly
avoided. The scope ceilings are deferrals out of the first implementation, not
permanent architectural foreclosures — the same module seam that keeps a project
loosely coupled is where a deferred heavy regime (phase-field, full TCAD, GCM,
CFD) could later be slotted. (See ADR `docs/decisions/0001-language-and-performance.md`
for how that seam doubles as the language boundary for a compiled module.)

---

## 9. Terms of use (settled — do not re-litigate)

- **Copyright:** a non-issue. Equations, models, and physical facts are not
  copyrightable. Implement from principles; write original code and prose; do not
  copy verbatim listings or figures.
- **Export control:** *no dimension* for steel or the planet model (published
  fundamental science). Has a dimension only for EW, jet propulsion, and advanced
  chipmaking — and in all three the **published-information / educational
  carve-out** covers a generic-parameter teaching tool. The line is *generic
  illustrative physics vs. specific real-system targeting or recipes.* The trio
  sits firmly in the carve-out. (Not legal advice; for EW/jet, get real guidance
  only if the work moves toward specific fielded-system data.)
- **Datasets:** the one recurring diligence item. Check each dataset's license
  before redistributing (climate reanalysis, topography, CALPHAD databases,
  corpora). Scientific/educational data is mostly openly licensed with
  attribution.
- **Reference codes** (pycalphad, SUPREM, climlab, MESA, REBOUND, EngineSim,
  Landlab, USBR manuals) are for **validation**, not for copying internals; mind
  their own software licenses.

---

## 10. Template for each per-project plan

The program coheres only if every individual plan has the same shape. Each
per-project plan (in `docs/plans/`) must specify:

1. **One-line vision** and the dramatic early win that anchors phase 1.
2. **Shared engines consumed**, each tagged `[to build & freeze here]` or
   `[reuse frozen]` with a pointer to its contract.
3. **Phases**, each one a complete demonstrable artifact, with the validation
   triad instantiated *per phase* (which analytical limit, which conservation
   check, which benchmark/reference).
4. **Module map & contracts** — the files/APIs, kept short enough to load
   alongside any single task.
5. **Scope ceiling** — the named tar pit this project will *not* attempt, and the
   consequence it targets instead (§8).
6. **Terms-of-use status** — usually "clean per §9"; flag any dataset that needs
   a license check.
7. **Test runner** — the single command that verifies the whole project cheaply.
8. **Visualization & UX** — how the sim is shown and explored: the universal
   figure floor, the interactive surface it needs (notebook and/or thin web app),
   and which *mechanism* the visuals are designed to reveal (§12).

---

## 11. Working set & navigation

The per-session "load these files" pointer (the §6 hygiene item). To orient in a
new session:

- **Planning a project:** this file (§1–§10) + `PORTFOLIO.md` for the catalog.
- **Working on an engine:** that engine's `CONTRACT.md` + its tests + the
  one-page contracts of consumers — never the consumers' internals.
- **Working on a project phase:** that project's plan in `docs/plans/` + the
  contracts of the engines it consumes.
- **Re-deciding something foundational:** check `docs/decisions/` first — it may
  already be settled (and if it changes, append a new ADR that supersedes the
  old, never edit history).

The immediate build target is in the active project plan's "Immediate next step"
section — currently `docs/plans/steel-production.md`. Steel **Phase 1 is complete**:
1a (diffusion/heat spine) **built & frozen** — `engines/diffusion/CONTRACT.md` is
the first sealed engine contract; 1b (Fe-C equilibrium, `fe_c.py`) and 1c
(transformation kinetics — `kinetics.py`/`pathint.py`/`cooling.py` + the banked
four-curves anchor demo) **built**. **Phase 2a built** — `projects/steel/jominy.py`,
the first *spatial* reuse of the frozen heat solver: the Jominy end-quench bar as a
transient **fin equation** (frozen conduction solver + lateral air loss composed by
operator splitting, engine untouched), validated against the lumped-capacitance
limit, bar energy conservation, and a resolution-converged thermal benchmark
(cooling-rate-vs-distance vs the published Jominy equivalence); output =
cooling-rate-vs-distance. **Phase 2b built** — the alloy **hardenability** C-curve shift
(`kinetics.hardenability_factor` / `ccurve_for_steel`): Mn/Cr/Mo slide the TTT curve right
by a Grossmann-potency multiplicative time-shift on `τ` (default identity → the 1080 demo
stays byte-identical), so deep-hardening 4140 stays martensitic far deeper into the Jominy
bar than shallow 1045 — the divergence validated through the frozen thermal field. Full
suite **147 green**. Next is Steel **Phase 2c** — the microstructure→hardness map → the
Jominy *hardness*-vs-distance artifact and the 1045/4140 hardness benchmark.

---

## 12. Visualization & UX

Education and experimentation (§1) require that every simulator can be *seen* and
*explored*. Visualization is a program-level shared concern, governed by the same
discipline as the solver toolkit. Full rationale + alternatives: ADR
`docs/decisions/0002-visualization-and-ux.md`.

1. **Separate compute from render.** Engines never import a plotting library; the
   viz layer consumes the same plain data (arrays / numeric records) the
   validation tests and any compiled reimplementation consume. The array-out
   contract (ADR 0001) serves all three.
2. **Visualization is never in the correctness path.** A figure consumes
   already-validated data; it is never evidence of validity. Test the numbers
   (§7), then draw them — the guard against "looks plausible ⇒ correct."
3. **A shared `viz/` toolkit, peer to `engines/`,** of reusable primitives
   (line/series, 2-D field/heatmap, time-animation, sweep-comparison grid,
   annotated overlay), promoted from project-local by rule-of-three (§6).
4. **Progressive enhancement** (mirrors the phasing doctrine): a universal
   *matplotlib static-figure floor* (the banked artifact — testable, zero-deploy)
   → *interactive* notebooks (ipywidgets) and/or a thin Streamlit/Gradio app for
   slider-driven what-ifs (cheap because compute is light by design) →
   *selective* Plotly / web / WebGL only where a sim's payoff demands it.
5. **Visualize the mechanism, not just the output** — design views to reveal
   *why* (a cooling path traversing the TTT C-curve), per target #1.

**The floor is universal; the interactive surface is per-need.** The toolkit
supports both notebook and web-app targets, but each project builds only the
interactive surface its pedagogy calls for — not mandatorily both.

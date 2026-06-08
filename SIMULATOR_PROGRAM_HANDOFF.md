# Educational Simulator Program — Handoff

## 0. What this document is

This is the **program-level plan** for a suite of educational, interactive,
experimentation-focused physics/engineering/science simulators. It is **not** a
plan for any single simulator — each of those gets its own plan (Section 10
defines the template they must follow).

The job of this document is to carry the cross-cutting decisions that an
individual project plan cannot re-derive on its own: the shared toolkit, the
build order, the architecture doctrine that keeps the work coherent under a
limited context window, the validation methodology, and the scope ceilings.

**How to use it in a planning step:** treat Sections 2–9 as fixed constraints
("invariants") that every per-project plan inherits. When planning a specific
simulator, generate the detail using the Section 10 template, and check the
result against these invariants rather than re-litigating them.

---

## 1. Targets (unchanged across all projects)

- **Education** — teach real mechanisms, not black boxes.
- **Interactivity** — expose the parameters that produce dramatic, counter-
  intuitive transitions; those are simultaneously the best teaching moments
  and the cheapest verification.
- **Experimentation** — let the user run sweeps and "what-ifs."
- **Aim far/deep in perspective** — the deep end is a direction to grow toward,
  not a gate to clear. Every phase must bank a working, demonstrable artifact.

---

## 2. Program invariants (every project inherits these)

1. **Build the toolkit once, reuse it everywhere.** A small set of solver
   engines underlies the whole portfolio. Build the solver-heavy projects
   first; later ones become recomposition. (Section 5.)
2. **Phase so each stage banks a working artifact.** "Start simple" means a
   *complete, demonstrable* thing, with realism layered on top. This is how an
   over-ambitious project fails gracefully into something real.
3. **Wire in the validation triad from day one** — analytical limit +
   conservation law + known benchmark. This is what turns token spend into
   progress instead of spin. (Section 7.)
4. **Target the consequence, not the mechanism, where the mechanism is a wall.**
   (Section 8.)
5. **Reuse only frozen, validated modules.** For anything still in flux, a
   little duplication is safer than premature sharing. (Section 6.)
6. **Updating docs is part of every change.** Docs that drift are worse than
   none. (Section 6.)

---

## 3. The portfolio

Chosen first three are marked ★. Feasibility tiers: VF = very feasible,
F = feasible, F→B = feasible core, borderline deep end. "Anchor" = the primary
validation hook. "Engine" = the shared solver it draws on (Section 5).

| Project | Tier | Simple → deep | Anchor | Engine |
|---|---|---|---|---|
| **★ Steel production** | VF | Fe-C + lever rule, Avrami kinetics → TTT/CCT, Jominy, structure→properties → CALPHAD; phase-field (avoid) | erfc diffusion, Jominy curves; pycalphad | Diffusion/heat |
| **★ Microchip fabrication** | VF | Deal-Grove oxidation, erfc diffusion, aerial image → resist kinetics, OPC, process→device → 2D/3D TCAD (avoid) | Deal-Grove & erfc exact; SUPREM | Diffusion/heat |
| **★ Earth-system / planet** | F (capstone) | 0-D → 1-D EBM (Snowball) → shallow-water atmos/ocean → coupler → biomes → tectonics → GCM (infeasible) | 0-D analytic temp, energy conservation; climlab | Diffusion/heat + Fluid/PDE |
| EW simulator | F | Propagation + radar eq + detection → jamming/EP, DF, scenario (generic params only) | Radar range, ROC | Signal/detection |
| Jet engine | VF (cycle) | Ideal Brayton → real efficiencies, turbofan, off-design → CFD (avoid) | Energy conservation; EngineSim | ODE + thermo |
| Galaxy / N-body | VF | Direct-sum → Barnes-Hut, collisions → + gas/SPH | Energy/momentum conservation; REBOUND | N-body gravity |
| Star structure/evolution | F | Structure ODEs (Lane-Emden) → evolution → HR tracks | Lane-Emden exact; MESA | ODE |
| Supernova | F (consequences only) | Ni-56 light curve, ejecta → mechanism (infeasible) | Observed light curves | ODE |
| Biology suite | F | Pop genetics, Gray-Scott, Gillespie+repressilator, Hodgkin-Huxley | HW equilibrium, mean-field limit | ODE/PDE |
| Landscape evolution | VF | 1-D hillslope → 2-D fluvial nets → uplift vs. erosion | Steady-state slope; Landlab | Diffusion/heat |
| Groundwater flow | VF | Darcy 1-D → well drawdown → contaminant transport | Theis analytic | Diffusion/heat |
| Sediment basin | F | Deposition + compaction → burial heat history | Layered analytic | Diffusion/heat |
| Seismic waves | F | 1-D wave → layered media → full-waveform | Travel-time curves | Fluid/PDE (wave) |
| Glacier/ice-sheet | F | Shallow-ice 1-D → 2-D flow | Glen's-law profiles | Fluid/PDE; feeds planet |
| Truss/frame analyzer | VF | 2-D truss (hand-calc) → 3-D frame → buckling/modal | Exact statics | Stiffness/FEM |
| Earthquake building | VF | Shear-building modal → recorded ground motion | Analytic natural freqs | FEM + ODE |
| Building heat/comfort | VF | Wall conduction → solar gain + mass | Steady-state analytic | Diffusion/heat |
| Traffic flow | VF | LWR PDE → shocks/jams; car-following | Conservation law | Fluid/PDE |
| Pipe networks | VF | Hardy Cross loop (hand-calc) → larger nets | Hand-solved loops | Circuit-solver math |
| Room acoustics | F | Cavity modes (analytic) → ray-tracing | Modal freqs | Fluid/PDE (wave) |
| Arch/gravity dam | VF | 2-D statics → arch cylinder theory → trial-load → 3-D FEM | Hand-calc stability; USBR | Stiffness/FEM |
| Sailing ship | F | Force-balance VPP → polar → 6-DOF + stability → seakeeping; CFD (avoid) | Published polars; GZ analytics | Fluid (lift) + rigid-body |
| Computer algebra | F→B | Symbolic diff → simplify → integrate | Differentiate-back | Interpreter/parser |
| Theorem prover | F→B | Propositional → FOL → type checker | Proof checks | Interpreter/parser |
| Numerical/bignum lib | VF | Bignums → root-find/quadrature → linalg | Machine-precision | Numeric core |
| Dynamical systems/fractals | VF | Logistic map → attractors → Mandelbrot | Feigenbaum constant | ODE + viz |
| Cellular automata | VF | Life → Rule 110 → Turing-completeness | Known patterns | Grid |
| Sound-change sim | F | Ordered rules → daughter langs → phylo trees | Attested cognates | FST/rule engine |
| Phonology FST | F | Rewrite rules → surface forms | Documented alternations | FST |
| Formal grammar parser | VF | CYK/Earley → Chomsky hierarchy | Known grammars | Interpreter/parser |
| n-gram LM | VF | Counts → smoothing → entropy/perplexity | Zipf/entropy | Stats |
| Classical MT/spell-check | VF | Edit-distance (exact) → noisy channel | DP exact | DP |
| Conlang toolkit | F | Phonotactics → etymology engine | (creative) | FST + sound-change |

---

## 4. Build order for the chosen three, and why

**Steel → Microchip → Planet.** This is not only a difficulty ramp; the order
*is* part of the coupling solution (Section 6).

1. **Steel first.** Cleanest on every axis — terms of use, analytical
   validation (Fe-C lever rule, Avrami kinetics, Jominy hardenability all have
   exact/semi-exact answers), and the most dramatic payoff for the least
   scaffolding: *same steel, four cooling curves, four different materials.*
   The **diffusion/heat solver is built and frozen here**, validated against
   erfc carbon-diffusion profiles. The validation-triad habit is established on
   easy ground.

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
(shallow-water on a rotating sphere) that steel and chip do not. If de-risking
is a priority, prototype that solver early rather than at the end.

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
complexity-management tools whose benefit must be engineered for explicitly here.

**The reframe:** the goal is *not* for the agent to hold the project in context.
The context window is fixed; the architecture's job is to keep the **working set
for any single task small** so the agent never needs the whole.

Three mechanisms do that work:

1. **Interface contracts are the unit of context.** Each module exposes a
   small, documented API. To work on the diffusion solver, the agent loads its
   internals plus the one-page *contracts* of what touches it — not the chip,
   steel, and planet code. Short contracts mean many fit at once.

2. **Tests substitute for context.** A frozen erfc validation test lets the
   agent modify the diffusion solver and *know from the test* whether it broke a
   contract that chip/steel/planet rely on — without ever seeing their code. The
   validation triad is therefore also the agent's **externalized memory** of
   every contract: the safety net for code not currently in context.

3. **Docs are reconstitutable context.** An `ARCHITECTURE.md`, per-module
   `README`s, and a decision log let each session rebuild the map cheaply.
   **Updating docs is part of every change** — non-negotiable.

**Consequences for how the work is structured:**

- **Build order = coupling solution.** Never do simultaneous shared development
  across live codebases. Freeze-before-reuse means you always reuse a sealed,
  tested unit, which is what makes reuse safe rather than fragile.
- **Reuse only frozen modules; rule-of-three over DRY-at-all-costs.** For code
  still in flux, deliberate duplication localizes the blast radius. Promote to a
  shared module only once the interface has stabilized across ≥3 uses.
- **The residual hard case: cross-cutting interface changes** — altering a
  shared API used in more code than fits in context. No clean automated answer.
  Make such changes rare, small, and deliberate; lean on the test suites to
  localize breakage; this is the point where the human holding the high-level
  map still matters. Plan to minimize the number of these.

**Practical hygiene (applies to every repo):** small files, clear names, a fast
single-command test runner (so the agent can navigate selectively and verify
cheaply), short contracts, and a per-session "load these files" pointer in the
docs.

---

## 7. The validation triad (methodology + memory)

Every solver and every phase must be checked three ways:

1. **Analytical limit** — an exact answer in a special case (Deal-Grove,
   erfc diffusion, 0-D EBM temperature, Lane-Emden, Feigenbaum constant…).
2. **Conservation law** — a free correctness check (energy, mass, momentum).
3. **Published/observed benchmark** — a reference tool or dataset
   (pycalphad, SUPREM, climlab; Jominy curves; observed light curves).

When neither the user nor the agent can tell whether output is correct, the loop
runs forever producing plausible nonsense. The validation scaffolding *is* the
project, and (per Section 6) doubles as externalized contract memory.

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
  cadences; never one shared time loop. Design should be kept loosely coupled and extendable, so that in future steps could be taken into fields/features initially explicitly avoided.

---

## 9. Terms of use (settled — do not re-litigate)

- **Copyright:** a non-issue. Equations, models, and physical facts are not
  copyrightable. Implement from principles; write original code and prose; do
  not copy verbatim listings or figures.
- **Export control:** *no dimension* for steel or the planet model (published
  fundamental science). Has a dimension only for EW, jet propulsion, and
  advanced chipmaking — and in all three the **published-information /
  educational carve-out** covers a generic-parameter teaching tool. The line is
  *generic illustrative physics vs. specific real-system targeting or recipes.*
  The trio sits firmly in the carve-out. (Not legal advice; for EW/jet, get real
  guidance only if the work moves toward specific fielded-system data.)
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
per-project plan (the ones to be produced separately, e.g. via the planning
workflow) must specify:

1. **One-line vision** and the dramatic early win that anchors phase 1.
2. **Shared engines consumed**, each tagged `[to build & freeze here]` or
   `[reuse frozen]` with a pointer to its contract.
3. **Phases**, each one a complete demonstrable artifact, with the validation
   triad instantiated *per phase* (which analytical limit, which conservation
   check, which benchmark/reference).
4. **Module map & contracts** — the files/APIs, kept short enough to load
   alongside any single task.
5. **Scope ceiling** — the named tar pit this project will *not* attempt, and
   the consequence it targets instead (Section 8).
6. **Terms-of-use status** — usually "clean per program handoff Section 9"; flag
   any dataset that needs a license check.
7. **Test runner** — the single command that verifies the whole project
   cheaply.

---

## 11. Immediate next step

Produce the **Steel production plan** first, using the Section 10 template. Its
phase 1 builds the **diffusion/heat solver** as the reusable, erfc-validated
foundation and the Fe-C + Avrami "cooling curve in, microstructure out" core.
That single deliverable seeds the diffusion spine the other two projects inherit.

If de-risking the capstone is preferred instead, the alternative first
deliverable is a standalone **shallow-water fluid-solver plan** (the one engine
the trio doesn't otherwise build until late).

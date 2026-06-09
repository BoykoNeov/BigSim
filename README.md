# BigSim — Educational Simulator Program

[![full-gate](https://github.com/BoykoNeov/BigSim/actions/workflows/full-gate.yml/badge.svg)](https://github.com/BoykoNeov/BigSim/actions/workflows/full-gate.yml)

A suite of educational, interactive, experimentation-focused
physics / engineering / science simulators, built on a small set of shared,
separately-validated solver engines.

The aim is to **teach real mechanisms, not black boxes**: expose the parameters
that drive dramatic, counter-intuitive transitions, let users run sweeps and
"what-ifs," and grow each simulator from a complete simple artifact toward a
deep end — without chasing a research/compute wall.

## Quickstart

No build step is needed to *import* the code (the test config puts the repo root on
`sys.path`), but the dependencies still are. Install the core stack, then add the optional
extra for whichever surface you want:

```powershell
pip install -e .                  # core: numpy + scipy (compute + the headless test suite)
pip install -e .[viz]             # + matplotlib — required to render any demo figure
pip install -e .[viz,notebook]    # + ipywidgets/jupyter — the Steel teaching notebook
pip install -e .[viz,app]         # + streamlit — the Steel what-if web app
pip install -e .[calphad]         # + pycalphad — Steel's optional CALPHAD backend
```

**Run a simulator** — each demo prints a result and saves a figure to `docs/figures/`
(needs `[viz]`). A representative few (each project's README lists them all):

```powershell
pip install -e .[viz]
python -m projects.steel.demo_four_curves   # one steel, four quenches: pearlite → martensite
python -m projects.steel.demo_jominy        # Jominy hardness vs depth, 1045 vs 4140
python -m projects.chip.demo_oxidation      # Deal–Grove oxide growth, wet vs dry
python -m projects.chip.demo_device         # the process → MOSFET threshold-voltage flow
```

**Explore interactively** — slider-driven teaching notebooks for both projects; a shareable web
app for Steel (the flagship):

```powershell
pip install -e .[viz,notebook]
jupyter lab projects/steel/steel.ipynb      # sliders: carbon, alloy composition (C/Mn/Cr/Mo), quench, section, temper → microstructure
jupyter lab projects/chip/chip.ipynb        # per-phase sliders: diffusion, oxide, litho → V_t

pip install -e .[viz,app]
streamlit run projects/steel/app.py         # Steel only — the same what-ifs as a shareable web app
```

**Run the tests** (the tiered gate — [ADR 0003](docs/decisions/0003-test-execution-policy.md)):

```powershell
./run_tests.ps1 -m "not slow"     # routine fast lane — 338 tests, ~11 s
./run_tests.ps1                   # full suite — 347 tests (exceptional: engine edit, release, CI)
python -m tools.gate steel        # just one project + the modules it uses
```

> The CALPHAD backend (Steel Phase 4) needs pycalphad and, on Python 3.14, a documented
> two-step install — see [`projects/steel/README.md`](projects/steel/README.md). The committed
> test suite stays pycalphad-free, so none of the above requires it.

## How it's organized

- **[`ARCHITECTURE.md`](ARCHITECTURE.md)** — the program doctrine: invariants,
  build order, the shared solver toolkit, the validation methodology, scope
  discipline, terms of use, and the template every project plan follows.
  **Start here.**
- **[`PORTFOLIO.md`](PORTFOLIO.md)** — the full catalog of candidate simulators
  (feasibility tier, simple→deep arc, validation anchor, shared engine).
- **[`docs/plans/`](docs/plans/)** — per-project plans:
  [Steel production](docs/plans/steel-production.md) (#1) and
  [Microchip fabrication](docs/plans/microchip-fabrication.md) (#2).
- **[`docs/decisions/`](docs/decisions/)** — architecture decision records (ADRs).

## The core idea

A small toolkit of solver engines (diffusion/heat, fluid/PDE, ODE integrators,
FEM, N-body, …) underlies the whole portfolio. Solver-heavy projects are built
first; later ones become recomposition. Every engine is **frozen behind a
passing validation suite before anything reuses it**, and every phase is checked
three ways — an analytical limit, a conservation law, and a published benchmark.

## Build order (first three)

**Steel → Microchip → Earth-system / planet.** The diffusion/heat solver built
and frozen in Steel is the spine the other two inherit.

## Status

**The shared spine is frozen, the first two projects are complete, and the Earth-system capstone is under way (Phases 1–2 built).**

- **Engine — diffusion/heat (the spine):** built and **frozen** behind
  [`engines/diffusion/CONTRACT.md`](engines/diffusion/CONTRACT.md) — the erfc-validated,
  conservative 1-D parabolic solver (heat *and* mass mode) the whole trio inherits.
- **Steel — complete** (Phases 1–4 + the experimentation surface): Fe-C equilibrium →
  transformation kinetics → Jominy hardenability → structure→properties → tempering →
  carburizing → an optional CALPHAD backend, plus a headless sweep harness, an interactive
  teaching notebook, and a Streamlit what-if app.
  See [`projects/steel/README.md`](projects/steel/README.md).
- **Microchip — complete** (Phases 1–4 + a teaching notebook): dopant diffusion & the pn junction
  → Deal–Grove oxidation → aerial-image lithography → compact MOS threshold voltage, plus an
  interactive `chip.ipynb` (per-phase sliders → V_t); the first consumer of the frozen spine
  (it builds no new engine). See [`projects/chip/README.md`](projects/chip/README.md).
- **Planet (the Earth-system capstone) — Phases 1–2 built.** *Phase 1* (the latitudinal
  energy-balance model & the Snowball bifurcation): the diffusion spine reuses a **third** time as a
  sphere's latitudinal heat transport, with the radiation **Strang-split** around it (the Jominy
  idiom); one knob (the solar constant) traces a **Snowball hysteresis** — present-day Earth (ice line
  ~73°) freezes over at ~8 % dimming and re-melts only ~580 W/m² brighter. *Phase 2* (the payoff,
  banked early): a diagnostic precipitation field + an original Whittaker `(T,P)→biome` classifier
  map the climate to **bands of life** (equator→pole: rain forest → savanna → desert/grassland →
  temperate forest → boreal → tundra) that **migrate poleward as a CO₂ knob warms the planet**.
  Phases 3–4 (the new shallow-water engine, the coupler) are pending.
  See [`projects/planet/README.md`](projects/planet/README.md).

Eleven banked figures live in [`docs/figures/`](docs/figures/). The suite is **413 tests**, all
green (plus 1 live-climlab cross-check skipped unless the `[climate]` extra is installed): **398 run
in the ~13 s fast lane** (`./run_tests.ps1 -m "not slow"`), with the rest `slow`
live-solver/kernel tests reserved for the full gate (the tiered policy,
[ADR 0003](docs/decisions/0003-test-execution-policy.md)). See **Quickstart** above to run them.

## Implementation

Python + NumPy/SciPy by default, with a documented path to compiled kernels
(Numba / Cython / a Rust/C++/Julia module behind a frozen contract) where a
profiled hotspot justifies it. See
[ADR 0001](docs/decisions/0001-language-and-performance.md).

**Visualization** is a separate, progressively-enhanced layer — a universal
matplotlib figure floor, interactive notebooks and thin Streamlit apps for
what-ifs, and selective web/3-D where it pays off — that consumes headless
engine data and is never part of the correctness story. See
[ADR 0002](docs/decisions/0002-visualization-and-ux.md).

# BigSim — Educational Simulator Program

A suite of educational, interactive, experimentation-focused
physics / engineering / science simulators, built on a small set of shared,
separately-validated solver engines.

The aim is to **teach real mechanisms, not black boxes**: expose the parameters
that drive dramatic, counter-intuitive transitions, let users run sweeps and
"what-ifs," and grow each simulator from a complete simple artifact toward a
deep end — without chasing a research/compute wall.

## How it's organized

- **[`ARCHITECTURE.md`](ARCHITECTURE.md)** — the program doctrine: invariants,
  build order, the shared solver toolkit, the validation methodology, scope
  discipline, terms of use, and the template every project plan follows.
  **Start here.**
- **[`PORTFOLIO.md`](PORTFOLIO.md)** — the full catalog of candidate simulators
  (feasibility tier, simple→deep arc, validation anchor, shared engine).
- **[`docs/plans/`](docs/plans/)** — per-project plans. First up:
  [Steel production](docs/plans/steel-production.md).
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

Building — **Steel Phase 1 is complete** (the foundation) and **Phase 2 is underway**. The doctrine, catalog,
first project plan, and ADRs are in place; the **first engine is built and frozen**
(the erfc-validated 1-D diffusion/heat solver, `engines/diffusion/`, Steel Phase 1a
— the spine the whole trio inherits, sealed behind its
[`CONTRACT.md`](engines/diffusion/CONTRACT.md)); and steel's **Fe-C equilibrium**
(1b) and **transformation kinetics** (1c — Avrami/TTT, Scheil additivity/CCT,
Koistinen–Marburger + Andrews M_s) are built on top. The banked Phase-1 artifact:
*one steel (AISI 1080), four cooling rates, soft pearlite → file-hard martensite*
([`docs/figures/steel-four-curves.png`](docs/figures/steel-four-curves.png)). Full
suite **147 green**. **Steel Phase 2 is underway**: the Jominy end-quench *spatial
thermal* model (2a — first reuse of the heat solver, the transient fin equation) and
the *alloy hardenability* C-curve shift (2b — Mn/Cr/Mo slide the TTT curve right, so
deep-hardening 4140 stays martensitic far deeper into the bar than shallow 1045) are
built; next is 2c (microstructure→hardness → the Jominy hardness curve + 1045/4140
benchmark). Run the suite with `./run_tests.ps1`.

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

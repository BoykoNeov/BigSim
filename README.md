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

Building. The doctrine, catalog, first project plan (Steel), and the ADRs are in
place, and the **first engine is built and frozen**: the erfc-validated 1-D
diffusion/heat solver (`engines/diffusion/`, Steel Phase 1a) — the spine the
whole trio inherits, sealed behind its validation suite
([`CONTRACT.md`](engines/diffusion/CONTRACT.md)). Next: Steel Phase 1b (Fe-C
equilibrium). Run the suite with `./run_tests.ps1`.

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

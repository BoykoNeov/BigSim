# Educational Simulator Program — Portfolio Catalog

The full candidate catalog for the program. Doctrine that governs all of these
(invariants, build order, shared toolkit, validation, scope discipline, terms of
use, per-project plan template) lives in **`ARCHITECTURE.md`**.

Chosen first three are marked ★. Feasibility tiers: **VF** = very feasible,
**F** = feasible, **F→B** = feasible core, borderline deep end. "Anchor" = the
primary validation hook. "Engine" = the shared solver it draws on
(`ARCHITECTURE.md` §5).

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

# Python library options

Review date: 2026-10-16  
Status: provisional comparison; no final stack selected or benchmarked

The manuscript specifies daily stochastic state updates followed by constrained optimisation. A simulation engine, an optimisation modelling layer, and a solver serve different roles. The choice is therefore a small stack, not one package expected to do everything.

The fit assessments below are engineering inferences from the supplied model and the primary documentation. They are not performance measurements.

## Simulation time management

| Option | Relevant capability | Fit for this manuscript | Limitation / question |
| --- | --- | --- | --- |
| NumPy/SciPy plus an explicit Python daily loop | Sampling, array operations, statistical distributions and analysis | Closest provisional fit to the specified daily sequence; easy to inspect and replay | State transitions, output, and checkpoints are project code; does not provide a transfer/queue event scheduler |
| SimPy | Process-based discrete-event simulation, events and shared resources | Useful if individual transfers, completion times, queue contention, or within-day interactions become part of the accepted model | Those event semantics are not fully specified by the manuscript; adding them can change the experiment |
| salabim | Discrete-event simulation, queues, resources and monitoring | Alternative if process/resource modelling and monitoring are desired | Verify headless mode and dependencies; animation is not a research requirement |

Primary references:
- [NumPy random generation](https://numpy.org/doc/stable/reference/random/index.html)
- [NumPy parallel random streams](https://numpy.org/doc/stable/reference/random/parallel.html)
- [SciPy statistics](https://docs.scipy.org/doc/scipy/reference/stats.html)
- [SimPy overview](https://simpy.readthedocs.io/en/latest/)
- [salabim introduction](https://www.salabim.org/manual/Introduction.html)

The SimPy documentation itself cautions that the engine can be unnecessary for simple fixed-step models. For the current daily specification, first justify the need for within-day events before adopting a discrete-event engine.

## Optimisation modelling and numerical solving

The exact model includes binary decisions, continuous flows, and nonlinear convex congestion. "Supports optimisation" is insufficient evidence that a backend handles this combination.

| Option | Role and potential route | Required evidence / caveat |
| --- | --- | --- |
| Pyomo + compatible nonlinear mixed-integer solver | Algebraic formulation with explicit constraint families; candidate route for a faithful extensible model | Pyomo does not install a solver automatically. Verify the exact expression representation, solver interface, integer/nonlinear support, status reporting, and licensing |
| CVXPY + compatible mixed-integer conic solver | Convex/conic formulation using a verified equivalent congestion epigraph | Do not assume the default continuous solvers support integer variables. Check modelling rules and the concrete mixed-integer cone support |
| PySCIPOpt + SCIP | Direct Python modelling of a solver supporting mixed-integer nonlinear problems | Candidate for an open-source exact-model path; verify objective/epigraph construction, installation, and numerical behaviour on a tiny instance |
| Pyomo or another suitable MILP layer + HiGHS | Explicit piecewise-linear approximation of congestion | This is an approximation; bound error, record breakpoints, and evaluate the original objective on returned solutions |
| OR-Tools CP-SAT | Integer constraint programming | Not a direct representation of the manuscript's continuous-flow nonlinear model; discretisation and reformulation would need explicit justification |

For positive fixed effective capacity U:

`F/(U-F) = U/(U-F) - 1`.

This identity suggests an inverse-positive/conic route; it is not proof that an arbitrary library/solver pairing accepts the model. Failed links with U=0 need a separate zero-flow rule rather than evaluation of this expression.

Primary references:
- [Pyomo solver installation and available interfaces](https://pyomo.readthedocs.io/en/stable/getting_started/solvers.html)
- [CVXPY solver feature matrix](https://www.cvxpy.org/tutorial/solvers/index.html)
- [CVXPY mixed-integer constraints](https://www.cvxpy.org/tutorial/constraints/index.html)
- [SCIP project](https://www.scipopt.org/)
- [PySCIPOpt documentation](https://pyscipopt.readthedocs.io/en/latest/)
- [HiGHS project](https://highs.dev/)
- [OR-Tools CP-SAT constraints and status semantics](https://developers.google.com/optimization/cp/cp_solver)

An exact route must preserve all original constraint families. A shortest-path routine, continuous relaxation, or MILP with omitted congestion is not an equivalent solver for this model.

## Supporting components

| Component | Candidate | Scope |
| --- | --- | --- |
| Directed graph representation | [NetworkX](https://networkx.org/documentation/stable/) | Topology, reachability, stage/parent mapping validation; not replica-placement optimisation |
| Distribution conversion / statistics | NumPy and SciPy | Poisson/Beta/LogNormal/Weibull sampling and independent-replication analysis |
| Local independent replication execution | Python multiprocessing or [Joblib](https://joblib.readthedocs.io/en/stable/) | Bounded local parallelism; project-owned seed mapping/checkpoints |
| Global sensitivity extensions | [SALib](https://salib.readthedocs.io/en/latest/) | Later study; select methods consistent with dependent/constrained parameters |
| Distributed execution | Optional Dask, to evaluate later | Add only when pilot measurements establish a need |
| Result tables / storage | Standard CSV initially; pandas/PyArrow if justified | Keep mandatory dependencies and large trace volumes proportionate |
| Validation / testing | Typed configuration and pytest, concrete tools pending | Scientific invariants, integration, replay, and failure handling |

Distribution-interface references:
- [SciPy LogNormal parameterisation](https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.lognorm.html)
- [SciPy Weibull shape/scale interface](https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.weibull_min.html)
- [NumPy LogNormal mean/sigma interface](https://numpy.org/doc/stable/reference/random/generated/numpy.random.Generator.lognormal.html)

## Coherent stack options to present

| Option | Simulation layer | Optimisation layer | Appropriate when |
| --- | --- | --- | --- |
| A — Daily reference | Explicit daily loop + NumPy/SciPy | Pyomo with a verified nonlinear mixed-integer backend, or direct PySCIPOpt | Closely following the paper and prioritising transparent daily evolution |
| B — Daily conic model | Explicit daily loop + NumPy/SciPy | CVXPY with a verified mixed-integer conic backend | The congestion reformulation is accepted and conic tooling proves convenient |
| C — Event extension | SimPy, or salabim after comparison | One of the verified optimisation routes above | Within-day queues, transfer completion, or contention become explicit requirements |
| D — Scalable approximation | Daily loop + NumPy/SciPy | Selected piecewise-linear MILP + HiGHS | Pilot measurements motivate a quantified approximation accepted by the user |

Provisional recommendation: begin the selection discussion with A and B. Consider C if finer temporal behaviour is required. Treat D as a labelled alternative rather than silently replacing the exact model.

## Accepted selection and evidence

Selected on 2026-10-16: **Option A — Daily reference**, implemented as an explicit daily NumPy/SciPy loop with direct PySCIPOpt 6.1.0 modelling and the bundled SCIP backend. The model remains exact with respect to the congestion expression; no MILP approximation is selected.

Tested environment: CPython 3.12, macOS arm64. The `srcnet-mc probe-scip` model contains a binary activation, a continuous flow and the exact nonlinear congestion epigraph. It returned `optimal`, activation `1`, flow `2.0`, congestion `0.249999999875` (analytical value `0.25`) on 2026-10-16.

This is compatibility evidence only. It does not demonstrate complete constraint support, full-model numerical behaviour, runtime, or campaign feasibility. Pyomo/HiGHS remains the documented piecewise-linear fallback only; use requires a separately accepted approximation decision.

## Selection record to complete in Codex

- Chosen option and date: Option A, 2026-10-16.
- Simulation engine: explicit daily loop (not a discrete-event engine).
- Optimisation modelling library: PySCIPOpt 6.1.0.
- Numerical solver and Python interface: SCIP bundled with PySCIPOpt 6.1.0.
- Exact formulation or approximation: exact nonlinear congestion probe; production formulation pending B2.
- Dependency/version/license/architecture checks: CPython 3.12/macOS arm64; locked dependencies; digest-pinned container definition.
- Offline and daily timing interpretations: accepted contracts in `docs/SCENARIO_CONTRACTS.md`.
- Tiny-probe acceptance criteria and result: passed; see above.
- Decision IDs: ADR-013 to ADR-017.
- Reasons alternatives were rejected: SimPy/salabim add unspecified within-day semantics; Pyomo/HiGHS is approximate; CVXPY route was not selected.


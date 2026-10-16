# Decisions register

Created: 2026-10-16

Status vocabulary:
- **Accepted requirement**: directly required by the user or specified by the manuscript within its declared scope.
- **Proposed**: a design recommendation awaiting verification or selection.
- **Open**: a material unresolved choice.
- **Superseded**: retained history pointing to a replacement decision.

The selected stack and semantic contracts below were chosen by the user on 2026-10-16. Only the narrow SCIP compatibility probe described in ADR-013 has run; no SRCNet simulation or campaign has run.

## ADR-001 — Sequence and library-selection checkpoint

Status: Accepted requirement  
Source: user request; CODEX_PROMPT.md, Sections 1-2

Design first, compare suitable existing Python libraries, and let the user choose the final stack before backend implementation and Monte Carlo execution. After selection proceed incrementally through implementation and measured execution.

Consequence: initial documents may be prepared now; production dependency adoption and backend implementation remain pending. Ordinary local implementation after selection does not require repeated permission.

Validation: this starter package contains documents and the original manuscript, not a simulator.

## ADR-002 — Scientific provenance and source preservation

Status: Accepted project rule  
Source: cas-dc-template.tex; full mathematical model, worked example, simulation framework

Keep the source manuscript unchanged and trace implementation decisions to its active definitions and equations. The starter snapshot is docs/model/cas-dc-template.tex.

SHA-256: `230b5df7bab09097089d44c26da6685586cafa5913a62d444e59dfb8c4da7898`

Use the detailed formulation rather than treating the abbreviated "Problem Formalization" as complete. A changed source hash triggers an impact review.

Consequence: ambiguities become recorded decisions; implementation must not silently rewrite the model.

## ADR-003 — Python implementation and reproducible environment

Status: Accepted requirement; specific tooling open  
Source: user request

Scientific implementation and orchestration use Python. External solvers and compiled packages accessed from Python are permitted with declared requirements. Supply a locked native environment and a container workflow after stack selection.

Open choices: CPython version, dependency manager/lock format, base image, solver version/interface, and supported architectures. Select compatible versions from a real tested environment.

Validation: pending B1. No reproducible execution environment exists yet.

## ADR-004 — Discrete daily horizon and replication target

Status: Accepted manuscript baseline  
Source: "Simulation Horizon"; "Simulation Scenarios"

Use daily periods, baseline H=90 and N=1000 independent Monte Carlo replications per defined scenario. Keep H/N configurable. Small smoke/pilot profiles are explicitly labelled.

Consequence: a daily time loop is a relevant engine option; discrete-event simulation must have a stated purpose. No steady-state warm-up is implied.

Open: initial state, within-period transfer completion, and how deterministic quarterly inputs map into daily experiments.

## ADR-005 — Simulation and optimisation stack

Status: Open  
Source: user requirement; LIBRARY_OPTIONS.md

Options include NumPy/SciPy daily orchestration, SimPy, or salabim; independently compare Pyomo, CVXPY, or direct PySCIPOpt with a compatible solver.

Provisional recommendation: a daily loop with NumPy/SciPy is closest to the written time-step procedure. This is an inference from the manuscript, not an accepted selection.

Decision: pending user selection and actual backend compatibility evidence. No dependency is adopted by this entry.

## ADR-006 — Nonlinear congestion fidelity

Status: Accepted fidelity requirement; formulation/backend open  
Source: "Cost Components and Objective Function"; "Capacity, Availability, and Stability of the Links"

Retain Psi(F)=F/(U-F) with integer decisions, or clearly label a selected approximation. A positive fixed U permits the algebraically equivalent U/(U-F)-1 representation. Verify conic/nonlinear support using a real tiny model.

Alternative: explicitly selected piecewise-linear MILP approximation with documented error on the stability-bounded domain and recomputation of the original objective.

Consequences: generic MILP or continuous solvers alone cannot be assumed to solve the exact mixed-integer convex formulation. Failed links require zero-flow handling without undefined division.

Evidence: algebraic identity only; no solver integration tested.

## ADR-007 — Units and timing

Status: Open  
Source: "Demands, Compatibilities, and Resilience Rules"; "Nodal and Link Parameters"; "Simulation Horizon"

The worked example mixes PB per quarterly window, Gbps, milliseconds, and normalised per-PB quantities. Daily simulation requires an explicit unit convention and throughput conversion.

Options: consistent per-period volumes with daily capacities, or a rate-based formulation with storage-volume accounting kept separate. Both require coefficient/exposure-budget consistency.

Open: whether datasets complete within one period or need an explicit multi-period progress model; interpretation of the flow-weighted temporal objective.

Do not scale persistent storage by period length or reuse quarterly processing allowances daily. Validation: unit tests and worked conversions pending.

## ADR-008 — Static and adaptive policy semantics

Status: Open  
Source: "Offline Policy"; "Online Policy"; "Dataset Arrival Process"

A fixed per-dataset solution at t=0 does not define actions for previously unknown arrivals. Present a non-clairvoyant template/static-policy interpretation or a fixed known-demand comparison. A perfect-information baseline must have a separate label.

Open: what offline decisions remain fixed, how unseen demands are mapped, how infeasible fixed actions are scored, and what online re-optimisation may change.

Existing copies remain in place by default under the deterministic model's no-migration scope. Any migration extension needs explicit traffic, costs, and occupancy accounting.

Validation: pending design choice and policy-isolation tests.

## ADR-009 — Occupancy, retention, and direct reception

Status: Accepted dynamic balance; boundary/mapping choices open  
Source: "Dynamic Storage Occupancy"; "Dataset Retention Model"; "Direct Reception at Non-T0 Sites"

Preserve O_next=O+A-D and assign one retention lifetime per dataset. Define daily boundary rules and the relationship between dynamic dataset/storage indicators and deterministic replica assignments.

Open: how free storage at child nodes determines eligibility for direct reception at a non-T0 SE; expiry rounding; initial occupancy content/age; transaction rules for failed placement.

Consequence: previously stored replicas cannot be added again during re-optimisation. Persistent storage nodes and transfer-service SEs must remain distinct.

Validation: pending mass-balance, expiry, parent/child, and rollback tests.

## ADR-010 — Exogenous traces and paired comparisons

Status: Proposed  
Source: independent Monte Carlo replications; comparison of offline/online policies

Use stable per-replication/per-component NumPy seed streams. Share exogenous traces between policies within a replication, and isolate policy state and permitted observations. Preserve independence across replications.

Consequences: policy differences are evaluated with paired replication-level statistics; worker scheduling must not affect random input. Full trace availability to the harness does not imply future information available to policies.

Validation: replay, worker-count, state-isolation, and no-future-access tests pending.

## ADR-011 — Objective accounting and infeasibility

Status: Open  
Source: objective definitions; "Performance Indicators"

Resolve one-off versus recurring CAPEX, horizon aggregation, operational-feasibility measurement on empty days, undefined ratios, and successful-storage definitions.

Decide how the simulator handles an infeasible batch. Admission, rejection, retry, and backlog rules are additional operational semantics, not implicit features of the original all-demands model.

Requirements: preserve original objective components and weights; distinguish errors/timeouts from proven infeasibility; accompany cost comparisons with served demand/success rates.

Validation: pending explicit metric and failure contracts.

## ADR-012 — Evidence-based execution sizing

Status: Accepted workflow rule; concrete resources open  
Source: user hardware/software documentation requirement

Run smoke -> measured pilot -> full configured campaign. Derive full runtime/RAM/disk estimates from actual representative pilots. Document worker and solver-thread limits and distinguish estimates from measured requirements.

No runtime, memory use, solver speed, or completed campaign result has yet been measured. Candidate resource envelopes in README.md are planning estimates only.

## ADR-013 — Selected daily exact stack

Date: 2026-10-16  
Status: Accepted, with B2 full-model validation pending  
Source: user selection; Monte Carlo framework; nonlinear congestion objective

Decision: use an explicit daily NumPy/SciPy loop, PySCIPOpt 6.1.0, and the bundled SCIP backend under CPython 3.12. The formulation remains exact; Pyomo/HiGHS is retained only as a separately approved piecewise-linear fallback.

Evidence: `srcnet-mc probe-scip` returned `optimal` for a binary activation plus continuous exact-congestion model, with flow `2.0` and congestion `0.249999999875` against analytical `0.25` on macOS arm64.

Consequence: this confirms only the minimal expression/interface combination. B2 must independently validate every SRCNet constraint family and original objective on complete tiny fixtures.

## ADR-014 — Transfer completion and atomic infeasibility

Date: 2026-10-16  
Status: Accepted interpretation  
Source: daily procedure; user selection

Each demand batch must complete its required transfers inside its decision day. There is no multi-period transfer, reservation, backlog, retry, or partial admission. If a batch is infeasible, no new copies are committed and the event is reported as an atomic rejection, distinct from solver failures.

## ADR-015 — Policy, existing-copy, and scenario contracts

Date: 2026-10-16  
Status: Accepted interpretation  
Source: Offline Policy; Online Policy; Simulation Scenarios; user selection

Offline is a static non-clairvoyant template applied without current/future stochastic information. Online S4 placement considers only new arrivals. Existing copies are immutable; migration is out of scope. S1-S3 use fixed synthetic demand with daily storage reset, while S4 alone activates dynamic occupancy, arrivals, retention, direct reception and online re-optimisation.

## ADR-016 — Daily boundary and objective accounting

Date: 2026-10-16  
Status: Accepted interpretation  
Source: Markov model; occupancy/retention procedure; CAPEX objective; user selection

The initial distribution denotes `X(0)` and a transition produces day-one `X(1)`. Existing inventory ages and expires before new arrivals; newly admitted data enter with age zero. CAPEX is charged once at a resource's first activation per replication, not per re-solve.

## ADR-017 — Synthetic first fixture

Date: 2026-10-16  
Status: Accepted  
Source: incomplete worked instance; user selection

Build a small complete synthetic fixture before attempting an incomplete completion of the manuscript example or any calibrated campaign. Every configuration and result must label this provenance.

## Template for new decisions

- ID / title:
- Date:
- Status:
- Source sections/equations and manuscript hash:
- Context and unresolved issue:
- Options considered:
- Selected decision, and selection evidence if required:
- Rationale:
- Mathematical/metric consequences:
- Approximation and error implications:
- Implementation/configuration locations:
- Validation evidence:
- Alternatives rejected / superseded decisions:
- Remaining limitations and next action:


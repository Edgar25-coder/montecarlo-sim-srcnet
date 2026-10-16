# Initial manuscript review

Date: 2026-10-16  
Source: [cas-dc-template.tex](docs/model/cas-dc-template.tex)  
SHA-256: `230b5df7bab09097089d44c26da6685586cafa5913a62d444e59dfb8c4da7898`

This review is grounded in the supplied LaTeX. It identifies implementation-sensitive issues; it does not amend the paper or choose scientific interpretations. Line references identify this exact snapshot and may move in later versions.

## Source map

| Source lines | Active section | Implementation relevance |
| --- | --- | --- |
| 330-355 | Assumptions | Deterministic scope, complete copies, no deletion/migration, physical versus logical topology |
| 357-460 | Mathematical Model; Sets and Indices | Node roles, stages, SRC and parent-storage mappings |
| 461-586 | Parameters; Decision variables | Capacities, costs, compatibility, replicas, flow and activation |
| 587-754 | Objective components | Economic subcomponents, energy, temporal cost, nonlinear congestion, exposure proxy, utilisation |
| 755-1032 | Detailed Constraints | Full reception/replication, conservation, capacity, buffer, diversity, distance and risk constraints |
| 1065-1117 | Problem Formalization | Abbreviated restatement; does not replace the detailed constraints |
| 1121-1650 | Example of an Instantiation by SRC | Quarterly 3-dataset reference with partial/ranged parameters and an interpreted assignment |
| 1684-1933 | Monte Carlo framework and stochastic processes | Daily horizon, Markov links, sampling, occupancy, retention, direct reception |
| 1934-1961 | Procedure and policies | Daily order, fixed offline policy, periodically re-solved online policy |
| 1962-2012 | Indicators and scenarios | Objective summaries, success/availability/diversity/distance/direct metrics, S1-S4 |

Use semantic constraint IDs rather than relying on the printed "Constraint 22/23" references.

## Requirements that are explicit

- One daily time step; baseline H=90 and N=1000 independent Monte Carlo replications per scenario.
- Four link states: normal, congested, degraded, failed.
- State-dependent Beta capacity factors and LogNormal latencies.
- Poisson dataset counts, LogNormal sizes, Weibull retention.
- Dynamic storage balance O_next=O+A-D and free capacity B-O.
- Offline and online policies; S1-S4 with increasing stochastic/dynamic features.
- Six objective components and success, availability, diversity, distance and direct-reception indicators.
- At least one active T0, two transfer stages, complete replicas, resource limits, and resilience constraints.
- Replica lower bound: one for q>Q_large and two otherwise. Equality at the threshold belongs to the two-copy case.

## High-impact issues to resolve

| Issue | Source anchor | Why it matters / required treatment |
| --- | --- | --- |
| Quarterly example versus daily simulation | Example demands/node parameters; Simulation Horizon | Convert throughput budgets and volume/rate units consistently; quarterly arrivals cannot simply become daily indivisible demands |
| Static assumptions versus dynamic extension | Assumptions; dynamic occupancy/retention | Declare the scope transition. Deletion in S4 is explicitly introduced, while migration is not automatically introduced |
| Unseen arrivals under fixed offline decisions | Offline Policy; Dataset Arrival Process | Fixed per-dataset choices at t=0 do not define a policy for unknown future dataset IDs |
| Batch admission/infeasibility | Unique reception and replica constraints; success indicator | All-demands optimisation can fail for the entire batch. Partial success requires an additional explicit operational rule |
| Incomplete stochastic configuration | Markov/capacity/latency/arrival/retention subsections | Numerical matrices, moments/rates, initial conditions and correlations are not fully supplied |
| Initial state and transition timing | Markov model; Simulation Procedure step 1 | Decide whether the initial distribution is X(0) or X(1), avoiding an unintended extra transition |
| Failed links and zero division | Effective capacity; congestion objective | Enforce no flow on failed links and exclude undefined 0/0 evaluation |
| Storage and transfer-service indices | Dynamic occupancy; Direct Reception | B_s belongs to persistent storage nodes; B_v_free is used at receiving SEs without a complete aggregation rule |
| Dynamic placement indicator | Dynamic occupancy versus Decision variables | y_ks(t) needs a documented mapping from replica assignments; y_a already means link activation |
| Age and expiry boundaries | Dynamic occupancy prose; Retention Model; Procedure | Prose mentions age exceeding lifetime; the explicit inequality uses age>=L. Choose and document daily timing/rounding and entry age |
| Old replicas during re-optimisation | Online Policy; no-migration assumption | Do not add storage or historical transfer costs repeatedly; moving old copies needs an extension |
| Repeated CAPEX | Objective definitions; repeated solves | Decide which activation costs are one-off, recurring, or per solve before aggregating economic results |
| Temporal objective units | Total temporal cost formula | Propagation latency and time-per-unit-flow are combined then multiplied by flow; this requires an explicit interpretation |
| Exposure versus rerouting | C_RR formula and narrative | Failure-distance exposure is a proxy, not observed rerouting events |
| S1-S3 demand/storage semantics | Simulation Scenarios | Define fixed workload, reset/carryover, and static storage so that a daily loop does not introduce undeclared dynamics |
| Service availability | Performance Indicators | Define feasibility measurement on days with no arrivals; timeout is not physical unavailability |
| Hard-constraint compliance | Diversity/distance constraints and metrics | Validated feasible placements satisfy enabled hard constraints; infeasible or missing outcomes need separate accounting |
| Splittable transport versus indivisible storage | Assumptions; continuous flow domains | Complete-copy storage does not imply a unique unsplit path; do not add unrequested routing integrality |
| Initial T0 availability | Assumption and sum_i x_i>=1 | An activated T0 alone does not guarantee a usable path, enough buffers/storage, or admissible replicas |
| Set-notation inconsistencies | Sets and Indices | The A^0/A^1 descriptions appear to swap the symbols in the subset clauses; use the stated stage meanings and record the interpretation |
| Abbreviated formalisation and fragile indices | Problem Formalization | Some constraints are omitted in the restatement and the storage-flow sink index is inconsistent; implement from the detailed consistent definitions |
| Physical graph versus DAG | Assumptions; Mathematical Model | Do not reject a physical directed graph merely because it has cycles; distinguish it from the logical dependency DAG |
| Incomplete worked instance | Example topology, parameter ranges, distances | The paper does not fix every edge or parameter. Label any completed runnable fixture as a synthetic completion and verify it independently |

These issues should be grouped into the design brief. Routine coding choices do not require a separate user checkpoint.

## Concrete unit check

Using decimal PB and Gbps:

`volume_PB_per_period = bandwidth_Gbps * 1e9 * period_seconds / (8 * 1e15)`.

For a one-day period:
- 25 Gbps permits 0.27 PB/day before the utilisation bound.
- 100 Gbps permits 1.08 PB/day.
- 400 Gbps permits 4.32 PB/day.

With eta_bar=0.8, a 400 Gbps link permits at most 3.456 PB/day in that period-volume interpretation.

The worked example's 30 PB over 90 days corresponds to about 30.86 Gbps. A whole 30 PB object cannot complete in one day over a 400 Gbps link under those bounds. Daily indivisible workloads therefore need a justified scale/calibration or an explicitly extended multi-period transfer model.

The worked example's node-processing H_i=120 is PB per quarterly planning window. Under a constant-rate interpretation it corresponds to 120/90 PB/day; its persistent B_s=40 PB remains 40 PB. Buffer M_v is a volume and must retain its own model semantics.

The temporal objective and normalised coefficients/exposure budgets also require unit consistency; converting only the capacity numbers is insufficient.

## Validation starting points

The interpreted worked assignment has processing loads:
- g_i_esp=96;
- g_d_esp=42;
- g_d_uk=16;
- g_d_de=12;
- g_d_ca=4;
- terminal stored volumes 30, 12, 4, 12 and 4 PB.

These loads can be checked directly from alpha, beta and z. They do not establish full feasibility or optimality because link-family ranges, precise local capacities, distances and some other data remain incomplete.

Start with a complete tiny independently checkable fixture, then a documented synthetic completion of the example. Keep the 90-day deterministic reference distinct from daily stochastic configurations.

## Calibration/data inventory to request or label synthetic

- Complete directed arc lists and allowed pre/post-reception stages.
- Every node's role/SRC/parent relationship and required capacities/costs.
- Link capacities, operational services, latency/time/cost/energy/risk/distance values.
- Storage-to-storage distances and dataset-dependent resilience parameters.
- Source-SDP mix, compatibility rules, arrival rate and dataset-size moments.
- Markov transition counts/matrices, initial distributions and correlation assumptions.
- State-specific capacity and latency moments.
- Weibull shape and mean retention; initial dataset ages/lifetimes and occupancy.
- Objective weights/scaling and a declared horizon CAPEX convention.

Use explicit synthetic smoke settings if these inputs are unavailable. Do not describe demonstration output as empirical SRCNet calibration.


# Codex master prompt: SRCNet Monte Carlo simulation research framework

You are Codex acting as a scientific software architect, operations-research engineer, and reproducibility engineer. Work in the current repository.

Your objective is to DESIGN, then IMPLEMENT, and finally to provide  instructions to EXECUTE a reproducible Python framework for Monte Carlo experiments on the mathematical SRCNet data-transport, placement, and replication model in the supplied LaTeX manuscript.

## 1. Source of truth and scope

The manuscript is named `cas-dc-template.tex`. In this starter package it is at `docs/model/cas-dc-template.tex`. If it already exists elsewhere in the repository, identify the authoritative copy rather than creating competing versions. Inspect actual repository files before making changes. Read any existing `AGENTS.md` instructions.

Read the complete active mathematical formulation, not only its abbreviated "Problem Formalization". Read the worked instance and every subsection from "Monte Carlo Simulation Framework" through "Simulation Scenarios", including "Simulation Procedure". Ignore LaTeX comments as executable specifications; record relevant inconsistencies separately.

The manuscript describes:
- A directed network with Low/Mid SDP sources, T0 and non-T0 Storage Elements, transit nodes, persistent storage nodes, SRC membership, and parent-SE mappings.
- Initial reception followed by full-copy redistribution, link/node activation, compatibility, size-dependent replica requirements, capacity/buffer limits, link availability, failure exposure, SRC diversity, and geographical separation.
- Six weighted objective components: economic cost, physical energy, temporal cost, congestion, failure-distance exposure, and maximum link utilisation.
- Daily discrete-time simulation with baseline `H = 90` days and `N = 1000` independent Monte Carlo replications.
- S1 deterministic baseline; S2 independent link failures; S3 Markov-modulated network; S4 dynamic storage, arrivals, retention, direct reception, and online adaptation.
- Offline and online decision policies.

Preserve the manuscript unchanged. Record its SHA-256, relative path, and section/equation anchors in the project documentation and run manifests. Do not edit the paper to resolve an implementation difficulty. Distinguish an explicit manuscript requirement, an interpretation, a synthetic parameter, and a proposed model extension.

All new code, identifiers, docstrings, comments, documentation, CLI help, logs, plots, reports, and commit messages must be in English. All project algorithms and orchestration must be implemented in Python. Python packages with compiled numerical dependencies and external solvers accessed from Python are allowed if documented. Shell snippets, Dockerfiles, YAML, and packaging metadata are infrastructure, not alternate scientific implementations.

## 2. Mandatory first phase: design and library comparison

Complete Phase A before adopting a simulation framework, optimisation modelling library, or solver. The user will select the final library/stack afterward.

During Phase A:
1. Inspect repository state, the manuscript, available input data, and execution environment without changing unrelated work.
2. Produce a model-to-code traceability table, a model ambiguity register, a minimal architecture, a validation strategy, a dependency comparison, and an incremental implementation plan.
3. Create or update `README.md`, `AGENTS.md`, `PLAN.md`, and `DECISIONS.md`. Preserve applicable existing instructions.
4. Evaluate existing Python libraries from their official documentation. Cite URLs and the review date. Separate simulation time management, sampling/statistics, graph representation, optimisation modelling, numerical solving, and parallel execution.
5. Present a short recommendation and a small set of coherent stack options. Explain tradeoffs specifically for this manuscript.
6. Finish this phase at a clear user-selection checkpoint. Do not silently install/adopt a candidate, implement its production backend, or run the Monte Carlo campaign.

Evaluate at least (order is preference):
- NumPy/SciPy with an explicit daily time loop: direct fit for the current discrete-time procedure, random distributions, and statistics.
- SimPy: process-based discrete-event simulation if within-day transfers, queues, shared resources, or completion events are needed.
- salabim: an alternative discrete-event engine with queues, resources, and monitoring; assess headless operation and additional dependency cost.
- NetworkX for directed topology and structural validation; it is not a replacement for constrained optimisation.
- Pyomo and CVXPY as alternative optimisation modelling layers, each paired with a compatible solver.
- SCIP/PySCIPOpt as a possible open-source nonlinear mixed-integer route; verify the concrete formulation/interface.
- A documented MILP approximation with a compatible MILP solver, such as HiGHS, only as an explicitly labelled alternative.
- SALib for optional later sensitivity analysis; Joblib or Python multiprocessing for local independent replications. Consider Dask only if measured scale justifies it.

Compare purpose, mathematical expressiveness, solver requirements, installation, licensing, current compatibility, reproducibility, checkpointing integration, extension cost, and likely bottlenecks. Do not treat these complementary packages as interchangeable engines. Do not recommend MCMC/posterior-inference libraries merely because this task uses the term Monte Carlo.

The phase-selection response must include the proposed simulation engine, modelling layer, actual solver, exact/approximate formulation, and material semantic decisions still unresolved. Group the scientific clarification points in this response instead of repeatedly interrupting for routine implementation choices.

After the user selects the stack, continue through Phases B and C within the selected scope without requesting repeated permission for ordinary local work.

## 3. Mathematical audit before implementation

Map every set, parameter, variable, objective term, constraint family, stochastic process, and metric to a documented representation, implementation location, and validation check.

Preserve the full constraint set, including:
- At least one activated T0, unique compatible initial reception, direct-reception thresholds, and activation consistency.
- Size-dependent minimum replicas: one when `q_k > Q_large`, otherwise two. This is a lower bound, not an implicit "exactly" rule.
- Unique storage assignment for each active replica, replica-origin linearisation, no repeated parent non-T0 SE, optional SRC diversity, and geographical separation.
- Separate flow conservation on the pre-reception and post-reception arc sets, non-negative continuous flows, and aggregate physical-link load.
- Processing load definitions and limits, aggregate and individual temporary buffers, persistent storage limits, and individual replica fit.
- Service availability, endpoint activation, utilisation stability, and failure-exposure budgets.

Keep dataset placement indivisible and replicas complete. The published continuous flows do not by themselves enforce a single unsplit path: report this distinction and do not add path-integrality constraints without recording a model extension.

Audit and resolve, or explicitly block affected features on, these issues:
- Bandwidth in Gbps versus dataset volume in PB; processing capacities in the worked example are per 90-day planning window, whereas simulation steps are daily. Define a unit table and explicit conversions. Do not reuse 90-day transfer allowances as daily allowances or scale persistent storage by time.
- Whether an object must finish all required transfers within one day, or can span periods. Multi-period progress, transfer reservations, and physical queue scheduling are extensions unless specified and accepted.
- The introductory deterministic/no-deletion assumptions versus the explicitly stochastic/dynamic simulation extension.
- The initial Markov-state distribution, per-link versus shared parameters, cross-link independence assumptions, failed-link semantics, and unavailable-service indicators.
- The dynamic subsection's `y_ks(t)` versus the deterministic model's link-activation `y_a`. Define any dataset/storage indicator from the replica assignment variables; do not introduce conflicting meanings.
- Storage is attached to `s in S`, while direct reception occurs at `v in E`. Define the parent/child capacity check and distinguish necessary eligibility from a fully feasible placement.
- The offline policy is fixed at `t=0` but S4 introduces unseen datasets. Propose a non-clairvoyant static policy/template, a fully specified fixed workload comparison, or a separately labelled perfect-information oracle. Explain what remains fixed and what may be evaluated at arrival.
- Online re-optimisation of new demands versus migration/re-creation of existing copies. Keep existing copies fixed unless an explicit extension accounts for migration traffic, costs, and occupancy.
- CAPEX over repeated daily solves; objective aggregation over the horizon; measured peak utilisation versus auxiliary `eta`.
- The published `T` is a flow-weighted temporal objective. Its mixed latency/time-per-volume units need interpretation; do not present it as observed dataset completion latency without a physical timing model.
- `C_RR` is the failure-distance exposure proxy, not a simulated count or measured cost of rerouting events.
- A single infeasible object can make a batch infeasible. Rejection, admission control, backlog, retries, and partial success require explicit semantics rather than an unannounced change to the all-demands optimisation model.
- The worked instance gives ranges and partial edge data, not a complete calibrated dataset. Complete missing values only in a labelled synthetic configuration.
- The set descriptions appear to swap the subset symbols for `A^0` and `A^1`, the formalisation is abbreviated, and the diversity/distance indicators use fragile equation numbers. Use stable semantic identifiers and report the inconsistencies.

Use `MODEL_REVIEW.md`, if present, as an initial review to verify rather than as a replacement for reading the source. Record selected interpretations and their consequences in `DECISIONS.md`. Never invent empirical SRCNet data.

## 4. Optimisation fidelity and numerical correctness

The convex link congestion term is `Psi_a(F) = F / (U_a - F)`, with binary decisions elsewhere. A continuous convex solver or a generic MILP solver is not automatically sufficient.

Before adopting the selected backend:
- Demonstrate on a tiny real model that the exact combination of modelling library and solver handles the required integer variables and nonlinear/convex terms.
- For a positive fixed effective capacity `U`, consider the equivalent form `U * inv_pos(U - F) - 1`, or an equivalent conic epigraph. Verify the modelling system's rules and the solver's support rather than assuming that a literal variable division is accepted.
- If a piecewise-linear approximation is selected, document breakpoints, approximation direction, error bounds over `0 <= F/U <= eta_bar`, and sensitivity to refinement. Recompute the original objective on returned solutions. Keep exact-model and approximation results separate.
- Do not drop congestion, relax integrality, force exactly the minimum replica count, truncate routes, or replace optimisation with shortest paths while claiming equivalence.
- For failed/disabled links enforce zero flow and exclude undefined `0/0` congestion expressions. For operational links enforce `eta_bar < 1` and robust numerical tolerances.
- Keep economic-cost subcomponents, physical energy, and original weights visible. Do not silently normalise objectives or remove the intentional appearance of energy in both economic cost and a separately weighted physical objective.
- Independently verify returned assignments and flows against the original constraints. Persist solver status, incumbent availability, objective, bound/gap when supported, runtime, options, and diagnostic information.
- Distinguish optimal, feasible-with-gap, proven infeasible, time limit without incumbent, numerical failure, invalid model/configuration, and backend error. Unknown is not proven infeasible.
- Heuristic fallbacks are optional labelled policies, never silent replacements.

## 5. Stochastic specification and daily procedure

Implement the manuscript's distributions through named, validated parameter objects:
- Each link has a Markov chain on `{N, C, D, F}`. Validate dimensions, probabilities, row sums, state ordering, and the initial distribution.
- If estimating `p_ij = N_ij / sum_j N_ij`, define how unobserved rows are treated. Do not silently smooth or manufacture observations.
- In states N/C/D, sample capacity factors from Beta distributions. Convert mean `m` and variance `v` using `c = m*(1-m)/v - 1`, `alpha = m*c`, `beta = (1-m)*c`. Require `0 < m < 1` and `0 < v < m*(1-m)`. A deterministic factor is a separate explicit case.
- Use a documented zero-capacity/unavailable rule for state F. Never sample a latency to make a failed link traversable.
- For positive latency and dataset sizes use LogNormal moment conversion: `sigma2 = log1p(cv**2)`, `sigma = sqrt(sigma2)`, `mu = log(mean) - sigma2/2`. NumPy expects the underlying normal's standard deviation, not its variance. SciPy uses a different parameter interface; test the adapter.
- Generate dataset counts with Poisson `lambda` in datasets/day; do not confuse arrival rate with objective weights. Define source-SDP/class assignment, compatibility, and dataset identities.
- Sample one Weibull retention lifetime per dataset, with shape `kappa > 0` and scale `theta = mean_retention / Gamma(1 + 1/kappa)`. Share that lifetime across its copies unless an extension explicitly changes the model. Specify rounding/boundary rules for daily age checks.

For each independent Monte Carlo replication, reset all mutable state. For every day follow the published order:
1. Update link states using the Markov model.
2. Sample state-dependent capacities and latencies.
3. Generate arrivals and sample dataset sizes and their dataset-level retention lifetimes.
4. Advance ages, expire eligible existing datasets, and account for released storage.
5. Compute the free storage presented to the optimiser.
6. Apply the selected offline/online policy using only its allowed information.
7. Independently validate a usable solution; atomically commit newly created copies and update occupancy.
8. Record decisions, objective components, feasibility/solver outcomes, storage balances, and operational indicators.

Explicitly define whether the initial distribution describes `X(0)` or `X(1)`. Document a single daily boundary convention so that newly generated data do not age or expire accidentally before their first placement.

Maintain `O_s(t+1) = O_s(t) + A_s(t) - D_s(t)` using newly created persistent replicas only. Re-optimisation must not repeatedly add existing copies or re-charge historical transfers. Keep pre-expiry, post-expiry, and end-of-day occupancy distinct. Validate `0 <= O_s <= B_s`, exact releases, and transactional rollback on unsuccessful placement.

This is a finite 90-day study by default. Do not silently add a steady-state warm-up or discard initial days.

## 6. Scenario and policy contracts

Create an explicit feature matrix and configuration for S1-S4, not just scenario names:
- S1: deterministic, fixed network/storage parameters and a defined fixed demand experiment matching the deterministic formulation.
- S2: independent link failures with fixed operational-state capacities/latencies and a documented availability law. Do not add Markov persistence or dynamic storage.
- S3: temporally correlated Markov links and conditional capacity/latency variation, with the demand/storage semantics specified.
- S4: the complete dynamic framework, including arrivals, retention, occupancy, direct reception, and online re-optimisation.

Define which features remain fixed across scenarios and whether demand or occupancy are reset or carried over. Do not repeatedly fill an allegedly static baseline unless that interpretation has been selected.

Compare offline/online policies on the same policy-independent exogenous traces within each replication. Clone state before each policy run. Neither policy may inspect future random events unless it is explicitly labelled a perfect-information oracle. Distinguish having a full trace in the experiment harness from revealing it to a policy.

A scenario extension must add configuration, source/decision references, validation, tests, documentation, and a results label. Existing baseline configurations must retain their meaning.

## 7. Incremental Python architecture

Use a small `src/`-layout package, for example `src/srcnet_mc/`. Build only the modules needed for completed increments. Avoid a monolithic simulation script and avoid implementing several interchangeable engines before one works.

Proposed responsibilities:
- `domain/`: typed immutable topology, node/link/dataset records, units, and identifiers.
- `config/`: schema validation, defaults, scenario composition, and resolved configuration.
- `stochastic/`: Markov evolution, samplers, trace creation, calibration interfaces, and RNG management.
- `optimization/`: variable definitions, independently registered constraint/objective families, solver adapter, and result contract.
- `policies/`: offline and online policies consuming a restricted observable-state interface.
- `simulation/`: daily step, storage/retention lifecycle, state transitions, and orchestration.
- `metrics/` and `analysis/`: objective accounting, estimators, paired comparisons, tables, and figures.
- `execution/`: bounded parallelism, checkpoints, manifests, and restart.
- `io/` and `cli.py`: configuration loading, versioned outputs, and command-line entry points.

Keep contracts simple: `Policy.decide(observed_state, demands) -> DecisionResult`, `Optimizer.solve(problem) -> SolveResult`, `Constraint.apply(context)`, and scenario/metric registration, or a simpler equivalent justified in the design. Do not pass hidden global RNGs or a mutable future trace into policy objects.

Support adding a distribution, constraint, policy, scenario, metric, or solver adapter through a local documented change. Demonstrate one small extension using a real, independently meaningful test.

Suggested repository contents include `README.md`, `AGENTS.md`, `PLAN.md`, `DECISIONS.md`, `pyproject.toml`, one locked dependency workflow, `Dockerfile`, `.dockerignore`, `configs/`, `docs/`, `src/`, `tests/`, and ignored `outputs/`. Adapt to existing repository conventions. Add CI for the fast reproducibility checks; do not run the full research campaign in CI.

## 8. Reproducibility, configuration, and restart

After stack selection:
- Choose a supported CPython version compatible with the selected solver. Pin it, direct/transitive dependencies, solver version, and container base digest. Document how to rebuild or intentionally update the lock.
- Provide an isolated native environment and a Docker route with the same configuration and scientific entry points. Keep solver-license handling explicit and never embed credentials.
- Use NumPy `Generator` and a recorded `SeedSequence` hierarchy or equivalent. Derive streams from stable replication/component identifiers, not worker scheduling, global RNG state, Python's unstable `hash()`, or root-seed-plus-worker arithmetic.
- Separate link states, capacity, latency, counts, sizes, retention, and policy randomness so that adding one component does not silently perturb unrelated streams.
- Keep independent streams across Monte Carlo replications and common random inputs across paired policy evaluations. Store exogenous traces or enough immutable information to regenerate them exactly.
- Hold random draws stable when worker count or task order changes. Keep deterministic scientific identifiers/rows separate from timestamps and runtime metadata.
- Record root seed, RNG algorithm and hierarchy, resolved configuration, config/input/model hashes, Git revision and dirty status, dependency/solver versions, solver seed and thread options, OS/architecture, and container identity.
- Promise exact random-input replay under the locked environment; distinguish that from numerical equivalence across hardware and from non-unique optimiser decisions.
- Parallelise independent replications first. Bound workers and solver/BLAS threads to avoid oversubscription. Do not parallelise sequential days with shared evolving state.
- Checkpoint completed work atomically. Resume only compatible configurations/model/code; reject mismatches. Avoid duplicate outputs, overwritten campaigns, and double-counted metrics. Establish a safe replication-level restart before adding intra-replication restart.

Every configurable parameter must document its name, mathematical symbol, meaning, type, units, scope, allowed range, baseline/default, provenance, and impact. Include Markov matrices/initial states, Beta moments, latency/size moments, lambda, retention parameters, topology/costs/capacities, initial occupancy, objective weights, replica/diversity/distance rules, policy settings, solver tolerances/time limits, seed, N, H, workers, and output detail.

Separate manuscript values, observed calibration, synthetic demonstrations, and unresolved parameters. Reject invalid configs clearly instead of clipping values or silently using convenient defaults.

## 9. Metrics and statistical analysis

Retain the six manuscript objective components `C_econ, E, T, C_cong, C_RR, eta` and their subcomponents. Define horizon aggregation explicitly: additive quantities, one-off costs, time averages, maxima, and final-state measures require different rules.

Implement `SR`, operational availability `A`, SRC-diversity compliance `P_SRC`, distance compliance `P_DIST`, and `P_dir` with explicit numerators, denominators, units, observation windows, and treatment of incomplete/failed placements. Define what counts as successful storage: all required complete replicas and active hard constraints must be satisfied. Distinguish "ever successfully stored" from "still retained at day H".

A zero denominator is missing/not-applicable with its count and reason, not automatic success or failure. Explain why enabled hard diversity/distance constraints imply compliance on validated feasible solutions; report infeasibility separately. Estimate service availability using a defined operational feasibility rule even on days with zero arrivals.

Compute means, sample standard deviations, empirical percentiles, and 95% confidence intervals across independent Monte Carlo replication summaries. Daily observations within a replication are dependent; do not use `N*H` as the independent sample size. Use paired replication differences for offline/online comparisons. Explain the interval method and assumptions; distinguish a ratio of totals from a mean of per-replication ratios. Document quantile uncertainty when reported.

Keep unsuccessful runs and backend errors visible in counts and summaries. Do not silently drop them or replace undefined objectives with zero. Label costs conditional on successful placement, and accompany policy cost comparisons with workload served and success rates so a failing policy does not appear better merely by moving less data.

Add Monte Carlo standard errors and a pilot convergence assessment. Keep stochastic uncertainty separate from solver gaps and model-approximation error. Optional tail-risk or sensitivity extensions must be labelled and justified.

## 10. Documentation and output contract

`README.md` must be the runnable entry point, with links to detailed docs. Include:
1. Purpose, scientific scope, source manuscript, fidelity limits, selected stack, and current development status.
2. Repository structure and where to add components.
3. Hardware/software prerequisites, OS/architecture compatibility, solver installation/licensing, and native/container routes.
4. Exact step-by-step setup, validation, smoke, pilot, full campaign, resume, and reporting commands tested in the selected environment.
5. Parameter tables, scenario feature matrix, policy definitions, units, defaults/provenance, and worked configuration examples.
6. Expected outputs, schemas, field definitions, units, status codes, manifest contents, and interpretation.
7. Statistical methods, reproducibility guarantees, benchmark findings, known limits, and troubleshooting.

Propose a versioned output layout such as:
- `outputs/<campaign_id>/manifest.json` and `resolved_config.yaml`;
- per-replication/per-policy summaries and, when configured, daily/placement/link/storage records in CSV or Parquet;
- solver diagnostics, explicit status tables, and resume checkpoints;
- aggregate summaries, paired comparisons, figures, and a human-readable report.

Choose formats based on the selected dependencies and expected volume. Do not require Parquet support accidentally. Document suppression of large detailed traces and store enough provenance to reconstruct them.

`AGENTS.md` must explain source precedence, allowed phase progression, English/Python rules, session startup, documentation maintenance, test commands once implemented, commit rules, and scientific prohibitions.

`PLAN.md` must be a persistent tracker with milestone IDs, status, dependencies, deliverables, acceptance criteria, actual validation evidence, blockers, and the next concrete action. Never mark an implementation or campaign complete because a scaffold or command was written.

`DECISIONS.md` must retain dated ADR-style entries: context, source anchors, options, decision/status, rationale, mathematical implications, approximation/error implications, consequences, and validation evidence. Preserve superseded decisions and distinguish proposed from accepted. Updating the manuscript hash triggers a traceability/decision review.

## 11. Meaningful validation

Use fast, substantive tests appropriate to scientific risk:
- Analytical checks of distribution moment conversions, invalid-parameter handling, deterministic special cases, and known Markov transitions.
- Deterministic small optimisations with hand-checkable solutions or exhaustive tiny references; evaluate the manuscript worked assignment independently before calling it feasible.
- Flow conservation, full replica volumes, capacity/availability, processing/buffers, activation, compatibility, size-threshold boundaries, diversity, distance, and failure-exposure checks.
- Zero-arrival days, all failed links, no available route, overlarge objects, insufficient storage, expiry at a daily boundary, and inconsistent initial occupancy.
- Occupancy mass balance, no duplicate additions/releases, state reset, no policy leakage, and no future-information access.
- Different worker counts/order producing the same exogenous traces; an interrupted/resumed campaign producing the same scientific records as an uninterrupted campaign.
- Solver timeout/error statuses and approximation fidelity where applicable.
- S1 agreement with the deterministic reference; scenario toggles that enable only their documented features.
- A clean-environment smoke run using the published native/container instructions.

Use reproducible fixtures and justified tolerances. Avoid flaky "random sample mean must equal theoretical mean" tests. Test model invariants independently from implementation helpers; do not write tests that merely repeat the production calculation.

## 12. Phases, execution, and resource requirements

Phase A: model/repository audit, library comparison, architecture, scientific interpretation brief, initial documents, then the user-selection checkpoint.

Phase B, after selection: reproducible environment and actual backend compatibility probe; deterministic reference optimiser; daily state/sampling/storage engine; scenarios and policies; metrics, restart, parallel execution, and reporting. Deliver working vertical increments with acceptance evidence.

Phase C: execute smoke tests, then a measured pilot, then the complete configured campaign once validation and the documented resource budget permit. The manuscript target remains N=1000, H=90 for each defined scenario, even if early runs use smaller explicitly labelled profiles.

Before the full campaign, benchmark representative easy and difficult instances and record:
- Wall time, CPU time, peak RSS, output volume, model-building time, solver time, status/gap distribution, and throughput.
- Estimated total solve count. Four daily online scenarios alone can require up to `4*1000*90 = 360000` solves; offline initial solves and any additional re-solves must be accounted for separately.
- Expected full-campaign runtime, memory, and disk from the pilot, with uncertainty and parallel-scaling limits. Do not present an extrapolation as a measurement.
- Worker and solver-thread limits. Describe GPU use only if a selected, measured backend benefits from it.
- Minimum/comfortable requirements for smoke, pilot, and full runs, clearly separating estimates from tested hardware.
- Optional cluster/Slurm execution only if available and useful; keep the local/container workflow complete.

Run bounded local checks and pilots within the chosen execution scope. Do not create billable cloud resources or exceed an agreed compute budget. If a full campaign is blocked by actual missing capacity, a required semantic choice, unavailable solver, or execution limits, save the tested implementation, completed results, exact restart command, and the specific blocker. Do not fabricate results or claim all 1000 replications ran.

## 13. Git and session continuity

Inspect `git status` before changes. Preserve user work. Use a dedicated local branch when appropriate. The user authorises meaningful local commits as part of this development; never push, publish, or rewrite existing history without an explicit instruction.

Group coherent significant changes into commits, for example:
1. `docs: audit SRCNet model and propose simulation architecture`
2. `build: add locked Python and container environment`
3. `feat: implement validated deterministic optimisation reference`
4. `feat: add daily stochastic network and storage lifecycle`
5. `feat: add scenario and offline-online policy experiments`
6. `feat: add reproducible Monte Carlo execution and reporting`
7. `perf: record pilot measurements and execution profiles`
8. `docs: report completed campaign and reproducibility evidence`

Adapt grouping to actual increments. Include relevant docs/configs/tests in each coherent commit; avoid commits for every keystroke. Do not commit secrets, environments, caches, huge raw traces, or unreviewed generated data. Commit small synthetic fixtures and curated reproducibility reports. Retain larger campaign artifacts outside Git with hashes and documented locations.

At the start of every later session read `AGENTS.md`, `README.md`, `PLAN.md`, `DECISIONS.md`, recent commits, and relevant tests. Resume the next unfinished accepted milestone. Before ending, update plan/decisions with what actually happened, validations, blockers, artifact locations, and one executable next action when available.

## 14. Response required now

Start with Phase A only. Deliver:
- A concise scientific audit with manuscript anchors and unresolved issues.
- A reasoned Python library/solver comparison and provisional recommendation.
- The proposed architecture, scenario/policy contracts, reproduction and validation plans, and initial resource-estimation strategy.
- Updated `README.md`, `AGENTS.md`, `PLAN.md`, and `DECISIONS.md`, with honest statuses.
- A focused user-selection brief for the simulation engine and optimisation stack, including any choices that materially affect the model.

Do not implement or execute the Monte Carlo framework until the user has made that selection. After selection, follow this same prompt through implementation, measured execution, and documented results.


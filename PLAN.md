# Development plan

Date: 2026-10-16  
Current phase: B1 complete — reproducible environment and solver compatibility probe  
Implementation status: package skeleton and narrow SCIP probe implemented; SRCNet optimiser pending  
Selected simulation engine / modelling library / solver: explicit daily loop / PySCIPOpt 6.1.0 / bundled SCIP  
Execution status: no SRCNet simulations, benchmarks, pilots, or campaigns have run

This file tracks the future Codex development, not the preparation of the starter package. The supplied audit and comparison are design inputs to verify. Update status and evidence as work is actually completed.

## Supplied materials

- [x] English master prompt and agent instructions.
- [x] Byte-identical manuscript snapshot and source checksum.
- [x] Initial manuscript review and Python library comparison.
- [x] Initial plan and decisions register.
- [x] Audit of the actual target repository and supplied source hash.
- [x] User selection of the final stack and material semantics.
- [x] Package skeleton, locked native dependency set, digest-pinned container definition, and narrow solver probe.
- [ ] SRCNet deterministic optimiser, validation fixtures, and simulation results.

## Milestones

| ID | Status | Depends on | Deliverables | Acceptance evidence |
| --- | --- | --- | --- | --- |
| A1 | Complete | None | Repository inventory; authoritative-source identification; full model/constraint/metric traceability | Source SHA verified; `docs/TRACEABILITY.md` created |
| A2 | Complete | A1 | Unit audit, missing-parameter list, offline/online semantics, scenario feature matrix | Accepted contracts in ADR-014 to ADR-017 and `docs/SCENARIO_CONTRACTS.md` |
| A3 | Complete | A1-A2 | Current library/solver comparison, architecture, feasibility-probe design, resource strategy | `LIBRARY_OPTIONS.md`, selected stack and real probe design |
| G1 | Complete | A3 | User's simulation engine, modelling layer, solver, formulation and key semantic choices | User selection recorded in ADR-013 to ADR-017 |
| B1 | Complete | G1 | Package skeleton, pinned environment, solver probe, native/container setup, fast CI | CPython 3.12 venv; `pytest -q` 1 passed; probe optimal on 2026-10-16 |
| B2 | In progress | B1 | Deterministic optimiser, independent feasibility checker, complete tiny fixtures | Synthetic vertical fixture solves and independent checks pass; broader constraint fixtures remain pending |
| B3 | Pending | B2 | Markov traces, samplers, seed hierarchy, daily state and retention/storage lifecycle | Moment conversions, Markov checks, mass balance, expiry boundaries, replay/reset checks |
| B4 | Pending | B3 | S1-S4 configurations, offline/online contracts, restricted policy observations | Feature isolation, same-input paired policies, no future leakage, immutable existing copies |
| B5 | Pending | B4 | Metrics, independent-replication statistics, outputs/manifests, CLI, bounded parallel runner | Correct denominators/aggregation; worker-independent traces; status/error accounting |
| B6 | Pending | B5 | Checkpoint/resume and reporting, documented extension example | Interrupted/resumed scientific records agree with uninterrupted reference; local/container smoke |
| C1 | Pending | B6 | Measured pilot and hardware/runtime/disk report; full-campaign profile | Actual runtime/RSS/output size/status/gaps; estimates clearly separated from measurements |
| C2 | Pending | C1 and resolved scientific inputs | Full configured N=1000, H=90 campaign per scenario and intended policy comparison | Requested and completed counts; manifests; retained failures; validated aggregation and paired intervals |
| C3 | Pending | C2 | Research report, reproducibility instructions, final documentation | Results tied to source/config/code/solver versions; runnable restart/report commands; limitations |

An unsuccessful compatibility probe reopens the relevant stack choice; it does not justify silently changing the mathematical model.

## Development sequence and coherent commits

1. Model audit, architecture, and comparison documentation.
2. Locked Python/container environment and tested solver integration.
3. Validated deterministic optimisation and independent checking.
4. Stochastic daily network/storage lifecycle.
5. Scenario and policy experiments.
6. Reproducible Monte Carlo execution, statistics, restart, and reporting.
7. Pilot measurements and resource profiles.
8. Completed campaign evidence and research report.

Adapt commit grouping to the actual increments. Include documentation and relevant tests with each increment. Store exact resulting commit references in the execution journal after they exist.

## Blocking scientific decisions

| Item | Current state | Required before |
| --- | --- | --- |
| Simulation engine, modelling layer, solver, exact/approximate formulation | Selected; full-model validation pending | B2 |
| Daily units, throughput conversion and transfer completion semantics | Completion semantics selected; complete unit table pending | B2-B3 |
| Offline behaviour for unseen arrivals and scope of online decisions | Selected | B4 |
| CAPEX accounting and horizon metric aggregation | CAPEX selected; full metric aggregation pending | B4-B5 |
| Missing stochastic/calibration parameters and complete topology | No empirical inputs supplied | Calibrated full campaign |
| Batch infeasibility, admission/retry rules, zero-arrival availability definition | Unresolved | B4-B5 |

Synthetic experiments, including a full controlled campaign, may proceed after accepted explicit synthetic settings are supplied. They must not be described as calibrated SRCNet results. Missing empirical data alone does not block a deliberately synthetic study.

## Validation journal

| Date / milestone | Command or check | Environment and input | Actual result / artifact | Commit |
| --- | --- | --- | --- | --- |
| 2026-10-16 / B1 | `.venv/bin/python -m pytest -q`; `.venv/bin/srcnet-mc probe-scip`; `docker run --rm srcnet-mc:local probe-scip` | CPython 3.12, macOS arm64; NumPy 2.3.5, SciPy 1.16.3, PySCIPOpt 6.1.0; digest-pinned Python 3.12 Docker image | 1 passed; native and container SCIP probes returned optimal, activation 1, flow 2.0, congestion 0.249999999875 | Pending |

Replace this placeholder row when the first actual check is run. Record failures as well as passes and keep consequential evidence.

## Execution campaign tracker

For each campaign retain: campaign ID; scenario/policies; N and H requested/completed; seed; config/model/code hashes; solver/formulation; workers/threads; successful, infeasible, incomplete and error counts; artifact path; run state; and resume command. Do not count missing/error replications as successful completion.

## Next action

Extend B2 with negative/edge fixtures and independently validate remaining processing and buffer constraint families before building stochastic scenarios.


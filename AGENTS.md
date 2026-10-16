# Agent instructions

## Mission and current phase

Develop a reproducible Python Monte Carlo framework for the SRCNet mathematical model, progressing through design, implementation, and measured execution.

Current status: B1 complete. The selected stack is an explicit daily NumPy/SciPy loop with PySCIPOpt 6.1.0 and its bundled SCIP backend, tested on CPython 3.12/macOS arm64 by the narrow `probe-scip` compatibility check. The deterministic SRCNet optimiser and all simulation scenarios remain unimplemented. Continue through accepted milestones without repeatedly requesting permission for ordinary local development.

Read `CODEX_PROMPT.md` for the complete task. The current package is a starter specification, not an implemented simulator.

## Session startup and resumption

1. Read applicable agent instructions, `README.md`, `PLAN.md`, `DECISIONS.md`, and the complete master prompt if it has not been read in this session.
2. Inspect Git status and recent history. Preserve unrelated and uncommitted user changes.
3. Locate the authoritative `cas-dc-template.tex`. The starter copy is `docs/model/cas-dc-template.tex`; compare its hash with `docs/model/SOURCE.sha256`.
4. Read the full mathematical formulation and simulation subsections, not only the shortened formalisation. Follow the relevant source anchors in `MODEL_REVIEW.md` and verify them against the current source.
5. Resume the next unfinished accepted milestone. Do not restart completed work without a reason.

If there are multiple manuscript copies, determine which is authoritative. A changed source hash requires review of traceability, assumptions, scenarios, and affected tests before resuming a campaign.

## Scientific rules

- Preserve the original manuscript. Record inconsistencies and proposed resolutions; never silently repair the equations by changing the source.
- Apply the full mathematical constraints. A shortened restatement is not permission to omit the detailed constraints.
- Distinguish source requirements, interpretation choices, synthetic inputs, approximations, extensions, and measured observations.
- Keep full replicas and indivisible placement. Do not silently enforce unsplit routing when the published flows are continuous.
- Preserve the nonlinear congestion objective or document and validate an explicitly selected approximation.
- Verify the concrete solver's integer and nonlinear/conic capabilities. A modelling package is not itself a solver.
- Independently check feasible solutions. A timeout or backend error is not proven model infeasibility.
- Keep storage-node capacity separate from SE reception capability, daily throughput separate from persistent volume, and Monte Carlo replication IDs separate from dataset replica slots.
- Do not reinterpret the failure-exposure proxy as measured rerouting or the temporal objective as physical completion latency.
- Do not introduce clairvoyance into online/offline policies.
- Keep failures, dropped workloads, missing ratios, and unsuccessful solves visible in results.
- Never fabricate calibrated inputs, benchmarks, solver results, or completed campaign counts.

Use `DECISIONS.md` for alternatives and rationale. Escalate a material change in scientific meaning in the grouped design brief; continue independent work while a genuinely unresolved choice blocks a particular feature.

## Implementation conventions

All new project content is in English. Scientific algorithms, orchestration, data preparation, and analysis are implemented in Python. Document any compiled dependencies or external numerical solvers accessed from Python.

Use a small typed `src/` package with clear boundaries between domain/configuration, stochastic traces, optimisation, policies, daily state, metrics, execution, and I/O. Prefer simple explicit interfaces over a general-purpose plugin framework.

No hardcoded experimental parameters in production logic. Validate schemas, units, probabilities, thresholds, and capacities. Retain resolved configuration and provenance with every run.

Use explicit per-component random generators and stable seed derivation. Policies comparing the same replication receive the same exogenous inputs with separate mutable state. Changing worker count must not change those inputs.

New constraints, policies, distributions, scenarios, metrics, and backends require a local extension point, a meaningful test, documentation, and a results/configuration identifier. Preserve baseline configuration semantics.

## Validation and execution

The verified B1 commands are `.venv/bin/python -m pytest -q` and `.venv/bin/srcnet-mc probe-scip`. These check only the narrow solver compatibility model, not SRCNet. Add campaign commands only after they have been implemented and verified.

For each significant increment run the checks appropriate to the change. Core scientific checks include independent constraint validation, deterministic tiny references, unit conversion, storage balance, seed replay, scenario isolation, and solver status handling.

Use smoke -> measured pilot -> full campaign progression. The manuscript target is 1000 independent Monte Carlo replications over 90 daily periods for each defined scenario. Smaller runs must be labelled smoke or pilot. Estimate CPU/RAM/disk/runtime from measured pilots before a full run. Keep worker and solver thread counts bounded.

Do not launch a full campaign while scientific semantics, calibration, or required capabilities are unresolved. Run within documented local resource limits; do not provision billable infrastructure implicitly.

## Documentation maintenance

- `README.md`: truthful current status, setup and execution instructions, parameters, scenarios, outputs, requirements, extension guide, and links.
- `PLAN.md`: milestone state, dependencies, acceptance checks, evidence, blockers, and next action.
- `DECISIONS.md`: dated proposed/accepted/superseded decisions, model anchors, implications, and validation.
- `MODEL_REVIEW.md`: verified scientific ambiguities and traceability starting points.
- `LIBRARY_OPTIONS.md`: alternatives, primary references, compatibility evidence, and the recorded selection.

Update documentation in the same coherent change as the code/configuration it describes. Report estimates separately from measurements.

## Git and handoff

The task authorises meaningful local commits. Inspect the diff and use descriptive English commit messages. Group related code, tests, configuration, and documentation; avoid one commit per minor edit.

Do not push, publish, force-update history, discard user work, or modify external systems without an explicit instruction. Do not commit credentials, virtual environments, caches, large raw traces, or generated output directories. Record large research artifacts with locations and hashes.

Before ending a session:
1. Run relevant checks and record their actual outcome.
2. Update plan status and any decisions; leave unrun work pending.
3. Save sufficient manifests/checkpoints to resume completed work.
4. Report completed milestones, remaining blockers, and the next concrete action.
5. Make a coherent local commit when the increment is complete. Reference actual existing commits rather than inventing a commit ID or attempting to embed a commit's own hash in its content.

